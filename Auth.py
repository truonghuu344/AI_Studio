import bcrypt
from Database.LAR_Database import get_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?,?,?,?)", (username, email, hashed, 'user'))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()    

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, id, role, is_active FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[3] == 0:  # Check if user is inactive
        return False
    
    if user and verify_password(password, user[0]):
        return True
    return False

def get_user_info(username):
    """Lấy thông tin user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role, is_active FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user
