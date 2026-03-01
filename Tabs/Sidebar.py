import streamlit as st
from CSS import local_css
from Database.IMG_Database import get_history


def render_side_bar():
    """Render sidebar with user info, status, image count, and settings"""
    
    with st.sidebar:
        st.title("⚙️ Dashboard")
        st.divider()
        
        # ==================== USER PROFILE SECTION ====================
        st.subheader("👤 User Profile")
        
        # Get user info
        username = st.session_state.get("username", "Guest")
        st.write(f"**Username:** {username}")
        
        # Get number of created images
        try:
            history = get_history()
            image_count = len(history) if history else 0
        except:
            image_count = 0
        
        st.write(f"**Images Created:** 🖼️ {image_count}")
        st.write(f"**Status:** ✅ Online")
        
        st.divider()
        
        # Empty space to push logout to bottom
        st.write("")
        st.write("")
        
        # ==================== LOGOUT ====================
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()



