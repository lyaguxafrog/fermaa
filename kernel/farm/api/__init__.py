# -*- coding: utf-8 -*-



from flask import Blueprint


from farm.api import user_resource
from farm.api import post_resource
from farm.api import marketplace_api
from farm.api import chat_resource

api_blueprint = Blueprint('api', __name__)
