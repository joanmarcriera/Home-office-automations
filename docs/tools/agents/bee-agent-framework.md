# Bee Agent Framework

## What it is
The Bee Agent Framework is an open-source framework by IBM (under the i-am-bee organization) for building, deploying, and orchestrating AI agents. It supports both TypeScript and Python and is designed for production-ready, reliable agentic workflows.

## What problem it solves
It focuses on agent reliability and observability. It provides "Requirement Agents" that can enforce specific rules during execution, and detailed execution traces to help debug complex agent behaviors.

## Where it fits in the stack
[Framework / Agent / Orchestration] - A robust framework for enterprise-grade autonomous agents.

## Typical use cases
- Enterprise automation requiring strict governance and reliability
- Multi-agent systems with complex planning and execution steps
- Cross-language projects (TS/Python)

## Strengths
- **Reliability**: Built-in safeguards and "Requirement Agents" to prevent common agent failure modes.
- **Observability**: Excellent execution tracing and logging.
- **Multi-language**: Official support for both TypeScript and Python.
- **Protocol Support**: Early adoption of [MCP](../../knowledge_base/agent_protocols.md) and ACP.

## Limitations
- **Complexity**: Might be more complex than lightweight frameworks for simple tasks.
- **Community**: Newer compared to established frameworks like LangChain.

## When to use it
- For production applications where reliability and debugging are critical.
- If you need a framework that natively supports the Model Context Protocol.

## When not to use it
- For quick, throwaway prototypes where simplicity is the main goal.

## Getting started
### Installation (TypeScript)
```bash
npm install beeai-framework
```

### Working Example (TypeScript)
```typescript
import { BeeAgent } from "beeai-framework/agents/bee/agent";
import { UnstructuredRawModel } from "beeai-framework/backend/unstructured";
import { DuckDuckGoSearchTool } from "beeai-framework/tools/search/duckduckgo";

async function main() {
    // 1. Create the agent with a tool
    const agent = new BeeAgent({
        llm: new UnstructuredRawModel({ modelId: "gpt-4o" }),
        tools: [new DuckDuckGoSearchTool()],
        memory: []
    });

    // 2. Run a query
    const response = await agent.run({ prompt: "What is the Bee Agent Framework?" });
    console.log(response.result.text);
}

main();
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0 License)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md)
- [LangGraph](langgraph.md)

## Sources / References
- [GitHub Repository](https://github.com/i-am-bee/beeai-framework)
- [IBM Research Blog](https://research.ibm.com/blog/ai-agent-reliability-beeai)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
