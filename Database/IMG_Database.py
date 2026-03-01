import sqlite3 as sql
from datetime import datetime
import os


def init_db():
    conn = sql.connect('history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS image_history(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        prompt TEXT,
                                                        enhanced_prompt TEXT,
                                                        image_path TEXT,
                                                        style TEXT,
                                                        timestamp DATETIME)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                  username TEXT UNIQUE,
                                                  password TEXT,
                                                  email TEXT UNIQUE,
                                                  created_at DATETIME)''')
    conn.commit()
    conn.close()

def save_history(prompt, enhanced_prompt, image_path, style):
    conn = sql.connect('history.db')
    c = conn.cursor()
    c.execute("INSERT INTO image_history (prompt, enhanced_prompt, image_path, style, timestamp) VALUES(?, ?, ?, ?, ?)", 
              (prompt, enhanced_prompt, image_path, style, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def get_history():
    conn = sql.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM image_history ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return data

def delete_history_item(item_id):
    conn = sql.connect('history.db')
    c = conn.cursor()

    c.execute("SELECT image_path FROM image_history WHERE id = ?", (item_id,))
    path = c.fetchone()
    if path and os.path.exists(path[0]):
        os.remove(path[0])

    c.execute("DELETE FROM image_history WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def delete_all_history():
    conn = sql.connect('history.db')
    c = conn.cursor()

    c.execute("DELETE FROM image_history")
    conn.commit()
    conn.close()
    if os.path.exists('outputs'):
        for file in os.listdir('outputs'):
            file_path = os.path.join('outputs', file)
            try: 
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
