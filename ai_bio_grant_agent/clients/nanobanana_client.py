from pathlib import Path
import requests
from config.settings import NANOBANANA_API_KEY, NANOBANANA_BASE_URL


class NanoBananaClient:
    """Placeholder client. Replace endpoint/payload according to real API docs."""

    def __init__(self):
        if not NANOBANANA_API_KEY:
            raise ValueError("NANOBANANA_API_KEY is missing. Please set it in .env")
        if not NANOBANANA_BASE_URL:
            raise ValueError("NANOBANANA_BASE_URL is missing. Please set it in .env")
        self.base_url = NANOBANANA_BASE_URL.rstrip("/")
        self.headers = {"Authorization": f"Bearer {NANOBANANA_API_KEY}"}

    def generate_image(self, prompt: str, save_path: Path) -> str:
        url = f"{self.base_url}/images/generations"
        payload = {"prompt": prompt, "size": "1536x1024"}
        res = requests.post(url, headers=self.headers, json=payload, timeout=180)
        res.raise_for_status()
        data = res.json()

        image_url = data.get("data", [{}])[0].get("url")
        if not image_url:
            raise ValueError("No image URL returned by nanobanana API")

        img = requests.get(image_url, timeout=120)
        img.raise_for_status()
        save_path.write_bytes(img.content)
        return str(save_path)
