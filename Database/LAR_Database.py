from hmac import new
import sqlite3 as sql
from datetime import datetime
import shutil
import os
from Database.IMG_Database import delete_all_history
DB_PATH = os.path.join("Database", "User.db")



def get_connection():
    return sql.connect(DB_PATH, check_same_thread=False)

def create_user_table():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE,
              email TEXT UNIQUE,
              password TEXT,
              role TEXT DEFAULT 'user',
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
              is_active INTEGER DEFAULT 1,
              credits INTEGER DEFAULT 50
              )''')
    conn.commit()
    
    try:
        c.execute("ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1")
        conn.commit()
    except:
        pass 
    try:
        c.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        conn.commit()
    except:
        pass  
    try:
        c.execute("ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        conn.commit()
    except:
        pass
    try:
        c.execute("ALTER TABLE users add COLUMN credits INTEGER DEFAULT 50")
    except:
        pass 
    conn.close()



def get_user_role(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT role, id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result

def get_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, role, created_at, is_active FROM users ORDER BY id ASC")
    data = c.fetchall()
    conn.close()
    return data
# Cập nhật vai trò
def update_user_role(user_id, role):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()
# Cập nhật trạng thái
def update_user_status(user_id, is_active):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET is_active = ? WHERE id = ?", (is_active, user_id))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()
# Xóa tài khoản
def delete_user(user_id):
    try:
        delete_all_history(user_id)
        user_folder = f"outputs/user_{user_id}"
        if os.path.exists(user_folder):
            shutil.rmtree(user_folder)
    except Exception as e:
        print(f"Lỗi xóa dữ liệu liên quan: {e}")

    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        c.execute("SELECT MAX(id) FROM users")
        max_id = c.fetchone()[0]
        if max_id is None: max_id = 0

        c.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'users'", (max_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi khi xóa user và reset ID: {e}")
        return False
    finally:
        conn.close()

def get_user_credits(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def update_user_credits(user_id, amount):
    conn = get_connection()
    c = conn.cursor()
    try:
        current_credits = get_user_credits(user_id)
        new_credits = current_credits + amount
        
        if new_credits < 0:
            return False
        c.execute("UPDATE users SET credits = ? WHERE id = ?", (new_credits, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi cập nhật credits: {e}")
        return False
    finally:
        conn.close()

def check_credit_rq(user_id, cost):
    current_credits = get_user_credits(user_id)
    return current_credits >= cost




def create_admin_account(username, email, password):
    from Auth import hash_password
    conn = get_connection()
    c = conn.cursor()
    hashed = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, email, password, role, created_at) VALUES (?,?,?,?,?)", 
                 (username, email, hashed, 'admin', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def init_default_admin():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, role FROM users WHERE username = 'admin'")
    user = c.fetchone()

    if user:
        user_id, role = user
    
        if role != "admin":
            c.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
            conn.commit()
    else:
        create_admin_account("admin", "admin@example.com", "admin123")
    conn.close()

