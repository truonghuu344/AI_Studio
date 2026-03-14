import sqlite3 as sql
from datetime import datetime


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
              role TEXT DEFAULT 'user',
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
              is_active INTEGER DEFAULT 1)
              ''')
    conn.commit()
    
    # Migration: Thêm cột is_active nếu chưa tồn tại
    try:
        c.execute("ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1")
        conn.commit()
    except:
        pass  # Cột đã tồn tại
    
    # Migration: Thêm cột role nếu chưa tồn tại
    try:
        c.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        conn.commit()
    except:
        pass  # Cột đã tồn tại
    
    # Migration: Thêm cột created_at nếu chưa tồn tại
    try:
        c.execute("ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        conn.commit()
    except:
        pass  # Cột đã tồn tại
    
    conn.close()

def create_admin_account(username, email, password):
    """Tạo tài khoản admin"""
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

def get_user_role(username):
    """Lấy role của user"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT role, id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result

def get_all_users():
    """Lấy tất cả users"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, role, created_at, is_active FROM users ORDER BY created_at DESC")
    data = c.fetchall()
    conn.close()
    return data

def update_user_role(user_id, role):
    """Cập nhật role của user"""
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

def update_user_status(user_id, is_active):
    """Cập nhật trạng thái active/inactive"""
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

def delete_user(user_id):
    """Xóa user"""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def init_default_admin():
    """Tự động tạo tài khoản admin mặc định nếu chưa tồn tại"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    admin_count = c.fetchone()[0]
    conn.close()
    
    if admin_count == 0:
        create_admin_account("admin", "admin@example.com", "admin123")
    