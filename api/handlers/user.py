from api import app, request, multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


@app.route("/users/<int:user_id>")
def get_user_by_id(user_id):
    user = UserModel.query.get_or_404(user_id, f"User with id={user_id} not found")
    return user_schema.dump(user), 200


@app.route("/users")
def get_users():
    users = UserModel.query.all()
    return users_schema.dump(users), 200


@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.json
    username = user_data.get("username")
    
    existing_user = UserModel.query.filter_by(username=username).first()
    if existing_user:
        return {"message": "Username already exists"}, 400
    
    user = UserModel(**user_data)
    user.save()
    return user_schema.dump(user), 201



@app.route("/users/<int:user_id>", methods=["PUT"])
@multi_auth.login_required(role="admin")
def edit_user(user_id):
    user_data = request.json
    user = UserModel.query.get_or_404(user_id, f"User with id={user_id} not found")
    user.username = user_data["username"]
    user.save()
    return user_schema.dump(user), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
@multi_auth.login_required(role="admin")
def delete_user(user_id):
    """
    Пользователь может удалять ТОЛЬКО свои заметки
    """
    raise NotImplemented("Метод не реализован")