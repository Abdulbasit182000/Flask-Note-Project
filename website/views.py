from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .serializers import validae_note_data
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        form_data={
            'note': request.form.get('note')
        }
        validated_data = validae_note_data(form_data)

        if validated_data:
            from .models import Note
            from . import db
            note = request.form.get('note')
            new_note = Note(data=note, user_id= current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added', category='success')
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    from .models import Note
    from . import db
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
