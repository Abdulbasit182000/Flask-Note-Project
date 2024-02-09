from flask import Blueprint, render_template, request, flash, redirect, url_for
from .serializers import validate_signup_data
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    from .models import User
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        form_data = {
            'email': request.form.get('email'),
            'firstName': request.form.get('firstName'),
            'password1': request.form.get('password1'),
            'password2': request.form.get('password2')
        }
        validated_data = validate_signup_data(form_data)

        if validated_data:
            from .models import User
            from . import db

            email = request.form.get('email')
            firstName = request.form.get('firstName')
            password = request.form.get('password1')
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))
        
        else:
            print('here')
            flash('account creation failed', category='error')

    return render_template("sign_up.html", user=current_user)