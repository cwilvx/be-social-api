from . import api
from app import rest
from app.models import Posts
from flask_restful import Resource, reqparse, Api

post_instance = Posts()
post_parser = reqparse.RequestParser()
# post_parser.add_argument('')

@api.route('/')
def index():
    return {'message':'success!'}

class AddNewPost(Resource):
    def post(self):
        data = post_parser.parse_args()

        if data['post_body'] == '' or None:
            return {'msg': 'post cannot be blank'}, 401

        new_post_data = {
            'post_body': data['post_body']
        }
        try:
            post_instance.save(new_post_data)
            return {'msg': 'Published!'}, 201
        except:
            return {'msg': 'Something went wrong'}, 500


rest.add_resource(AddNewPost, '/posts/new')
