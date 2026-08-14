# Agent Framework Learning Map

## What it is

The Agent Framework Learning Map is a structured guide designed to help developers and architects navigate the rapidly evolving ecosystem of AI agent frameworks. It categorizes tools into stateful runtimes, lightweight SDKs, role-based frameworks, and specialized components to provide a clear path from conceptual learning to production deployment in early January 2027.

## What problem it solves

The explosion of agentic tools has created a "choice overload" problem where every framework is marketed as a general-purpose solution. This map solves that by differentiating between tools optimized for research, rapid prototyping, autonomous coding, or high-reliability production orchestration. It prevents "framework fatigue" by recommending a specific learning order based on the desired outcome and current industry capabilities.

## Where it fits in the stack

**Category**: Knowledge Base / Learning Path. It sits in the **architectural decision layer**, serving as a meta-framework that informs the selection of specific tools like [LangGraph](../tools/frameworks/langgraph.md), [CrewAI](../tools/frameworks/crewai.md), or [AutoGen](../tools/frameworks/autogen.md).

## Typical use cases

- **Architectural Triage**: Deciding whether a project requires a stateful graph (LangGraph) or a conversational multi-agent system (AutoGen).
- **Skill Upgrading**: Following a curated path to move from basic prompt chains to complex, long-horizon autonomous agents using Claude 5.1 or GPT-5.5.
- **Homelab Automation**: Selecting the right "personal OS" (OpenClaw) and routing layer (LiteLLM) for local-first agent workflows.
- **Enterprise Prototyping**: Quickly identifying role-based frameworks (CrewAI) for demonstrating multi-agent collaboration to stakeholders.

### Quick classification (Early January 2027)

| Tool | Type | Learn from it | Use in production | Best reason to study or adopt |
| :--- | :--- | :---: | :---: | :--- |
| [LangGraph](../tools/frameworks/langgraph.md) | Stateful agent orchestration runtime | Excellent | Excellent | Reliable graph control flow, state, loops, and checkpoints for serious agent engineering. |
| [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md) | Lightweight agent SDK | Excellent | Strong | Minimal agent abstractions around tools, handoffs, sessions, and tracing. |
| [CrewAI](../tools/frameworks/crewai.md) | Role-based multi-agent framework | Good | Moderate | Fast prototyping and clear mental model for role-playing collaborative agents. |
| [AutoGen](../tools/frameworks/autogen.md) | Conversation-driven multi-agent framework | Excellent | Mixed | Influential reference point for agent-to-agent collaboration and research experiments. |
| [OpenHands](../tools/development_ops/openhands.md) | Coding agent platform | Excellent | Emerging | Full software-engineering agent loop with terminal, editor, browser, and verification. |
| [OpenClaw](../tools/development_ops/openclaw.md) | Personal agent operating system / orchestrator | Fascinating | Experimental | Persistent personal agents with tools, skills, memory, sessions, and human override. |
| [Browser Use](../tools/automation_orchestration/browser-use.md) | Browser automation layer for agents | Very useful | Strong | Lets agents operate real websites when APIs are unavailable or incomplete. |
| [GPT Researcher](../tools/agents/gpt-researcher.md) | Deep research agent | Strong niche | Strong niche | Good reference implementation for planning, browsing, synthesis, and report writing. |
| [Letta](../tools/agents/letta.md) | Memory-first agent framework | Important ideas | Emerging | Persistent memory architecture for long-lived agents and personal assistants. |
| [DeerFlow](../tools/agents/deerflow.md) | Multi-agent research and coding harness | Excellent | Emerging | Modern sub-agent, tool-routing, sandbox, and long-horizon workflow patterns. |

## Strengths

- **Outcome-Oriented**: Focuses on what the tool is *best for*, not just what it can do.
- **Classification Clarity**: Separates libraries (SDKs) from environments (Operating Systems) and specialized modules.
- **Local-First Friendly**: Prioritizes stacks that work well with local models and privacy-conscious architectures.
- **Model Agnostic**: Explicitly supports routing between Claude 5.1 (reasoning), GPT-5.5 (speed), and Llama 4 (local).
- **MCP Native**: Emphasizes frameworks that natively support the Model Context Protocol (MCP 3.1) and FastMCP (v3.1) for universal tool access.

## Limitations

- **Fast-Moving Field**: New frameworks emerge weekly, requiring frequent updates to maintain relevance.
- **Subjective "Defaults"**: Recommendations for "production-ready" tools reflect current repository standards and may vary by specific use case.
- **Depth vs Breadth**: Provides a high-level map rather than deep technical tutorials for every individual framework.

## When to use it

- When you are starting a new agentic project and need to choose an architecture.
- When you are overwhelmed by the number of GitHub repos claiming to be "the best" agent framework.
- When you want to understand the difference between an Agent SDK and an Agent Operating System.

## When not to use it

- If you have already standardized on a specific stack and only need deep API documentation.
- If you are building a simple, stateless chatbot that does not require agentic reasoning or tool use.

## Getting started

To begin your journey with agent frameworks, follow this path:

1. **The Hello World of Agents**: Start by reading the [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md) documentation. It provides the simplest abstraction for tool calling and handoffs.
2. **Master the State**: Move to [LangGraph](../tools/frameworks/langgraph.md). Build a simple circular workflow (e.g., a "Correction Loop" where one agent writes and another audits).
3. **Explore Multi-Agent Dynamics**: Deploy a [CrewAI](../tools/frameworks/crewai.md) team of three agents (Researcher, Writer, Editor) to see how role-playing affects output quality.
4. **Autonomous Execution**: Install [Aider](../tools/development_ops/aider.md) or explore the [OpenHands](../tools/development_ops/openhands.md) codebase to see how agents interact with a real terminal and file system.

