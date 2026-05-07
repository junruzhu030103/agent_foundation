from clients.qwen_client import QwenClient
from config.prompts import DRAFT_PROMPT


def draft_sections(topic: str, evidence_cards, references):
    client = QwenClient()
    prompt = DRAFT_PROMPT.format(topic=topic, evidence_cards=evidence_cards, references=references)
    data = client.chat_json(prompt, temperature=0.5)
    return (
        data["rationale_text"],
        data["objectives_text"],
        data["plan_text"],
        data["fig1_prompt"],
        data["fig2_prompt"],
    )
