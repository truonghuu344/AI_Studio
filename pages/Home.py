import streamlit as st
from Database.IMG_Database import init_db
from Database.LAR_Database import create_user_table
from CSS import local_css
from Tabs.Generate_Image import render_Generate_Image
from Tabs.Lifestyle_Shot import render_Lifestyle_Shot
from Tabs.AI_Chatbot import render_AI_Chatbot
from Tabs.Sidebar import render_side_bar
from Tabs.History_Tab import render_History_Tab



local_css()
init_db()

st.title("Text to image", anchor = False)

if not st.session_state.get("logged_in", False):
    col_login, col_register = st.columns([1, 1], vertical_alignment="center")
    
    with col_login:
        st.markdown("""<style> .stButton {
            padding-top: 10px !important;           
        } </style> """, unsafe_allow_html=True)
        if st.button("Login", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()
    with col_register:
        st.markdown("""<style> .stButton {
            padding-top: 10px !important;           
        } </style> """, unsafe_allow_html=True)
        if st.button("Register", use_container_width=True):
            st.session_state.page = "Register"
            st.rerun()


if st.session_state.get("logged_in"):
    render_side_bar()

if st.session_state["logged_in"]:
    render_AI_Chatbot()

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
