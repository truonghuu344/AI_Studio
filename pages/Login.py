
import streamlit as st
from Auth import login_user


def render_Login():
    st.set_page_config(page_title="Đăng nhập", layout="centered")

    if "logged_in" not in st.session_state: 
        st.session_state["logged_in"] = False

    st.title("Đăng nhập")

    with st.container():
        username = st.text_input("Tài khoản", placeholder="Nhập tài khoản của bạn...", width = 592)
        password = st.text_input("Mật khẩu", placeholder="Nhập mật khẩu của bạn...", type="password", width = 592) 
        col1, col2, col3 = st.columns([1, 1, 1], gap="large")
        with col1:
            if st.button("Đăng nhập", type="primary"):
                if login_user(username, password):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.success("Đăng nhập thành công!")
                    st.session_state["page"] = "Home"
                    st.rerun()
                else:
                    st.error("Tài khoản hoặc mật khẩu không đúng!")
        with col3:
            if st.button("Đăng ký"):    
                st.session_state["page"] = "Register"
                st.rerun()
                  
render_Login()