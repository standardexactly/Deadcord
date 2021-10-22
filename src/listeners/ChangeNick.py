import threading
from src.core.Util import *
from src.core.Server import *
from src.core.Endpoints import *
from flask_restful import Resource
from src.core.Container import tokens


class ChangeNick(Resource):

    def post(self, server_id):
        params = json.loads(request.get_data().decode())

        if "nick" in params and not None or not "":

            nick_threads = []
            nick = clean_input(params["nick"])[0]

            for token in tokens.return_tokens():
                nick_thread = threading.Thread(target=change_nick, args=[nick, server_id, token])
                nick_thread.daemon = True
                nick_threads.append(nick_thread)

            execute_threads(nick_threads)

            return response(200, "Bot nickname is finished.")
        else:
            return response(500, "Could not nickname bots.", 3)
