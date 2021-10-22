import threading
from src.core.Util import *
from flask_restful import request
from flask_restful import Resource
from src.core.Container import tokens
from src.core.Endpoints import *


class JoinServer(Resource):

    def post(self):
        params = json.loads(request.get_data().decode())

        if "invite" in params:

            invite = clean_input(params["invite"])[0]

            if "discord" in invite:

                check_invite = invite.split("/")

                if check_invite[3] == 'invite':
                    invite_code = check_invite[4]
                else:
                    invite_code = check_invite[3]

                join_threads = []

                for token in tokens.return_tokens():
                    join_thread = threading.Thread(target=send, args=[f'invites/{invite_code}', "POST", token])
                    join_thread.daemon = True
                    join_threads.append(join_thread)

                execute_threads(join_threads)

                return response(200, "Bots have joined the target server.")

            else:
                return response(400, "Invalid server invite, include full invite URL.")

        else:
            return response(500, "Could not join server, missing parameters.", 3)
