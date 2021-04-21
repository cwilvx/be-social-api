import datetime
import json

from bson import json_util
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import jwt_required
from flask_restful import reqparse
from flask_restful import Resource

from app.models import Users

user_instance = Users()
user_parser = reqparse.RequestParser()

user_parser.add_argument("username", help="This field is required", required=True)
user_parser.add_argument("password", help="This field is required", required=True)


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    @staticmethod
    def post():
        user = get_jwt_identity()
        access_token = create_refresh_token(identity=user)
        return {"access_token": access_token}, 200


class UserRegistration(Resource):
    @staticmethod
    def post():
        data = user_parser.parse_args()
        username = data["username"]
        password = data["password"]

        if data["username"] == "" or None:
            return {"msg": "username is required"}, 401

        current_user = user_instance.get_user_by_username(username)
        if current_user:
            return {"msg": "username {} already exists".format(username)}, 401

        new_user = {
            "username": username,
            "password": user_instance.generate_hash(password),
            "joined_at": datetime.datetime.now(),
        }

        try:
            user_instance.save(new_user)
            user = json.loads(json.dumps(new_user, default=json_util.default))
            return user, 201
        except:
            return {"msg": "Something went wrong"}


class UserLogin(Resource):
    @staticmethod
    def post():
        data = user_parser.parse_args()
        current_user = user_instance.get_user_by_username(data["username"])

        if not current_user:
            return {"msg": "User {} does not exist".format(data["username"])}, 401

        if user_instance.verify_hash(data["password"], current_user["password"]):
            user = {
                "username": current_user["username"],
                "user_id": str(current_user["_id"]),
            }

            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)

            return {
                "msg": "Logged in as {}".format(current_user["username"]),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
        else:
            return {"msg": "Wrong credentials"}, 401


class GetCurrentUser(Resource):
    @jwt_required
    @staticmethod
    def post():
        current_user = get_jwt_identity()
        return current_user
