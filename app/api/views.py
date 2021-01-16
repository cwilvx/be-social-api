from . import api
import json

from bson import json_util
from app.models import Posts
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required

post_instance = Posts()
post_parser = reqparse.RequestParser()
post_parser.add_argument('post_body', help='This field cannot be blank!')

@api.route('/')
def index():
    return {'msg':'success!'}

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
            'user': current_user['user_id']
        }

        try:
            post_instance.save(new_post_data)
            return {'msg': 'Published!'}, 201
        except:
            return {'msg': 'Something went wrong'}, 500

class AllPosts(Resource):
    def get(self):
        all_posts = []
        posts = post_instance.get_all_posts()
        for post in posts:
            post_obj = json.dumps(post, default=json_util.default)
            post_item = json.loads(post_obj)
            all_posts.append(post_item)

        return (all_posts)

