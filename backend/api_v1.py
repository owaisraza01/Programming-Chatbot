from flask import Blueprint
from flask_restx import Api
from apis.programming import api as programming_lang
blueprint = Blueprint('api', __name__, url_prefix='/')
api = Api(blueprint,
    title='flask Api for Programming Chatbot',
    version='1.0',
    description='flask Api for Programming CHatbot',
)

api.add_namespace(programming_lang)
