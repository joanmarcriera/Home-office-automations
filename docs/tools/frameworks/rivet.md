# Rivet

## What it is
Rivet is an open-source visual AI programming environment and TypeScript library. It allows developers to build, test, and debug complex multi-agent AI systems using a node-based editor. As of May 2026, it has expanded into a comprehensive "Infrastructure for the agentic era" with the launch of **agentOS**.

## What problem it solves
It provides a powerful visual interface for designing AI logic, making it easier to manage complex flows, debug issues, and collaborate on agentic behaviors. With **agentOS**, it solves the high cost and slow cold-starts of traditional sandboxed environments for agentic code execution.

## Where it fits in the stack
**Framework / Visual Orchestrator / Agent Runtime**.

## Typical use cases
- **Agent Design**: Crafting intricate logic for autonomous or semi-autonomous AI agents using a node-based editor.
- **Stateful Workflows**: Implementing durable, replayable workflows for TypeScript that support sleep, join, and human-in-the-loop.
- **Sandboxed Code Execution**: Running untrusted AI-generated code in **agentOS** (Wasm/V8 isolates) with ~6ms cold starts.
- **Edge Data Storage**: Utilizing **SQLite for Rivet Actors** to manage millions of isolated databases at the edge.

## Strengths
- **Developer-Centric**: Built for developers with a focus on extensibility and powerful visual debugging.
- **Performance**: agentOS provides a full POSIX environment that is 32x cheaper than traditional sandboxes.
- **Durable Execution**: Rivet Workflows provide robust state management and replayability.
- **Unified Agent API**: The **Sandbox Agent SDK** provides a single API for integrating with various coding agents like Claude Code or Amp.

## Limitations
- **Learning Curve**: The visual editor and its various node types can take some time to master.
- **Transitioning Ecosystem**: Rapidly evolving from a visual editor into a full-stack agent infrastructure provider.

## When to use it
- When building sophisticated AI agents that require complex logic, state management, and durable workflows.
- When you need a high-performance, low-cost sandbox for executing AI-generated code.
- When you value high-quality visual debugging and inspection tools.

## When not to use it
- For trivial AI tasks where a simple API call is sufficient.
- If you are not comfortable with node-based visual programming for logic design.

## Getting started

### Installation
To use Rivet in your project:
```bash
npm install @ironclad/rivet-node
```

### Running a Graph
You can load and run a `.rivet-project` file in your Node.js application:

```typescript
import { runGraph, loadProject, NodeId } from '@ironclad/rivet-node';

async function runRivetGraph() {
  const project = await loadProject('path/to/project.rivet-project');

  const results = await runGraph(project, {
    graph: 'Main Graph' as NodeId,
    inputs: {
      userInput: { type: 'string', value: 'Hello Rivet!' }
    },
    // Required if using OpenAI nodes
    openAiKey: process.env.OPENAI_API_KEY,
  });

  console.log(results.output.value);
}

runRivetGraph();
```

### Rivet Workflows Example
```typescript
import { workflow } from '@ironclad/rivet-node';

const myWorkflow = workflow('example', async (c) => {
  const result = await c.callAgent('researcher', { query: 'May 2026 AI trends' });
  await c.sleep('1 day'); // Durable sleep
  return await c.callAgent('writer', { data: result });
});
```

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free (OSS version); Usage-based for Rivet Cloud/agentOS.
- **Self-hostable**: Yes

## Related tools / concepts
- [Langflow](langflow.md)
- [Flowise](../ai_knowledge/flowise.md)
- [AutoGen](autogen.md)
- [Promptfoo](../benchmarking/promptfoo.md)
- [LangGraph](langgraph.md)
- [PydanticAI](pydantic-ai.md)
- [Temporal](../orchestration/temporal.md)
- [Claude Code](../development_ops/claude-code.md) — Supported via Sandbox Agent SDK.

## Sources / References
- [Official Website](https://rivet.ironcladapp.com/)
- [Changelog](https://rivet.dev/changelog/)
- [GitHub](https://github.com/Ironclad/rivet)
- [Sandbox Agent SDK](https://sandboxagent.dev/)

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-05-31)

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high
