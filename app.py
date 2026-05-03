# app.py
import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "page" not in st.session_state:
    st.session_state.page = "Home"

# Router
if st.session_state["logged_in"]:
    pg = st.navigation(["pages/Home.py"], position="hidden")
else:
    if st.session_state.page == "Login":
        pg = st.navigation(["pages/Login.py"], position="hidden")
    elif st.session_state.page == "Register":
        pg = st.navigation(["pages/Register.py"], position="hidden")
    else:
        pg = st.navigation(["pages/Home.py"], position="hidden")
pg.run()

