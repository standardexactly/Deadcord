import threading
from src.core.Util import *
from src.core.Server import *
from flask_restful import request
from flask_restful import Resource
from src.core.Container import tokens


class TokenReact(Resource):

    def post(self):
        params = json.loads(request.get_data().decode())

        if "channel_id" and "message_id" and "emoji" in params:

            channel_id = params["channel_id"]
            message_id = params["message_id"]
            emoji = params["emoji"].replace("'", " ")

            react_threads = []

            console_log(f'Bots are reacting to message: {message_id}.')

            for token in tokens.return_tokens():
                react_thread = threading.Thread(target=react, args=[channel_id, message_id, emoji, token])
                react_thread.daemon = True
                react_threads.append(react_thread)

            execute_threads(react_threads)

        else:
            return response(500, "No parameters provided.", 2)
