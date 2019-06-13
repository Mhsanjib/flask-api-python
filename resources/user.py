import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="username cannot be blank.")
    parser.add_argument("password", type=str, required=True, help="password cannot be blank.")

    def post(self):

        data = UserRegister.parser.parse_args()

        if not data["username"] or not data["password"]:
            return {"message": "not enough request paramaters"}, 400

        if UserModel.find_by_username(data["username"]):
            return {"message": "username already exists"}, 400

        # user = UserModel(data["username"], data["password"])
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "user successfully created"}, 201

