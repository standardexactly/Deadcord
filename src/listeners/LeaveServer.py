from src.core.Util import *
from src.core.Endpoints import *
from flask_restful import Resource
from src.core.Container import tokens


class LeaveServer(Resource):

    def get(self, server_id):
        for token in tokens.return_tokens():
            leave = send(f'users/@me/guilds/{server_id}', 'DELETE', token, {'lurking': False})

            if "code" in leave.text:
                console_log('Bot not found in server.', 1)
