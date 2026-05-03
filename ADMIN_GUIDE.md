## Hệ thống Admin & Phân quyền - Hướng dẫn

### 1. Khởi tạo Tài khoản Admin

Trước khi chạy ứng dụng, bạn cần tạo tài khoản admin:

```bash
python init_admin.py
```

**Tài khoản Admin mặc định:**
- Tài khoản: `admin`
- Mật khẩu: `admin123`
- Email: `admin@example.com`

⚠️ **Lưu ý:** Hãy thay đổi mật khẩu admin sau khi đăng nhập lần đầu!

### 2. Các Chức năng Admin

Sau khi đăng nhập với tài khoản admin, sẽ xuất hiện tab **🔐 Admin** với các chức năng:

#### A. **📋 Quản lý Tài khoản**
- Xem danh sách tất cả tài khoản đã đăng ký
- Thay đổi role của user (user → moderator → admin)
- Kích hoạt/Vô hiệu hoá tài khoản
- Xóa tài khoản

#### B. **👤 Chi tiết Tài khoản**
- Xem chi tiết một tài khoản cụ thể
- Thông tin: ID, tài khoản, email, role, trạng thái, ngày tạo
- Xóa tài khoản nếu cần thiết

#### C. **⚙️ Cài đặt**
- Xem thống kê hệ thống
- Tổng số tài khoản
- Số tài khoản đang hoạt động
- Số tài khoản admin

### 3. Hệ thống Phân quyền

**Các Role có sẵn:**
- `user` - Tài khoản người dùng bình thường (quyền mặc định)
- `moderator` - Tài khoản quản lý (có thể được thêm trong tương lai)
- `admin` - Tài khoản quản trị viên

### 4. Lưu trữ Dữ liệu Riêng cho Mỗi User

**Mỗi tài khoản có:**
- Dữ liệu người dùng riêng lưu trong bảng `users`
- Lịch sử ảnh riêng - mỗi ảnh được gắn với `user_id`
- Không xảy ra trùng lặp dữ liệu giữa các user

**Database Structure:**

*User.db:*
```
users table:
- id (INTEGER PRIMARY KEY)
- username (TEXT UNIQUE)
- email (TEXT UNIQUE)
- password (TEXT - hashed)
- role (TEXT - user/moderator/admin)
- created_at (DATETIME)
- is_active (INTEGER - 0/1)
```

*history.db:*
```
image_history table:
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER - FK to users.id)
- prompt (TEXT)
- enhanced_prompt (TEXT)
- image_path (TEXT)
- style (TEXT)
- timestamp (DATETIME)
```

### 5. Validation Khi Đăng Ký Và Đăng Nhập

**Đăng ký:**
- Tài khoản không được để trống
- Email không được để trống
- Mật khẩu không được để trống
- Mật khẩu xác nhận phải khớp

**Đăng nhập:**
- Tài khoản không được để trống
- Mật khẩu không được để trống
- Tài khoản phải tồn tại và đang hoạt động

### 6. Bảo Mật

- Mật khẩu được mã hoá bằng bcrypt
- Tài khoản vô hiệu hoá không thể đăng nhập
- Admin có thể quản lý tất cả tài khoản

### 7. Các File Liên Quan

- `init_admin.py` - Script khởi tạo tài khoản admin
- `Database/LAR_Database.py` - Quản lý bảng users và các hàm admin
- `Auth.py` - Xác thực và hashing mật khẩu
- `Tabs/Admin_Dashboard.py` - Giao diện admin
- `pages/Home.py` - Hiển thị tab admin nếu user là admin
- `pages/Login.py` - Lưu user_id và role vào session
- `Database/IMG_Database.py` - Lưu history với user_id

---

**Phiên bản 1.0** - Ngày: 2026-03-01
