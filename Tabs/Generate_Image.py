from PIL import Image
from API import generate_text_to_image, enhance_prompt
from CSS.CSS import local_css
import streamlit as st
import io
import os
from datetime import datetime
from Database.IMG_Database import save_history, get_user_folder, get_history
from Database.LAR_Database import update_user_credits, check_credit_rq, get_user_credits


def render_Generate_Image():
    local_css()
    user_id = st.session_state.get("user_id")
    user_role = st.session_state.get("role")
    user_api_key = st.session_state.get("api_key")
    
    if "user_input" not in st.session_state:
        st.session_state["user_input"] = ""
    
    if "original_prompt" not in st.session_state:
        st.session_state["original_prompt"] = ""
    if "generated_img_paths" not in st.session_state:
        st.session_state["generated_img_paths"] = []
        history_data = get_history(user_id)
    

    col1, col2, col3 = st.columns(3, gap="large")
    
    # Cột settings
    with col2:
        st.subheader("Setting", anchor = False)
        num_images = st.select_slider("Number of images", options=[1, 2, 3, 4, 5], key="num_imgs")
        aspect_ratio = st.selectbox("Aspect ratio", options=["1:1", "16:9", "4:3", "9:16", "3:2", "21:9"], index=0, key="ratio")
        upscale = st.checkbox("Enhance image quality", key="upscale")
        
        st.subheader("Style Options", anchor = False)
        style = st.selectbox("Image Style", ["Realistic", "Cinematic", "Anime", "Digital Art", "Oil Painting"], key="style_opt")

    # Cột tạo ảnh
    with col1:     
        st.subheader("Generate Image", anchor = False)
        if "enhanced_prompt" in st.session_state:
            st.session_state["user_input"] = st.session_state["enhanced_prompt"]
            del st.session_state["enhanced_prompt"]
     
        user_prompt = st.text_area(
            "Input Prompt",
            key="user_input",
            placeholder="Nhập prompt...",
            height=300,
        )
        

        btn_col1, btn_col2 = st.columns(2, gap="xxlarge")

        # Nút Nâng cấp prompt
        with btn_col1:
            if st.button("Enhance Prompt"):
                if user_prompt:
                    st.session_state["original_prompt"] = user_prompt
                    with st.spinner("Đang nâng cấp prompt..."):
                        enhanced_text = enhance_prompt(user_prompt, api_key=user_api_key)
                    if enhanced_text.startswith("Lỗi"):
                        st.error(enhanced_text)
                    else:
                        st.session_state["enhanced_prompt"] = enhanced_text
                        st.rerun()
                else:
                    st.warning("Vui lòng nhập nội dung trước khi nâng cấp")
        # Nút Generate Images
        with btn_col2:
            cost_per_image = 10
            total_cost = num_images * cost_per_image

            if st.button("Generate Images", type="primary"):
                if not user_api_key:
                    st.error("⚠️ Vui lòng nhập API Key ở Sidebar trước!")
                elif user_prompt:
                    is_admin = (user_role == "admin")
                    proceed = False
                    if is_admin:
                        proceed = True
                    else:
                        if check_credit_rq(user_id, total_cost):
                            proceed = True
                        else:
                            current_credits = get_user_credits(user_id)
                            st.error(f"Bạn không đủ credits. Cần {total_cost} credits. Hiện tại bạn có {current_credits} credits.")
                    if proceed:
                        with st.spinner("Đang khởi tạo hình ảnh..."):
                            final_prompt = f"generate {user_prompt}, with style {style}"
                            if upscale:
                                final_prompt += ", high resolution, 8k, extremely detailed"
                            
                            result = generate_text_to_image(final_prompt, num_images, aspect_ratio, api_key=user_api_key)
                            # Lưu prompt
                            stored_original = st.session_state.get("original_prompt", "").strip()
                            p_original = stored_original if (stored_original and stored_original != user_prompt) else user_prompt
                            p_enhanced = user_prompt if (stored_original and stored_original != user_prompt) else ""
    
                            if not isinstance(result, str):
                                if not is_admin:
                                    update_user_credits(user_id, -total_cost)
                                user_folder = get_user_folder(user_id)
                                file_paths = []

                                for idx, img in enumerate(result):
                                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                    file_name = f"img_{timestamp}_{idx+1}.jpg"
                                    file_path = os.path.join(user_folder, file_name)
                                    file_paths.append(file_path)

                                    img_rgb = img.convert("RGB")    
                                    max_width = 768
                                    w_percent = (max_width / float(img_rgb.size[0]))
                                    h_size = int((float(img_rgb.size[1]) * float(w_percent)))
                                    img_rgb = img_rgb.resize((max_width, h_size), Image.Resampling.LANCZOS)
                                    img_rgb.save(file_path, "JPEG", quality=95, optimize=True)
                                    
                                    
 
                                    save_history(st.session_state["user_id"], p_original, p_enhanced, file_path, style)
                                
                                st.session_state["generated_img"] = result
                                st.session_state["generated_img_paths"] = file_paths
                                st.session_state["display_original_prompt"] = p_original
                                st.session_state["display_enhanced_prompt"] = p_enhanced
                                st.session_state["original_prompt"] =  "" 
                                
                                st.success(f"Đã lưu {len(result)} ảnh vào History Tab")
                                st.rerun()
                            else:
                                st.error(f"Lỗi API: {result}")
                else:
                    st.warning("Vui lòng nhập prompt")
    # Cột kết quả
    with col3:
        st.subheader("Result", anchor = False)
        images = []

        if st.session_state.get("generated_img_paths"):
            for path in st.session_state["generated_img_paths"]:
                if path and os.path.exists(path):
                    try:
                        images.append(Image.open(path).convert("RGB"))
                    except Exception:
                        pass

        if not images and "generated_img" in st.session_state:
            fallback_images = st.session_state["generated_img"]
            if not isinstance(fallback_images, list):
                fallback_images = [fallback_images]
            images = fallback_images

        if images:
            grid_cols = st.columns([1, 1])
            for idx, img in enumerate(images):
                with grid_cols[idx % 2]:
                    st.image(img, caption=f"Ảnh {idx + 1}", use_container_width=True)
                    try:
                        buf = io.BytesIO()
                        img.save(buf, format="PNG")
                        st.download_button(
                            label=f"Download #{idx + 1}",
                            data=buf.getvalue(),
                            file_name=f"ai_image_{idx+1}_{datetime.now().strftime('%H%M%S')}.png",
                            mime="image/png",
                            key=f"dl_btn_{idx}",
                            use_container_width=True
                        )
                    except Exception:
                        st.error("Lỗi khi chuẩn bị file tải về.")
            if len(images) > 0:
                st.toast(f"Đã tạo xong {len(images)} ảnh!")
    
            
