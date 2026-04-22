#!/usr/bin/env python3
"""
Base models and classes for the Home Admin Agent.
"""

from typing import Annotated, List, Dict, Type, Any, TypedDict, Optional, Union
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

try:
    from langgraph.graph.message import add_messages
except ImportError:
    # Fallback for environments without langgraph
    def add_messages(left, right):
        return left + right

class ToolMetadata(BaseModel):
    name: str
    description: str
    args_schema: Type[BaseModel]
    category: str  # e.g., 'knowledge', 'automation', 'tasks'

class BaseHomeTool(ABC):
    @classmethod
    @abstractmethod
    def get_metadata(cls) -> ToolMetadata:
        pass

    @abstractmethod
    async def run(self, **kwargs) -> str:
        """Execute the tool's primary logic."""
        pass

class AgentState(TypedDict):
    # Messages in the conversation
    messages: Annotated[List[Any], add_messages]
    # The current plan (sequence of steps)
    plan: List[str]
    # Results from executed steps
    results: List[str]
    # Shared context across tools
    context: Dict[str, Any]
    # Final response to user
    final_response: Optional[str]
