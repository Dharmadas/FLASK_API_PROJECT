# import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import safe_str_cmp
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username', type=str,
    required=True, 
    help="username is required."
    )
_user_parser.add_argument(
    'password', type=str,
    required=True, 
    help="password is required."
    )

class UserRegister(Resource):    
    
    def post(self):    
        request_data = _user_parser.parse_args()

        if UserModel.find_by_username(request_data['username']):
            return {'message': 'User with username already exists.'}, 400

        user = UserModel(**request_data)
        user.save()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # user = (request_data['username'], request_data['password'])
        # sql = "INSERT INTO users VALUES(NULL, ?, ?)"
        # cursor.execute(sql, user)

        # connection.commit()
        # connection.close()

        return {'message': 'User created.'}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        user.delete()
        return {"message": "User deleted."}

class UserLogin(Resource):

    def post(self):
        request_data = _user_parser.parse_args()

        # find user in db
        user = UserModel.find_by_username(request_data['username'])

        # check password
        if user and safe_str_cmp(user.password, request_data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        return {"message": "Invalid credentials."}, 401