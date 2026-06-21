# Rivet

## What it is
Rivet is an open-source visual AI programming environment and TypeScript library developed by Ironclad. It allows developers to build, test, and debug complex multi-agent AI systems using a node-based editor. As of June 2026, it has evolved into a comprehensive agent infrastructure provider with the launch of **agentOS**, **Rivet Actors**, and a full Rust-based rewrite of its core libraries (RivetKit 2.3).

## What problem it solves
It provides a powerful visual interface for designing AI logic, making it easier to manage complex flows and collaborate on agentic behaviors. It solves the performance and cost bottlenecks of traditional sandboxed environments through **agentOS**, which uses Wasm and V8 isolates for near-instant cold starts. Additionally, **Rivet Actors** address the need for stateful, distributed agent execution with million-scale isolated databases via **SQLite for Rivet Actors**.

## Where it fits in the stack
**Framework / Visual Orchestrator / Agent Runtime / Edge Infrastructure**.

## Typical use cases
- **Visual Agent Design**: Designing intricate logic for autonomous or semi-autonomous AI agents using a node-based editor.
- **Stateful Edge Computing**: Deploying millions of isolated, stateful actors that run at the edge with built-in SQLite persistence.
- **High-Performance Sandboxing**: Running untrusted AI-generated code in **agentOS** with ~6ms cold starts, significantly faster than traditional Docker-based sandboxes.
- **Serverless Agent Hosting**: Utilizing **Rivet Compute** to host and scale agent actors without managing underlying infrastructure.

## Strengths
- **Developer-Centric Debugging**: Real-time visual inspection of prompt chains and agent execution.
- **Extreme Performance**: agentOS provides a full POSIX environment that is 32x cheaper and significantly faster than traditional VMs.
- **Stateful Concurrency**: Native support for stateful actors using the **Rust SDK** or **Effect SDK** for Rivet Actors.
- **Local-First / Edge-Native**: SQLite-per-actor architecture allows for massive horizontal scaling at the edge.

## Limitations
- **Visual Overhead**: For extremely simple prompt calls, the visual graph overhead may be unnecessary.
- **Ecosystem Velocity**: The rapid shift towards a Rust-based core and Actor model requires keeping up with frequent breaking changes in the SDKs.

## When to use it
- When building sophisticated AI agents that require complex logic, state management, and durable workflows.
- When you need a high-performance, low-cost sandbox for executing AI-generated code.
- When you want to deploy stateful AI services at the edge that scale to zero.

## When not to use it
- For trivial, single-prompt AI tasks.
- If you prefer purely code-based orchestration without any visual design or debugging components.

## Getting started

### Installation
To use Rivet in your project:
```bash
npm install @ironclad/rivet-node
```

### Rivet Actors Setup
To create a new stateful actor using the Rust SDK:
```bash
cargo add rivet-actor
```

### Local Development
Download the Rivet desktop application from the [Official Website](https://rivet.ironcladapp.com/) to start building graphs visually.

## CLI examples

### Running a Graph via CLI
```bash
rivet run my-project.rivet-project --graph "Main Graph" --input userInput="Hello AI"
```

### Deploying to Rivet Compute
```bash
rivet deploy --actor my-agent-actor
```

## API examples

### Running a Graph in Node.js
```typescript
import { runGraph, loadProject, NodeId } from '@ironclad/rivet-node';

async function runRivetGraph() {
  const project = await loadProject('path/to/project.rivet-project');

  const results = await runGraph(project, {
    graph: 'Main Graph' as NodeId,
    inputs: {
      userInput: { type: 'string', value: 'Hello Rivet!' }
    },
    openAiKey: process.env.OPENAI_API_KEY,
  });

  console.log(results.output.value);
}
```

### Creating an Actor (Rust SDK)
```rust
use rivet_actor::prelude::*;

#[actor]
async fn my_actor(ctx: Context, input: String) -> Result<String> {
    let state: MyState = ctx.get_state().await?;
    let response = ctx.call_llm("gpt-4o", input).await?;
    Ok(response)
}
```

## Related tools / concepts
- [Langflow](langflow.md) — Visual workflow builder.
- [Flowise](../ai_knowledge/flowise.md) — Node-based UI for LLM flows.
- [AutoGen](ag2.md) — Rebranded as AG2, focused on multi-agent conversation.
- [Promptfoo](../benchmarking/promptfoo.md) — Evaluation and testing for Rivet graphs.
- [LangGraph](langgraph.md) — Code-centric multi-agent orchestration.
- [PydanticAI](pydantic-ai.md) — Type-safe agent framework from Pydantic.
- [Temporal](../orchestration/temporal.md) — Durable execution often compared with Rivet Workflows.
- [Claude Code](../development_ops/claude-code.md) — Supported via Sandbox Agent SDK integration.

## Sources / References
- [Official Website](https://rivet.ironcladapp.com/)
- [Rivet Developer Blog](https://rivet.dev/blog/)
- [GitHub Repository](https://github.com/Ironclad/rivet)
- [agentOS Documentation](https://sandboxagent.dev/)

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-06-21)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
