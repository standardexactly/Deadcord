import sys
import random
from time import sleep
from src.core.Util import *
from src.core.Endpoints import *
from src.core.Container import tokens


def random_name():
    name_fetch = requests.get('https://api.namefake.com/').text
    name = json.loads(name_fetch)
    return name["username"]


def start_message_thread(messages, channels, mode, users=[]):
    message = random.choice(messages)
    bot_tokens = tokens.return_tokens()

    if mode == 1:
        built_message = f'@everyone {message}'
    elif mode == 2:
        built_message = f'<@{random.choice(users)}> {message}'
    elif mode == 3:
        blank_payload = ""
        for newline in range(1700):
            blank_payload += "\n"

        built_message = f"\n‎{blank_payload}‎\n"
    elif mode == 4:
        lag_payload = ""
        for newline in range(140):
            lag_payload += ":chains: "

        built_message = f"\n‎{lag_payload}‎\n"
    else:
        built_message = message

    while get_temp_data('spam_flag') == 0:
        try:
            channel = random.choice(channels)
            bot_send = bot_message(random.choice(bot_tokens), channel, built_message)

            if "code" in bot_send:
                if channel in channels:
                    channels.remove(channel)

            if "global" in bot_send:
                sleep(9)

        except:
            pass


def bot_message(token, channel, message):
    bot_message_send = send(f'channels/{channel}/messages', 'POST', token, {"content": message})
    return bot_message_send.json()


def change_avatar(url, token):
    avatar = requests.get(url)
    image = "data:image/png;base64," + b64encode(avatar.content).decode('utf-8')
    imagePayload = {"avatar": image}

    avatar_change = send("users/@me", "PATCH", token, imagePayload).text

    if "code" in avatar_change:
        return False
    else:
        return True


def change_nick(name, server_id, token):
    if name == "random":
        nickname = random_name()
    else:
        nickname = name

    send(f'guilds/{server_id}/members/@me', 'PATCH', token, {'nick': nickname})


def reset_avatar(token):
    imagePayload = {"avatar": None}
    avatar_change = send("users/@me", "PATCH", token, imagePayload).text

    if "code" in avatar_change:
        return False
    else:
        return True


def scrape_user_ids(channel):
    user_ids = []
    for author in scrape_messages(channel, 100):
        if author['author']['id'] not in user_ids:
            user_ids.append(author['author']['id'])

    return user_ids


def scrape_usernames(channel):
    usernames = []
    for username in scrape_messages(channel, 30):
        if username['author']['username'] not in usernames:
            usernames.append(username['author']['username'])

    return usernames


def scrape_messages(channel_id, amount):
    token = tokens.return_tokens()[0]
    r = send(f'channels/{channel_id}/messages?limit={int(amount)}', 'GET', token)
    return json.loads(r.text)


def scrape_avatars(channel):
    avatars = {}
    for avatar in scrape_messages(channel, 100):
        if avatar['author']['username'] not in avatars.keys():
            if avatar['author']['avatar'] is not None:
                avatars[avatar['author']['avatar']] = [avatar['author']['username'], avatar['author']['id']]

    return avatars


def scrape_channels(server_id):
    lead_token = tokens.return_tokens()[0]
    channels = send(f'guilds/{server_id}/channels', 'GET', lead_token).text
    data = json.loads(channels)

    found_channels = []

    for channel in data:
        if 'bitrate' not in channel and channel['type'] == 0:
            if channel not in found_channels:
                found_channels.append(channel["id"])

    return found_channels


def can_ping_everyone(channel):
    msg = json.loads(bot_message(tokens.return_tokens()[0], channel, "@everyone"))
    if msg["mention_everyone"]:
        return True
    else:
        return False


def react(channel_id, message_id, emoji, token):
    react_send = send(f'channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me', 'PUT', token)
    return react_send.json()


def ping_token(token):
    token_ping = send('users/@me/library', 'GET', token).status_code

    if token_ping == 200:
        console_log(token, 2)
    elif token_ping == 401:
        console_log(token, 1)
    elif token_ping == 403:
        console_log(token, 3)


def disguise_token(server_id, token):
    reset_avatar(token)
    avatar_change = change_avatar(f'https://picsum.photos/200/200', token)

    if avatar_change:
        alias = send(f'guilds/{server_id}/members/@me', 'PATCH', token, {'nick': random_name() + str(random.randint(1, 100))}).text
