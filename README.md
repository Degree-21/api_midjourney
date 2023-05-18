# Midjourney_api Usage Instructions

## 中文教程：[README_zh.md](./README_zh.md)
## Note

- You need to have a subscription to the Midjourney robot, and open your own channel and add it to your designated channel.
- You need to create a bot yourself and join it to the above channels to use the subsequent api.
- Due to rapid development of the code, there may be instability. If there is any problem, please contact me in time.
- Part of the code comes from: https://github.com/George-iam/Midjourney_api
- For Chinese users who need to modify the proxy, please modify the proxy = "" in .env to the proxy address.

## Modify the init.json file

Before using Midjourney_api, you need to modify the data in the init.json file. This file supports multi-account configuration, including:

- discord_user_token: authorization for Discord, used for user authorization;
- message_receiver_url: callback address, currently not filled.

Please modify the init.json file according to the following format:

```json
[
    {
        "discord_user_token": "*.GwNqMb.rqwJWt-ALeGgpUmIuUyYCBMJsuJIULeC2BJXpI",
        "discord_bot_token": "*.GvTX-J._T6TQKZWFk_KwayDJxflhuNB_4cvbgvJKtQF9Q",
        "discord_server_id": "*",
        "discord_channel_id": "*",
        "message_receiver_url": "",
        "use_status": "1",
        "listen_status": "1"
    }
]
```
Where `use_status` and `listen_status` are parameters used by the system, please do not modify them.

## Start the service

After modifying the init.json file, you can start the Midjourney_api service by executing the following command:

```
python3 install -r requirements.txt  
python3 init_db.py  
python3 app.py
```

## Use API

Before performing the following operations, please make sure that the relevant dependencies have been installed and the data has been initialized as described above.

### API Address

The API address is: `http://127.0.0.1:5000/send_prompt`

### Parameters

The request parameters should contain the following fields:

```json
{
    "message_receiver_url": "",
    "prompt": "debug"
}
```

Where `message_receiver_url` field is the prompt callback address, and `prompt` is the prompt word to be entered.

### Example Code

You can refer to the following example code to use the API:

```python
import requests
import json

url = 'http://127.0.0.1:5000/send_prompt'

payload = {
    "message_receiver_url": "",
    "prompt": "debug"
}

headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.content)
```

### Note

When using the API, please note the following:

- It will randomly take one bot to listen from the init.json file you imported.
- It will wait for the message recording data to return and call back to the message_receiver_url you specified through post.

I hope this document is helpful to you. If you have any other needs or questions, please contact me.