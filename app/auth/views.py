import datetime
import json

from bson import json_util
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
# request arguments
user_parser.add_argument('username', help='This field is required', required=True)
user_parser.add_argument('password', help='This field is required', required=True)


class TokenRefresh(Resource):
    """Generates a new access token."""
    @jwt_refresh_token_required
    @staticmethod
    def post():
        """
        Generates a new access token in exchange for a refresh token.

        :return: access_token: The json containing the access token and another refresh token.
        :rtype: json
        """
        user = get_jwt_identity()
        access_token = create_refresh_token(identity=user)
        return {'access_token': access_token}, 200


class UserRegistration(Resource):
    """Add a new document to the database."""
    @staticmethod
    def post():
        """
        Parses the request and gets the user details, then sends to the database.

        :return: user: A json string containing the user details.
        :rtype: json
        """
        # get username and password from request
        data = user_parser.parse_args()
        username = data['username']
        password = data['password']

        # disable duplicate username
        username_exists = user_instance.get_user_by_username(username)
        if username_exists:
            return {'msg': 'username {} already exists'.format(username)}, 401

        # define document schema
        new_user = {
            'username': username,
            'password': user_instance.generate_hash(password),
            'joined_at': datetime.datetime.now()
        }

        # save the user
        try:
            user_instance.save(new_user)
            user = json.loads(json.dumps(new_user, default=json_util.default))
            return user, 201
        except:
            return {'msg': 'Something went wrong'}


class UserLogin(Resource):

    @staticmethod
    def post():
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


class GetCurrentUser(Resource):
    @jwt_required
    @staticmethod
    def post():
        current_user = get_jwt_identity()
        return current_user
