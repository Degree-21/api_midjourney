import multiprocessing as mp
import bot_client
from flask import Flask, request
import db_query

app = Flask(__name__)

# 全局变量
bot_dict = {}


@app.route('/')
def index():
    return 'Hello, World!'


# @app.route("/robot_process", methods=['POST'])
# def robot_process():
#     data = request.get_json()
#     process_type = data["process_type"]
#     if process_type == "1":
#         api_request_id = data["discord_bot_token"]
#         parent_conn, child_conn = mp.Pipe()
#         process = mp.Process(target=start_bot, args=(data,))
#         process.start()
#         bot_dict[api_request_id] = (process, parent_conn, child_conn)
#         return '{"data":"","message":"success","code":200}'
#     stop_bot(params=data)
#     return '{"data":"","message":"success","code":200}'


@app.route("/send_prompt", methods=['POST'])
def send_prompt():
    data = request.get_json()
    mj_config = db_query.get_random_config()
    if mj_config is None:
        return '{"data":"","message":"not listen account","code":500}'

    # mj_config.
    client_class = bot_client.BotClient(client_info=data)
    try:
        client_class.send_mj_prompt(data["prompt"])
        task_data = {
            'task_name': hash(data["prompt"]),
            'task_status': 1,
            'discord_server_id': mj_config["discord_server_id"],
            "prompt": data["prompt"],
            'discord_channel_id': mj_config["discord_channel_id"],
            'message_receiver_url': data["message_receiver_url"]
        }
        db_query.insert_task_data(task_data)

        return '{"data":"","message":"success","code":200}'
    except Exception as e:
        print(e)
        return '{"data":"","message":"fail","code":500}'


# sync start bot
def start_bot(params):
    api_request_id = params["discord_bot_token"]
    # 根据一个bot token获取一个数据
    bot_info = db_query.get_config_by_discord_bot_token(api_request_id)
    client_class = bot_client.BotClient(client_info=params)
    if bot_info is None:
        params["listen_status"] = db_query.ListenStatus
        params["use_status"] = db_query.UseStatus
        db_query.insert_config(params)
    else:
        db_query.update_listen_status_by_discord_bot_token(api_request_id, db_query.ListenStatus)
    client_class.run()
    return "Bot started for api request {}".format(api_request_id)


# stop bot listen
def stop_bot(params):
    print("stop", params)
    api_request_id = params["discord_bot_token"]
    if api_request_id in bot_dict:
        parent_conn, child_conn = bot_dict[api_request_id][1:]
        process = bot_dict[api_request_id][0]
        child_conn.send("stop")  # 向子进程发送停止信号
        process.terminate()  # 终止子进程
        process.join()
        del bot_dict[api_request_id]
    db_query.update_listen_status_by_discord_bot_token(api_request_id, db_query.NotListenStatus)


def cache_start():
    listen_all = db_query.get_listen_status_data()
    if len(listen_all) < 1:
        raise Exception("not init json datat")
    for v in listen_all:
        process = mp.Process(target=start_bot, args=(v,))
        process.start()


if __name__ == '__main__':
    db_query.init_db()
    cache_start()
    app.run()
