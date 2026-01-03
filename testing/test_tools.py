"""
Phase 1 Tool Verification Script

This script validates:
1. Postgres Tool
2. Vector Search Tool
3. External Mock Tool

Run this BEFORE moving to Phase 2.
"""

from tools.postgres_tool import PostgresTool
from tools.vector_tool import VectorSearchTool
from tools.external_tool import ExternalMockTool


def test_postgres_tool() -> None:
    """Test Postgres SELECT queries."""
    print("\n--- Testing Postgres Tool ---")

    pg = PostgresTool()

    # 1. Fetch all customers
    result = pg.run_query("SELECT * FROM customers;")
    assert result["row_count"] == 3
    print("✔ Fetch all customers")

    # 2. Fetch tickets for customer_id = 1
    result = pg.run_query(
        "SELECT * FROM tickets WHERE customer_id = %(cid)s;",
        {"cid": 1},
    )
    assert result["row_count"] == 2
    print("✔ Fetch tickets by customer")

    # 3. Join customers and tickets
    result = pg.run_query(
        """
        SELECT c.name, t.issue, t.status
        FROM customers c
        JOIN tickets t ON c.id = t.customer_id
        WHERE c.id = 1;
        """
    )
    assert result["row_count"] == 2
    print("✔ Join customers and tickets")

    # 4. Empty result case
    result = pg.run_query(
        "SELECT * FROM tickets WHERE customer_id = 999;"
    )
    assert result["row_count"] == 0
    print("✔ Empty result handled correctly")


def test_vector_tool() -> None:
    """Test Vector Search Tool."""
    print("\n--- Testing Vector Search Tool ---")

    vector = VectorSearchTool()

    # 1. Relevant query
    result = vector.search("How do I reset my password?")
    assert len(result["documents"]) > 0
    print("✔ Password reset query matched")

    # 2. Another relevant query
    result = vector.search("What is your refund policy?")
    assert len(result["documents"]) > 0
    print("✔ Refund policy query matched")

    # 3. Irrelevant query
    result = vector.search("How do airplanes fly?")
    assert len(result["documents"]) == 0
    print("✔ Irrelevant query returns empty")


def test_external_tool() -> None:
    """Test External Mock Tool."""
    print("\n--- Testing External Mock Tool ---")

    external = ExternalMockTool()

    # 1. Weather
    result = external.run("weather", "today")
    assert result is not None
    print("✔ Weather mock response")

    # 2. Crypto
    result = external.run("crypto", "bitcoin")
    assert result is not None
    print("✔ Crypto mock response")

    # 3. Unsupported type
    result = external.run("sports", "football")
    assert result is None
    print("✔ Unsupported query returns empty")


if __name__ == "__main__":
    print("=== PHASE 1 TOOL TESTS START ===")

    test_postgres_tool()
    test_vector_tool()
    test_external_tool()

    print("\n=== ALL PHASE 1 TESTS PASSED ===")
