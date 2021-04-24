import sqlite3
from time import ctime

def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            res = func(conn, *args, **kwargs)
        return res
    return inner

@ensure_connection
def init_indexes_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS indexes_base')
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS indexes_base ( 
            user_id            TEXT,
            username           TEXT,
            light              TEXT,
            cold_water         TEXT, 
            hot_water          TEXT, 
            gas                TEXT, 
            indexes_date       TEXT
        )
            ''')
    conn.commit()


@ensure_connection
def get_user_index(conn: sqlite3.Connection, user_id: int):
    c = conn.cursor()
    c.execute('SELECT * FROM indexes_base WHERE user_id=?', (user_id ,))
    return c.fetchone()

@ensure_connection
def write_indexes(conn: sqlite3.Connection, user_id: int, username: str,light : str, cold_water: str,hot_water: str, gas : str ):
    c = conn.cursor()
    c.execute('INSERT INTO indexes_base (user_id, username, light,  cold_water, hot_water , gas , indexes_date) VALUES(?, ?, ?, ? , ? , ? , ?)',
              (user_id, username, light, cold_water, hot_water, gas , ctime()))
    conn.commit()