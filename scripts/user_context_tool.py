#!/usr/bin/env python3
"""
User Context Fetcher Tool
Provides the Home Admin Agent with user-specific context such as preferences,
schedules, and roles.
"""

import os
import sys
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from home_admin_agent import BaseHomeTool, ToolMetadata
except ImportError:
    # Fallback/mock for standalone testing
    class ToolMetadata(BaseModel):
        name: str
        description: str
        args_schema: Any
        category: str

    class BaseHomeTool:
        pass

class UserContextArgs(BaseModel):
    user_id: str = Field(description="The unique identifier for the family member (e.g., 'husband', 'wife').")

class UserContextFetcher(BaseHomeTool):
    """
    Tool to fetch user-specific context to personalize agent responses.
    In a real implementation, this would query a database or contact service.
    """

    # Mock database of family context
    MOCK_CONTEXT = {
        "husband": {
            "name": "John",
            "role": "Father",
            "preferences": {
                "communication": "Concise, prefers Telegram for alerts.",
                "interests": ["Smart Home", "Gardening", "Tech News"]
            },
            "recent_context": "Has a big presentation tomorrow morning."
        },
        "wife": {
            "name": "Jane",
            "role": "Mother",
            "preferences": {
                "communication": "Detailed, prefers Email for long summaries.",
                "interests": ["Cooking", "Family History", "Reading"]
            },
            "recent_context": "Planning a weekend trip for the family."
        }
    }

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="user_context_fetcher",
            description="Retrieves user-specific preferences, roles, and recent context to personalize assistance.",
            args_schema=UserContextArgs,
            category="knowledge"
        )

    async def run(self, user_id: str) -> str:
        """Fetch and return context for the specified user."""
        context = self.MOCK_CONTEXT.get(user_id.lower())
        if not context:
            return f"No specific context found for user '{user_id}'."

        return json.dumps(context, indent=2)

if __name__ == "__main__":
    import asyncio

    async def main():
        fetcher = UserContextFetcher()
        print("--- Testing UserContextFetcher ---")

        print("\n[Husband Context]")
        res = await fetcher.run(user_id="husband")
        print(res)

        print("\n[Wife Context]")
        res = await fetcher.run(user_id="wife")
        print(res)

        print("\n[Unknown User]")
        res = await fetcher.run(user_id="guest")
        print(res)

    asyncio.run(main())
