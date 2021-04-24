import sqlite3
from time import ctime


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            res = func(conn, *args, **kwargs)
        return res

    return inner


@ensure_connection
def init_workers_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS workers')
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS workers ( 
            id            INTEGER PRIMARY KEY,
            user_id       INTEGER, 
            first_name    TEXT,
            work          TEXT 
               
            )
            ''')
    conn.commit()


@ensure_connection
def сhoose_workers(conn: sqlite3.Connection, work: str):
    c = conn.cursor()
    c.execute('SELECT * FROM user_base WHERE work=?', (work ,))
    row = []
    for user_id in c.fetchall():
        i = user_id
        row.append(i)

    return row


@ensure_connection
def add_workers(conn: sqlite3.Connection, user_id: int, position_id: int):
    c = conn.cursor()
    c.execute('INSERT INTO workers (user_id, position_id) VALUES(?,?)',
              (user_id, position_id))
    conn.commit()


@ensure_connection
def get_positions(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute('SELECT id, name FROM position')
    return c.fetchall()

@ensure_connection
def get_user_positions(conn: sqlite3.Connection, user_id: int):
    c = conn.cursor()
    c.execute('SELECT position_id, position.name FROM workers '
              'JOIN position ON position.id=position_id WHERE user_id=?', (user_id, ))
    return c.fetchall()


@ensure_connection
def get_workers(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute('SELECT workers.user_id, user_base.first_name, user_base.last_name, position.name '
              'FROM workers '
              'JOIN user_base ON user_base.user_id=workers.user_id '
              'JOIN position ON position.id=workers.position_id '
              'ORDER BY user_base.last_name, user_base.first_name')
    return c.fetchall()