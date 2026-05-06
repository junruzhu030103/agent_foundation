from services.topic_service import generate_topic
from services.retrieval_service import build_queries, fetch_pubmed, build_evidence_cards
from services.drafting_service import draft_sections
from services.figure_service import generate_two_figures
from services.validator import validate_grant


def topic_node(state):
    topic, novelty, feasibility = generate_topic()
    return {"topic": topic, "novelty_points": novelty, "feasibility_points": feasibility}


def query_node(state):
    queries = build_queries(state["topic"])
    return {"pubmed_queries": queries}


def retrieve_node(state):
    papers = fetch_pubmed(state["pubmed_queries"], top_k=20)
    return {"papers": papers}


def evidence_node(state):
    cards, refs = build_evidence_cards(state["papers"], keep_refs=12)
    return {"evidence_cards": cards, "references": refs}


def draft_node(state):
    rationale, objectives, plan, fig1_prompt, fig2_prompt = draft_sections(
        topic=state["topic"],
        evidence_cards=state["evidence_cards"],
        references=state["references"],
    )
    return {
        "rationale_text": rationale,
        "objectives_text": objectives,
        "plan_text": plan,
        "fig1_prompt": fig1_prompt,
        "fig2_prompt": fig2_prompt,
    }


def figure_node(state):
    fig1_path, fig2_path = generate_two_figures(state["fig1_prompt"], state["fig2_prompt"])
    return {"fig1_path": fig1_path, "fig2_path": fig2_path}


def assemble_node(state):
    md = f"""# {state['topic']}

## 一、立项依据
![立项依据图]({state['fig1_path']})

{state['rationale_text']}

## 二、研究内容与研究目标
{state['objectives_text']}

## 三、具体研究方案
![研究方案图]({state['fig2_path']})

{state['plan_text']}

## 参考文献
""" + "\n".join([f"{i+1}. {r}" for i, r in enumerate(state["references"])])
    return {"final_markdown": md}


def validate_node(state):
    report = validate_grant(state["final_markdown"])
    return {"validation_report": report}
