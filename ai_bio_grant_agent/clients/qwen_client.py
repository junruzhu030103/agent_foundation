import json
import base64
import os
import requests
from pathlib import Path
from config.settings import QWEN_BASE_URL, QWEN_MODEL, QWEN_IMAGE_MODEL


class QwenClient:
    def __init__(self):
        api_key = os.environ.get("QWEN_API_KEY", "")
        if not api_key:
            raise ValueError("QWEN_API_KEY is missing. Please set it in environment variables")
        self.base_url = QWEN_BASE_URL.rstrip("/")
        self.model = QWEN_MODEL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def chat_json(self, prompt: str, temperature: float = 0.5) -> dict:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": "你是严谨的科研写作助手。输出必须是合法JSON。"},
                {"role": "user", "content": prompt},
            ],
        }
        resp = requests.post(url, headers=self.headers, json=payload, timeout=120)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)

    def generate_image(self, prompt: str, save_path: Path, size: str = "1536x1024") -> str:
        url = f"{self.base_url}/images/generations"
        payload = {
            "model": QWEN_IMAGE_MODEL,
            "prompt": prompt,
            "size": size,
        }
        resp = requests.post(url, headers=self.headers, json=payload, timeout=180)
        resp.raise_for_status()
        data = resp.json()
        image_data = data.get("data", [{}])[0]

        image_b64 = image_data.get("b64_json")
        if image_b64:
            save_path.write_bytes(base64.b64decode(image_b64))
            return str(save_path)

        image_url = image_data.get("url")
        if image_url:
            img_resp = requests.get(image_url, timeout=120)
            img_resp.raise_for_status()
            save_path.write_bytes(img_resp.content)
            return str(save_path)

        raise ValueError("No image data returned by qwen image API")
