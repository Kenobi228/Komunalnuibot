import sqlite3
from time import ctime

def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            res = func(conn, *args, **kwargs)
        return res
    return inner

@ensure_connection
def init_user_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS user_base')
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS user_base ( 
            user_id            INTEGER PRIMARY KEY NOT NULL,
            username           TEXT,
            first_name         TEXT,
            last_name          TEXT, 
            flat               TEXT,
            reg_date           TEXT 
        )
            ''')
    conn.commit()

@ensure_connection
def get_user(conn: sqlite3.Connection, user_id: int):
    c = conn.cursor()
    c.execute('SELECT * FROM user_base WHERE user_id=?', (user_id ,))
    return c.fetchone()

@ensure_connection
def get_user_id(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute('select user_id from user_base')
    row = []
    for user_id in c.fetchall():
        i = user_id
        row.append(i)

    return row

@ensure_connection
def register_user(conn: sqlite3.Connection, user_id: int, username: str, first_name: str, last_name: str, flat: str):
    c = conn.cursor()
    c.execute('INSERT INTO user_base (user_id, username, first_name,  last_name, flat, reg_date) VALUES(?, ?, ? , ? , ?, ?)',
              (user_id, username, first_name, last_name,flat, ctime()))
    conn.commit()
