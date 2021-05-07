from flask import Blueprint

from . import errors
from . import views

auth = Blueprint("auth", __name__)
