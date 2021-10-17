from src.core.Util import *
from base64 import b64encode
from selenium import webdriver
from flask_restful import request
from flask_restful import Resource
from src.core.Container import tokens


class JoinServer(Resource):

    def post(self, server_id):
        params = json.loads(request.get_data().decode())

        xsuperraw = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "browser_version": "91.0.4472.124",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": 89709,
            "client_event_source": None
        }

        if "invite" and "channel_id" in params:

            xcontentraw = {
                "location": "Join Guild",
                "location_guild_id": server_id,
                "location_channel_id": params['channel_id'],
                "location_channel_type": 0
            }

            # TODO: Make a input clean function.
            invite = params['invite'].replace('\n', '')

            xsuper = b64encode(json.dumps(xsuperraw).encode('utf-8')).decode("utf-8")
            xcontent = b64encode(json.dumps(xcontentraw).encode('utf-8')).decode("utf-8")

            options = webdriver.ChromeOptions()
            options.headless = True
            options.add_argument("--no-sandbox")
            options.add_argument("--log-level=3")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-crash-reporter")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-in-process-stack-traces")
            options.add_argument("--disable-logging")
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])

            if "discord" in invite:

                check_invite = invite.split("/")

                if check_invite[3] == 'invite':
                    invite_code = check_invite[4]
                else:
                    invite_code = check_invite[3]

                browser = webdriver.Chrome(options=options, executable_path=os.path.join('chromedriver.exe'))

                browser.get('https://discord.com/login')

                for token in tokens.return_tokens():

                    browser.execute_script(
                        'const iframe = document.createElement("iframe");document.head.append(iframe);const pd = Object.getOwnPropertyDescriptor(iframe.contentWindow, "sessionStorage");iframe.remove();    Object.defineProperty(window, "sessionStorage", pd);')
                    browser.execute_script(f"window.sessionStorage.setItem('token', '\"{token}\"');")
                    browser.refresh()

                    browser.execute_script(
                        'fetch("https://discord.com/api/v9/invites/' + invite_code + '", {"headers": {"accept": "*/*","accept-language": "en-US","authorization": "' + token + '","sec-ch-ua-mobile": "?0","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","x-context-properties": "' + xcontent + '","x-super-properties": "' + xsuper + '"},"referrer": "https://discord.com/channels/@me","referrerPolicy": "strict-origin-when-cross-origin","body": null,"method": "POST","mode": "cors","credentials": "include"});')

                browser.close()

                return response(200, "Bots have joined the target server.")

            else:
                return response(400, "Invalid server invite, include full invite URL.")

        else:
            return response(500, "Could not join server, missing parameters.", 3)
