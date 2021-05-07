from flask import Blueprint

from . import errors, views

auth = Blueprint("auth", __name__)
