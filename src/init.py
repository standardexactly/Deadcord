import sys
import logging
from src.core import *
from flask import Flask
from src.app import api_bp

os.system('cls')

startup = Style.BRIGHT + f'''

                         ██████╗ ███████╗ █████╗ ██████╗  ██████╗ ████████╗ ██████╗ ██████╗ 
                         ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██████████╗██╔══██╗██╔══██╗
                         ██║  ██║█████╗  ███████║██║  ██║██║     ██║ ██  ██║██████╔╝██║  ██║
                         ██║  ██║██╔══╝  ██╔══██║██║  ██║██║     ████  ████║██╔══██╗██║  ██║
                         ██████╔╝███████╗██║  ██║██████╔╝╚██████╗╚████████╔╝██║  ██║██████╔╝
                         ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ █═█═█═█═╝ ╚═╝  ╚═╝╚═════╝   

                                    ┏━━━━━━━━━━━━━━━━━━ Info ━━━━━━━━━━━━━━━━┓
                                      {Fore.RESET}{Fore.LIGHTMAGENTA_EX}@ Package: {Fore.WHITE}Deadcord-Engine{Fore.LIGHTMAGENTA_EX}
                                      {Fore.RESET}{Fore.LIGHTMAGENTA_EX}@ Author: {Fore.WHITE}Galaxzy#4845{Fore.LIGHTMAGENTA_EX}
                                      {Fore.RESET}{Fore.LIGHTMAGENTA_EX}@ Warning: {Fore.RED}Use at your own risk!{Fore.LIGHTMAGENTA_EX}
                                    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛       
                                    
{Fore.LIGHTBLACK_EX} Starting the Deadcord Engine ~ {random_quote()}{Fore.RESET} ~ {Fore.LIGHTMAGENTA_EX}Version 0.0.1{Fore.RESET}
{Fore.WHITE}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{Fore.RESET}
'''.replace('█', f'{Fore.WHITE}█{Fore.LIGHTMAGENTA_EX}')

# Show startup dialog.
print(startup)

# Start a listening server.
app = Flask(__name__)

# Disable not needed console output.
if not get_config("boot_mode") == 1:
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

# Routing and config
app.register_blueprint(api_bp, url_prefix='/deadcord')


# Fiddle with COR's to receive requests.
@app.after_request
def after_request(status):
    status.headers.add('Access-Control-Allow-Origin', '*')
    status.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    status.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return status
