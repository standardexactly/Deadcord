from time import sleep
from src.core.Util import *

locations = {
    'Desktop': return_path('Desktop'),
    'Documents': return_path('Documents'),
    'Downloads': return_path('Downloads'),
    'Deadcord': '../../'
}


class Tokens:

    def __init__(self):
        self.tokens = []

        for loc, path in locations.items():
            console_log(f'Searching {loc}.')
            full_path = os.path.join(path, "tokens.txt")
            if os.path.exists(full_path):
                console_log(f'Token file found in {loc}.', 2)
                self.get_tokens(full_path)
                found = True
                break
            else:
                found = False

        if not found:
            if console_log('Could not find any token files. Search again?', 4).lower() == 'y':
                self.__init__()
            else:
                console_log('No token files found. Deadcord will now shutdown.', 3)
                sleep(4)
                exit()

    def get_tokens(self, file):
        self.tokens.clear()
        if os.path.exists(file):
            with open(file, "r") as token:
                lines = token.readlines()
                for line in lines:
                    extract = line.replace('\n', '')
                    if not extract[0] == "#":
                        self.tokens.append(extract)
                return True
        else:
            return False

    def return_tokens(self):
        return self.tokens

    def clear_tokens(self):
        self.tokens.clear()
