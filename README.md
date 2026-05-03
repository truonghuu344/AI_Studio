# 🎨 TextToImage - AI Image Generator Platform

Một ứng dụng web được xây dựng với **Streamlit** cho phép người dùng tạo hình ảnh từ mô tả văn bản bằng AI, cùng với các tính năng quản lý người dùng, lịch sử ảnh và hệ thống quản trị.

## 📋 Mục lục

- [Tổng quan](#tổng-quan)
- [Tính năng chính](#tính-năng-chính)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Cấu hình](#cấu-hình)
- [Sử dụng](#sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Các tính năng chi tiết](#các-tính-năng-chi-tiết)
- [Hệ thống phân quyền](#hệ-thống-phân-quyền)
- [Troubleshooting](#troubleshooting)

## 🎯 Tổng quan

**TextToImage** là một nền tảng AI tích hợp cho phép người dùng:

- 🖼️ **Tạo ảnh từ mô tả**: Sử dụng mô hình FLUX.1-schnell từ Hugging Face để tạo hình ảnh chất lượng cao từ prompt văn bản
- 💬 **Trò chuyện với AI**: Chatbot tích hợp OpenAI để tương tác và nhận trợ giúp
- 📚 **Lưu lịch sử**: Theo dõi tất cả hình ảnh đã tạo, prompt và thông số
- 👥 **Quản lý người dùng**: Hệ thống xác thực an toàn với role-based access control
- ⚙️ **Admin Dashboard**: Quản lý toàn bộ người dùng, role, quyền truy cập và thống kê hệ thống
- 💳 **Hệ thống Credit**: Kiểm soát sử dụng thông qua hệ thống credit/token
- 🎨 **Tùy chọn phong cách**: Chọn từ các phong cách ảnh khác nhau (Realistic, Cinematic, Anime, Digital Art, Oil Painting)

## ✨ Tính năng chính

### Người dùng thông thường

| Tính năng | Mô tả |
|----------|-------|
| **Đăng ký / Đăng nhập** | Tạo tài khoản và xác thực an toàn |
| **Tạo ảnh AI** | Nhập prompt, chọn tùy chọn (aspect ratio, số lượng, style) |
| **Tăng cường prompt** | Tự động cải thiện mô tả để tạo ảnh tốt hơn |
| **Upscale ảnh** | Nâng cao chất lượng hình ảnh được tạo |
| **Xem lịch sử** | Xem tất cả hình ảnh đã tạo trước đó |
| **Ai Chatbot** | Trò chuyện với AI để nhận gợi ý, hỗ trợ |
| **Quản lý Credit** | Theo dõi số credit còn lại |

### Admin

| Tính năng | Mô tả |
|----------|-------|
| **Quản lý tài khoản** | Xem danh sách, thay đổi role, kích hoạt/vô hiệu hoá |
| **Chi tiết người dùng** | Xem thông tin chi tiết từng tài khoản |
| **Cài đặt hệ thống** | Xem thống kê tổng quan (tổng user, active user, admin) |
| **Xóa tài khoản** | Xóa các tài khoản người dùng nếu cần |

## 🔧 Yêu cầu hệ thống

- **Python**: 3.8 hoặc cao hơn
- **Streamlit**: Framework web interactive
- **SQLite**: Cơ sở dữ liệu tích hợp
- **API Keys**: 
  - Hugging Face API Token (để tạo ảnh)
  - OpenAI API Token (để chatbot)
  - Remove.bg Token (tùy chọn, để xóa nền ảnh)

## 📦 Cài đặt

### 1. Clone hoặc tải dự án

```bash
cd TextToImage
```

### 2. Tạo virtual environment (tùy chọn nhưng khuyến khích)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Cài đặt các dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình biến môi trường

Tạo file `.env` ở thư mục gốc với nội dung:

```env
HF_TOKEN=your_huggingface_api_token_here
REMOVE_BG_TOKEN=your_removebg_api_token_here (optional)
OPENAI_API_KEY=your_openai_api_key_here
```

Để lấy các token:
- **Hugging Face**: https://huggingface.co/settings/tokens
- **OpenAI**: https://platform.openai.com/api-keys
- **Remove.bg**: https://www.remove.bg/api (tùy chọn)

### 5. Khởi tạo tài khoản Admin

Chạy script để tạo tài khoản admin mặc định:

```bash
python init_admin.py
```

**Tài khoản admin mặc định:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`

⚠️ **Lưu ý quan trọng:** Hãy đổi mật khẩu admin sau khi đăng nhập lần đầu!

## 🚀 Sử dụng

### Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở trên `http://localhost:8501`

### Quy trình sử dụng cơ bản

1. **Đăng ký tài khoản** (nếu chưa có)
   - Nhập username, email, password
   - Xác nhận password

2. **Đăng nhập**
   - Sử dụng username và password

3. **Tạo ảnh**
   - Vào tab "🎨 Generate Image"
   - Nhập prompt mô tả hình ảnh bạn muốn
   - Chọn tùy chọn (số lượng, tỷ lệ khung hình, phong cách)
   - Nhấn nút "Generate"
   - Chờ AI tạo hình ảnh (mất vài giây)

4. **Xem lịch sử**
   - Vào tab "📚 History"
   - Xem tất cả hình ảnh đã tạo trước đó

5. **Chat với AI**
   - Vào tab "💬 AI Chatbot"
   - Đặt câu hỏi hoặc nhận gợi ý về prompt

## 📁 Cấu trúc dự án

```
TextToImage/
│
├── app.py                    # File chính, router ứng dụng
├── API.py                    # Các hàm gọi API (Hugging Face, OpenAI)
├── Auth.py                   # Xác thực người dùng (bcrypt)
├── init_admin.py             # Script khởi tạo tài khoản admin
├── requirements.txt          # Các dependency
├── README.md                 # File này
├── ADMIN_GUIDE.md            # Hướng dẫn quản trị viên
│
├── CSS/                      # Styling
│   ├── __init__.py
│   └── CSS.py                # Custom CSS cho Streamlit
│
├── Database/                 # Cơ sở dữ liệu
│   ├── __init__.py
│   ├── IMG_Database.py       # Lưu/lấy lịch sử ảnh
│   ├── LAR_Database.py       # Quản lý users, credits, roles
│   └── history.db            # File SQLite database
│
├── models/                   # AI models
│   └── AI_Analyzer.py        # Xử lý/phân tích AI
│
├── pages/                    # Các trang chính
│   ├── __init__.py
│   ├── Home.py               # Trang chủ
│   ├── Login.py              # Trang đăng nhập
│   └── Register.py           # Trang đăng ký
│
├── Tabs/                     # Các tab/chức năng
│   ├── __init__.py
│   ├── Sidebar.py            # Sidebar điều hướng
│   ├── Generate_Image.py     # Tạo ảnh từ mô tả
│   ├── AI_Chatbot.py         # Chatbot AI
│   ├── History_Tab.py        # Xem lịch sử
│   ├── Admin_Dashboard.py    # Quản lý admin
│   └── Lifestyle_Shot.py     # Tính năng phụ
│
└── outputs/                  # Thư mục lưu ảnh theo user
    ├── user_2/
    ├── user_3/
    ├── user_4/
    └── user_5/
```

## 🔑 Các tính năng chi tiết

### 1. Hệ thống xác thực (Auth.py)

- Mã hóa mật khẩu với **bcrypt** (không lưu mật khẩu rõ)
- Session management với Streamlit
- Xác thực đăng nhập/đăng ký

### 2. Tạo ảnh (Generate_Image.py & API.py)

**Mô hình AI:** FLUX.1-schnell từ Hugging Face

**Tùy chọn:**
- **Số lượng ảnh**: 1-5 ảnh
- **Tỷ lệ khung hình**: 1:1, 16:9, 4:3, 9:16, 3:2, 21:9
- **Upscale chất lượng**: Nâng cao độ phân giải
- **Phong cách**: Realistic, Cinematic, Anime, Digital Art, Oil Painting

### 3. Cơ sở dữ liệu (Database/)

**IMG_Database.py:**
- Lưu lịch sử ảnh (prompt, đường dẫn, style, timestamp)
- Truy xuất lịch sử theo user_id
- Quản lý thư mục ảnh theo user

**LAR_Database.py:**
- Quản lý tài khoản người dùng
- Hệ thống credit/token
- Role management (user, moderator, admin)
- Kích hoạt/vô hiệu hoá tài khoản

### 4. Admin Dashboard (Admin_Dashboard.py)

Các chức năng:
- 📋 **Quản lý tài khoản**: Xem danh sách, thay đổi role, xóa
- 👤 **Chi tiết tài khoản**: Thông tin chi tiết từng user
- ⚙️ **Cài đặt hệ thống**: Thống kê toàn hệ

## 👥 Hệ thống phân quyền

### Các Role

| Role | Quyền |
|------|-------|
| **user** | Sử dụng tính năng tạo ảnh, chat, xem lịch sử |
| **moderator** | Quản lý (đang phát triển) |
| **admin** | Toàn bộ quyền quản lý hệ thống |

### Dữ liệu riêng biệt

Mỗi người dùng có:
- **Tài khoản riêng**: Lưu username, email, password mã hóa
- **Thư mục ảnh riêng**: `/outputs/user_{user_id}/`
- **Lịch sử riêng**: Chỉ xem được lịch sử ảnh của mình
- **Credit riêng**: Theo dõi sử dụng riêng

## 📊 Hệ thống Credit

- Mỗi người dùng có credit/token để giới hạn sử dụng
- Mỗi lần tạo ảnh sẽ tiêu tốn credit
- Admin có thể quản lý credit của người dùng

## 🐛 Troubleshooting

### Lỗi: "HF_TOKEN not found"
**Giải pháp:** 
- Kiểm tra file `.env` có chứa `HF_TOKEN=...`
- Chắc chắn file `.env` ở thư mục gốc
- Khởi động lại ứng dụng

### Lỗi: "Database file not found"
**Giải pháp:**
- Chạy `python init_admin.py` để khởi tạo database
- Hoặc xóa file `Database/history.db` và tạo lại

### Ứng dụng không mở được
**Giải pháp:**
- Kiểm tra port 8501 không được sử dụng
- Cố gắng chạy trên port khác: `streamlit run app.py --server.port 8502`

### Lỗi: "OAuthException" hoặc "Invalid token"
**Giải pháp:**
- Kiểm tra lại API tokens
- Đảm bảo tokens có quyền truy cập đúng
- Token có thể hết hạn, lấy token mới

### Ảnh không được tạo ra
**Giải pháp:**
- Kiểm tra HF_TOKEN có hiệu lực
- Kiểm tra internet connection
- Xem log/message lỗi trong Streamlit
- Thử với prompt đơn giản hơn

## 📝 File cấu hình

### requirements.txt

```
streamlit              # Web framework
huggingface_hub        # Hugging Face API
pillow                 # Image processing
requests               # HTTP requests
python-dotenv          # Environment variables
openai                 # OpenAI API
bcrypt                 # Password hashing
streamlit-authenticator # Authentication components
```

### .env (tạo riêng)

```env
HF_TOKEN=your_token_here
OPENAI_API_KEY=your_key_here
REMOVE_BG_TOKEN=your_token_here (optional)
```

## 🎓 Hướng dẫn cho Admin

Chi tiết về hệ thống admin, xem file [ADMIN_GUIDE.md](ADMIN_GUIDE.md)

### Bắt đầu nhanh

```bash
# 1. Khởi tạo admin
python init_admin.py

# 2. Chạy ứng dụng
streamlit run app.py

# 3. Đăng nhập với admin@example.com / admin123
# 4. Đổi mật khẩu trong settings
# 5. Quản lý người dùng trong tab Admin
```

## 🔐 Bảo mật

- ✅ Mật khẩu được mã hóa bằng **bcrypt**
- ✅ API tokens được lưu trong `.env` (không commit)
- ✅ Session management an toàn qua Streamlit
- ✅ Role-based access control
- ✅ User data isolation (mỗi user chỉ xem data của mình)

**Khuyến cáo:**
- Thay đổi mật khẩu admin mặc định
- Không commit file `.env` lên Git
- Thường xuyên kiểm tra quyền truy cập
- Sử dụng strong password cho tài khoản admin

---
Project này được phát triển cho mục đích giáo dục và sử dụng nội bộ.
---

**Phiên bản**: 1.0.0  
**Cập nhật lần cuối**: Tháng 4, 2026  
**Trạng thái**: Active Development

---

## 🌐 Mô tả thêm (English)

**TextToImage** is a comprehensive AI-powered web application built with Streamlit that enables users to generate images from text descriptions using advanced AI models. The platform includes:

### Core Features:
- **AI Image Generation**: Creates high-quality images from text prompts using FLUX.1-schnell model
- **Multi-format Support**: Various aspect ratios and image styles
- **User Management**: Secure authentication with password encryption
- **Admin Panel**: Complete system administration and user management
- **History Tracking**: Personal image generation history per user
- **AI Chatbot**: Integrated AI assistant for guidance and support
- **Credit System**: Usage control through token/credit management

### Technology Stack:
- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **AI Models**: Hugging Face (Image Generation), OpenAI (Chatbot)
- **Security**: bcrypt for password hashing
- **API Integration**: Multiple AI services

### Architecture:
The application follows a modular structure with separate components for authentication, image generation, database management, and admin functions, ensuring scalability and maintainability.

For complete setup and usage instructions, see the Vietnamese sections above.
