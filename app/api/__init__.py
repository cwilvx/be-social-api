from flask import Blueprint

from . import errors
from . import views

api = Blueprint("api", __name__)
