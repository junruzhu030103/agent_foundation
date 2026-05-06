from clients.qwen_client import QwenClient
from config.prompts import TOPIC_PROMPT


def generate_topic():
    client = QwenClient()
    data = client.chat_json(TOPIC_PROMPT, temperature=0.8)
    return data["topic"], data["novelty_points"], data["feasibility_points"]
