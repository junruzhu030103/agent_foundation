from typing import List, Dict, Tuple
from clients.qwen_client import QwenClient
from clients.pubmed_client import PubMedClient
from config.prompts import QUERY_PROMPT


def build_queries(topic: str) -> List[str]:
    client = QwenClient()
    data = client.chat_json(QUERY_PROMPT.format(topic=topic), temperature=0.4)
    return data.get("queries", [])


def fetch_pubmed(queries: List[str], top_k: int = 20) -> List[Dict]:
    pm = PubMedClient()
    pmids = []
    for q in queries:
        pmids.extend(pm.search_pmids(q, retmax=max(top_k // max(len(queries), 1), 5)))
    pmids = list(dict.fromkeys(pmids))[:top_k]
    return pm.fetch_details(pmids)


def build_evidence_cards(papers: List[Dict], keep_refs: int = 12) -> Tuple[List[Dict], List[str]]:
    selected = [p for p in papers if p.get("title")][:keep_refs]
    cards = []
    refs = []
    for p in selected:
        citation = _format_reference(p)
        cards.append({
            "claim": p.get("title", ""),
            "support": (p.get("abstract", "")[:280] + "...") if p.get("abstract") else "Abstract not available",
            "citation": citation,
        })
        refs.append(citation)
    return cards, refs


def _format_reference(p: Dict) -> str:
    authors = ", ".join(p.get("authors", [])[:3])
    if len(p.get("authors", [])) > 3:
        authors += ", et al"
    return f"{authors}. {p.get('title','')}. {p.get('journal','')}. {p.get('year','')}. PMID:{p.get('pmid','')}"
