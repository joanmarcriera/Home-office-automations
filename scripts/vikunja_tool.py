#!/usr/bin/env python3
"""
Vikunja Tools for Home Admin Agent
Allows the agent to query, create, and update tasks and relations in Vikunja via its REST API.
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
            endpoint = f"{api_url}/tasks"
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            tasks = response.json()
            if not tasks:
                return "No tasks found matching the criteria."

            formatted_tasks = []
            for task in tasks[:10]:
                status = "Done" if task.get("done") else "Pending"
                due = task.get("due_date", "No due date")
                formatted_tasks.append(f"- [{status}] {task.get('title')} (ID: {task.get('id')}, Due: {due})")

            result = "\n".join(formatted_tasks)
            if len(tasks) > 10:
                result += f"\n... and {len(tasks) - 10} more tasks."

            return result

        except requests.exceptions.RequestException as e:
            return f"Error querying Vikunja: {str(e)}"

class VikunjaCreateArgs(BaseModel):
    title: str = Field(..., description="The title of the task.")
    project_id: int = Field(..., description="The ID of the project to create the task in.")
    description: Optional[str] = Field(None, description="The description of the task.")
    due_date: Optional[str] = Field(None, description="The due date of the task (ISO 8601 format).")
    priority: Optional[int] = Field(None, description="Priority level (1: low, 5: high).")

class VikunjaCreateTool(BaseHomeTool):
    """Tool for creating a new task in Vikunja."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="vikunja_create_tool",
            description="Creates a new task in a specified Vikunja project.",
            args_schema=VikunjaCreateArgs,
            category="tasks"
        )

    async def run(self, title: str, project_id: int, description: Optional[str] = None, due_date: Optional[str] = None, priority: Optional[int] = None) -> str:
        api_url = os.environ.get("VIKUNJA_API_URL", "http://localhost:3456/api/v1")
        api_token = os.environ.get("VIKUNJA_API_TOKEN")

        if not api_token:
            return "Error: VIKUNJA_API_TOKEN not set in environment."

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        data = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority
        }
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        try:
            endpoint = f"{api_url}/projects/{project_id}/tasks"
            response = requests.put(endpoint, headers=headers, json=data, timeout=10)
            response.raise_for_status()

            task = response.json()
            return f"Successfully created task '{task.get('title')}' with ID: {task.get('id')} in project {project_id}."

        except requests.exceptions.RequestException as e:
            return f"Error creating Vikunja task: {str(e)}"

class VikunjaUpdateArgs(BaseModel):
    task_id: int = Field(..., description="The ID of the task to update.")
    title: Optional[str] = Field(None, description="The new title of the task.")
    description: Optional[str] = Field(None, description="The new description of the task.")
    due_date: Optional[str] = Field(None, description="The new due date (ISO 8601).")
    done: Optional[bool] = Field(None, description="Whether the task is completed.")
    priority: Optional[int] = Field(None, description="New priority level.")

class VikunjaUpdateTool(BaseHomeTool):
    """Tool for updating an existing task in Vikunja."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="vikunja_update_tool",
            description="Updates an existing Vikunja task's details.",
            args_schema=VikunjaUpdateArgs,
            category="tasks"
        )

    async def run(self, task_id: int, **kwargs) -> str:
        api_url = os.environ.get("VIKUNJA_API_URL", "http://localhost:3456/api/v1")
        api_token = os.environ.get("VIKUNJA_API_TOKEN")

        if not api_token:
            return "Error: VIKUNJA_API_TOKEN not set in environment."

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        # Filter out None values from kwargs
        data = {k: v for k, v in kwargs.items() if v is not None}

        try:
            endpoint = f"{api_url}/tasks/{task_id}"
            response = requests.post(endpoint, headers=headers, json=data, timeout=10)
            response.raise_for_status()

            return f"Successfully updated task ID: {task_id}."

        except requests.exceptions.RequestException as e:
            return f"Error updating Vikunja task: {str(e)}"

class VikunjaRelationArgs(BaseModel):
    task_id: int = Field(..., description="The source task ID.")
    other_task_id: int = Field(..., description="The target task ID.")
    relation_type: str = Field(..., description="Type of relation (subtask, parent, blocking, blocked_by, precedes, follows, related, duplicate_of, duplicates, copied_from, copied_to).")

class VikunjaRelationTool(BaseHomeTool):
    """Tool for creating a relation between two tasks in Vikunja."""

    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="vikunja_relation_tool",
            description="Creates a relation between two Vikunja tasks.",
            args_schema=VikunjaRelationArgs,
            category="tasks"
        )

    async def run(self, task_id: int, other_task_id: int, relation_type: str) -> str:
        api_url = os.environ.get("VIKUNJA_API_URL", "http://localhost:3456/api/v1")
        api_token = os.environ.get("VIKUNJA_API_TOKEN")

        if not api_token:
            return "Error: VIKUNJA_API_TOKEN not set in environment."

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        data = {
            "other_task_id": other_task_id,
            "relation_type": relation_type
        }

        try:
            endpoint = f"{api_url}/tasks/{task_id}/relations"
            response = requests.put(endpoint, headers=headers, json=data, timeout=10)
            response.raise_for_status()

            return f"Successfully created '{relation_type}' relation between task {task_id} and {other_task_id}."

        except requests.exceptions.RequestException as e:
            return f"Error creating Vikunja relation: {str(e)}"

if __name__ == "__main__":
    import asyncio
    async def main():
        print("Vikunja tools loaded.")
    asyncio.run(main())
