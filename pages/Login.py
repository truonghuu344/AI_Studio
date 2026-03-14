
import streamlit as st
from Auth import login_user, get_user_info

def render_Login():
    st.set_page_config(page_title="Đăng nhập", layout="wide", initial_sidebar_state="collapsed")
    
   
    
    # Remove default margins
    st.markdown("""
        <style>
            .main { padding: 0 !important; }
            .stApp { background: #000814 !important; }
        </style>
    """, unsafe_allow_html=True)

    if "logged_in" not in st.session_state: 
        st.session_state["logged_in"] = False

    # Center container
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="auth-card">
                <h1 class="auth-title">✨ Chào mừng trở lại</h1>
                <p class="auth-subtitle">Đăng nhập để tiếp tục hành trình của bạn</p>
        """, unsafe_allow_html=True)
        
        # Login Form
        username = st.text_input(
            "👤 Tài khoản",
            placeholder="Nhập tài khoản của bạn...",
            key="username_input"
        )
        
        password = st.text_input(
            "🔐 Mật khẩu",
            placeholder="Nhập mật khẩu của bạn...",
            type="password",
            key="password_input"
        )
        
        # Remember me & Forgot password
        col_check, col_forgot = st.columns([1, 1])
        with col_check:
            remember_me = st.checkbox("Ghi nhớ tôi", key="remember")
        with col_forgot:
            st.markdown('<a href="#" style="color: #818cf8; text-decoration: none; font-size: 12px;">Quên mật khẩu?</a>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Login Button
        col_btn1, col_btn2 = st.columns([1, 1])
        
        login_clicked = False
        register_clicked = False
        
        with col_btn1:
            if st.button("🚀 Đăng nhập", type="primary", use_container_width=True, key="login_btn"):
                login_clicked = True
        
        with col_btn2:
            if st.button("📝 Đăng ký", use_container_width=True, key="register_btn"):
                register_clicked = True
        
        if login_clicked:
            if not username or not password:
                st.error("❌ Vui lòng điền đầy đủ thông tin!")
            elif login_user(username, password):
                user_info = get_user_info(username)
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["user_id"] = user_info[0]
                st.session_state["role"] = user_info[3]
                st.success("✅ Đăng nhập thành công! Đang chuyển hướng...")
                st.session_state["page"] = "Home"
                st.rerun()
            else:
                st.error("❌ Tài khoản hoặc mật khẩu không đúng!")
        
        if register_clicked:
            st.session_state["page"] = "Register"
            st.rerun()
        
        # Bottom Text
        st.markdown("""
            <div class="auth-link">
                Chưa có tài khoản? 
                <a href="#" onclick="location.href='#register'">Đăng ký ngay</a>
            </div>
            </div>
            </div>
        """, unsafe_allow_html=True)

render_Login()
