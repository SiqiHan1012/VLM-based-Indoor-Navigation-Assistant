import os
import json
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI
from app.core.config import DASHSCOPE_API_KEY, VLM_MODEL

DASHSCOPE_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

def pil_to_data_url(pil_img: Image.Image, fmt="JPEG") -> str:
    buf = BytesIO()
    pil_img.save(buf, format=fmt)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/{fmt.lower()};base64,{b64}"

def run_vlm_inference(pil_image: Image.Image, prompt: str):
    if not DASHSCOPE_API_KEY:
        print("[Error] DASHSCOPE_API_KEY missing")
        return "", {}

    client = OpenAI(api_key=DASHSCOPE_API_KEY, base_url=DASHSCOPE_BASE)
    data_url = pil_to_data_url(pil_image)

    try:
        resp = client.chat.completions.create(
            model=VLM_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": data_url}},
                    {"type": "text", "text": prompt}
                ]
            }],
            max_tokens=128,
            temperature=0.0,
            top_p=0.2,
            stream=False
        )
        raw_text = resp.choices[0].message.content
        
        # 尝试解析 JSON
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1:
            json_str = raw_text[start:end+1]
            return raw_text, json.loads(json_str)
        return raw_text, {}
        
    except Exception as e:
        print(f"[VLM Error] {e}")
        return str(e), {}