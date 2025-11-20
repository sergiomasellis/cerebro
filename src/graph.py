from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    clone_node,
    plan_documentation,
    fix_linkages,
    write_files,
    create_overview,
    create_doc_subgraph,
)


def create_docs_agent():
    from langgraph.types import Send

    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("clone_repo", clone_node)
    workflow.add_node("plan_documentation", plan_documentation)
    workflow.add_node("fix_linkages", fix_linkages)
    workflow.add_node("write_files", write_files)
    workflow.add_node("create_overview", create_overview)

    # Create and add subgraph nodes for each doc type
    doc_ids = [
        "100",
        "101",
        "200",
        "311",
        "330",
        "421",
        "500",
        "600",
        "701",
        "800",
        "850",
        "900",
        "930",
        "980",
    ]
    subgraphs = {}
    for doc_id in doc_ids:
        subgraph = create_doc_subgraph(doc_id)
        subgraphs[doc_id] = subgraph
        workflow.add_node(f"generate_{doc_id}", subgraph)

    # Define edges
    workflow.set_entry_point("clone_repo")

    workflow.add_edge("clone_repo", "plan_documentation")

    # After planning, send to relevant doc generators
    def assign_generators(state: AgentState):
        planned = state["planned_docs"]
        return [Send(f"generate_{doc_id}", state) for doc_id in planned.keys()]

    workflow.add_conditional_edges(
        "plan_documentation",
        assign_generators,
        [f"generate_{doc_id}" for doc_id in doc_ids],
    )

    # After all generators, go to fix_linkages
    for doc_id in doc_ids:
        workflow.add_edge(f"generate_{doc_id}", "fix_linkages")
    workflow.add_edge("fix_linkages", "write_files")
    workflow.add_edge("write_files", "create_overview")
    workflow.add_edge("create_overview", END)

    return workflow.compile()
