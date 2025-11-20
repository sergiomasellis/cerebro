from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    clone_node,
    plan_documentation,
    generate_docs,
    fix_linkages,
    write_files,
)


def create_docs_agent():
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("clone_repo", clone_node)
    workflow.add_node("plan_documentation", plan_documentation)
    workflow.add_node("generate_docs", generate_docs)
    workflow.add_node("fix_linkages", fix_linkages)
    workflow.add_node("write_files", write_files)

    # Define edges
    workflow.set_entry_point("clone_repo")

    workflow.add_edge("clone_repo", "plan_documentation")
    workflow.add_edge("plan_documentation", "generate_docs")
    workflow.add_edge("generate_docs", "fix_linkages")
    workflow.add_edge("fix_linkages", "write_files")
    workflow.add_edge("write_files", END)

    return workflow.compile()
