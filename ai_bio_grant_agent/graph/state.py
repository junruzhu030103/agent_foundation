from typing import TypedDict, List, Dict, Any


class GrantState(TypedDict, total=False):
    topic: str
    novelty_points: List[str]
    feasibility_points: List[str]

    pubmed_queries: List[str]
    papers: List[Dict[str, Any]]
    evidence_cards: List[Dict[str, Any]]

    rationale_text: str
    objectives_text: str
    plan_text: str

    fig1_prompt: str
    fig2_prompt: str
    fig1_path: str
    fig2_path: str

    references: List[str]
    final_markdown: str
    validation_report: Dict[str, Any]