### Recommended Learning Order (Early January 2027 Update)

#### Fundamentals
1. [LangGraph](../tools/frameworks/langgraph.md) (paired with Claude 5.1 / GPT-5.5 / Gemini 4.0 Pro for reasoning)
2. [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md) (using GPT-5.5 or Gemini 4.0 Flash)
3. [CrewAI](../tools/frameworks/crewai.md)
4. [AutoGen](../tools/frameworks/autogen.md)

#### Coding Agents
1. [OpenHands](../tools/development_ops/openhands.md) (with Claude 5.1 / Aider)
2. [OpenClaw](../tools/development_ops/openclaw.md)

#### Specialized Patterns
1. [Browser Use](../tools/automation_orchestration/browser-use.md)
2. [GPT Researcher](../tools/agents/gpt-researcher.md)
3. [Letta](../tools/agents/letta.md)
4. [DeerFlow](../tools/agents/deerflow.md)

## CLI examples

### Initializing a LangGraph project
Developers often start with a template to ensure state management is correctly configured.
```bash
# Clone the LangGraph starter template
git clone https://github.com/langchain-ai/langgraph-starter.git
cd langgraph-starter
pip install -r requirements.txt
```

### Running an OpenHands session
For autonomous coding tasks, OpenHands provides a CLI to launch the environment.
```bash
# Run OpenHands via Docker for a sandboxed coding environment
docker run -it \
    -e SANDBOX_USER_ID=$(id -u) \
    -e WORKSPACE_BASE=$PWD/workspace \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $PWD/workspace:/opt/workspace \
    ghcr.io/all-hands-ai/openhands:0.15
```

## API examples

### Simple Agent Handoff (OpenAI Agents SDK)
A minimal example showing how to hand off a task between two specialized agents using GPT-5.5.
```python
from openai_agents import Agent, Runner

def get_weather(location: str):
    return f"The weather in {location} is 72°F and sunny."

weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a weather specialist.",
    tools=[get_weather]
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine if the user needs weather info and hand off if so.",
)

# Handing off task from triage to weather
runner = Runner()
response = runner.run(triage_agent, "What is the weather in San Francisco?")
print(response.final_text)
```

### Stateful Graph Logic (LangGraph with Pydantic v2 validation)
Defining a simple cycle where an auditor checks the work of a writer using Claude 5.1, parsing results strictly with Pydantic v2.
```python
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END

class AgentState(BaseModel):
    draft_text: str = Field(..., description="The current text draft.")
    audit_notes: str = Field(default="", description="Auditor feedback notes.")
    status: Literal["draft", "rewrite", "approved"] = Field(default="draft")

def writer(state: Dict[str, Any]) -> Dict[str, Any]:
    # Write draft content
    return {"draft_text": "SOTA 2027 dynamic routing.", "status": "draft"}

def auditor(state: Dict[str, Any]) -> Dict[str, Any]:
    text = state.get("draft_text", "")
    if "2027" in text and len(text) > 10:
        return {"status": "approved", "audit_notes": "Meets SOTA quality standard."}
    return {"status": "rewrite", "audit_notes": "Draft needs year and size corrections."}

workflow = StateGraph(dict)
workflow.add_node("writer", writer)
workflow.add_node("auditor", auditor)

workflow.set_entry_point("writer")
workflow.add_edge("writer", "auditor")
workflow.add_conditional_edges(
    "auditor",
    lambda x: x["status"],
    {"rewrite": "writer", "approved": END}
)

app = workflow.compile()
```

### MCP 3.1 Task Protocol JSON Schema
Standardized MCP 3.1 Task Protocol JSON payload structure for tool calling and task dispatching between agents.
```json
{
  "$schema": "https://modelcontextprotocol.org/schemas/3.1/task-protocol.json",
  "task_id": "task-abc-123",
  "executor": "claude-5.1-sonnet",
  "tool_calls": [
    {
      "name": "fetch_mcp_context",
      "arguments": {
        "repository": "home-automation",
        "query": "LangGraph state preservation"
      }
    }
  ],
  "state_token": "token_session_xyz_789"
}
```

## Related tools / concepts

- [AI Tooling Landscape](ai_tooling_landscape.md)
- [AI Builder Index](ai_builder_index.md)
- [Agent Protocols](agent_protocols.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [OpenClaw Workflow Prompts](patterns/openclaw-workflow-prompts.md)
- [Data Copilot Text-to-SQL Architecture](../architecture/data-copilot-text-to-sql.md)
- [Multi-Agent KnowledgeOps](../architecture/multi_agent_knowledgeops.md)
- [Flows](../architecture/flows.md)
- [Infrastructure](../architecture/infrastructure.md)
- [LiteLLM](../services/litellm.md)
- [Model Context Protocol](agent_protocols.md)

## Sources / References

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/)
- [CrewAI documentation](https://docs.crewai.com/)
- [AutoGen documentation](https://microsoft.github.io/autogen/)
- [OpenHands documentation](https://docs.openhands.dev/)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [Browser Use documentation](https://docs.browser-use.ai/)
- [GPT Researcher GitHub](https://github.com/assafelovic/gpt-researcher)
- [Letta documentation](https://docs.letta.com/)
- [DeerFlow GitHub](https://github.com/bytedance/deer-flow)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.org/spec)

## Contribution Metadata

- Last reviewed: 2027-01-04
- Confidence: high
