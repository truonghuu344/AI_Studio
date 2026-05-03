import streamlit as st
from Auth import register_user


def render_Register():
    st.set_page_config(page_title="Đăng ký", layout="wide", initial_sidebar_state="collapsed")
    

    
    # Remove default margins
    st.markdown("""
        <style>
            .main { 
                padding: 0 !important; 
            }
            .stApp { 
                background: #dea050;
                background: linear-gradient(90deg,rgba(222, 160, 80, 1) 0%, rgba(119, 192, 207, 1) 32%, rgba(171, 87, 199, 1) 64%, rgba(201, 46, 80, 1) 92%);
            }
            .stForm {
                width: 600px;
                border: 4px solid white;
                height: 600px;
                margin: 10px auto;
            
            }
            .auth-card  {
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # Center container
    with st.form("register_form"):
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="auth-card">
                <h1 class="auth-title"> 📝 Đăng ký </h1>
                <p class="auth-subtitle">Tạo tài khoản để khám phá những tính năng tuyệt vời</p>
        """, unsafe_allow_html=True)
        
        # Registration Form
        username = st.text_input(
            "👤 Tên tài khoản",
            placeholder="Chọn tên tài khoản của bạn...",
            key="reg_username_input"
        )
        
        email = st.text_input(
            "Email",
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
            "🔐 Xác nhận mật khẩu",
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
            if st.form_submit_button("✨ Tạo tài khoản", type="primary", use_container_width=True, key="register_btn_submit"):
                register_clicked = True
        
        with col_btn2:
            if st.form_submit_button("Đăng nhập", use_container_width=True, key="back_to_login_btn"):
                back_clicked = True
        
        if register_clicked:
            username = (username or "").strip()
            email = (email or "").strip()

            if not username or not email or not password:
                st.toast("Vui lòng điền đầy đủ thông tin!")
            elif "@" not in email or "." not in email:
                st.toast("Email không hợp lệ!")
            elif password != password_confirm:
                st.toast("Mật khẩu xác nhận không khớp!")
            elif len(password) < 6:
                st.toast("Mật khẩu phải có ít nhất 6 ký tự!")
            elif register_user(username, email, password):
                st.success("✅ Đăng ký thành công! Đang chuyển hướng sang đăng nhập...")
                st.balloons()
                st.session_state["page"] = "Login"
                st.rerun()
            else:
                st.toast("Đăng ký thất bại! Tài khoản hoặc email có thể đã tồn tại.")
        
        if back_clicked:
            st.session_state["page"] = "Login"
            st.rerun()
        

render_Register()
