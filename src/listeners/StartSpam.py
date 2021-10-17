import threading
from src.core.Util import *
from src.core.Server import *
from flask_restful import request
from flask_restful import Resource
from src.core.Container import tokens


class StartSpam(Resource):

    def post(self, server_id):
        params = json.loads(request.get_data().decode())

        if "message_content" in params:

            # Store needed data.
            channels = scrape_channels(server_id)
            user_ids = scrape_user_ids(channels[0])
            messages = []

            # TODO: Make a input clean function.
            lines = params["message_content"].splitlines()
            for line in lines:
                messages.append(line)

            # Enable spam flag.
            change_temp_data('spam_flag', 0)

            # Start the main spam thread.
            if len(channels) > 0:
                thread_amount = len(tokens.return_tokens())

                console_log("Started spam.")

                for t in range(thread_amount):
                    spam_thread = threading.Thread(target=start_message_thread, args=[messages, channels, 1])
                    spam_thread.start()
            else:
                return response(500, "An error occurred. No channels available.", 2)

        else:
            return response(500, "Could not start spam, no message content provided.", 3)
