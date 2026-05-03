
import streamlit as st
from Auth import login_user, get_user_info


def render_Login():
   
    st.set_page_config(
        page_title="Đăng nhập", 
        layout="wide", 
        initial_sidebar_state="collapsed")
    st.markdown("""
    <style>
        .stApp {
            background: #466799;
            background: linear-gradient(90deg,rgba(42, 123, 155, 1) 0%, rgba(171, 87, 199, 1) 29%, rgba(105, 202, 127, 1) 55%, rgba(105, 211, 207, 1) 81%, rgba(237, 221, 83, 1) 100%);
        }
        .stForm {
            width: 600px;
            border: 4px solid white;
            height: 550px;
            margin: 10px auto;
            padding-left: 50px;
            padding-right: 50px;
        }
        h1 {
            text-align: center;
        }
    </style>""", unsafe_allow_html = True)
    

    with st.form("login_form"):
        st.markdown("""<h1> 🔐Đăng nhập </h1> """, unsafe_allow_html = True)
        tk = st.text_input("Tài khoản", placeholder = "Nhập tài khoản của bạn", )
        mk = st.text_input("Mật khẩu", placeholder = "Nhập mật khẩu của bạn", type = "password" )
        st.markdown("""</br>""", unsafe_allow_html=True)

        # Nút remember me và quên mật khẩu
        # col1, col2 = st.columns([0.75,1])
        # with col1:
        #     remember_me = st.checkbox("Remember me")
        # with col2:
        #     st.markdown("""<div style='text-align: right;'>
        #                             <a href='#' style='text-decoration: none; color: white;'>Quên mật khẩu?</a>
        #                 </div>""",unsafe_allow_html=True)
        
        dangnhap = st.form_submit_button("Đăng nhập", use_container_width = True, )
        if dangnhap:
            user = login_user(tk, mk)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.session_state["role"] = user["role"]
                st.session_state["username"] = user["username"]
                st.session_state["user_id"] = user["id"]
                
                st.session_state.page = "Home"
                st.rerun()
            else:
                st.error("Tài khoản hoặc mật khẩu không đúng")

        st.write("-------------------------------------Chưa có tài khoản?------------------------------------")
        dangky = st.form_submit_button("đăng ký", type="primary", use_container_width = True)
        if dangky:
            st.session_state.page = "Register"
            st.rerun()
render_Login()
