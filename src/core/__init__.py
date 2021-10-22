from .Inject import Injector
from .Endpoints import *
from .Container import *
from .Server import *
from .Quotes import *
from .Tokens import *
from .Util import *

# Create config file if it doesnt exist.
if not os.path.exists('config.json'):
    with open('config.json', 'w') as config:
        config.write("""{"boot_mode": 0}""")
        config.close()

# Display boot mode.
console_log(f'Booting on mode {str(get_config("boot_mode"))}.')

# Check if client is injected.
Injector()
