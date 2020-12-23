from flask import  request
from app.models import Post
from app import db
from . import api

@api.route('/')
def index():
    return {'message':'success!'}

@api.route('/post', methods=["GET", "POST"])
def post():
    if request.method == 'POST':
        post_data = Post(post_id=request.post_id.data, post_owner=request.post_owner.data, post_title=request.post_title.data, post_body=request.post_body.data)
        db.session.add(post_data)
        db.session.commit()
