import threading
from src.core.Server import *
from flask_restful import Resource
from src.core.Container import tokens


class DisguiseTokens(Resource):

    def get(self, server_id):

        disguise_threads = []

        for token in tokens.return_tokens():
            disguise_thread = threading.Thread(target=disguise_token, args=[server_id, token])
            disguise_thread.daemon = True
            disguise_threads.append(disguise_thread)

        execute_threads(disguise_threads)

        return response(200, "Bots attempted to disguise. If they haven't disguised, might be a server issue.")
