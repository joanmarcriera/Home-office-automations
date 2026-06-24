# Agentic Workflows

## What it is
Agentic workflows are design patterns where Large Language Models (LLMs) are not just used for single-turn responses, but are part of a multi-step, iterative process where they can reason, use tools, and make decisions to achieve a goal.

## What problem it solves
It enables the automation of complex tasks that require more than a single LLM call, such as multi-step research, software development, or sophisticated data analysis, by allowing the model to "think" and act over several turns.

## Where it fits in the stack
It is the **Orchestration and Reasoning Layer** of the AI stack. It sits above the **Intelligence Layer** (individual models) and integrates with the **Tool/Action Layer** (APIs and services) to complete end-to-end tasks.

## Core concepts
- **Planning**: The agent breaks down a complex goal into smaller, manageable steps.
- **Tool Use**: The agent can interact with external systems (APIs, databases, web browsers) to gather information or perform actions.
- **Reflection**: The agent evaluates its own performance or output and makes adjustments to its plan or behavior.
- **Multi-agent Collaboration**: Multiple specialized agents work together, each handling a part of the overall workflow.

## Typical use cases
- **Autonomous Coding Assistants**: Agents that can write, test, and debug code (e.g., [Claude Code](../../tools/development_ops/claude-code.md), [Aider](../../tools/development_ops/aider.md)).
- **Complex Research Tasks**: Agents that can search the web using [Tavily](../../tools/providers/tavily.md), synthesize information with [Claude 4.7](../../tools/ai_knowledge/claude.md), and write reports.
- **Personal Assistants**: Agents that can manage calendars, book flights, and handle emails using [GPT-5.5](../../tools/ai_knowledge/openai.md) and [Llama 4 Maverick](../../tools/ai_knowledge/meta_llama.md).

## Strengths
- **Handles Complexity**: Can solve problems that are too difficult for a single LLM prompt.
- **Greater Autonomy**: Reduces the need for constant human intervention in complex tasks.
- **Improved Performance**: Iterative reasoning and reflection can lead to higher-quality results.

## Limitations
- **Reliability Issues**: Agents can sometimes get stuck in loops or make poor decisions over multiple turns.
- **Cost and Latency**: Multi-turn workflows consume more tokens and take longer to complete.
- **Security Risks**: Giving agents the ability to use tools requires careful management of permissions and trust boundaries.

## When to use it
- When a task requires multiple steps, tool use, or iterative refinement.
- When you want to automate a complex process that previously required significant human oversight.

## When not to use it
- For simple, straightforward tasks where a single LLM call is sufficient.
- When high speed and low cost are the primary requirements.

## Related tools / concepts
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md)
- [Tool Calling & MCP](tool-calling-and-mcp.md)
- [CrewAI](../../tools/frameworks/crewai.md)
- [Home Admin Agent Architecture](../home-admin-agent-architecture.md)
- [Model Routing Guide](../model_routing_guide.md)
- [System Prompts](../system_prompts.md)
- [LangGraph](../../tools/frameworks/langgraph.md)
- [AutoGPT](../../tools/agents/autogpt.md)

## Sources / References
- [Anthropic: Agentic Workflows](https://www.anthropic.com/news/agentic-workflows)
- [Andrew Ng: Agentic Design Patterns](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/)

## Contribution Metadata
- Last reviewed: 2026-06-07
- Confidence: high
