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