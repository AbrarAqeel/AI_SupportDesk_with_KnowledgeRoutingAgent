"""
External Mock Tool

Responsibilities:
- Return predefined responses
- No real API calls
"""

from typing import Dict, Optional


class ExternalMockTool:
    """
    Simulates external APIs like weather or crypto.
    """

    def run(self, tool_type: str, query: str) -> Optional[Dict[str, str]]:
        """
        Execute mock external request.

        Args:
            tool_type: 'weather' or 'crypto'
            query: User query

        Returns:
            dict with result and source, or None if unsupported
        """
        tool_type = tool_type.lower()

        if tool_type == "weather":
            return {
                "result": "The weather today is sunny with a temperature of 25°C.",
                "source": "mock",
            }

        if tool_type == "crypto":
            return {
                "result": "Bitcoin price is $30,000.",
                "source": "mock",
            }

        return None
