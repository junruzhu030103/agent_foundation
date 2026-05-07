from langgraph.graph import StateGraph, END
from graph.state import GrantState
from graph.nodes import (
    topic_node,
    query_node,
    retrieve_node,
    evidence_node,
    draft_node,
    figure_node,
    assemble_node,
    validate_node,
)


def build_workflow():
    g = StateGraph(GrantState)

    g.add_node("topic", topic_node)
    g.add_node("query", query_node)
    g.add_node("retrieve", retrieve_node)
    g.add_node("evidence", evidence_node)
    g.add_node("draft", draft_node)
    g.add_node("figure", figure_node)
    g.add_node("assemble", assemble_node)
    g.add_node("validate", validate_node)

    g.set_entry_point("topic")
    g.add_edge("topic", "query")
    g.add_edge("query", "retrieve")
    g.add_edge("retrieve", "evidence")
    g.add_edge("evidence", "draft")
    g.add_edge("draft", "figure")
    g.add_edge("figure", "assemble")
    g.add_edge("assemble", "validate")
    g.add_edge("validate", END)

    return g.compile()
