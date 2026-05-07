# Agent Framework Learning Map

This page turns a mixed list of agent frameworks, agent products, and specialised agents into a practical learning and adoption map. It is meant to avoid treating every agent project as interchangeable: some are best studied for architecture, some are practical production components, and some are niche tools to compose into a larger stack.

## Quick classification

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

## Frameworks

Use this bucket when the goal is to build custom agent workflows in code.

- [LangGraph](../tools/frameworks/langgraph.md) is the best default to study first when reliability matters. Its graph model makes state, loops, and checkpoints explicit enough for production agent engineering.
- [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md) is the cleanest small surface for teams that want tools, handoffs, sessions, and tracing without adopting a heavy framework.
- [CrewAI](../tools/frameworks/crewai.md) is useful for learning role-based collaboration quickly, especially for business-process prototypes.
- [AutoGen](../tools/frameworks/autogen.md) remains important for research and design literacy around conversational multi-agent systems, but production use needs discipline around complexity and observability.

## Agent Products And Operating Environments

Use this bucket when the goal is to run a full agent environment, not just import a library.

- [OpenHands](../tools/development_ops/openhands.md) is the strongest reference for autonomous software engineering loops because it combines planning, editing, command execution, browser use, and verification.
- [OpenClaw](../tools/development_ops/openclaw.md) is the most relevant experimental operating system for personal agents, especially where messaging channels, skills, memory, and scheduled tasks matter.
- [DeerFlow](../tools/agents/deerflow.md) is a useful modern harness to study for coordinated research/coding flows with sub-agents and tool routing.

## Specialised Agents And Components

Use this bucket when the tool solves one important slice of a larger workflow.

- [Browser Use](../tools/automation_orchestration/browser-use.md) should be treated as a browser capability layer. Prefer APIs first, then use browser automation for websites that do not expose reliable machine interfaces.
- [GPT Researcher](../tools/agents/gpt-researcher.md) is strongest as a research and report-generation reference implementation.
- [Letta](../tools/agents/letta.md) is worth studying when the hard problem is persistent memory, not simply tool calling.

## Recommended Learning Order

### Fundamentals

1. [LangGraph](../tools/frameworks/langgraph.md)
2. [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md)
3. [CrewAI](../tools/frameworks/crewai.md)
4. [AutoGen](../tools/frameworks/autogen.md)

### Coding Agents

1. [OpenHands](../tools/development_ops/openhands.md)
2. [OpenClaw](../tools/development_ops/openclaw.md)

### Specialised Patterns

1. [Browser Use](../tools/automation_orchestration/browser-use.md)
2. [GPT Researcher](../tools/agents/gpt-researcher.md)
3. [Letta](../tools/agents/letta.md)
4. [DeerFlow](../tools/agents/deerflow.md)

## Narrow Stack For OpenClaw-Style Local Orchestration

For a low-cost, local-model-friendly agent stack with GitHub Actions and personal workflow automation, prioritise:

| Layer | Recommended tool | Why |
| :--- | :--- | :--- |
| Personal agent runtime | [OpenClaw](../tools/development_ops/openclaw.md) | Channel adapters, skills, memory, sessions, and scheduled workflows. |
| Durable agent control flow | [LangGraph](../tools/frameworks/langgraph.md) | Explicit state and graph execution when workflows outgrow prompt chains. |
| Browser capability | [Browser Use](../tools/automation_orchestration/browser-use.md) | Structured browser control for web tasks without stable APIs. |
| Research workflow | [GPT Researcher](../tools/agents/gpt-researcher.md) | Planning, browsing, and synthesis pattern to reuse or adapt. |
| Tool protocol | [Model Context Protocol](agent_protocols.md) | Common connector layer for tools and data access. |
| Automation shell | [n8n](../services/n8n.md) | Human-visible workflow gates, approvals, retries, and integrations. |
| Model routing | [LiteLLM](../services/litellm.md) | OpenAI-compatible routing across local and hosted models. |

## Practical Adoption Notes

- Do not choose by popularity alone. Choose by workflow shape: coding, research, browser operation, personal assistant, or production application runtime.
- Treat "good to study" and "good to run" as different decisions. AutoGen and OpenClaw are valuable to study even when LangGraph or OpenAI Agents SDK is the safer production default.
- Keep specialised tools composable. Browser Use, GPT Researcher, and Letta are often better as components in a broader system than as the whole architecture.
- Use [Model Context Protocol](agent_protocols.md) and [LiteLLM](../services/litellm.md) as stabilising layers when combining local models, cloud models, and tool access.

## Related tools / concepts

- [AI Tooling Landscape](ai_tooling_landscape.md)
- [AI Builder Index](ai_builder_index.md)
- [Agent Protocols](agent_protocols.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [OpenClaw Workflow Prompts](patterns/openclaw-workflow-prompts.md)

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

- Last reviewed: 2026-05-06
- Confidence: medium
