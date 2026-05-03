import sqlite3 as sql
from datetime import datetime
import os
from unicodedata import category
DB_PATH = os.path.join("Database", "history.db")

def connect_db():
    return sql.connect(DB_PATH, check_same_thread=False)
def init_db():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS image_history(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        user_id INTEGER,
                                                        prompt TEXT,
                                                        enhanced_prompt TEXT,
                                                        image_path TEXT,
                                                        style TEXT,
                                                        category TEXT,
                                                        timestamp DATETIME)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                  username TEXT UNIQUE,
                                                  password TEXT,
                                                  email TEXT UNIQUE,
                                                  created_at DATETIME)''')
    c.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON image_history(user_id)")
    conn.commit()
    conn.close()

def save_history(user_id, prompt, enhanced_prompt, image_path, style, category="Others"):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO image_history (user_id, prompt, enhanced_prompt, image_path, style, category, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?)", 
              (user_id, prompt, enhanced_prompt, image_path, style, category, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = connect_db()
    c = conn.cursor()
    if user_id is not None:
        c.execute(
            "SELECT id, prompt, enhanced_prompt, image_path, style, timestamp "
            "FROM image_history WHERE user_id = ? ORDER BY timestamp DESC",
            (user_id,),
        )
    else:
        c.execute(
            "SELECT id, prompt, enhanced_prompt, image_path, style, timestamp "
            "FROM image_history ORDER BY timestamp DESC"
        )
    data = c.fetchall()
    conn.close()
    return data


def delete_history_item(item_id, user_id):
    conn = connect_db()
    c = conn.cursor()

    c.execute("SELECT image_path FROM image_history WHERE id = ? AND user_id = ?", (item_id, user_id, ))
    path = c.fetchone()
    try:
        if path and os.path.exists(path[0]):
            os.remove(path[0])
    except Exception as e:
        print(f"Lỗi xóa file: {e}")
    c.execute("DELETE FROM image_history WHERE id = ? AND user_id = ?", (item_id, user_id))
    conn.commit()
    conn.close()
    

def delete_all_history(user_id):
    conn = connect_db()
    c = conn.cursor()

    c.execute("SELECT image_path FROM image_history WHERE user_id = ?", (user_id,))
    paths = c.fetchall()

    for path in paths:
        try:
            if path and os.path.exists(path[0]):
                os.remove(path[0])
        except Exception as e:
            print(f"Lỗi xóa file: {e}")
    
    c.execute("DELETE FROM image_history WHERE user_id = ?", (user_id, ))
    conn.commit()
    conn.close()
    cleanup_user_folder(user_id)

def get_user_folder(user_id):
    folder = f"outputs/user_{user_id}"
    os.makedirs(folder, exist_ok = True)
    return folder
def cleanup_user_folder(user_id):
    folder = f"outputs/user_{user_id}"
    if os.path.exists(folder) and not os.listdir(folder):
        os.rmdir(folder)
        
def update_image_category(image_id: int, category: str):
    """Cập nhật category cho 1 ảnh sau khi AI phân tích."""
    conn = connect_db()
    c = conn.cursor()
    c.execute("UPDATE image_history SET category = ? WHERE id = ?", (category, image_id))
    conn.commit()
    conn.close()
    
def get_all_history_by_user(user_id: int):
    """Lấy toàn bộ history kèm category của 1 user."""
    conn = connect_db()
    c = conn.cursor()
    c.execute(
        "SELECT id, prompt, enhanced_prompt, image_path, style, category, timestamp "
        "FROM image_history WHERE user_id = ? ORDER BY timestamp DESC",
        (user_id,)
    )
    data = c.fetchall()
    conn.close()
    return data

def get_uncategorized_images(user_id: int):
    """Lấy ảnh chưa được phân loại (category = 'Others' hoặc NULL)."""
    conn = connect_db()
    c = conn.cursor()
    c.execute(
        "SELECT id, prompt, enhanced_prompt, image_path, style FROM image_history "
        "WHERE user_id = ? AND (category IS NULL OR category = 'Others')",
        (user_id,)
    )
    data = c.fetchall()
    conn.close()
    return data

        
        

