import sqlite3
from collections import namedtuple
from time import ctime


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            res = func(conn, *args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS user_message')
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS user_message ( 
            id            INTEGER PRIMARY KEY,
            user_id       INTEGER NOT NULL,
            first_name    TEXT,
            adres         TEXT NOT NULL,
            text          TEXT NOT NULL,
            text_date     TEXT
        )
            ''')
    conn.commit()


@ensure_connection
def add_message(conn, user_id: int, first_name: str, adres: str, text: str):
    c = conn.cursor()
    c.execute('INSERT INTO user_message (user_id,first_name, adres, text, text_date) VALUES(?, ?, ?, ?, ?)',
              (user_id, first_name, adres, text,  ctime()))
    conn.commit()


@ensure_connection
def get_messages(conn, is_addoption: bool = None):
    c = conn.cursor()
    sql = 'SELECT user_message.id, user_base.first_name, user_base.last_name, text, adres ' \
          'FROM user_message ' \
          'JOIN user_base ON user_base.user_id = user_message.user_id'
    # if is_addoption is False:
    #     sql += ' AND addoption == ""'
    # elif is_addoption is True:
    #     sql += ' AND addoption != ""'
    c.execute(sql)
    return c.fetchall()


@ensure_connection
def get_message(conn, message_id: int):
    UserMessage = namedtuple('UserMessage', ('id', 'user_id', 'first_name', 'last_name', 'text', 'adres'))

    c = conn.cursor()
    sql = 'SELECT user_message.id, user_message.user_id, user_base.first_name, user_base.last_name, text, adres ' \
          'FROM user_message ' \
          'JOIN user_base ON user_base.user_id = user_message.user_id ' \
          'WHERE user_message.id=?'
    c.execute(sql, (message_id, ))
    item = c.fetchone()
    if item:
        return UserMessage(*item)


@ensure_connection
def set_messages_worker_user(conn, message_id: int, user_id: int):
    c = conn.cursor()
    c.execute('UPDATE user_message SET worker_user_id=? WHERE id=?', (user_id, message_id))

