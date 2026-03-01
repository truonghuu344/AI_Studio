import sqlite3 as sql


def get_connection():
    return sql.connect('User.db', check_same_thread=False)

def create_user_table():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE,
              email TEXT UNIQUE,
              password TEXT,
              role TEXT DEFAULT 'user')
              ''')
    conn.commit()
    conn.close()
    