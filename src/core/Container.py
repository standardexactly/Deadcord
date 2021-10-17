import os
from src.core.Tokens import Tokens

# Fetch tokens.
tokens = Tokens()

# Needed computer paths.
pc_roaming = os.getenv('APPDATA')
pc_local = os.getenv('LOCALAPPDATA')
