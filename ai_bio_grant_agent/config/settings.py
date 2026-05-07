from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "outputs")
FIGURE_DIR = OUTPUT_DIR / "figures"

QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")

PUBMED_EMAIL = os.getenv("PUBMED_EMAIL", "")
PUBMED_TOOL = os.getenv("PUBMED_TOOL", "ai_bio_grant_agent")


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
