from src.core.Util import *
from src.core.Endpoints import *
from flask_restful import Resource
from src.core.Container import tokens


class ChangeNick(Resource):

    def post(self, server_id):
        params = json.loads(request.get_data().decode())

        if "nick" in params and not None or not "":
            for token in tokens.return_tokens():
                nick = send(f'guilds/{server_id}/members/@me', 'PATCH', token, {'nick': params["nick"].replace('\n', '')})

                if "code" in nick:
                    console_log('Could not apply nickname to bot.', 1)

            return response(200, "Bot nickname is finished.")
        else:
            return response(500, "Could not nickname bots.", 3)
