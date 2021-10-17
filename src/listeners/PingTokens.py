from src.core.Util import *
from src.core.Endpoints import *
from flask_restful import Resource
from src.core.Container import tokens


class PingTokens(Resource):

    def get(self):
        for token in tokens.return_tokens():
            token_ping = send('users/@me/library', 'GET', token).text
            if "code" not in json.loads(token_ping):
                console_log(token, 2)
            else:
                console_log(token, 3)

        return response(200, 'Token ping complete.')
