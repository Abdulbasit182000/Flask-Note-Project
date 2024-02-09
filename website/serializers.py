from flask import flash
from .Validation import UserModel, NoteModel

def validate_signup_data(request_form):
    from .models import User, Note

    try:
        user = UserModel(**request_form)
        record = User.query.filter_by(email=user.email).first()
        if record:
            return None
        else:
            return user
    except ValueError as e:
        flash('account creation failed', category='error')
        return None

def validae_note_data(request_form):
    from .models import User,Note

    try:
        note = NoteModel(**request_form)
        return note
    
    except ValueError as e:
        flash('Note has exceeded the length of 256', category='error')
        return None
