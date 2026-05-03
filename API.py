import io
import os
import requests
import random
from PIL import Image
from huggingface_hub import InferenceClient
from openai import OpenAI
from rembg import remove, new_session
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

hf_client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)
oai_client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=HF_TOKEN)

def generate_text_to_image(prompt, num_images=1, aspect_ratio="1:1", api_key = None):
    if not api_key:
        return "Lỗi: Vui lòng nhập API Key ở Sidebar"
    hf_client = InferenceClient(provider="hf-inference", api_key=api_key)
    
    ratios = {
        "1:1": (1024, 1024),
        "16:9": (1280, 720),
        "4:3": (1024, 768),
        "9:16": (720, 1280),
        "3:2": (1216, 832),
        "21:9": (1536, 640)
    }
    
    w, h = ratios.get(aspect_ratio, (1024, 1024))
    images = []
    try:
        for _ in range(int(num_images)):
            seed = random.randint(0, 2**32 - 1)
            img = hf_client.text_to_image(
                prompt,
                model="black-forest-labs/FLUX.1-schnell",
                width=w,
                height=h,
                seed = seed
            )
            images.append(img)
        return images
    except Exception as e:
        return f"Lỗi generate ảnh: {e}"


def enhance_prompt(prompt, api_key = None):
    if not api_key:
        return "Lỗi: Vui lòng nhập API Key ở Sidebar"
    
    try:
        oai_client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=api_key)
        res = oai_client.chat.completions.create(
            model="google/gemma-4-31B-it",
            messages=[
                {"role": "system", "content": "Expand the user's description into a detailed artistic prompt. Output ONLY the prompt."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )
        return res.choices[0].message.content.strip().replace('"', '')
    except Exception as e:
        return f"Lỗi: {e}"


rembg_session = None
 
def get_rembg_session():
    global rembg_session
    if rembg_session is None:
        rembg_session = new_session("u2net")
    return rembg_session

def remove_background(image_data: bytes) -> tuple[bool, bytes | str]:
    try:
        session = get_rembg_session()
        output_bytes: bytes = remove(image_data, session=session)
        return True, output_bytes
    except Exception as e:
        return False, str(e)

def ai_chatbot(messages, api_key = None):
    if not api_key:
        return "Lỗi: Vui lòng nhập API Key ở Sidebar"
    try:
        oai_client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=api_key)
        return oai_client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=messages,
            stream=True
        )
    except Exception as e:
        return f"Lỗi: {e}"

