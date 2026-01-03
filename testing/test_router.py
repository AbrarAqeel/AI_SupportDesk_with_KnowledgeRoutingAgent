"""
Phase 2 Router Tests
"""

from router.router_node import RouterNode, Route


def run_router_tests() -> None:
    router = RouterNode()
    history = []

    # POSTGRES
    assert router.route("Show tickets for customer John", history) == Route.POSTGRES
    assert router.route("What is the status of ticket 2?", history) == Route.POSTGRES

    # VECTOR
    assert router.route("How do I reset my password?", history) == Route.VECTOR
    assert router.route("Explain the refund policy", history) == Route.VECTOR

    # EXTERNAL
    assert router.route("What is the weather today?", history) == Route.EXTERNAL
    assert router.route("Bitcoin price right now", history) == Route.EXTERNAL

    # LLM
    assert router.route("Hello, how are you?", history) == Route.LLM
    assert router.route("Explain this system", history) == Route.LLM

    print("=== ALL ROUTER TESTS PASSED ===")


if __name__ == "__main__":
    run_router_tests()
