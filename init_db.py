import json
import db_query

# 初始化创建
db_query.init_db()
with open('init.json') as f:
    data = json.load(f)
    for v in data:
        db_query.insert_config(v)


