import streamlit as st
from Database.IMG_Database import init_db
from Database.LAR_Database import create_user_table, init_default_admin
from CSS.CSS import local_css
from Tabs.Generate_Image import render_Generate_Image
from Tabs.Lifestyle_Shot import render_Lifestyle_Shot
from Tabs.AI_Chatbot import render_AI_Chatbot
from Tabs.Sidebar import render_side_bar
from Tabs.History_Tab import render_History_Tab
from Tabs.Admin_Dashboard import render_Admin_Dashboard



local_css()
init_db()
create_user_table()
init_default_admin()  # Tự động tạo admin nếu chưa tồn tại

st.title("Text to image", anchor = False)


if not st.session_state.get("logged_in", False):
    col1, col2, col3 = st.columns([1, 1, 2])
    with col3:
        col1, col2 = st.columns([1,1])
        with col2:
            login, register = st.columns([1,1])
            with login:
                if st.button("Login", use_container_width=True):
                    st.session_state.page = "Login"
                    st.rerun()
            with register:
                if st.button("Register", use_container_width=True):
                    st.session_state.page = "Register"
                    st.rerun()
      

if st.session_state.get("logged_in"):
    render_side_bar()

if st.session_state["logged_in"]:
    render_AI_Chatbot()

# Kiểm tra nếu user là admin
if st.session_state.get("role") == "admin":
    GenerateImage, LifestyleShot, HistoryTab, Admin = st.tabs(["Generate Image", "Lifestyle Shot", "History Tab", "🔐 Admin"])
else:
    GenerateImage, LifestyleShot, HistoryTab = st.tabs(["Generate Image", "Lifestyle Shot", "History Tab"])

#Tab1
with GenerateImage:
    if not st.session_state["logged_in"]:
        st.warning("Bạn cần đăng nhập để sử dụng tính năng này.")
    else:
        render_Generate_Image()
#Tab2
with LifestyleShot:
    if not st.session_state["logged_in"]:
        st.warning("Bạn cần đăng nhập để sử dụng tính năng này.")
    else:
        render_Lifestyle_Shot()
#Tab3
with HistoryTab:
    if not st.session_state["logged_in"]:
        st.warning("Bạn cần đăng nhập để sử dụng tính năng này.")
    else:
        render_History_Tab()

#Tab4 - Admin
if st.session_state.get("role") == "admin":
    with Admin:
        render_Admin_Dashboard()
