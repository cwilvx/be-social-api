from flask import Blueprint
from . import views, errors

api = Blueprint('api', __name__)

