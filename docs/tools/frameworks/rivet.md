# Rivet

## What it is
Rivet is an open-source visual AI programming environment and TypeScript library. It allows developers to build, test, and debug complex multi-agent AI systems using a node-based editor.

## What problem it solves
It provides a powerful visual interface for designing AI logic, making it easier to manage complex flows, debug issues, and collaborate on agentic behaviors compared to pure code-based approaches.

## Where it fits in the stack
**Framework / Visual Orchestrator**.

## Typical use cases
- **Agent Design**: Crafting intricate logic for autonomous or semi-autonomous AI agents.
- **Debugging AI Flows**: Using the visual editor to step through and inspect the state of an AI pipeline.
- **Prompt Engineering**: Designing and testing prompts within a structured workflow.

## Strengths
- **Developer-Centric**: Built by developers for developers, with a focus on powerful features and extensibility.
- **Real-time Debugging**: Excellent tools for inspecting the execution of nodes and identifying bottlenecks.
- **TypeScript First**: Offers a robust TypeScript library for integrating Rivet graphs into applications.

## Limitations
- **Learning Curve**: The visual editor and its various node types can take some time to master.
- **Ecosystem Maturity**: While powerful, its ecosystem of pre-built components is still growing.

## When to use it
- When building sophisticated AI agents that require complex logic and state management.
- When you value high-quality visual debugging and inspection tools.

## When not to use it
- For trivial AI tasks where a simple API call is sufficient.
- If you are not comfortable with node-based visual programming.

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

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes (Visual Editor)

## Related tools / concepts
- [Langflow](langflow.md)
- [Flowise](../ai_knowledge/flowise.md)
- [AutoGen](autogen.md)
- [Promptfoo](../benchmarking/promptfoo.md)
- [LangGraph](langgraph.md)

## Sources / References
- [Official Website](https://rivet.ironcladapp.com/)
- [GitHub](https://github.com/Ironclad/rivet)

## Contribution Metadata
- Last reviewed: 2026-05-07
- Confidence: high
