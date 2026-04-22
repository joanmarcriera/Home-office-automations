#!/usr/bin/env python3
"""
Home Admin Agent - AgentExecutor
Implements a Plan-and-Execute orchestration loop using LangGraph.
"""

import os
import sys
import json
from typing import Annotated, List, Dict, Type, Any, TypedDict, Optional, Union
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import add_messages
    from agent_memory import MemoryManager
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("Warning: langgraph or agent_memory not available.")

# --- Tool Registry and Base Class ---

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

class ToolRegistry:
    """Registry for dynamic tool discovery."""
    def __init__(self):
        self._tools: Dict[str, Any] = {}

    def register(self, tool_instance: Any):
        metadata = tool_instance.get_metadata()
        self._tools[metadata.name] = tool_instance

    def get_tool(self, name: str) -> Any:
        return self._tools.get(name)

    def list_tools(self) -> List[ToolMetadata]:
        return [t.get_metadata() for t in self._tools.values()]

# --- Dummy Test Tool ---

class TestToolArgs(BaseModel):
    query: str = Field(description="The query to echo back.")

class TestTool(BaseHomeTool):
    @classmethod
    def get_metadata(cls) -> ToolMetadata:
        return ToolMetadata(
            name="test_tool",
            description="A simple tool for testing the agent executor. Echoes the input query.",
            args_schema=TestToolArgs,
            category="testing"
        )

    async def run(self, query: str) -> str:
        return f"Tool Response: {query}"

# --- Agent State ---

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

# --- Agent Executor ---

class HomeAdminAgent:
    def __init__(self, db_path: str = "agent_memory.db"):
        self.registry = ToolRegistry()
        self.registry.register(TestTool())
        self.memory_manager = MemoryManager(db_path)

    def _build_workflow(self, saver):
        builder = StateGraph(AgentState)

        # 1. Planner: Breaks down the user request into a plan
        async def planner_node(state: AgentState):
            print("--- NODE: PLANNER ---")
            messages = state["messages"]
            last_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])

            # Simple simulation: if "test" is in message, plan a test tool call
            if "test" in last_message.lower():
                plan = ["Call test_tool with query='Hello from planner'"]
            else:
                plan = ["Respond directly to user"]

            return {"plan": plan, "results": []}

        # 2. Executor: Executes the steps in the plan
        async def executor_node(state: AgentState):
            print("--- NODE: EXECUTOR ---")
            plan = state.get("plan", [])
            results = []

            for step in plan:
                if "Call test_tool" in step:
                    tool = self.registry.get_tool("test_tool")
                    if tool:
                        result = await tool.run(query="Automated execution")
                        results.append(result)
                elif "Respond directly" in step:
                    results.append("No tools needed.")

            return {"results": results}

        # 3. Replanner: Decides if the task is done or needs more steps
        async def replanner_node(state: AgentState):
            print("--- NODE: REPLANNER ---")
            results = state.get("results", [])

            if results:
                # Task considered done in this simplified loop
                final_response = f"I've completed the task. Results: {', '.join(results)}"
                return {"final_response": final_response, "plan": []}

            return {"plan": []}

        builder.add_node("planner", planner_node)
        builder.add_node("executor", executor_node)
        builder.add_node("replanner", replanner_node)

        builder.set_entry_point("planner")
        builder.add_edge("planner", "executor")
        builder.add_edge("executor", "replanner")
        builder.add_edge("replanner", END)

        return builder.compile(checkpointer=saver)

    async def run(self, input_text: str, thread_id: str = "default"):
        if not LANGGRAPH_AVAILABLE:
            print("LangGraph not available.")
            return None

        async with self.memory_manager.get_async_checkpointer() as saver:
            workflow = self._build_workflow(saver)

            config = {"configurable": {"thread_id": thread_id}}
            inputs = {
                "messages": [("user", input_text)],
                "plan": [],
                "results": [],
                "context": {},
                "final_response": None
            }

            print(f"Running agent for thread: {thread_id}")
            async for event in workflow.astream(inputs, config=config):
                for node, output in event.items():
                    print(f"[{node}]: {output}")

            # Get final state
            final_state = await workflow.aget_state(config)
            return final_state.values.get("final_response")

if __name__ == "__main__":
    import asyncio

    async def main():
        agent = HomeAdminAgent()
        print("Home Admin Agent initialized.")
        print("Available tools:", [t.name for t in agent.registry.list_tools()])

        response = await agent.run("Please run a test for me.")
        print(f"\nFinal Agent Response: {response}")

    asyncio.run(main())
