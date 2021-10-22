import json
import requests
from .Cloudflare import *
from base64 import b64encode


def send(endpoint, method, token, data=None, proxies=None):
    if data is None:
        data = {}

    base = "https://discord.com/api/v9/"
    user_agent = rand_user_agent()

    headers = {
        "Accept": "*/*",
        "Accept-language": "en-GB",
        "Authorization": token,
        "Content-length": "2",
        "Content-type": "application/json",
        "Cookie": get_cookie(),
        "Origin": "https://discord.com",
        "Sec-fetch-dest": "empty",
        "Sec-fetch-mode": "cors",
        "Sec-fetch-site": "same-origin",
        "User-agent": user_agent,
        "X-debug-options": "bugReporterEnabled",
        "X-super-properties": b64encode(json.dumps(fake_device(user_agent)).encode('utf-8')).decode("utf-8"),
    }

    if method == 'GET':
        remove = ["Content-length", "Content-type"]
        for key in remove:
            del headers[key]

        r = requests.get(base + endpoint, headers=headers)
    elif method == 'POST':
        r = requests.post(base + endpoint, headers=headers,
                          json=data)
    elif method == 'PUT':
        r = requests.put(base + endpoint, headers=headers,
                         json=data)
    elif method == 'PATCH':
        r = requests.patch(base + endpoint, headers=headers,
                           json=data)
    elif method == 'DELETE':
        r = requests.delete(base + endpoint, headers=headers,
                            json=data)

    return r
