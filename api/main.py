"""
FastAPI entry point for AI Support Desk.

Phase 4 responsibilities:
- HTTP transport only
- Call LangGraph
- Maintain last 10 messages
"""

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from graph.graph_builder import build_graph

# -------------------------
# App setup
# -------------------------

app = FastAPI(
    title="AI Support Desk",
    version="1.0.0",
)

graph = build_graph()

# In-memory conversation history (Phase 4 scope)
conversation_history: List[str] = []


# -------------------------
# Request / Response models
# -------------------------

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


# -------------------------
# API endpoint
# -------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint.

    - Accepts user message
    - Routes via LangGraph
    - Returns final answer
    """

    global conversation_history

    # Append user message
    conversation_history.append(request.message)

    # Keep only last 10 messages
    conversation_history = conversation_history[-10:]

    # Initial graph state
    state = {
        "user_message": request.message,
        "conversation_history": conversation_history,
        "route": None,
        "tool_result": None,
        "final_answer": None,
    }

    # Invoke graph
    result = graph.invoke(state)

    return ChatResponse(answer=result["final_answer"])
