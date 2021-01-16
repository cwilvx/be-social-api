import datetime

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    
)
from app.models import Users
from flask_restful import Resource, reqparse

user_instance = Users()
user_parser = reqparse.RequestParser()

user_parser.add_argument('username', help='This field is required', required=True)
user_parser.add_argument('password', help='This field is required', required=True)

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        access_token = create_refresh_token(identity=user)
        return {'access_token': access_token}, 200

class UserRegistration(Resource):
    def post(self):
        data = user_parser.parse_args()
        username = data['username']
        password = data['password']

        if data['username'] == '' or None:
            return {'msg': 'username is required'}, 401

        current_user = user_instance.get_user_by_username(username)
        if current_user:
            return {'msg': 'username {} already exists'.format(username)}, 401

        new_user = {
            'username': username,
            'password': user_instance.generate_hash(password),
            'joined_at': datetime.datetime.now()
        }

        try:
            user_instance.save(new_user)
            return {'msg': 'User {} was successfully created'.format(username)},201
        except:
            return {'msg': 'Something went wrong'}

class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        current_user = user_instance.get_user_by_username(data['username'])

        if not current_user:
            return {'msg': 'User {} does not exist'.format(data['username'])}, 401

        if user_instance.verify_hash(data['password'], current_user['password']):
            user = {
                'username': current_user['username'],
                'user_id': str(current_user['_id'])
            }

            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)

            return {
                'msg': 'Logged in as {}'.format(current_user['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {'msg': 'Wrong credentials'}, 401
