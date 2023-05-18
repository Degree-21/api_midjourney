# Midjourney_api使用说明

## 注意事项

- 你需要有一个Midjourney订阅机器人，并且开自己开通一个频道，将他添加到你指定的频道
- 你需要自己创建一个机器人，并且加入到上面的频道中，才可以使用后续的api
- 代码由于快速开发，可能存在不稳定型，有问题请及时与我联系
- 部分代码来自：https://github.com/George-iam/Midjourney_api
- 国内用户需要修改代理的话请修改 bot_client 中的 __proxy = ""  

## 修改init.json文件

在使用Midjourney_api之前，您需要先修改init.json文件中的数据。该文件支持多账号配置，具体信息包括：

- discord_user_token: Discord的authorization，用于用户授权；
- message_receiver_url: 回调地址，暂时不填。

请按照以下格式修改init.json文件：

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
其中 use_status和listen_status均为系统使用的参数，请勿修改。

## 启动服务

完成init.json文件的修改后，您可以执行以下命令来启动Midjourney_api服务：

```
python3 install -r requirements.txt  
python3 init_db.py  
python3 app.py
```

## 使用API

在进行下列操作之前，请确保已经按照上面安装了相关依赖及初始化数据

### API地址

API地址为：`http://127.0.0.1:5000/send_prompt`

### 参数

请求参数应包含以下字段：

```json
{
    "message_receiver_url": "",
    "prompt": "debug"
}
```

其中，`message_receiver_url` 字段为 prompt 回调地址，`prompt` 为需要输入的提示词。

### 示例代码

可以参考以下示例代码来使用 API：

```python
import requests
import json

url = 'http://127.0.0.1:5000/send_prompt?a=1'

payload = {
    "message_receiver_url": "",
    "prompt": "debug"
}

headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.content)
```

### 注意事项

在使用 API 时需要注意以下事项：

- 他将从你导入的init.json中随机取一个机器人监听
- 他将会等待 消息记录的数据返回后回调到你给定的 message_receiver_url， 通过post的形式

希望这份文档能够对您有所帮助。如果您有其他需求或疑问，欢迎与我联系。

