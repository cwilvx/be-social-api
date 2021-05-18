import json
import sys

from bson import json_util
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restful import Resource
from flask_restful import reqparse

from app.models import Posts
from . import api

post_instance = Posts()
post_parser = reqparse.RequestParser()

# define request fields
post_parser.add_argument("post_body", help="This field cannot be blank!")
post_parser.add_argument("tags", action="append")
post_parser.add_argument("q", help="This field cannot be blank!")


@api.route("/wp-admin")
def index():
    """Returns a simple json string."""
    return {"msg": "See no evil! 🙈"}


class AddNewPost(Resource):
    """Adds a new document to the database."""

    @jwt_required
    def post(self):
        """
        Parses a request and add a single document to the database.

        :returns: post_data: The document added to the database.
        :rtype: json
        """
        data = post_parser.parse_args()

        # check for JWT token
        try:
            current_user = get_jwt_identity()
        except NoAuthorizationError:
            return {"msg": "Missing Authorization Headers"}

        # check for empty request body
        if data["post_body"] is None:
            return {"msg": "blank post not allowed"}, 401

        # define document schema
        new_post_data = {
            "user": current_user["user_id"],
            "post_body": data["post_body"],
            "tags": data["tags"],
        }

        # send the document to the database, then return it as response
        try:
            post_instance.insert_post(new_post_data)
            post_data = json.loads(
                json.dumps(new_post_data, default=json_util.default))

            return post_data, 201
        except:
            e = sys.exc_info()[0]
            return {"error": "{e}".format(e)}, 500


class GetPosts(Resource):
    """Returns the specified number of documents."""

    def get(self):
        """
        Gets all the posts in the database based on the last_id and the limit.
        Also gets a single post if a post_id is passed.

        query-parameters :
            last_id (mongodb pointer): A pointer to the last document in the previous page.
            limit (int): The number of documents to retrieve. Default = 50.
        :returns: all_posts: A list of all the documents matching the query parameters.
        :rtype: da
        """
        post_id = request.args.get("post_id")
        if post_id:
            post = post_instance.get_post_by_id(post_id)

            if post is None:
                return {"msg": "Post does not exist!"}, 404
            else:
                # convert post pointer to JSON
                post_obj = json.dumps(post, default=json_util.default)
                post_item = json.loads(post_obj)

                return post_item
        else:
            all_posts = []

            last_id = request.args.get("last_id")
            limit = request.args.get("limit")

            if limit is None:
                limit = 50

            posts = post_instance.get_all_posts(limit, last_id)
            # convert the document cursor to JSON.
            for post in posts:
                post_obj = json.dumps(post, default=json_util.default)
                post_item = json.loads(post_obj)
                all_posts.append(post_item)

            return all_posts


class DeleteSinglePost(Resource):
    """Deletes a document matching provided _oid."""
    @jwt_required
    def post(self):
        """Deletes a single document matching the provided id.
        query-parameters: str post_id: The id of the document to be deleted.
        """

        current_user = get_jwt_identity()
        data = post_parser.parse_args()
        post_id = data["post_id"]

        try:
            # check for empty request
            if post_id:
                post = post_instance.get_post_by_id(post_id)

                # check for non-existent post
                if post is None:
                    return {"msg": "Post does not exist"}, 404

                # allow only deleting own posts
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
    """Returns all the documents that contain the search query."""
    def get(self):
        """
        Retrieves all documents that contain the search query.

        query-parameters: str q: The string to search for.

        :return: query_results: A list of all the documents that contain the search query.
        :rtype query_results: json
        """
        data = post_parser.parse_args()
        query = data["q"]

        query_results = []
        posts = post_instance.search_post_body(query)
        for post in posts:
            post_obj = json.dumps(post, default=json_util.default)
            post_item = json.loads(post_obj)
            query_results.append(post_item)

        return query_results
