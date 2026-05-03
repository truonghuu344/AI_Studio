import os
from openai import OpenAI
import streamlit as st

from API import ai_chatbot
from Database.LAR_Database import get_user_credits, update_user_credits, check_credit_rq


def render_AI_Chatbot():
 
    locals()
    
    api_key = st.session_state.get("api_key")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{
            "role": "system",
            "content": "Bạn là trợ lý AI. Trả lời câu hỏi bằng tiếng Việt"
        }]


    with st.popover("Chat with AI"):
        st.markdown("Tin nhắn")
        chat_container = st.container(height = 300)

        with chat_container:
            for m in st.session_state["messages"]:
                if isinstance(m, dict) and "role" in m:
                    if m["role"] != "system":
                        with st.chat_message(m["role"]):
                            st.markdown(m["content"])

        chat_cost = 2
        user_id = st.session_state["user_id"]
        user_role = st.session_state["role"]

        if prompt := st.chat_input("Nhập câu hỏi...", key ="input_float"):
            is_admin = user_role == "admin"

            if not is_admin and not check_credit_rq(user_id, chat_cost):
                st.error(f"Bạn không có đủ credits. Vui lòng nạp thêm credits.")
                return
            else:
                st.session_state["messages"].append({
                    "role": "user",
                    "content": prompt,
                })
                chat_container.chat_message("user").write(prompt)

                with chat_container.chat_message("assistant"):
                    res_box = st.empty()
                    full_res = ""

                    stream = ai_chatbot(st.session_state["messages"], api_key=api_key)

                    if isinstance(stream, str):
                        st.error(stream)
                    else:                 
                        for chunk in stream:
                            try:
                                content = chunk.choices[0].delta.content
                                if content:
                                    full_res += content
                                    res_box.markdown(full_res + "▌")
                            except (IndexError, AttributeError):
                                continue

                        res_box.markdown(full_res)
                        if not is_admin:
                            update_user_credits(user_id, -chat_cost)
            
                        st.session_state["messages"].append({
                            "role": "assistant",
                            "content": full_res
                        })
                        st.rerun()





