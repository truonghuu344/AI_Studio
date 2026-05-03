from API import remove_background

import streamlit as st
import io
from PIL import Image

def render_Lifestyle_Shot():

    user_api_key = st.session_state.get("api_key")
    if "processed_img" not in st.session_state:
        st.session_state["processed_img"] = None
    if "file_ext" not in st.session_state:
        st.session_state["file_ext"] = "png"
        
    layout1, layout2 = st.columns([1, 1], gap="large")

    with layout1:

        st.subheader("Product Photography", anchor = False)

        uploaded_image = st.file_uploader("Upload Image", [".PNG", ".JPG", ".JPEG"])
        # Tải ảnh
        if uploaded_image is not None:
            uploaded_image.seek(0)
            image = Image.open(uploaded_image)
            with st.container(border=True):
                image_col1, image_col2 = st.columns(2, gap="small")

                with image_col1:
                    st.image(image, "Ảnh gốc", width=400, use_container_width=True)

                with image_col2:
                    if st.session_state["processed_img"] is None:
                        st.success("Chờ xử lý packshot...")
                    else:
                        st.image(st.session_state["processed_img"], "Ảnh sau khi sửa")

    with layout2:
        # CSS
        st.markdown("""<div class = "layout2">""", unsafe_allow_html=True)

        edit_option = st.selectbox("Select Edit Option", ["Xóa nền", "Đổi màu nền", "Đổi ảnh nền"], width=550)
        bg_image_file = None
        bg_color = "#FFFFFF"
        if edit_option == "Đổi màu nền":
            bg_color = st.color_picker("Chọn màu nền", "#FFFFFF")
        elif edit_option == "Đổi ảnh nền":
            bg_image_file = st.file_uploader('Tải ảnh nền mới', type=["jpg", "jpeg", "png"])
        sku = st.text_area("SKU (optional)", width=550, height=200)

        # Nút tạo
        if st.button("Create", use_container_width=False):
            if uploaded_image is not None:
                with st.spinner("Đang xử lý..."):
                    try:
                        uploaded_image.seek(0)
                        img_bytes = uploaded_image.read()

                        success, result = remove_background(img_bytes)

                        if success:
                            processed_img = Image.open(io.BytesIO(result)).convert("RGBA")
                            save_format = "PNG"
                            # Đổi màu nền
                            if edit_option == "Đổi màu nền":
                                new_bg = Image.new("RGBA", processed_img.size, bg_color)
                                final_img = Image.alpha_composite(new_bg, processed_img)
                                final_img = final_img.convert("RGB")
                                save_format = "JPEG"
                            # Đổi ảnh nền
                            elif edit_option == "Đổi ảnh nền" and bg_image_file is not None:
                                background = Image.open(bg_image_file).convert("RGBA")
                                background = background.resize(processed_img.size, Image.Resampling.LANCZOS)
                                final_img = Image.alpha_composite(background, processed_img)
                                final_img = final_img.convert("RGB")
                                save_format = "JPEG"
                            else:
                                final_img = processed_img
                                

                            buf = io.BytesIO()
                            final_img.save(buf, format=save_format)
                            st.session_state["processed_img"] = buf.getvalue()
                            st.session_state["file_ext"] = save_format.lower()
                            st.rerun()
                        else:
                            st.error(result)
                    except Exception as e:
                        st.error(f"System error: {e}")
            else:
                st.warning("Tải ảnh lên trước")

        if st.session_state["processed_img"] is not None:
            ext = st.session_state.get("file_ext", "png")
            file_name = f"{sku if sku else 'result'}.{ext}"
            st.download_button(
                label="Tải ảnh",
                data=st.session_state["processed_img"],
                file_name=file_name,
                mime=f"image/{ext}",
                use_container_width=False,
            )
