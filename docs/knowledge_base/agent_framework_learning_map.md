# Agent Framework Learning Map

## What it is
The Agent Framework Learning Map is a structured guide designed to help developers and architects navigate the rapidly evolving ecosystem of AI agent frameworks. It categorizes tools into stateful runtimes, lightweight SDKs, role-based frameworks, and specialized components to provide a clear path from conceptual learning to production deployment.

## What problem it solves
The explosion of agentic tools has created a "choice overload" problem where every framework is marketed as a general-purpose solution. This map solves that by differentiating between tools optimized for research, rapid prototyping, autonomous coding, or high-reliability production orchestration. It prevents "framework fatigue" by recommending a specific learning order based on the desired outcome.

## Where it fits in the stack
**Category**: Knowledge Base / Learning Path. It sits in the **architectural decision layer**, serving as a meta-framework that informs the selection of specific tools like [LangGraph](../tools/frameworks/langgraph.md), [CrewAI](../tools/frameworks/crewai.md), or [AutoGen](../tools/frameworks/autogen.md).

## Typical use cases
- **Architectural Triage**: Deciding whether a project requires a stateful graph (LangGraph) or a conversational multi-agent system (AutoGen).
- **Skill Upgrading**: Following a curated path to move from basic prompt chains to complex, long-horizon autonomous agents using Claude 4.8.
- **Homelab Automation**: Selecting the right "personal OS" (OpenClaw) and routing layer (LiteLLM) for local-first agent workflows.
- **Enterprise Prototyping**: Quickly identifying role-based frameworks (CrewAI) for demonstrating multi-agent collaboration to stakeholders.

## Strengths
- **Outcome-Oriented**: Focuses on what the tool is *best for*, not just what it can do.
- **Classification Clarity**: Separates libraries (SDKs) from environments (Operating Systems) and specialized modules.
- **Local-First Friendly**: Prioritizes stacks that work well with local models and privacy-conscious architectures.
- **Model Agnostic**: Explicitly supports routing between Claude 4.8 (reasoning), GPT-5.5 (speed), and Llama 4 Maverick (local).

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

### Quick classification

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

## CLI examples
Working with agent frameworks often starts with initialization or CLI-based interaction.

```bash
# Initialize a LangGraph project using the LangChain CLI
langchain app new my-agent --template langgraph

# Start an OpenHands development session
docker run -it --pull always \
    -e SANDBOX_USER_ID=$(id -u) \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $(pwd)/workspace:/opt/workspace \
    ghcr.io/all-hands-ai/openhands:0.12

# Run an Aider session with Claude 4.8
aider --model anthropic/claude-3-5-sonnet-20241022  # Update to 4.8 alias when available
```

## API examples
Integration examples for common frameworks.

```python
# OpenAI Agents SDK (June 2026 pattern)
from openai_agents import Agent, Runner

agent = Agent(
    name="Researcher",
    instructions="Find the latest trends in Agentic AI.",
    tools=[search_tool]
)

# Handoff pattern
agent.add_handoff(target="Writer")

# LangGraph stateful graph
from langgraph.graph import StateGraph

builder = StateGraph(MyState)
builder.add_node("research", research_node)
builder.add_node("write", write_node)
builder.set_entry_point("research")
builder.add_edge("research", "write")
graph = builder.compile()
```

## Related tools / concepts
- [LangGraph](../tools/frameworks/langgraph.md)
- [CrewAI](../tools/frameworks/crewai.md)
- [AutoGen](../tools/frameworks/autogen.md)
- [OpenHands](../tools/development_ops/openhands.md)
- [OpenClaw](../tools/development_ops/openclaw.md)
- [LiteLLM](../services/litellm.md)
- [Model Context Protocol](agent_protocols.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [AI Tooling Landscape](ai_tooling_landscape.md)
- [Browser Use](../tools/automation_orchestration/browser-use.md)

### Recommended Learning Order (June 2026 Update)

**Fundamentals**
1. [LangGraph](../tools/frameworks/langgraph.md) (paired with Claude 4.8 for reasoning)
2. [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md) (using GPT-5.5)
3. [CrewAI](../tools/frameworks/crewai.md)
4. [AutoGen](../tools/frameworks/autogen.md)

**Coding Agents**
1. [OpenHands](../tools/development_ops/openhands.md) (with Claude 4.8 / Aider)
2. [OpenClaw](../tools/development_ops/openclaw.md)

**Specialised Patterns**
1. [Browser Use](../tools/automation_orchestration/browser-use.md)
2. [GPT Researcher](../tools/agents/gpt-researcher.md)
3. [Letta](../tools/agents/letta.md)
4. [DeerFlow](../tools/agents/deerflow.md)

### Narrow Stack For OpenClaw-Style Local Orchestration

| Layer | Recommended tool | Why |
| :--- | :--- | :--- |
| Personal agent runtime | [OpenClaw](../tools/development_ops/openclaw.md) | Channel adapters, skills, memory, sessions, and scheduled workflows. |
| Durable agent control flow | [LangGraph](../tools/frameworks/langgraph.md) | Explicit state and graph execution when workflows outgrow prompt chains. |
| Browser capability | [Browser Use](../tools/automation_orchestration/browser-use.md) | Structured browser control for web tasks without stable APIs. |
| Research workflow | [GPT Researcher](../tools/agents/gpt-researcher.md) | Planning, browsing, and synthesis pattern to reuse or adapt. |
| Tool protocol | [Model Context Protocol](agent_protocols.md) | Common connector layer for tools and data access. |
| Automation shell | [n8n](../services/n8n.md) | Human-visible workflow gates, approvals, retries, and integrations. |
| Model routing | [LiteLLM](../services/litellm.md) | OpenAI-compatible routing across local and hosted models. |

### Practical Adoption Notes
- **Model Selection**: Claude 4.8 is preferred for complex architectural planning and LangGraph orchestration, while GPT-5.5 excels at high-throughput tool calling.
- Do not choose by popularity alone. Choose by workflow shape: coding, research, browser operation, personal assistant, or production application runtime.
- Treat "good to study" and "good to run" as different decisions. AutoGen and OpenClaw are valuable to study even when LangGraph or OpenAI Agents SDK is the safer production default.
- Keep specialised tools composable. Browser Use, GPT Researcher, and Letta are often better as components in a broader system than as the whole architecture.

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

## Contribution Metadata
- Last reviewed: 2026-06-25
- Confidence: high
