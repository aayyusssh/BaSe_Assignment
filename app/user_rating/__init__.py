from flask import Blueprint


user_rating = Blueprint('user_rating', __name__)

from . import views