#!/usr/bin/env python3
"""
Vikunja Query Tool for Home Admin Agent
Allows the agent to query tasks from Vikunja via its REST API.
"""

import os
import requests
from typing import List, Optional, Dict, Any, Type
from pydantic import BaseModel, Field
from agent_models import BaseHomeTool, ToolMetadata

class VikunjaQueryArgs(BaseModel):
    project_id: Optional[int] = Field(None, description="Filter tasks by project ID.")
    filter_query: Optional[str] = Field(None, description="A filter query string for Vikunja (e.g., 'done = false').")
    search: Optional[str] = Field(None, description="Search term for task titles.")

class VikunjaQueryTool(BaseHomeTool):
    """Tool for querying tasks from Vikunja."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="vikunja_query_tool",
            description="Queries tasks from Vikunja. Can filter by project, search term, or custom filter string.",
            args_schema=VikunjaQueryArgs,
            category="tasks"
        )

    async def run(self, project_id: Optional[int] = None, filter_query: Optional[str] = None, search: Optional[str] = None) -> str:
        # Fetch configuration from environment variables
        api_url = os.environ.get("VIKUNJA_API_URL", "http://localhost:3456/api/v1")
        api_token = os.environ.get("VIKUNJA_API_TOKEN")

        if not api_token:
            return "Error: VIKUNJA_API_TOKEN not set in environment."

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        params = {}
        if project_id:
            params["project"] = project_id
        if filter_query:
            params["filter"] = filter_query
        if search:
            params["s"] = search

        try:
            # Note: Using requests.get synchronously for simplicity in this reference implementation.
            # In a production async environment, httpx would be preferred.
            endpoint = f"{api_url}/tasks"
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            tasks = response.json()
            if not tasks:
                return "No tasks found matching the criteria."

            # Format the output for the agent
            formatted_tasks = []
            for task in tasks[:10]:  # Limit to 10 tasks for brevity
                status = "Done" if task.get("done") else "Pending"
                due = task.get("due_date", "No due date")
                formatted_tasks.append(f"- [{status}] {task.get('title')} (ID: {task.get('id')}, Due: {due})")

            result = "\n".join(formatted_tasks)
            if len(tasks) > 10:
                result += f"\n... and {len(tasks) - 10} more tasks."

            return result

        except requests.exceptions.RequestException as e:
            return f"Error querying Vikunja: {str(e)}"

if __name__ == "__main__":
    import asyncio
    import sys

    # Mock environment for testing if needed
    # os.environ["VIKUNJA_API_TOKEN"] = "test_token"

    async def main():
        tool = VikunjaQueryTool()
        print(f"Tool: {tool.get_metadata().name}")
        # result = await tool.run(search="test")
        # print(result)

    asyncio.run(main())
