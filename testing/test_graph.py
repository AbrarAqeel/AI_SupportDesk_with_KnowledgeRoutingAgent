"""
Phase 3 LangGraph Integration Test

Purpose:
- Validate graph wiring
- Ensure routing + tools + LLM work together
"""

from graph.graph_builder import build_graph


def run_graph_tests() -> None:
    graph = build_graph()

    test_cases = [
        {
            "name": "Postgres route",
            "input": "Show tickets for customer John",
        },
        {
            "name": "Vector route",
            "input": "How do I reset my password?",
        },
        {
            "name": "External route",
            "input": "What is the weather today?",
        },
        {
            "name": "LLM direct route",
            "input": "Explain this system",
        },
    ]

    for case in test_cases:
        print(f"\n--- Testing: {case['name']} ---")

        state = {
            "user_message": case["input"],
            "conversation_history": [],
            "route": None,
            "tool_result": None,
            "final_answer": None,
        }

        result = graph.invoke(state)

        assert result["final_answer"] is not None
        assert isinstance(result["final_answer"], str)
        assert len(result["final_answer"]) > 0

        print("✔ Final answer produced")
        print("Response:")
        print(result["final_answer"])


if __name__ == "__main__":
    print("=== PHASE 3 GRAPH TESTS START ===")
    run_graph_tests()
    print("\n=== PHASE 3 GRAPH TESTS PASSED ===")
