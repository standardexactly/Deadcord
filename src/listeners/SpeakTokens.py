import threading
from src.core.Util import *
from src.core.Server import *
from flask_restful import Resource


class SpeakTokens(Resource):

    def post(self, server_id):
        params = json.loads(request.get_data().decode())

        if "message_content" in params:

            speak_threads = []
            bot_tokens = tokens.return_tokens()
            channels = scrape_channels(server_id)
            message = clean_input(params["message_content"])[0]

            for channel in channels:
                speak_thread = threading.Thread(target=bot_message, args=[random.choice(bot_tokens), channel, message])
                speak_thread.daemon = True
                speak_threads.append(speak_thread)

            execute_threads(speak_threads, 0.06)

            return response(200, 'Token speak complete.')

        else:
            return response(500, "No parameters provided.", 2)