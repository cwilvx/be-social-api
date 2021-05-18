from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from config import config_options
from . import api
from . import auth

rest = Api()
jwt = JWTManager()


# the application factory
def create_app(config_name):
    # initialize app instance
    app = Flask(__name__)
    # cors headers for remote access
    CORS(app)
    app.config.from_object(config_options[config_name])
    config_options[config_name].init_app(app)

    rest.init_app(app)
    jwt.init_app(app)

    # register ./auth module
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # register ./api module
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app


# mapping the auth endpoints
rest.add_resource(auth.views.UserRegistration, "/auth/signup")
rest.add_resource(auth.views.UserLogin, "/auth/login")
rest.add_resource(auth.views.TokenRefresh, "/auth/token/refresh")
rest.add_resource(auth.views.GetUser, "/auth/profile")
rest.add_resource(auth.views.GetUSerById, "/auth/user")

# mapping the posts endpoints
rest.add_resource(api.views.GetPosts, "/")
rest.add_resource(api.views.AddNewPost, "/posts/new")
rest.add_resource(api.views.DeleteSinglePost, "/posts/delete")
rest.add_resource(api.views.SearchPosts, "/posts/search")


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user
