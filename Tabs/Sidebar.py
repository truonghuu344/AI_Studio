import streamlit as st
from Database.IMG_Database import get_history
from Database.LAR_Database import get_user_credits



def render_side_bar():
    with st.sidebar:
        st.markdown("<h1 style='color: white;'>⚙️ Dashboard</h1>", unsafe_allow_html=True)
        st.divider()
        
        st.subheader("👤 User Profile")
        user_role = st.session_state.get("role")
        username = st.session_state.get("username", "Guest")
        st.markdown(f"<span style='color:white'>**Username:** {username} </span>", unsafe_allow_html = True)
     
        
        try:
            user_id = st.session_state.get("user_id")
            history = get_history(user_id)
            image_count = len(history) if history else 0
        except:
            image_count = 0
        try:
            current_credits = get_user_credits(user_id)
        except:
            current_credits = 0
        st.markdown(f"<span style='color:white'>**Images Created:**  {image_count} 🖼️</span>", unsafe_allow_html = True)
        
        if user_role != "admin":
            st.markdown(f"<span style='color:white'> **Credits:**  {current_credits} 🪙</span>", unsafe_allow_html = True)
        st.markdown(f"<span style='color:white'>**Status:**  Online ✅ </span>", unsafe_allow_html = True)

        st.divider()
        api = st.text_input("API key", type="password", placeholder="Enter your API key here")
        st.session_state["api_key"] = api
        
        
        st.divider()
     
        st.markdown("""
            <style>
            div.stButton {
                color: white !important;
            }
            div.stButton:hover {
                background-color: rgb(255, 102, 102) !important;
                border-radius: 10px;
            }
            </style?
        """, unsafe_allow_html = True)
        if st.button("Logout", use_container_width=True, type="secondary"):
           
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.session_state["user_id"] = None
            st.session_state["role"] = None
  
            st.session_state["user_input"] = "" 
            st.session_state["original_prompt"] = ""
            st.session_state["enhanced_prompt"] = ""
  
            if "generated_img" in st.session_state:
                st.session_state["generated_img"] = []
            if "generated_img_paths" in st.session_state:
                st.session_state["generated_img_paths"] = []
            
            st.rerun()



