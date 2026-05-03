# AI_Analyzer.py
import json
import re
import os
import base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

# Nạp biến môi trường từ file .env nếu có
load_dotenv()

# --- CẤU HÌNH MODEL ---
# Model miễn phí tốt nhất cho vision + reasoning trên HF
VISION_MODEL = "meta-llama/Llama-3.2-11B-Vision-Instruct"
TEXT_MODEL   = "Qwen/Qwen2.5-7B-Instruct" 

CATEGORIES = [
    "Portrait", "Landscape", "Fantasy", "Sci-Fi", "Architecture",
    "Food", "Animals", "Abstract", "Horror", "Romance",
    "Action", "Nature", "Urban", "Historical", "Others"
]

CLASSIFY_PROMPT = f"""Classify this image into ONE category from: {', '.join(CATEGORIES)}.
Reply ONLY with valid JSON, no markdown:
{{"category": "<one of the categories above>", "confidence": <0.0-1.0>, "reason": "<short reason>"}}"""

PREDICT_PROMPT = """Analyze this user's image generation history and predict what they will create next.
Reply ONLY with valid JSON, no markdown:
{{
  "top_themes": ["theme1", "theme2", "theme3"],
  "style_preference": "...",
  "creative_pattern": "...",
  "next_predictions": [
    {{"theme": "...", "probability": 0.0, "reason": "..."}},
    {{"theme": "...", "probability": 0.0, "reason": "..."}},
    {{"theme": "...", "probability": 0.0, "reason": "..."}}
  ],
  "suggested_prompt": "a specific prompt the user would likely enjoy"
}}"""

# --- HÀM BỔ TRỢ ---

def get_openai_client():
    """
    Khởi tạo OpenAI client một cách an toàn.
    Lấy API Key từ Streamlit Session State hoặc biến môi trường.
    """
    api_key = st.session_state.get("api_key") or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        # Trả về None thay vì để thư viện OpenAI báo lỗi crash app[cite: 1]
        return None

    return OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=api_key
    )

def _encode_image_url(path: str) -> str:
    """Encode ảnh thành base64 data URL cho vision model[cite: 1]."""
    suffix = Path(path).suffix.lower()
    media_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".png": "image/png", ".webp": "image/webp"}
    media_type = media_map.get(suffix, "image/jpeg")
    with open(path, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode()
    return f"data:{media_type};base64,{b64}"

def _parse_json(text: str) -> dict:
    """Làm sạch và ép kiểu dữ liệu trả về thành JSON[cite: 1]."""
    # Xóa các ký tự thừa và markdown code blocks[cite: 1]
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    
    # Fallback cơ bản nếu parse lỗi[cite: 1]
    return {"category": "Others", "confidence": 0.0, "reason": "JSON Parsing Error"}

# --- CÁC HÀM CHÍNH ---

def classify_image(image_path: str, prompt: str = "") -> dict:
    """Phân loại ảnh dùng Llama Vision qua HF API[cite: 1]."""
    client = get_openai_client()
    if not client:
        return {"category": "Others", "confidence": 0.0, "reason": "Thiếu API Key"}

    try:
        if image_path and os.path.exists(image_path):
            data_url = _encode_image_url(image_path)
            response = client.chat.completions.create(
                model=VISION_MODEL,
                max_tokens=200,
                messages=[
                    {"role": "system", "content": "You are an image classifier. Reply ONLY with JSON."},
                    {"role": "user", "content": [
                        {"type": "text", "text": f"Prompt: {prompt}\n{CLASSIFY_PROMPT}"},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]}
                ]
            )
        else:
            # Fallback nếu không có file ảnh[cite: 1]
            response = client.chat.completions.create(
                model=TEXT_MODEL,
                max_tokens=200,
                messages=[
                    {"role": "system", "content": "You are an image classifier. Reply ONLY with JSON."},
                    {"role": "user", "content": f"Image prompt: {prompt}\n\n{CLASSIFY_PROMPT}"}
                ]
            )
        return _parse_json(response.choices[0].message.content)
    except Exception as e:
        return {"category": "Others", "confidence": 0.0, "reason": str(e)}

def predict_next_themes(history: list[dict]) -> dict:
    """Dự đoán xu hướng sáng tạo tiếp theo của người dùng[cite: 1]."""
    client = get_openai_client()
    if not client:
        return {"error": "Thiếu API Key"}

    try:
        history_text = json.dumps(history, ensure_ascii=False, indent=2)
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            max_tokens=600,
            messages=[
                {"role": "system", "content": "You are a data analyst. Reply ONLY with JSON."},
                {"role": "user", "content": f"History:\n{history_text}\n\n{PREDICT_PROMPT}"}
            ]
        )
        return _parse_json(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}