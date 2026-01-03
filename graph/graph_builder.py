"""
LangGraph wiring for AI Support Desk.
"""

import os
import re
import string
from typing import Dict, Any, TypedDict, List

from transformers import AutoTokenizer, AutoModelForCausalLM
from langgraph.graph import StateGraph, END

from router.router_node import RouterNode, Route
from tools.postgres_tool import PostgresTool
from tools.vector_tool import VectorSearchTool
from tools.external_tool import ExternalMockTool

# ======================================================
# LLM setup (Hugging Face)
# ======================================================

LLM_AVAILABLE = os.getenv("LLM_AVAILABLE", "false") == "true"
MODEL_DIR = "models/qwen2.5-0.5b"

tokenizer = None
model = None

if LLM_AVAILABLE:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR,
        device_map="cpu",
    )
    model.eval()


# ======================================================
# State definition
# ======================================================

class GraphState(TypedDict):
    user_message: str
    conversation_history: List[str]
    route: str | None
    tool_result: Dict[str, Any] | None
    final_answer: str | None


# ======================================================
# Nodes
# ======================================================

def router_node(state: GraphState) -> GraphState:
    router = RouterNode()
    state["route"] = router.route(
        state["user_message"],
        state["conversation_history"],
    ).value
    return state


def postgres_node(state: GraphState) -> GraphState:
    """
    Execute Postgres queries for ticket or customer requests.
    Cleans punctuation from customer names to prevent query failures.
    """
    tool = PostgresTool()
    message = state["user_message"].lower()

    # 1. Ticket status by ID
    if "ticket" in message:
        match = re.search(r'ticket\s*#?(\d+)', message)
        if match:
            ticket_id = match.group(1)
            query = "SELECT id, issue, status FROM tickets WHERE id = %s"
            state["tool_result"] = tool.run_query(query, (ticket_id,))
            return state

    # 2. Customer city/location info
    if "city" in message or "from" in message:
        id_match = re.search(r'customer\s*(\d+)', message)
        if id_match:
            cust_id = id_match.group(1)
            query = "SELECT name, city FROM customers WHERE id = %s"
            state["tool_result"] = tool.run_query(query, (cust_id,))
            return state

    # 3. Tickets by customer name (NOW WITH PUNCTUATION FIX)
    if "customer" in message:
        try:
            raw_name = message.split("customer", 1)[1].strip()
            # Remove full stops or other punctuation from the name
            clean_name = raw_name.translate(str.maketrans('', '', string.punctuation)).title()

            query = """
            SELECT t.id, t.issue, t.status
            FROM tickets t
            JOIN customers c ON t.customer_id = c.id
            WHERE c.name = %s
            """
            state["tool_result"] = tool.run_query(query, (clean_name,))
            return state
        except Exception:
            pass

    state["tool_result"] = None
    return state


def vector_node(state: GraphState) -> GraphState:
    tool = VectorSearchTool()
    result = tool.search(state["user_message"])
    state["tool_result"] = result if result["documents"] else None
    return state


def external_node(state: GraphState) -> GraphState:
    """
    Dynamically detects tool type for ExternalMockTool.
    """
    tool = ExternalMockTool()
    msg = state["user_message"].lower()

    # Detect crypto vs weather based on keywords
    tool_type = "crypto" if any(kw in msg for kw in ["bitcoin", "btc", "crypto", "price"]) else "weather"

    state["tool_result"] = tool.run(tool_type, state["user_message"])
    return state


def llm_node(state: GraphState) -> GraphState:
    """
    Final response node with deterministic formatting.
    """
    tool_result = state.get("tool_result")
    user_msg = state["user_message"].lower()

    if tool_result and "rows" in tool_result:
        rows = tool_result["rows"]
        if not rows:
            state["final_answer"] = "No tickets or customer data found."
            return state

        first_row = rows[0]
        if "issue" in first_row:
            state["final_answer"] = "\n".join(
                f"Ticket #{r['id']} — {r['issue']} (Status: {r['status']})"
                for r in rows
            )
        elif "city" in first_row:
            state["final_answer"] = f"Customer {first_row['name']} is from {first_row['city']}."
        return state

    if tool_result and "documents" in tool_result:
        content = tool_result["documents"][0]["content"]
        if ":" in content:
            content = content.split(":", 1)[1].strip()
        state["final_answer"] = content
        return state

    if tool_result and "result" in tool_result:
        state["final_answer"] = tool_result["result"]
        return state

    system_keywords = ["explain this system", "what can you do", "how do you work"]
    if any(kw in user_msg for kw in system_keywords):
        state["final_answer"] = (
            "I am an AI Support Desk system. I answer questions about customers, "
            "tickets, support policies, and general information by routing requests "
            "to verified internal tools."
        )
        return state

    state["final_answer"] = "I don't have enough information to answer that."
    return state


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("router", router_node)
    graph.add_node("postgres", postgres_node)
    graph.add_node("vector", vector_node)
    graph.add_node("external", external_node)
    graph.add_node("llm", llm_node)

    graph.set_entry_point("router")
    graph.add_conditional_edges(
        "router",
        lambda s: s["route"],
        {
            Route.POSTGRES.value: "postgres",
            Route.VECTOR.value: "vector",
            Route.EXTERNAL.value: "external",
            Route.LLM.value: "llm",
        },
    )
    graph.add_edge("postgres", "llm")
    graph.add_edge("vector", "llm")
    graph.add_edge("external", "llm")
    graph.add_edge("llm", END)

    return graph.compile()
