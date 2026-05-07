# Bee Agent Framework

## What it is
The Bee Agent Framework is an open-source framework by IBM for building, deploying, and orchestrating AI agents. It supports both TypeScript and Python and is designed for production-ready, reliable agentic workflows.

## What problem it solves
It focuses on agent reliability and observability. It provides "Requirement Agents" that can enforce specific rules during execution, and detailed execution traces to help debug complex agent behaviors.

## Where it fits in the stack
[Framework / Agent / Orchestration] - A robust framework for enterprise-grade autonomous agents.

## Typical use cases
- Enterprise automation requiring strict governance and reliability
- Multi-agent systems with complex planning and execution steps
- Cross-language projects (TS/Python)

## When to use it
- **Enterprise-Grade Agents**: When you need a framework designed for scale, security, and production-readiness.
- **Observability Requirements**: If you need detailed execution traces and logs to debug complex agent behaviors.
- **Policy Enforcement**: When you need to use "Requirement Agents" to enforce rules during execution.
- **Hybrid Teams**: When working in environments that use both TypeScript and Python.

## When not to use it
- **Simple Prototyping**: For quick, one-off scripts, simpler frameworks like raw OpenAI SDK or LiteLLM might be faster.
- **Minimal Resource Environments**: The framework's comprehensive features may introduce more overhead than needed for simple tasks.

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

### Basic Usage
Initialize an agent with a model and a set of tools to start performing tasks.

## CLI examples
```bash
# Initialize a new Bee project (TypeScript)
npx beeai-framework init my-agent

# Run a Bee agent in development mode
npx beeai-framework dev

# List available tools in the project
npx beeai-framework tools list
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

        const response = await agent.run({ prompt: "Who won the 2024 World Series?" });
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

    response = agent.run(prompt="Who won the 2024 World Series?")
    print(response.result.text)
    ```

## Strengths
- **Reliability**: Built-in safeguards and "Requirement Agents" to prevent common agent failure modes.
- **Observability**: Excellent execution tracing and logging.
- **Multi-language**: Official support for both TypeScript and Python.
- **Protocol Support**: Native support for [MCP](../../knowledge_base/agent_protocols.md).

## Limitations
- **Complexity**: Might be more complex than lightweight frameworks for simple tasks.
- **Community**: Newer compared to established frameworks like LangChain.

## Related tools / concepts
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md)
- [LangGraph](../frameworks/langgraph.md)
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [Phidata](phidata.md)
- [Superpowers](superpowers.md)
- [Agno](agno.md)

## Sources / References
- [GitHub Repository](https://github.com/i-am-bee/beeai-framework)
- [Official Documentation](https://i-am-bee.github.io/beeai-framework/)
- [IBM Research Blog](https://research.ibm.com/blog/ai-agent-reliability-beeai)

## Contribution Metadata
- Last reviewed: 2026-05-29
- Confidence: high
