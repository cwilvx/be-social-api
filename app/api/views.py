import json
import random
import string

from bson import json_util
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from app.models import Posts
from . import api

post_instance = Posts()
post_parser = reqparse.RequestParser()
post_parser.add_argument('post_body', help='This field cannot be blank!')
post_parser.add_argument('post_id', help='This field cannot be blank')


def generate_post_id():
    post_id = ''.join(random.choice(string.ascii_letters)
                      for i in range(10)
                      )
    return post_id


@api.route('/wp-admin')
def index():
    return {'msg': 'See no evil! 🙈'}


class AddNewPost(Resource):
    @jwt_required
    def post(self):
        data = post_parser.parse_args()
        current_user = get_jwt_identity()

        if data['post_body'] == '' or None:
            return {'msg': 'blank post not allowed'}, 401

        post_exists = post_instance.get_post_by_body(data['post_body'])
        if post_exists:
            return {'msg': 'already exists'}

        new_post_data = {
            'post_body': data['post_body'],
            'user': current_user['user_id'],
            'post_id': generate_post_id()
        }

        try:
            post_instance.save(new_post_data)
            post_data = json.loads(json.dumps(new_post_data, default=json_util.default))

            return post_data, 201
        except:
            return {'msg': 'Something went wrong'}, 500


class AllPosts(Resource):
    @staticmethod
    def get():
        all_posts = []
        posts = post_instance.get_all_posts()
        for post in posts:
            post_obj = json.dumps(post, default=json_util.default)
            post_item = json.loads(post_obj)
            all_posts.append(post_item)

        return all_posts


class SinglePost(Resource):
    @staticmethod
    def post():
        data = post_parser.parse_args()
        post_id = data['post_id']

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
        """Deletes a post

        Returns:
            410 (status)
        """
        current_user = get_jwt_identity()
        data = post_parser.parse_args()
        post_id = data['post_id']

        try:
            if post_id:
                post = post_instance.get_post_by_id(post_id)

                if post is None:
                    return {"msg": "Post does not exist"}, 404
                else:
                    post_obj = json.dumps(post, default=json_util.default)
                    post_item = json.loads(post_obj)

                    if current_user['user_id'] == post['user']:
                        try:
                            post_instance.delete_post(post_id)
                            return {'msg': 'Post deleted successfully'}, 410
                        except:
                            return {'msg': 'An exception occurred'}, 500
                    else:
                        return {'msg': 'Permission denied'}, 403
            else:
                return {"msg": "post_id is required!"}
        except:
            return {"msg": "Something went wrong!"}, 500
