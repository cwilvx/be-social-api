import datetime
import json

from bson import json_util
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,

)
from flask_restful import Resource, reqparse

from app.models import Users

user_instance = Users()
user_parser = reqparse.RequestParser()
# request arguments
user_parser.add_argument('username', help='This field is required', required=True)
user_parser.add_argument('password', help='This field is required', required=True)


class TokenRefresh(Resource):
    """Generates a new access token."""
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
    """Generate an access token for a user upon password confirmation."""
    @staticmethod
    def post():
        """
        Takes in a raw password, verifies it against it's hash and generates and returns an access_token upon success.

        :return: access_token: A json string containing the access_token and a companion refresh token.
        :rtype: str
        """
        # get the username from the request.
        data = user_parser.parse_args()
        username = user_instance.get_user_by_username(data['username'])

        # check whether user exists in db
        if not username:
            return {'msg': 'User {} does not exist'.format(data['username'])}, 401

        # verify the password
        if user_instance.verify_hash(data['password'], username['password']):
            # format the username and user_id
            user = {
                'username': username['username'],
                'user_id': str(username['_id'])
            }

            # generate access and refresh token
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)

            # format and return the above
            return {
                       'msg': 'Logged in as {}'.format(username['username']),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'msg': 'Wrong credentials'}, 401


class GetCurrentUser(Resource):
    """Gets the current user identity from a JWT access token"""
    @jwt_required
    def post(self):
        """
        Performs magic to a JWT access token using get_jwt_identity() and returns the user details.
        :return:
        :rtype:
        """
        current_user = get_jwt_identity()
        return current_user
