import sqlite3


path = 'data/main.db'

def create_table():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            fullname VARCHAR(100),
            username VARCHAR(100),
            login VARCHAR(100),
            password VARCHAR(100),
            client_id INTEGER, 
            balance INTEGER, 
            container INTEGER, 
            phone TEXT, 
            org_name TEXT
    )""")
    conn.commit()
    conn.close()


def add_user(user_id, fullname, username, login, password, client_id, balance, container, phone, organization_name):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    if not c.fetchone():
        sql_query = f"INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?)"
        new_data = (user_id, fullname, username, login, password, client_id, balance, container, phone, organization_name)
        c.execute(sql_query, new_data)
        conn.commit()
    conn.close()


def get_client_id(user_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT client_id FROM users WHERE user_id = '{user_id}'")
    client_id = c.fetchone()[0]
    return client_id


def is_available(user_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    client_id = c.fetchone()
    return client_id

def logout_user(user_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")
    conn.commit()
    conn.close()