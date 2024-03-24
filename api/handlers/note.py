from api import app, multi_auth, request
from api.models.note import NoteModel
from api.schemas.note import note_schema, notes_schema


@app.route("/notes/<int:note_id>", methods=["GET"])
@multi_auth.login_required
def get_note_by_id(note_id):
    # DONE: авторизованный пользователь может получить только свою заметку или публичную заметку других пользователей
    #  Попытка получить чужую приватную заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = NoteModel.query.get_or_404(note_id, f"Note with id={note_id} not found")
    if note.author_id != user.id and note.private:
        return "You are not allowed to view this note", 403
    return note_schema.dump(note), 200


@app.route("/notes", methods=["GET"])
@multi_auth.login_required
def get_notes():
    # DONE: авторизованный пользователь получает только свои заметки и публичные заметки других пользователей
    user = multi_auth.current_user()
    notes = NoteModel.query.filter_by(author_id=user.id)
    return notes_schema.dump(notes), 200


@app.route("/notes", methods=["POST"])
@multi_auth.login_required
def create_note():
    user = multi_auth.current_user()
    note_data = request.json
    note = NoteModel(author_id=user.id, **note_data)
    note.save()
    return note_schema.dump(note), 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
@multi_auth.login_required
def edit_note(note_id):
    # DONE: Пользователь может редактировать ТОЛЬКО свои заметки.
    #  Попытка редактировать чужую заметку, возвращает ответ с кодом 403
    author = multi_auth.current_user()
    note = NoteModel.query.get_or_404(note_id, f"Note with id={note_id} not found")
    if note.author_id != author.id:
        return "You are not allowed to edit this note", 403
    note_data = request.json
    note.text = note_data["text"]
    note.private = note_data.get("private") or note.private
    note.save()
    return note_schema.dump(note), 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@multi_auth.login_required
def delete_note(self, note_id):
    # DONE: Пользователь может удалять ТОЛЬКО свои заметки.
    #  Попытка удалить чужую заметку, возвращает ответ с кодом 403
    author = multi_auth.current_user()
    note = NoteModel.query.get_or_404(note_id, f"Note with id={note_id} not found")
    if note.author_id != author.id:
        return "You are not allowed to delete this note", 403
    note.delete()
    return "Note deleted successfully", 200
    
   