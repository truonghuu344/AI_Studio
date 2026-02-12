import streamlit as st
import os
from Database.Database import get_history

def render_History_Tab():
    st.header("Lịch sử tạo ảnh")
    history_data  = get_history()
    for item in history_data:
        with st.expander(f"Prompt: {item[1][:50]}... ({item[5]})"):
            col_a, col_b = st.columns([1, 2])
            with col_a:
                if os.path.exists(item[3]):
                    st.image(item[3])
            with col_b:
                st.write(f"Prompt gốc: {item[1]}")
                st.write(f"Prompt đã chỉnh sửa: {item[2]}")
                st.write(f"Ngày tạo: {item[5]}")

