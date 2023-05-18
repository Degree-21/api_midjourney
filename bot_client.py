import asyncio
import discord
import os
import certifi
import json
import requests
import re

import db_query
import define
from gevent import monkey

# monkey.patch_all()
from multiprocessing import Process, Queue

# import gevent

os.environ["SSL_CERT_FILE"] = certifi.where()


class BotClient:
    # discord user token
    __discord_user_token = ""
    # discord bot token
    __discord_bot_token = ""
    # discord server id
    __discord_server_id = ""
    # discord channel id
    __discord_channel_id = ""
    # message call_back
    __message_receiver_url = ""
    # discord_client
    __discord_client = None
    #
    __flags = "--v 5"
    # use status
    __use_status = False

    # __proxy = "http://127.0.0.1:7890"
    __proxy = os.getenv("proxy")

    def __init__(self, client_info: dict):
        self.__discord_user_token = client_info["discord_user_token"]
        self.__discord_bot_token = client_info["discord_bot_token"]
        self.__discord_server_id = client_info["discord_server_id"]
        self.__discord_channel_id = client_info["discord_channel_id"]
        self.__message_receiver_url = client_info["message_receiver_url"]
        self.__flags = "--v 5"
        self.__use_status = False
        self.__discord_client = None

    def set_use_status(self, status: bool):
        self.__use_status = status

    def get_use_status(self):
        return self.__use_status

    def run(self):
        print(self.__proxy)
        intents = discord.Intents.all()
        client = discord.Client(intents=intents, proxy=self.__proxy)
        self.__discord_client = client
        self.__register_listen()
        self.__discord_client.run(self.__discord_bot_token)

    def close(self):
        self.__discord_client.close()

    def __register_listen(self):
        @self.__discord_client.event
        async def on_message(message):
            self.call_back_message()

        @self.__discord_client.event
        async def on_ready():
            print('已登录为 {0.user}'.format(self.__discord_client))
            self.call_back_message()

    def call_back_message(self):
        chat_history = self.get_images()
        for v in chat_history:
            if v["author"]["id"] != "936929561302675456":
                continue
            prompt = define.get_message(v["content"])
            task_info = db_query.get_task_by_prompt(prompt)
            if task_info is None:
                continue
            if len(task_info["message_receiver_url"]) < 1:
                print("task not call back prompt [{}] , text [{}]".format(prompt, v))
                continue
            response = requests.post(url=task_info["message_receiver_url"], json=v)
            print("on_message call back info [{}]".format(response.text))

    def send_mj_prompt(self, prompt: str):
        header = {
            'authorization': self.__discord_user_token
        }

        prompt = prompt.replace('_', ' ')
        prompt = " ".join(prompt.split())
        prompt = re.sub(r'[^a-zA-Z0-9\s]+', '', prompt)
        prompt = prompt.lower()
        application_id = "936929561302675456"
        version = "1077969938624553050"
        payload = {'type': 2,
                   'application_id': application_id,
                   'guild_id': self.__discord_server_id,
                   'channel_id': self.__discord_channel_id,
                   'session_id': "cb06f61453064c0983f2adae2a88c223",
                   'data': {
                       'version': version,
                       'id': "938956540159881230",
                       'name': 'imagine',
                       'type': 1,
                       'options': [{'type': 3, 'name': 'prompt', 'value': str(prompt) + ' ' + self.__flags}],
                       'attachments': []}
                   }
        r = requests.post('https://discord.com/api/v9/interactions', json=payload, headers=header, proxies={
            'http': self.__proxy,
            'https': self.__proxy,
        })
        if r.status_code != 204:
            raise Exception('prompt [{}] send fail , response [{}]'.format(prompt, r.text))
        # while r.status_code != 204:
        #     r = requests.post('https://discord.com/api/v9/interactions', json=payload, headers=header)
        print('prompt [{}] successfully sent! , resp [{}]'.format(prompt, r.text))

    def get_images(self):
        header = {
            'authorization': self.__discord_user_token
        }
        r = requests.get(
            f'https://discord.com/api/v10/channels/{self.__discord_channel_id}/messages?limit={50}',
            headers=header, proxies={
                'http': self.__proxy,
                'https': self.__proxy,
            })
        json_map = json.loads(r.text)
        return json_map
