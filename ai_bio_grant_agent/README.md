# AI Biology Grant Agent (Single Proposal)

A minimal LangGraph-based agent to generate one AI-for-biology grant application with:
- Rationale (~1000 Chinese characters) + 1 figure
- Research content & objectives (~500 Chinese characters)
- Detailed research plan (~1500 Chinese characters) + 1 figure
- >=10 references from PubMed

## Quick Start

1. Copy environment file:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run:

```bash
python main.py
```

Output file:
- `outputs/grant_application_001.md`

## Notes

- Figures are generated via `qwen-image-2.0` through the compatible OpenAI-style image generation endpoint.
- PubMed uses NCBI E-utilities (`esearch` + `efetch`).
