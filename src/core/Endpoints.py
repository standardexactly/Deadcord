import requests


def send(endpoint, method, token, data=None, useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36", proxies=None):
    base = "https://discord.com/api/v9/"

    if method == 'GET':
        r = requests.get(base + endpoint, headers={'Authorization': token, 'User-Agent': useragent},
                         json=data)
    elif method == 'POST':
        r = requests.post(base + endpoint, headers={'Authorization': token, 'User-Agent': useragent},
                          json=data)
    elif method == 'PUT':
        r = requests.put(base + endpoint, headers={'Authorization': token, 'User-Agent': useragent},
                         json=data)
    elif method == 'PATCH':
        r = requests.patch(base + endpoint, headers={'Authorization': token, 'User-Agent': useragent},
                           json=data)
    elif method == 'DELETE':
        r = requests.delete(base + endpoint, headers={'Authorization': token, 'User-Agent': useragent},
                            json=data)
    return r
