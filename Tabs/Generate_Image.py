from PIL import Image
from API import generate_text_to_image, enhance_prompt
from CSS import local_css
import streamlit as st
import io
import os
from datetime import datetime
from Database.Database import save_history

def render_Generate_Image():
    local_css()
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col2:
        st.subheader("Setting")
        num_images = st.select_slider("Number of images", options=[1, 2, 3, 4, 5], key="num_imgs")
        aspect_ratio = st.selectbox("Aspect ratio", options=["1:1", "16:9", "4:3", "9:16", "3:2", "21:9"], index=0, key="ratio")
        upscale = st.checkbox("Enhance image quality", key="upscale")
        
        st.subheader("Style Options")
        style = st.selectbox("Image Style", ["Realistic", "Cinematic", "Anime", "Digital Art", "Oil Painting"], key="style_opt")

    with col1:
        # Khởi tạo session state
        if "user_input" not in st.session_state:
            st.session_state["user_input"] = ""
        if "original_prompt" not in st.session_state:
            st.session_state["original_prompt"] = ""

        st.subheader("Generate Image")
        user_prompt = st.text_area("Input Prompt",
                                   value=st.session_state["user_input"],
                                   placeholder="Nhập prompt...",
                                   height=300)
        
        btn_col1, btn_col2 = st.columns(2, gap="xxlarge")
        
        with btn_col1:
            if st.button("Enhance Prompt"):
                if user_prompt:

                    st.session_state["original_prompt"] = user_prompt
                    with st.spinner("Đang nâng cấp prompt..."):
                        enhanced_text = enhance_prompt(user_prompt)
                    
                    if enhanced_text.startswith("Lỗi"):
                        st.error(enhanced_text)
                    else:
                        st.session_state["user_input"] = enhanced_text
                        st.rerun()
                else:
                    st.warning("Vui lòng nhập nội dung trước khi nâng cấp")

        with btn_col2:
            if st.button("Generate Images", type="primary"):
                if user_prompt:
                    with st.spinner("Đang khởi tạo hình ảnh..."):
                        final_prompt = f"{user_prompt}, style {style}"
                        if upscale:
                            final_prompt += ", high resolution, 8k, extremely detailed"
                        
                        result = generate_text_to_image(final_prompt, num_images, aspect_ratio)
                        
                        if not isinstance(result, str):
                            if not os.path.exists('outputs'):
                                os.makedirs('outputs')

                            for idx, img in enumerate(result):
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                file_name = f"img_{timestamp}_{idx+1}.jpg"
                                file_path = os.path.join("outputs", file_name)

                                # Xử lý làm nhỏ ảnh và lưu
                                img_rgb = img.convert("RGB")    
                                max_width = 768
                                w_percent = (max_width / float(img_rgb.size[0]))
                                h_size = int((float(img_rgb.size[1]) * float(w_percent)))
                                img_rgb = img_rgb.resize((max_width, h_size), Image.Resampling.LANCZOS)
                                img_rgb.save(file_path, "JPEG", quality=95, optimize=True)

                                if st.session_state["original_prompt"]:
                                    p_original = st.session_state["original_prompt"]
                                    p_enhanced = user_prompt
                                else:
                                    p_original = user_prompt
                                    p_enhanced = ""
                                
                                save_history(p_original, p_enhanced, file_path, style)
                            
                            st.session_state["generated_img"] = result
                            # Reset prompt gốc sau khi đã lưu xong vào database
                            st.session_state["original_prompt"] = "" 
                            st.success(f"Đã lưu {len(result)} ảnh vào thư mục outputs/")
                        else:
                            st.error(f"Lỗi API: {result}")
                else:
                    st.warning("Vui lòng nhập prompt")

    with col3:
        st.subheader("Result")
        if "generated_img" in st.session_state:
            images = st.session_state["generated_img"]
            if not isinstance(images, list):
                images = [images]
                
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
                    except Exception as e:
                        st.error("Lỗi khi chuẩn bị file tải về.")
            
            if len(images) > 0:
                st.success(f"Đã tạo xong {len(images)} ảnh!")