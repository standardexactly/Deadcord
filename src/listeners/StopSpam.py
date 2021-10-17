from src.core.Util import *
from flask_restful import Resource


class StopSpam(Resource):

    def get(self):
        if change_temp_data('spam_flag', 1):
            return response(200, "Stopped current spam.")
        else:
            return response(500, "Could not stop spam! Please press CTR + C in the Deadcord engine.")
