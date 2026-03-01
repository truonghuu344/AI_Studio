import streamlit as st
from Auth import register_user

def render_Register():

    st.set_page_config(page_title="Đăng ký", layout="centered")
    st.title("Đăng ký")

    with st.container():
        username = st.text_input("Tạo tài khoản", placeholder="Nhập tên tài khoản...", width = 515)
        email = st.text_input("Email", placeholder="Nhập email của bạn...", width = 515)
        password = st.text_input("Tạo mật khẩu", placeholder="Nhập mật khẩu của bạn...", type="password", width = 515)
        password_confirm = st.text_input("Xác nhận mật khẩu", placeholder="Nhập lại mật khẩu...", type="password", width = 515)
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Đăng ký", type="primary"):
                if not username or not email or not password:
                    st.error("Vui lòng điền đầy đủ thông tin!")
                elif password != password_confirm:
                    st.error("Mật khẩu xác nhận không khớp!")
                elif register_user(username, email, password):
                    st.success("Đăng ký thành công! Đang chuyển hướng sang đăng nhập...")
                    st.balloons()
                    # Cập nhật state để app.py chuyển sang trang Login
                    st.session_state["page"] = "Login"
                    st.rerun()
                else:
                    st.error("Đăng ký thất bại! Tài khoản hoặc email có thể đã tồn tại.")
        with col2:
            if st.button("Quay lại đăng nhập"):
                st.session_state["page"] = "Login"
                st.rerun()
    
render_Register()