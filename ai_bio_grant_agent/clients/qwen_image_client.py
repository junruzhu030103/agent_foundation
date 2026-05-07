from pathlib import Path
import base64
import requests
from config.settings import QWEN_API_KEY, QWEN_BASE_URL


class QwenImageClient:
    def __init__(self):
        if not QWEN_API_KEY:
            raise ValueError("QWEN_API_KEY is missing. Please set it in .env")
        self.base_url = QWEN_BASE_URL.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {QWEN_API_KEY}",
            "Content-Type": "application/json",
        }

    def generate_image(self, prompt: str, save_path: Path, size: str = "1536x1024") -> str:
        url = f"{self.base_url}/images/generations"
        payload = {
            "model": "qwen-image-2.0",
            "prompt": prompt,
            "size": size,
            "response_format": "b64_json",
        }
        res = requests.post(url, headers=self.headers, json=payload, timeout=180)
        res.raise_for_status()
        data = res.json()

        item = (data.get("data") or [{}])[0]
        b64_data = item.get("b64_json")
        image_url = item.get("url")

        if b64_data:
            save_path.write_bytes(base64.b64decode(b64_data))
            return str(save_path)

        if image_url:
            img = requests.get(image_url, timeout=120)
            img.raise_for_status()
            save_path.write_bytes(img.content)
            return str(save_path)

        raise ValueError("No image content returned by qwen-image-2.0 API")
