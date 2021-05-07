from flask import Blueprint

from . import errors, views

api = Blueprint("api", __name__)
