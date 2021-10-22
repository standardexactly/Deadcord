import threading
from src.core.Util import *
from flask_restful import Resource
from src.core.Container import tokens
from src.core.Server import ping_token


class PingTokens(Resource):

    def get(self):
        ping_threads = []

        for token in tokens.return_tokens():
            ping_thread = threading.Thread(target=ping_token, args=[token])
            ping_thread.daemon = True
            ping_threads.append(ping_thread)

        execute_threads(ping_threads, 0.06)

        return response(200, 'Token ping complete.')
