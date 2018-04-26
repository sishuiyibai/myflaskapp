from flask import Blueprint

api = Blueprint('api_1_0', __name__)

from . import authentication, posts, users, comments, errors

