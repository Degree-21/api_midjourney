import sqlite3
import random
from collections import namedtuple

ListenStatus = 1
NotListenStatus = 2
UseStatus = 1
NotUseStatus = 2


def trace_sql(sql_statement):
    print("SQL执行：", sql_statement)


def get_conn():
    conn = sqlite3.connect('config.db')
    # conn.set_trace_callback(trace_sql)
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    # 创建表
    c.execute('''CREATE TABLE IF NOT EXISTS config
                    (id INTEGER PRIMARY KEY,
                    discord_user_token TEXT,
                    discord_bot_token TEXT,
                    discord_server_id TEXT,
                    discord_channel_id TEXT,
                    message_receiver_url TEXT,
                    use_status int,
                    listen_status int
                    )''')

    # 创建表
    c.execute('''CREATE TABLE IF NOT EXISTS task
                    (id INTEGER PRIMARY KEY,
                    task_name TEXT,
                    task_status TEXT,
                    discord_server_id TEXT,
                    discord_channel_id TEXT,
                    prompt TEXT,
                    message_receiver_url TEXT
                    )''')
    # # 读取JSON数据并插入到表中
    # tempJson = """[
    #     {
    #         "discord_user_token": "OTEyNjA2MzM5NzUzMTgxMjU1.GwNqMb.rqwJWt-ALeGgpUmIuUyYCBMJsuJIULeC2BJXpI",
    #         "discord_bot_token": "MTA5MjcxMjAyNDUzMTgxMjM2Mg.GvTX-J._T6TQKZWFk_KwayDJxflhuNB_4cvbgvJKtQF9Q",
    #         "discord_server_id": "1092711724379029547",
    #         "discord_channel_id": "1092732419825741856",
    #         "message_receiver_url": "",
    #         "use_status": "1",
    #         "listen_status": "1"
    #     }
    # ]"""
    # json_maps = json.loads(tempJson)
    # for data in json_maps:
    #     print(data.keys())
    #     c.execute(f"INSERT INTO config ({','.join(data.keys())}) VALUES (?, ?, ?, ?, ?,?,?)", tuple(data.values()))
    # # 增加字段
    conn.commit()
    conn.close()


def get_random_config():
    conn = get_conn()
    conn.set_trace_callback(trace_sql)
    c = conn.cursor()
    c.execute("SELECT * FROM config WHERE listen_status=1")
    results = c.fetchall()  # 获取查询结果，返回一个元组列表

    if not results:
        print('未找到符合条件的记录')
        return None

    # 随机选择一条记录
    result = random.choice(results)
    print('随机选中的记录：', result)

    # 将字段名与字段值组成字典
    columns = [desc[0] for desc in c.description]
    result_dict = dict(zip(columns, result))
    conn.close()
    return result_dict


def get_task_by_name(task_name):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM task WHERE task_name=?", (task_name,))
    result = c.fetchone()
    conn.close()

    if result:
        columns = [desc[0] for desc in c.description]
        return dict(zip(columns, result))
    else:
        return None


def get_task_by_prompt(prompt):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM task WHERE prompt=?", (prompt,))
    result = c.fetchone()
    conn.close()

    if result:
        columns = [desc[0] for desc in c.description]
        return dict(zip(columns, result))
    else:
        return None


def get_config_by_discord_bot_token(discord_bot_token):
    conn = get_conn()
    conn.set_trace_callback(trace_sql)
    # 连接到数据库
    c = conn.cursor()

    # 根据 discord_bot_token 查询记录
    c.execute("SELECT * FROM config WHERE discord_bot_token=?", (discord_bot_token,))
    result = c.fetchone()  # 获取查询结果，返回一个元组

    if not result:
        print(f'未找到 discord_bot_token 为 {discord_bot_token} 的记录')
        return None

    # 将字段名与字段值组成字典
    columns = [desc[0] for desc in c.description]
    result_dict = dict(zip(columns, result))
    conn.close()

    # 关闭连接
    return result_dict


def get_listen_status_data():
    conn = get_conn()
    cursor = conn.cursor()

    query = cursor.execute("SELECT * FROM config WHERE listen_status=?", (1,))
    results = query.fetchall()

    columns = [desc[0] for desc in cursor.description]
    Record = namedtuple('Record', columns)

    # 将结果集转换为数组映射
    return [dict(r._asdict()) for r in [Record(*row) for row in results]]


def insert_config(config):
    conn = get_conn()
    conn.set_trace_callback(trace_sql)
    # 连接到数据库
    c = conn.cursor()
    # 插入一条记录
    c.execute(
        "INSERT INTO config (discord_user_token, discord_bot_token, discord_server_id, discord_channel_id, message_receiver_url, use_status, listen_status) VALUES (:discord_user_token, :discord_bot_token, :discord_server_id, :discord_channel_id, :message_receiver_url, :use_status, :listen_status)",
        config)

    # 提交更改
    conn.commit()
    conn.close()


def update_listen_status_by_discord_bot_token(discord_bot_token, listen_status):
    conn = get_conn()
    conn.set_trace_callback(trace_sql)
    c = conn.cursor()
    # 根据 discord_bot_token 更新 listen_status
    sql = """UPDATE config SET listen_status=? WHERE discord_bot_token=?"""
    c.execute("UPDATE config SET listen_status=? WHERE discord_bot_token=?", (listen_status, discord_bot_token))
    print("UPDATE config SET listen_status=? WHERE discord_bot_token=?", (listen_status, discord_bot_token))
    # 提交更改
    conn.commit()
    conn.close()


def insert_task_data(task_dict):
    # 连接数据库
    conn = get_conn()

    # 创建游标对象
    cur = conn.cursor()

    # 插入数据
    cur.execute(
        "INSERT INTO task (task_name, task_status, discord_server_id, discord_channel_id,prompt, message_receiver_url) VALUES (?, ?, ?, ?, ?,?)",
        (task_dict['task_name'], task_dict['task_status'], task_dict['discord_server_id'],
         task_dict['discord_channel_id'], task_dict["prompt"], task_dict['message_receiver_url']))

    # 提交更改
    conn.commit()

    # 关闭连接
    conn.close()


if __name__ == "__main__":
    # get_random_config()
    # get_not_use_account()
    # res = get_config_by_discord_bot_token("1MTA5MjcxMjAyNDUzMTgxMjM2Mg.GvTX-J._T6TQKZWFk_KwayDJxflhuNB_4cvbgvJKtQF9Q")
    res = get_listen_status_data()
    print(res)
