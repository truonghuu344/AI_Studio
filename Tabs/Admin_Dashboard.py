import streamlit as st
from Database.LAR_Database import delete_user, get_all_users, update_user_role, update_user_status
import pandas as pd
import plotly.express as px
import os
from models.AI_Analyzer import classify_image, predict_next_themes
from Database.IMG_Database import get_all_history_by_user, get_uncategorized_images, update_image_category




def render_Admin_Dashboard():
    st.subheader("🔐 Admin Dashboard", anchor = False)
    
    # Tabs cho các chức năng
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Quản lý Tài khoản", "👤 Chi tiết Tài khoản", "⚙️ Thống kê", "🖼️ Phân loại"])
    
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
                    if role == "admin":
                        st.write("admin")
                    else:
                        new_role = st.selectbox(
                            "Role",
                            ["user", "moderator"],
                            index=["user", "moderator"].index(role),
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
                        if role != "admin":
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
                    if username == "admin":
                        st.error("Không thể xóa/vô hiệu tài khoản 'admin'!")
                        return
                    try:
                        delete_all_history(user_id)
                        delete_user(user_id)
                        st.success(f"Đã xóa hoàn toàn tài khoản '{username}'!")
                        st.rerun()
                    except Exception:
                        pass
                    update_user_status(user_id, 0)
                    st.success(f"Đã xóa hoàn toàn tài khoản '{username}'!")
                    st.rerun()
    
    with tab3:
        st.subheader("Thống kê")
        
        st.info("📊 Thống kê Hệ thống")
        users = get_all_users()
        if users:
            df = pd.DataFrame(users, columns=["ID", "Tài khoản", "Email", "Role", "Ngày tạo", "Status"])
            total_users = len(users)
            active_users = df['Status'].sum()
            role_counts = df['Role'].value_counts()
            
            count_admin = role_counts.get('admin', 0)
            count_user = role_counts.get('user', 0)
            count_mod = role_counts.get('moderator', 0)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Tổng Tài khoản", total_users)
            col2.metric("Tài khoản Hoạt động", active_users)
            col3.metric("Tài khoản Admin", count_admin)
            st.divider()
            st.write("**Chi tiết phân quyền:**")
            c1, c2, c3 = st.columns(3)
            c1.write(f"🔹 **User:** {count_user}")
            c2.write(f"🔸 **Moderator:** {count_mod}")
            c3.write(f"👑 **Admin:** {count_admin}")
            
            if st.checkbox("Hiển thị biểu đồ phân bổ"):
                col1, col2, col3 = st.columns(3)
                with col2:
                    if not role_counts.empty:
                    # Chuyển Series role_counts thành DataFrame để Plotly dễ đọc
                        df_pie = role_counts.reset_index()
                        df_pie.columns = ['Role', 'Số lượng']
                        
                        fig = px.pie(
                            df_pie, 
                            values='Số lượng', 
                            names='Role', 
                            title='Phân bổ quyền người dùng',
                            color_discrete_sequence=px.colors.qualitative.Pastel
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.write("Không có dữ liệu biểu đồ")
    with tab4:
        st.subheader("🔍 Phân tích & Dự đoán Thể loại Ảnh")
        users = get_all_users()
        if not users:
            st.info("Chưa có user nào.")
        else:
            user_options = {f"{u[1]} (ID:{u[0]})": u[0] for u in users if u[1] != "admin"}
            target_user_id = user_options[st.selectbox("👤 Chọn người dùng", list(user_options.keys()))]

            if not get_all_history_by_user(target_user_id):
                st.warning("Người dùng này chưa tạo ảnh nào.")
            else:
                # ── Classify ảnh chưa có category ──
                uncategorized = get_uncategorized_images(target_user_id)
                if uncategorized:
                    st.info(f"🤖 Có {len(uncategorized)} ảnh chưa được phân loại.")
                    if st.button("⚡ Phân loại tự động với AI", type="primary"):
                        bar = st.progress(0, text="Đang phân tích...")
                        for i, (img_id, prompt, enhanced, img_path, style) in enumerate(uncategorized):
                            result = classify_image(img_path, enhanced or prompt)
                            update_image_category(img_id, result.get("category", "Others"))
                            bar.progress((i + 1) / len(uncategorized),
                                         text=f"Phân loại {i+1}/{len(uncategorized)}: {result.get('category')}")
                        st.success("✅ Phân loại xong!")
                        st.rerun()

                # ── Build DataFrame ──
                df = pd.DataFrame(
                    get_all_history_by_user(target_user_id),
                    columns=["id", "prompt", "enhanced_prompt", "image_path", "style", "category", "timestamp"]
                )
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

                # Metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("🖼️ Tổng ảnh", len(df))
                c2.metric("🎨 Style chính", df["style"].mode()[0] if not df["style"].isna().all() else "—")
                c3.metric("📁 Thể loại chính", df["category"].mode()[0] if not df["category"].isna().all() else "—")
                st.divider()

                # Charts
                col1, col2 = st.columns(2)
                with col1:
                    cat_df = df["category"].value_counts().reset_index()
                    cat_df.columns = ["Thể loại", "Số lượng"]
                    st.plotly_chart(px.pie(cat_df, values="Số lượng", names="Thể loại",
                                          title="Phân bổ thể loại",
                                          color_discrete_sequence=px.colors.qualitative.Pastel),
                                   use_container_width=True)
                with col2:
                    style_df = df["style"].value_counts().reset_index()
                    style_df.columns = ["Style", "Số lượng"]
                    st.plotly_chart(px.bar(style_df, x="Style", y="Số lượng", title="Phân bổ Style",
                                          color="Số lượng", color_continuous_scale="Blues"),
                                   use_container_width=True)

                # Timeline (chỉ hiện khi có >= 2 ngày khác nhau)
                df["date"] = df["timestamp"].dt.date
                timeline = df.groupby(["date", "category"]).size().reset_index(name="count")
                if timeline["date"].nunique() > 1:
                    st.plotly_chart(px.line(timeline, x="date", y="count", color="category",
                                           title="Lịch sử tạo ảnh theo thời gian", markers=True),
                                   use_container_width=True)
                st.divider()

                # ── AI Prediction ──
                st.subheader("🔮 Dự đoán chủ đề tiếp theo")
                if st.button("🧠 Phân tích & Dự đoán với AI"):
                    history_for_ai = (
                        df[["prompt", "style", "category", "timestamp"]]
                        .assign(timestamp=df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S").fillna(""))
                        .tail(30)
                        .to_dict("records")
                    )
                    with st.spinner("AI đang phân tích..."):
                        prediction = predict_next_themes(history_for_ai)
                    if "error" in prediction:
                        st.error(f"Lỗi: {prediction['error']}")
                    else:
                        st.session_state[f"prediction_{target_user_id}"] = prediction

                if f"prediction_{target_user_id}" in st.session_state:
                    pred = st.session_state[f"prediction_{target_user_id}"]
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**🏷️ Theme yêu thích:**")
                        for t in pred.get("top_themes", []):
                            st.markdown(f"- {t}")
                        st.markdown(f"**🎨 Phong cách:** {pred.get('style_preference', '—')}")
                        st.markdown(f"**🧩 Pattern:** {pred.get('creative_pattern', '—')}")
                    with col_b:
                        st.markdown("**🔮 Dự đoán tiếp theo:**")
                        for item in pred.get("next_predictions", []):
                            prob = int(item.get("probability", 0) * 100)
                            st.markdown(f"**{item.get('theme')}** — {prob}%")
                            st.progress(prob / 100)
                            st.caption(item.get("reason", ""))
                    st.info(f"💡 **Gợi ý prompt:** {pred.get('suggested_prompt', '')}")

                # ── Gallery ──
                with st.expander("🖼️ Gallery ảnh của user"):
                    img_cols = st.columns(4)
                    for i, (_, row) in enumerate(df.iterrows()):
                        if row["image_path"] and os.path.exists(row["image_path"]):
                            with img_cols[i % 4]:
                                st.image(row["image_path"], use_container_width=True)
                                st.caption(f"**{row['category']}** · {row['style']}")
                                st.caption(row["prompt"][:50] + ("..." if len(row["prompt"]) > 50 else ""))
       
        