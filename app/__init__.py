from flask import Flask
from flask_restful import Api
from config import config_options
from . import api

rest = Api()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])
    config_options[config_name].init_app(app)

    rest.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return  app

rest.add_resource(api.views.AddNewPost, '/posts/new')
