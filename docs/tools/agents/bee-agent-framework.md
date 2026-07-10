# Bee Agent Framework

## What it is
The Bee Agent Framework (v1.x+, July 2026) is an open-source framework by IBM Research for building, deploying, and orchestrating production-grade AI agents. It provides complete feature parity between TypeScript and Python, allowing for robust multi-agent systems with native Model Context Protocol (MCP 3.0) and the **MCP 3.0 Task Protocol** support.

## What problem it solves
It focuses on the "Reliability Gap" in autonomous agents. By providing "Requirement Agents" that enforce runtime policies and "Observability-by-Design" via detailed execution traces, Bee ensures that complex multi-step agentic workflows using models like [Gemma 3](../ai_knowledge/local_llms.md) or [Claude 4.8](../ai_knowledge/claude.md) remain predictable, auditable, and production-ready.

## Where it fits in the stack
**Category**: Agent Orchestration Framework. It sits between the Model/Inference layer (supporting 10+ providers like Watsonx, Ollama, and OpenAI) and the Tool/Infrastructure layer, managing state, memory, and tool execution.

## Typical use cases
- **Enterprise Automation**: Workflows requiring strict governance, policy enforcement, and audit trails.
- **Multi-Agent Orchestration**: Systems where specialized agents (Planner, Executor, Reviewer) must collaborate on complex tasks.
- **Cross-Platform Development**: Projects that require shared agent logic between TypeScript (web/frontend) and Python (data/backend) environments.
- **Hybrid Cloud Agents**: Deploying agents that bridge local Ollama models with enterprise Watsonx.ai instances.

## Strengths
- **Reliability**: Built-in safeguards and policy enforcement agents to minimize agent drift and failure.
- **Observability**: Industry-leading execution tracing and OpenTelemetry integration.
- **Language Parity**: Simultaneous support for TypeScript and Python with identical architectural patterns.
- **Protocol Native**: Full, first-class support for MCP 3.0, enabling seamless tool and context integration.
- **Governance**: Hosted by the Linux Foundation under open governance for long-term stability.

## Limitations
- **Learning Curve**: The focus on enterprise reliability introduces more abstractions (Workflows, Templates, Providers) than minimal frameworks like Agno.
- **Overhead**: The comprehensive feature set may introduce more latency and resource usage than lightweight alternatives for simple tasks.
- **Maturity**: While robust, the ecosystem of community-contributed tools is still growing compared to LangChain.

## When to use it
- **Production AI Systems**: When you need a framework designed for scale, security, and enterprise-grade reliability.
- **Deep Observability Requirements**: If your use case requires detailed tracing to debug or audit complex agent decisions.
- **Multi-Language Teams**: When your organization utilizes both TS and Python and wants a unified agent architecture.
- **Linux Foundation Alignment**: If your project requires an open-governance framework with no vendor lock-in.

## When not to use it
- **Rapid Prototyping**: For simple, one-off scripts, lightweight SDKs like LiteLLM or raw provider APIs are faster.
- **Minimal Resource Environments**: If running on extremely constrained hardware where framework overhead must be minimized.
- **Single-Agent Chatbots**: For basic conversational UI without complex tool use or state management, Bee might be overkill.

## Getting started

### Installation
=== "TypeScript"
    ```bash
    npm install beeai-framework
    ```
=== "Python"
    ```bash
    pip install beeai-framework
    ```

### Basic Agent Setup
Initialize a Bee agent with a provider (e.g., Watsonx or OpenAI) and a set of tools.

## CLI examples
```bash
# Initialize a new Bee project template
beeai init my-enterprise-agent

# Start the Bee development server with live-reloading
beeai dev --port 18788

# Validate MCP server connectivity
beeai mcp verify http://localhost:18790
```

## API examples
=== "TypeScript"
    ```typescript
    import { BeeAgent } from "beeai-framework/agents/bee/agent";
    import { UnstructuredRawModel } from "beeai-framework/backend/unstructured";
    import { DuckDuckGoSearchTool } from "beeai-framework/tools/search/duckduckgo";

    async function main() {
        const agent = new BeeAgent({
            llm: new UnstructuredRawModel({ modelId: "gpt-4o" }),
            tools: [new DuckDuckGoSearchTool()],
            memory: []
        });

        const response = await agent.run({ prompt: "Synthesize a report on BeeAI framework updates." });
        console.log(response.result.text);
    }
    main();
    ```
=== "Python"
    ```python
    from beeai_framework.agents.bee.agent import BeeAgent
    from beeai_framework.backend.chat import ChatModel
    from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool

    agent = BeeAgent(
        llm=ChatModel.from_name("openai:gpt-4o"),
        tools=[DuckDuckGoSearchTool()],
        memory=[]
    )

    response = agent.run(prompt="Analyze the benefits of multi-language agent frameworks.")
    print(response.result.text)
    ```

## Related tools / concepts
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md)
- [MCP 3.0](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [LangGraph](../frameworks/langgraph.md)
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [Phidata](phidata.md)
- [Superpowers](superpowers.md)
- [Agno](agno.md)
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Claude 4.8](../ai_knowledge/claude.md)

## Sources / references
- [BeeAI Framework GitHub Repository](https://github.com/i-am-bee/beeai-framework)
- [Official BeeAI Documentation](https://i-am-bee.github.io/beeai-framework/)
- [IBM Research: AI Agent Reliability with BeeAI](https://research.ibm.com/blog/ai-agent-reliability-beeai)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
