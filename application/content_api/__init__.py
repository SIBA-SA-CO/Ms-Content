from flask import Blueprint

content_api_blueprint = Blueprint('content_api', __name__)

from . import routes

