"""
Postgres Tool

Responsibilities:
- Execute SELECT-only SQL queries
- Return rows and row count
- Never raise on empty results
"""

from typing import Any, Dict, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from config.settings import load_postgres_config


class PostgresTool:
    """
    Tool for executing read-only PostgreSQL queries.
    """

    def __init__(self) -> None:
        config = load_postgres_config()
        self._connection = psycopg2.connect(
            host=config.host,
            port=config.port,
            dbname=config.database,
            user=config.user,
            password=config.password,
        )

    def run_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a SELECT-only SQL query.

        Args:
            query: SQL SELECT query.
            params: Optional named parameters.

        Returns:
            dict with:
                - rows: list of rows (dict)
                - row_count: number of rows
        """
        if not query.strip().lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed.")

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            rows: List[Dict[str, Any]] = cursor.fetchall()

        return {
            "rows": rows,
            "row_count": len(rows),
        }
