import threading
from src.core.Util import *
from src.core.Endpoints import *
from flask_restful import Resource
from src.core.Container import tokens


class LeaveServer(Resource):

    def get(self, server_id):
        leave_threads = []

        for token in tokens.return_tokens():
            leave_thread = threading.Thread(target=send, args=[f'users/@me/guilds/{server_id}', 'DELETE', token, {'lurking': False}])
            leave_thread.daemon = True
            leave_threads.append(leave_thread)

        execute_threads(leave_threads)
