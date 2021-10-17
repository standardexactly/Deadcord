import sys
import random
from time import sleep
from src.core.Util import *
from src.core.Endpoints import *
from src.core.Container import tokens


def start_message_thread(messages, channels, mode=1, users=[]):
    message = random.choice(messages)
    while get_temp_data('spam_flag') == 0:
        try:
            if mode == 1:
                built_message = f'@everyone {message}'
            elif mode == 2:
                built_message = f'<@{random.choice(users)}> {message}'
            else:
                built_message = message

            channel = random.choice(channels)
            bot_send = bot_message(random.choice(tokens.return_tokens()), channel, built_message)

            if "code" in bot_send:
                if channel in channels:
                    channels.remove(channel)

            if "global" in bot_send:
                sleep(9)

        except:
            pass


def bot_message(token, channel, message):
    return send(f'channels/{channel}/messages', 'POST', token, {"content": message}).text


def scrape_user_ids(channel):
    user_ids = []
    for author in scrape_messages(channel, 80):
        user_ids.append(author['author']['id'])

    return user_ids


def scrape_messages(channel_id, amount):
    token = tokens.return_tokens()[0]
    r = send(f'channels/{channel_id}/messages?limit={int(amount)}', 'GET', token)
    return json.loads(r.text)


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


def speak(content, channels):
    for channel in channels:
        send(f'channels/{channel}/messages', 'POST', random.choice(tokens.return_tokens()), {"content": content})


def react(channel_id, message_id, emoji):
    for token in tokens.return_tokens():
        send(f'channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me', 'PUT', token)
