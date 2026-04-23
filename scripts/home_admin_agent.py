#!/usr/bin/env python3
"""
Home Admin Agent - AgentExecutor
Implements a Plan-and-Execute orchestration loop using LangGraph.
"""

import os
import sys
import json
from typing import List, Dict, Type, Any, Optional, Union
from pydantic import BaseModel, Field

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_models import BaseHomeTool, ToolMetadata, AgentState

try:
    from langgraph.graph import StateGraph, END
    from agent_memory import MemoryManager
    from family_value_tone import FamilyValueTone
    from vikunja_tool import VikunjaQueryTool, VikunjaCreateTool, VikunjaUpdateTool, VikunjaRelationTool
    from home_assistant_tool import HAStateQueryTool, HASceneTriggerTool, HALightControlTool
    from paperless_tool import PaperlessSearchTool
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("Warning: langgraph or dependencies not available.")

# --- Tool Registry ---

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

# --- Agent Executor ---

class HomeAdminAgent:
    def __init__(self, db_path: str = "agent_memory.db"):
        self.registry = ToolRegistry()
        self.registry.register(TestTool())
        if LANGGRAPH_AVAILABLE:
            self.registry.register(VikunjaQueryTool())
            self.registry.register(VikunjaCreateTool())
            self.registry.register(VikunjaUpdateTool())
            self.registry.register(VikunjaRelationTool())
            self.registry.register(HAStateQueryTool())
            self.registry.register(HASceneTriggerTool())
            self.registry.register(HALightControlTool())
            self.registry.register(PaperlessSearchTool())
        self.memory_manager = MemoryManager(db_path)
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """Loads the system prompt from the reference file or uses the default tone utility."""
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "docs", "reference-implementations", "llm-prompts", "family-context.md")
        try:
            if os.path.exists(prompt_path):
                with open(prompt_path, "r") as f:
                    content = f.read()
                    # Extract the markdown block if present
                    import re
                    match = re.search(r"```markdown\n(.*?)\n```", content, re.DOTALL)
                    if match:
                        return match.group(1)
            if 'FamilyValueTone' in globals():
                return FamilyValueTone.get_system_prompt()
            return "You are Ralph, the Home Admin Agent."
        except Exception as e:
            print(f"Error loading system prompt: {e}")
            if 'FamilyValueTone' in globals():
                return FamilyValueTone.get_system_prompt()
            return "You are Ralph, the Home Admin Agent."

    def _get_populated_system_prompt(self, context: Dict[str, Any]) -> str:
        """Populates the system prompt with dynamic context."""
        from datetime import datetime, timezone

        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        calendar_summary = context.get("calendar_summary", "No calendar data available.")
        task_summary = context.get("task_summary", "No task data available.")

        prompt = self.system_prompt
        prompt = prompt.replace("{{ current_date }}", current_date)
        prompt = prompt.replace("{{ calendar_summary }}", calendar_summary)
        prompt = prompt.replace("{{ task_summary }}", task_summary)

        return prompt

    def _build_workflow(self, saver):
        builder = StateGraph(AgentState)

        # 1. Planner: Breaks down the user request into a plan
        async def planner_node(state: AgentState):
            print("--- NODE: PLANNER ---")
            messages = state["messages"]
            context = state.get("context", {})

            # Populate system prompt with current context
            system_prompt = self._get_populated_system_prompt(context)
            print(f"DEBUG: System Prompt populated (length: {len(system_prompt)})")

            # In a real implementation, we would pass 'system_prompt'
            # and 'messages' to an LLM here.
            full_context_messages = [("system", system_prompt)] + messages

            last_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])

            # Simple simulation: if "test" is in message, plan a test tool call
            if "test" in last_message.lower():
                plan = ["Call test_tool with query='Hello from planner'"]
            elif "task" in last_message.lower() or "vikunja" in last_message.lower():
                plan = ["Call vikunja_query_tool with search='test'"]
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
                elif "Call vikunja_query_tool" in step:
                    tool = self.registry.get_tool("vikunja_query_tool")
                    if tool:
                        result = await tool.run(search="test")
                        results.append(result)
                elif "Call paperless_search_tool" in step:
                    tool = self.registry.get_tool("paperless_search_tool")
                    if tool:
                        result = await tool.run(query="test")
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
