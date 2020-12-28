from . import api
from app.models import Posts
from flask_restful import Resource, reqparse

post_instance = Posts()
post_parser = reqparse.RequestParser()
post_parser.add_argument('post_body', help='This field cannot be blank!')

@api.route('/')
def index():
    return {'msg':'success!'}

class AddNewPost(Resource):
    def post(self):
        data = post_parser.parse_args()

        if data['post_body'] == '' or None:
            return {'msg': 'blank post not allowed'}, 401

        post_exists = post_instance.get_post_by_body(data['post_body'])
        if post_exists:
            return {'msg': 'already exists'}

        new_post_data = {
            'post_body': data['post_body']
        }

        try:
            post_instance.save(new_post_data)
            return {'msg': 'Published!'}, 201
        except:
            return {'msg': 'Something went wrong'}, 500

class GetAllPosts(Resource):
    def get(self):
        all_posts = post_instance.get_all_posts()

        return all_posts
