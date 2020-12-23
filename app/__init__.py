from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config_options

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_options[config_name])
    config_options[config_name].init_app(app)

    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return  app

