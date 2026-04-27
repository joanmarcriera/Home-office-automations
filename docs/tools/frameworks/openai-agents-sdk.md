# OpenAI Agents SDK

## What it is
The OpenAI Agents SDK is a framework designed to build and orchestrate AI agents. It introduces a separation between the "harness" (the control logic) and the "compute" (the LLM reasoning), allowing for more flexible and scalable agent architectures.

## What problem it solves
It simplifies the process of creating agents that can use tools, maintain state, and perform complex multi-step tasks. By separating the harness from the compute, it enables better resource management and sandboxing.

## Where it fits in the stack
**Category**: Framework / Agents

## Typical use cases
- **Multi-step Reasoning**: Agents that need to perform a sequence of actions to reach a goal.
- **Tool-augmented Generation**: Integrating external APIs and tools into the agentic loop.
- **Sandboxed Execution**: Running agent code in isolated environments for security.

## Strengths
- **Decoupled Architecture**: Separates agent logic from LLM execution.
- **Native OpenAI Integration**: Designed to work seamlessly with the OpenAI platform.
- **Scalability**: Easier to manage multiple agents and concurrent tasks.

## Limitations
- **Platform Dependency**: Primarily optimized for OpenAI models.
- **Early Stage**: As a new evolution, ecosystem support and community tools are still maturing.

## When to use it
- Use when building complex agents on the OpenAI platform.
- Use when you need a clear separation between the agent's control logic and its reasoning engine.

## When not to use it
- Not necessary for simple, single-prompt chat interactions.
- If you are fully committed to a different framework like LangGraph or CrewAI.

## Licensing and cost
- **Open Source**: Yes (SDK)
- **Cost**: Free (SDK) / Usage-based (OpenAI API)
- **Self-hostable**: Yes (SDK logic)

## Related tools / concepts
- [Symphony (OpenAI)](../agents/symphony.md)
- [LangGraph](./langgraph.md)
- [Agency Swarm](../agents/agency-swarm.md)
- [Agentic Automation Canvas (AAC)](../agents/agentic-automation-canvas.md)

## Sources / References
- [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk)
- [OpenAI’s Agents SDK separates the harness from the compute](https://thenewstack.io/openai-agents-sdk-sandboxes/)
- [Agents SDK Sandboxes](https://www.zdnet.com/article/openai-agents-sdk-sandboxes/)

## Contribution Metadata
- Last reviewed: 2026-04-16
- Confidence: high
