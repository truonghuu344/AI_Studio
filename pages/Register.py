import streamlit as st
from Auth import register_user


def render_Register():
    st.set_page_config(page_title="Đăng ký", layout="wide", initial_sidebar_state="collapsed")
    

    
    # Remove default margins
    st.markdown("""
        <style>
            .main { padding: 0 !important; }
            .stApp { background: #000814 !important; }
        </style>
    """, unsafe_allow_html=True)

    # Center container
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="auth-card">
                <h1 class="auth-title">🌟 Bắt đầu hành trình</h1>
                <p class="auth-subtitle">Tạo tài khoản để khám phá những tính năng tuyệt vời</p>
        """, unsafe_allow_html=True)
        
        # Registration Form
        username = st.text_input(
            "👤 Tên tài khoản",
            placeholder="Chọn tên tài khoản của bạn...",
            key="reg_username_input"
        )
        
        email = st.text_input(
            "📧 Email",
            placeholder="Nhập email của bạn...",
            key="reg_email_input"
        )
        
        password = st.text_input(
            "🔐 Mật khẩu",
            placeholder="Tạo mật khẩu mạnh...",
            type="password",
            key="reg_password_input"
        )
        
        password_confirm = st.text_input(
            "✓ Xác nhận mật khẩu",
            placeholder="Nhập lại mật khẩu...",
            type="password",
            key="reg_password_confirm_input"
        )

        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Register Button
        col_btn1, col_btn2 = st.columns([1, 1])
        
        register_clicked = False
        back_clicked = False
        
        with col_btn1:
            if st.button("✨ Tạo tài khoản", type="primary", use_container_width=True, key="register_btn_submit"):
                register_clicked = True
        
        with col_btn2:
            if st.button("← Quay lại", use_container_width=True, key="back_to_login_btn"):
                back_clicked = True
        
        if register_clicked:
            if not username or not email or not password:
                st.error("❌ Vui lòng điền đầy đủ thông tin!")
            elif password != password_confirm:
                st.error("❌ Mật khẩu xác nhận không khớp!")
            elif register_user(username, email, password):
                st.success("✅ Đăng ký thành công! Đang chuyển hướng sang đăng nhập...")
                st.balloons()
                st.session_state["page"] = "Login"
                st.rerun()
            else:
                st.error("❌ Đăng ký thất bại! Tài khoản hoặc email có thể đã tồn tại.")
        
        if back_clicked:
            st.session_state["page"] = "Login"
            st.rerun()
        
        # Bottom Text
        st.markdown("""
            <div class="auth-link">
                Đã có tài khoản? 
                <a href="#" onclick="location.href='#login'">Đăng nhập ngay</a>
            </div>
            </div>
            </div>
        """, unsafe_allow_html=True)

render_Register()
