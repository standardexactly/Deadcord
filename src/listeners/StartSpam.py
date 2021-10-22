import threading
from src.core.Util import *
from src.core.Server import *
from flask_restful import request
from flask_restful import Resource
from src.core.Container import tokens


class StartSpam(Resource):

    def post(self, server_id):
        params = json.loads(request.get_data().decode())

        if "message_content" and "mode" in params:

            # Store needed data.
            channels = scrape_channels(server_id)
            user_ids = scrape_user_ids(channels[0])
            messages = clean_input(params["message_content"])
            avatars = scrape_avatars(channels[0])

            # Enable spam flag.
            change_temp_data('spam_flag', 0)

            # Start the main spam thread.
            if len(channels) > 0:

                spam_threads = []

                console_log("Started spam.")

                for t in range(len(tokens.return_tokens())):
                    spam_thread = threading.Thread(target=start_message_thread, args=[messages, channels, params["mode"], user_ids])
                    spam_thread.daemon = True
                    spam_threads.append(spam_thread)

                execute_threads(spam_threads)
            else:
                return response(500, "An error occurred. No channels available.", 2)

        else:
            return response(500, "Could not start spam, no message content provided.", 3)
