import io
import os
import requests
from PIL import Image
from huggingface_hub import InferenceClient
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
REMOVE_BG_KEY = os.getenv("REMOVE_BG_TOKEN")

hf_client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)
oai_client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=HF_TOKEN)

def generate_text_to_image(prompt, num_images=1, aspect_ratio="1:1"):
    ratios = {
        "1:1": (1024, 1024),
        "16:9": (1280, 720),
        "4:3": (1024, 768),
        "9:16": (720, 1280),
        "3:2": (1216, 832),
        "21:9": (1536, 640)
    }
    w, h = ratios.get(aspect_ratio, (1024, 1024))
    try:
        return [hf_client.text_to_image(prompt, model="stabilityai/stable-diffusion-xl-base-1.0", width=w, height=h)
                for _ in range(int(num_images))]
    except Exception as e:
        return f"Lỗi: {e}"

def enhance_prompt(prompt):
    try:
        res = oai_client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[
                {"role": "system", "content": "Expand the user's description into a detailed artistic prompt. Output ONLY the prompt."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        return f"Lỗi: {e}"

def remove_background(image_data):
    try:
        res = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': image_data},
            headers={'X-API-Key': REMOVE_BG_KEY},
            timeout=30
        )
        return (True, res.content) if res.status_code == 200 else (False, res.text)
    except Exception as e:
        return False, str(e)

def ai_chatbot(messages):
    try:
        return oai_client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=messages,
            stream=True
        )
    except Exception as e:
        return f"Lỗi: {e}"

