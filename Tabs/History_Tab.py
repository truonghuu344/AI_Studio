import streamlit as st
import os
from Database.IMG_Database import get_history, delete_history_item, delete_all_history

def render_History_Tab():
   
    
    st.header("Lịch sử tạo ảnh")
    
    history_data = get_history()
    
    if not history_data:
        st.info("Chưa có lịch sử tạo ảnh.")
        return


    col_header, col_action = st.columns([3, 1])
    with col_action:
        if st.button("🗑️ Xóa tất cả", use_container_width=True, type="secondary"):
            delete_all_history()
            st.rerun()

    st.divider()

    for item in history_data:

        with st.expander(f"Prompt: {item[1][:50]}... ({item[5]})"):
            col_a, col_b = st.columns([1, 2])
            
            with col_a:
                if os.path.exists(item[3]):
                    st.image(item[3], use_container_width=True)
                    
                    # Cột chứa 2 nút hành động dưới ảnh
                    btn_a, btn_b = st.columns(2)
                    with btn_a:
                        with open(item[3], "rb") as file:
                            st.download_button(
                                label="💾 Tải",
                                data=file,
                                file_name=os.path.basename(item[3]),
                                mime="image/png",
                                key=f"dl_{item[0]}",
                                use_container_width=True
                            )
                    with btn_b:
                        # Nút xóa từng mục
                        if st.button("🗑️ Xóa", key=f"del_{item[0]}", use_container_width=True):
                            delete_history_item(item[0])
                            st.rerun()
            
            with col_b:
                st.write(f"**Prompt gốc:** {item[1]}")
                st.write(f"**Prompt đã chỉnh sửa:** {item[2] if item[2] else 'Không có'}")
                st.write(f"**Phong cách:** {item[4]}")
                st.write(f"**Ngày tạo:** {item[5]}")