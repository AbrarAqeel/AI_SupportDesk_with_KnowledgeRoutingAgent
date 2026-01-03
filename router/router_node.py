from enum import Enum
from typing import List


class Route(Enum):
    POSTGRES = "postgres"
    VECTOR = "vector"
    EXTERNAL = "external"
    LLM = "llm"


class RouterNode:
    """
    Deterministic rule-based router.
    Strictly follows priority to ensure knowledge base queries
    aren't trapped by database keywords.
    """

    def route(self, message: str, history: List[str]) -> Route:
        text = message.lower()

        # 1. VECTOR DB PRIORITY (Policies/Guides/Escalation)
        # Check this first so "Ticket Escalation Policy" goes to Vector, not Postgres.
        if any(phrase in text for phrase in (
                "how do i", "help", "policy", "guide", "explain",
                "support", "password", "reset", "refund", "escalation"
        )):
            return Route.VECTOR

        # 2. POSTGRES SIGNAL WORDS (Customer/Ticket Data)
        if any(kw in text for kw in ["customer", "ticket", "issue", "status", "account", "id", "city"]):
            return Route.POSTGRES

        # 3. EXTERNAL TOOL SIGNAL WORDS (Weather/Crypto)
        if any(kw in text for kw in ["weather", "temperature", "price", "crypto", "bitcoin"]):
            return Route.EXTERNAL

        # 4. LLM DEFAULT
        return Route.LLM
