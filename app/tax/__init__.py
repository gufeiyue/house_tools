from flask import Blueprint


tax = Blueprint('tax', __name__)


from . import views