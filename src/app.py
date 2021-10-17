from .listeners import *
from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('deadcord', __name__)
api = Api(api_bp)

routes = {
    'PingTokens': '/ping-tokens/',
    'JoinServer': '/join-server/<int:server_id>/',
    'LeaveServer': '/leave-server/<int:server_id>/',
    'StartSpam': '/spam/<int:server_id>/',
    'StopSpam': '/stop-spam/',
    'ChangeNick': '/change-nick/<int:server_id>/'
}

for instance, path in routes.items():
    get_class = lambda x: globals()[x]
    api.add_resource(get_class(instance), path)
