from flask import Blueprint
from . import views, errors

auth = Blueprint('auth', __name__)

