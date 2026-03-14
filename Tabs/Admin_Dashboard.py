import streamlit as st
from Database.LAR_Database import get_all_users, update_user_role, update_user_status, delete_user

def render_Admin_Dashboard():
    st.header("🔐 Admin Dashboard", anchor = False)
    
    # Tabs cho các chức năng
    tab1, tab2, tab3 = st.tabs(["📋 Quản lý Tài khoản", "👤 Chi tiết Tài khoản", "⚙️ Cài đặt"])
    
    with tab1:
        st.subheader("Danh sách Tài khoản")
        
        users = get_all_users()
        
        if users:
            # Tạo một table để hiển thị
            col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 1.5, 1.5, 1.5])
            
            with col1:
                st.write("**ID**")
            with col2:
                st.write("**Tài khoản**")
            with col3:
                st.write("**Email**")
            with col4:
                st.write("**Role**")
            with col5:
                st.write("**Trạng thái**")
            with col6:
                st.write("**Hành động**")
            
            st.divider()
            
            for user in users:
                user_id, username, email, role, created_at, is_active = user
                
                col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 1.5, 1.5, 1.5])
                
                with col1:
                    st.write(user_id)
                with col2:
                    st.write(username)
                with col3:
                    st.write(email)
                with col4:
                    # Dropdown để thay đổi role
                    new_role = st.selectbox(
                        "Role",
                        ["user", "moderator", "admin"],
                        index=["user", "moderator", "admin"].index(role),
                        key=f"role_{user_id}",
                        label_visibility="collapsed"
                    )
                    if new_role != role:
                        update_user_role(user_id, new_role)
                        st.rerun()
                
                with col5:
                    status_text = "✅ Active" if is_active else "❌ Inactive"
                    st.write(status_text)
                
                with col6:
                    if is_active:
                        if st.button("🚫 Vô hiệu", key=f"deactivate_{user_id}", use_container_width=True):
                            if role != "admin":
                                update_user_status(user_id, 0)
                                st.success("Tài khoản đã bị vô hiệu!")
                                st.rerun()
                    else:
                        if st.button("✅ Kích hoạt", key=f"activate_{user_id}", use_container_width=True):
                            update_user_status(user_id, 1)
                            st.success("Tài khoản đã được kích hoạt!")
                            st.rerun()
                
                st.divider()
        else:
            st.info("Không có tài khoản nào")
    
    with tab2:
        st.subheader("Chi tiết Tài khoản")
        
        users = get_all_users()
        if users:
            usernames = [user[1] for user in users]
            selected_username = st.selectbox("Chọn tài khoản", usernames)
            
            selected_user = next((user for user in users if user[1] == selected_username), None)
            
            if selected_user:
                user_id, username, email, role, created_at, is_active = selected_user
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID:** {user_id}")
                    st.write(f"**Tài khoản:** {username}")
                    st.write(f"**Email:** {email}")
                with col2:
                    st.write(f"**Role:** {role}")
                    st.write(f"**Trạng thái:** {'✅ Active' if is_active else '❌ Inactive'}")
                    st.write(f"**Ngày tạo:** {created_at}")
                
                st.divider()
                
                # Nút xóa tài khoản
                st.warning("⚠️ Khu vực nguy hiểm")
                if st.button(f"🗑️ Xóa tài khoản '{username}'", use_container_width=True):
                    delete_user(user_id)
                    st.success(f"Tài khoản '{username}' đã bị xóa!")
                    st.rerun()
    
    with tab3:
        st.subheader("Cài đặt Hệ thống")
        
        st.info("📊 Thống kê Hệ thống")
        col1, col2, col3 = st.columns(3)
        
        users = get_all_users()
        total_users = len(users)
        active_users = sum(1 for user in users if user[5] == 1)
        admin_users = sum(1 for user in users if user[3] == 'admin')
        
        with col1:
            st.metric("Tổng Tài khoản", total_users)
        with col2:
            st.metric("Tài khoản Hoạt động", active_users)
        with col3:
            st.metric("Admin", admin_users)
