"""
Script để khởi tạo tài khoản admin mặc định
Chạy lệnh: python init_admin.py
"""
import sys
from Database.LAR_Database import create_user_table, create_admin_account

def init_admin():
    print("=" * 50)
    print("Khởi tạo tài khoản Admin")
    print("=" * 50)
    
    # Tạo bảng users
    create_user_table()
    print("✓ Bảng users đã được tạo hoặc đã tồn tại")
    
    # Tạo tài khoản admin
    admin_username = "admin"
    admin_email = "admin@example.com"
    admin_password = "admin123"
    
    # Kiểm tra xem admin đã tồn tại chưa
    from Database.LAR_Database import get_connection
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (admin_username,))
    existing_admin = c.fetchone()
    conn.close()
    
    if existing_admin:
        print(f"⚠️  Tài khoản admin '{admin_username}' đã tồn tại")
        print(f"   Email: {existing_admin[2]}")
    else:
        if create_admin_account(admin_username, admin_email, admin_password):
            print(f"✓ Tài khoản admin đã được tạo thành công!")
            print(f"  - Tài khoản: {admin_username}")
            print(f"  - Email: {admin_email}")
            print(f"  - Mật khẩu: {admin_password}")
            print("\n⚠️  LƯU Ý: Hãy thay đổi mật khẩu admin sau khi đăng nhập lần đầu!")
        else:
            print(f"✗ Không thể tạo tài khoản admin")
    
    print("=" * 50)

if __name__ == "__main__":
    init_admin()
