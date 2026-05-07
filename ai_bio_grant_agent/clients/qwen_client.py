import json
import requests
from config.settings import QWEN_API_KEY, QWEN_BASE_URL, QWEN_MODEL


class QwenClient:
    def __init__(self):
        if not QWEN_API_KEY:
            raise ValueError("QWEN_API_KEY is missing. Please set it in .env")
        self.base_url = QWEN_BASE_URL.rstrip("/")
        self.model = QWEN_MODEL
        self.headers = {
            "Authorization": f"Bearer {QWEN_API_KEY}",
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
