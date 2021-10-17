import os
import shutil
import requests
from src.core.Util import *
from src.core.Container import pc_local
from src.modules.Asar import extract_asar, build_asar


class Injector:

    def __init__(self):

        # Path to Discord.
        DISCORD = os.path.join(pc_local, "Discord")

        # Get latest version number.
        release = open(os.path.join(DISCORD, 'packages\\RELEASES'), 'r')
        release_line = release.readline().split('-')[2]
        version = release_line.split('.')[:-1]

        # Get correct injection path.
        MODULES = os.path.join(DISCORD, f'app-{".".join(version)}\\modules')

        # Get all desktop core folders.
        folder_numbers = []
        for folder in os.listdir(MODULES):
            if "discord_desktop_core" in folder:
                number = int(folder.split('-')[1])
                folder_numbers.append(number)

        # Find the most recent folder version.
        folder_numbers.sort()
        DESKTOP_CORE_PATH = os.path.join(MODULES, f'discord_desktop_core-{folder_numbers[-1]}')
        if os.path.exists(DESKTOP_CORE_PATH):
            ASAR_PATH = os.path.join(DESKTOP_CORE_PATH, 'discord_desktop_core')

            # Extract and backup Discord core.asar.
            extract_asar(ASAR_PATH + "\\core.asar", os.path.join(ASAR_PATH, 'asar_extracted'))

            # Modify core file.
            main_script_path = os.path.join(ASAR_PATH, "asar_extracted\\app\\mainScreen.js")
            with open(main_script_path, 'r') as core:
                file_data = core.read()

                if "mainWindow.webContents.on('dom-ready', () => { setTimeout(() => {" not in file_data:
                    need_inject = True
                else:
                    need_inject = False

                core.close()

            # Fetch and inject payload if not already injected.
            if need_inject:
                CLIENT_PATH = os.path.join(DISCORD, 'deadcord.js')
                console_log("Injecting client into the Discord core. This may take a few moments.")
                PAYLOAD = """
mainWindow = new _electron.BrowserWindow(mainWindowOptions);
  const fs = require('fs'); 
  mainWindow.webContents.on('dom-ready', () => { setTimeout(() => {
    mainWindow.webContents.executeJavaScript(`${fs.readFileSync('""" + os.path.abspath(CLIENT_PATH).replace('\\', '\\\\') + """')}`);
  }, 3000); });
"""
                file_data = file_data.replace('mainWindow = new _electron.BrowserWindow(mainWindowOptions);', PAYLOAD)
                with open(main_script_path, 'w') as core:
                    core.write(file_data)
                    core.close()

                # Fetch the latest Deadcord client
                client = requests.get('https://raw.githubusercontent.com/Atom345/Deadcord-Client/main/deadcord-client.js').text
                with open(CLIENT_PATH, 'w') as client_file:
                    client_file.write(client)
                    client_file.close()

                # Finally build injected Discord core asar.
                build_asar(os.path.join(ASAR_PATH, 'asar_extracted'), ASAR_PATH + "\\core.asar")
                console_log("Successfully injected Deadcord client into Discord.", 2)
            else:
                shutil.rmtree(os.path.join(ASAR_PATH, 'asar_extracted'))
                console_log("Client is already injected.")
