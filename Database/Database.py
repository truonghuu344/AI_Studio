import sqlite3 as sql
from datetime import datatime
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
    conn.commit()
    conn.close()

def save_history():
    conn = sql.connect('history.db')
    c = conn.cursor()
    c.execute("INSERT INTO image_history (prompt, enhanced_prompt, image_path, styyle, timestamp) VALUES(?, ?, ?, ?, ?)", 
              (prompt, ehanced_prompt, image_path, style, datetime.now()))
    conn.commit()
    conn.close()

def get_history():
    conn = sql.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM image_history ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return data