import psycopg2
import psycopg2.extras
from db import dbconnection

def get_dict_resultset(sql):
    conn = dbconnection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql)
    ans =cur.fetchall()
    dict_result = []
    for row in ans:
        dict_result.append(dict(row))
    return dict_result
