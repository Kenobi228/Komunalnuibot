import sqlite3
from time import ctime


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            res = func(conn, *args, **kwargs)
        return res

    return inner


@ensure_connection
def init_petition_db(conn, force: bool = False):
    cс = conn.cursor()
    if force:
        cс.execute('DROP TABLE IF EXISTS user_petition')
    cс.execute(''' 
        CREATE TABLE IF NOT EXISTS user_petition ( 
            id            INTEGER PRIMARY KEY,
            user_id       INTEGER NOT NULL, 
            first_name        TEXT,
            petition          TEXT NOT NULL , 
            petition_date     TEXT
            )
            ''')
    conn.commit()


@ensure_connection
def add_petition(conn: sqlite3.Connection, user_id: int, first_name: str, petition: str):
    c = conn.cursor()
    c.execute('INSERT INTO user_petition (user_id, first_name ,  petition , petition_date) VALUES(?,?, ?, ?)',
              (user_id, first_name, petition, ctime()))
    conn.commit()
