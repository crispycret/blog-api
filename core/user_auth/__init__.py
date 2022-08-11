


from flask import Blueprint

user_auth = Blueprint("user_auth", __name__)

from . import views
from . import models

