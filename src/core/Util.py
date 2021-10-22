import os
import json
import time
from flask import jsonify
from flask import request
from colorama import Fore, Style, init

if 'PYCHARM_HOSTED' in os.environ:
    convert = False
    strip = False
else:
    convert = None
    strip = None

init(convert=convert, strip=strip)

temp_data = {
    'large_action': 0,
    'voice_flag': 0,
    'spam_flag': 0
}


def get_temp_data(temp_object):
    global temp_data
    if temp_object in temp_data:
        return temp_data[temp_object]
    else:
        return False


def change_temp_data(temp_object, value):
    global temp_data
    if temp_object in temp_data:
        temp_data[temp_object] = value
        return True
    else:
        return False


def get_config(key):
    with open('config.json', 'r') as config:
        data = json.load(config)
        config.close()
        return data[key]


def change_config(key, value):
    with open('config.json', 'r') as config:
        data = json.load(config)
        data[key] = value

    os.remove('config.json')

    with open('config.json', 'w') as config_new:
        json.dump(data, config_new, indent=4)


def console_log(text, mode=0):
    timestamp = time.strftime('%H:%M:%S')

    if mode == 0:
        print(Fore.LIGHTBLACK_EX + f'[*] [{timestamp}] ' + text + Fore.RESET)
    elif mode == 1:
        print(Fore.LIGHTYELLOW_EX + f'[#] [{timestamp}] ' + text + Fore.RESET)
    elif mode == 2:
        print(Fore.LIGHTMAGENTA_EX + f'[$] [{timestamp}] ' + text + Fore.RESET)
    elif mode == 3:
        print(Fore.LIGHTRED_EX + f'[!] [{timestamp}] ' + text + Fore.RESET)
    elif mode == 4:
        return input("[?] " + text + ": ")
    else:
        return False


def response(code=200, message="Success", data=[]):
    if code == 200:
        console_log(message, 2)
    elif code == 500:
        console_log(message, 3)

    return jsonify({
        "code": code,
        "ip": request.environ['REMOTE_ADDR'],
        "message": message,
        "data": data
    })


def return_path(location):
    path = os.path.join(os.path.join(os.environ['USERPROFILE']), location)
    return path


def clean_input(text):
    params = []
    lines = text.splitlines()
    for line in lines:
        params.append(line.replace('\n', ''))

    return params


def execute_threads(threads=[], delay=0):
    for thread in threads:
        time.sleep(delay)
        thread.start()

    for thread in threads:
        thread.join()