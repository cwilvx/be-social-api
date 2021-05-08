import json
import sys

from bson import json_util
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restful import reqparse
from flask_restful import Resource

from . import api
from app.models import Posts

post_instance = Posts()
post_parser = reqparse.RequestParser()
post_parser.add_argument("post_body", help="This field cannot be blank!")
post_parser.add_argument("post_id")
post_parser.add_argument("tags", action="append")
post_parser.add_argument("q", help="This field cannot be blank!")


@api.route("/wp-admin")
def index():
    return {"msg": "See no evil! 🙈"}


class AddNewPost(Resource):
    @jwt_required
    def post(self):
        data = post_parser.parse_args()

        try:
            current_user = get_jwt_identity()
        except NoAuthorizationError:
            return {"msg": "Missing Authorization Headers"}

        if data["post_body"] is None:
            return {"msg": "blank post not allowed"}, 401

        new_post_data = {
            "user": current_user["user_id"],
            "post_body": data["post_body"],
            "tags": data["tags"],
        }

        try:
            post_instance.insert_post(new_post_data)
            post_data = json.loads(
                json.dumps(new_post_data, default=json_util.default))

            return post_data, 201
        except:
            e = sys.exc_info()[0]
            return {"error": "{e}".format(e)}, 500


class AllPosts(Resource):
    def get(self):

        all_posts = []
        last_id = request.args.get("last_id")
        limit = request.args.get("limit")
        if limit is None:
            limit = 50

        posts = post_instance.get_all_posts(limit, last_id)

        for post in posts:
            post_obj = json.dumps(post, default=json_util.default)
            post_item = json.loads(post_obj)
            all_posts.append(post_item)

        return all_posts


class SinglePost(Resource):
    def post(self):
        data = post_parser.parse_args()
        post_id = data["post_id"]

        if post_id:
            post = post_instance.get_post_by_id(post_id)

            if post is None:
                return {"msg": "Post does not exist!"}, 404
            else:
                post_obj = json.dumps(post, default=json_util.default)
                post_item = json.loads(post_obj)

                return post_item
        else:
            return {"msg": "post_id is required!"}


class DeletePost(Resource):
    @jwt_required
    def post(self):
        """Deletes a post.

        Returns:
            410 (status)
        """
        current_user = get_jwt_identity()
        data = post_parser.parse_args()
        post_id = data["post_id"]

        try:
            if post_id:
                post = post_instance.get_post_by_id(post_id)

                if post is None:
                    return {"msg": "Post does not exist"}, 404

                if current_user["user_id"] == post["user"]:
                    try:
                        post_instance.delete_post(post_id)
                        return {"msg": "Post deleted successfully"}, 410
                    except:
                        return {"msg": "An exception occurred"}, 500
                else:

                    return {"msg": "Permission denied"}, 403
            else:
                return {"msg": "post_id is required!"}
        except:
            return {"msg": "Something went wrong!"}, 500


class SearchPosts(Resource):
    def get(self):
        data = post_parser.parse_args()
        query = data["q"]

        query_results = []
        posts = post_instance.search_post_body(query)
        for post in posts:
            post_obj = json.dumps(post, default=json_util.default)
            post_item = json.loads(post_obj)
            query_results.append(post_item)

        return query_results
