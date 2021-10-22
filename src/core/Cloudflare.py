import random
import requests


def rand_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 "
        "Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " "Chrome/91.0.4472.124 "
        "Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.15 ""Chrome/83.0.4103.122 "
        "Electron/9.3.5 Safari/537.36 "
    ]

    return random.choice(agents)


def get_cookie():
    session = requests.Session()
    discord = session.get('https://discord.com')
    found_cookies = session.cookies.get_dict()
    return f'__dcfduid={found_cookies["__dcfduid"]}; __sdcfduid={found_cookies["__sdcfduid"]}; locale=en-GB'


def fake_device(user_agent):
    device_info = {
        "os": "Windows",
        "browser": "Chrome",
        "device": "",
        "system_locale": "en-US",
        "browser_user_agent": user_agent,
        "browser_version": "91.0.4472.124",
        "os_version": str(random.randint(8, 10)),
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": 36127,
        "client_event_source": None
    }

    return device_info
