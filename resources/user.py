import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be empty."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be empty."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": "username already registered."}, 400

        user = UserModel(**data)
        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred registering the user on the database."}, 500

        return {"message": "UserModel created successfully"}, 201
