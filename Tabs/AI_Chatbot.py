import os
from openai import OpenAI
import streamlit as st

from API import ai_chatbot


def render_AI_Chatbot():
   
    
    # Tạo biến
    locals()
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{
            "role": "system",
            "content": "Bạn là trợ lý AI. Trả lời câu hỏi bằng tiếng Việt"
        }]


    with st.popover("Chat with AI"):
        st.markdown("Tin nhắn")
        # Tạo khung chứa
        chat_container = st.container(height = 300)

        with chat_container:
            for m in st.session_state["messages"]:
                if isinstance(m, dict) and "role" in m:
                    if m["role"] != "system":
                        with st.chat_message(m["role"]):
                            st.markdown(m["content"])

        # Input của user
        if prompt := st.chat_input("Nhập câu hỏi...", key ="input_float"):
            st.session_state["messages"].append({
                "role": "user",
                "content": prompt,
            })
            # Hiển thị tin nhắn trong khung
            chat_container.chat_message("user").write(prompt)

            with chat_container.chat_message("assistant"):
                res_box = st.empty()
                full_res = ""

                stream = ai_chatbot(st.session_state["messages"])

                if isinstance(stream, str):
                    st.error(stream)
                else:                 
                    for chunk in stream:
                        content = chunk.choices[0].delta.content
                        if content:
                            full_res += content
                            res_box.markdown(full_res + "▓")
                    res_box.markdown(full_res)
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": full_res
                    })
                    st.rerun()









