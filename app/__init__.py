from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import config_options
from . import api, auth

rest = Api()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])
    config_options[config_name].init_app(app)

    rest.init_app(app)
    jwt.init_app(app)
    cors = CORS(app, resources={r'/*': {'origins': '*'}})

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app


rest.add_resource(api.views.AllPosts, '/')
rest.add_resource(api.views.AddNewPost, '/posts/new')
rest.add_resource(auth.views.UserRegistration, '/auth/signup')
rest.add_resource(auth.views.UserLogin, '/auth/login')
rest.add_resource(auth.views.TokenRefresh, '/auth/token/refresh')
rest.add_resource(api.views.SinglePost, '/posts/single')
rest.add_resource(api.views.DeletePost, '/posts/delete')
rest.add_resource(auth.views.GetCurrentUser, '/auth/user')


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user
