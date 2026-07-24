# Google Agent Development Kit (ADK)

## What it is
The Google Agent Development Kit (ADK) is an open-source framework designed for building, debugging, and deploying enterprise-grade AI agents at scale. As of late July 2026, the ADK is in General Availability (GA), serving as the unified orchestration layer for Google's agentic ecosystem, including **Gemini 3.5 series** (Ultra, Pro, Flash), **Gemini Spark**, **Gemini Omni**, and Vertex AI, fully integrated with **Model Context Protocol (MCP 3.1)**.

## What problem it solves
It addresses the "Prototype-to-Production" gap. While many frameworks excel at simple chat loops, the ADK provides the rigorous state-machine orchestration, standardized "Skills" (tool-calling), and robust evaluation frameworks required for mission-critical, multi-agent business workflows. It mitigates fragile multi-model handoffs and non-deterministic execution paths on complex datasets.

## Where it fits in the stack
**Category**: Frameworks / Enterprise Agent Framework. It sits between the frontier models (Gemini, Claude, GPT, Llama, Qwen) and the application layer, providing a structured runtime for agentic logic.

## Typical use cases
- **Multi-Agent Enterprise Orchestration**: Coordinating complex, multi-step tasks across specialized agents (e.g., an "Accountant Agent" and a "Legal Agent") using state-machine transitions.
- **Mission-Critical Workflows**: Building agents where execution paths must be predictable, auditable, and reliable.
- **Skill-Based Capability Extension**: Rapidly adding new tools to agents using standardized, cross-language Skill definitions.
- **Vertex AI Deployment**: Scaling agents to production using Google Cloud's native infrastructure (Cloud Run, GKE).
- **Cross-Framework Integration**: Interfacing local agent logic with remote **MCP 3.1** resources and tool definitions.

## Strengths
- **Production-Grade Reliability**: Based on the same infrastructure Google uses for internal AI services and consumer platforms.
- **Multi-Language Native**: Full, first-class support for Python, TypeScript, Go, and Java.
- **General Availability (GA)**: Fully supported with enterprise-grade SLAs, backward compatibility guarantees, and comprehensive documentation.
- **Native MCP 3.1 Integration**: Seamlessly connects to any Model Context Protocol server for tool, resource, and task access.
- **Standardized "Skills"**: A robust pattern for defining and discovering agent capabilities across different teams and languages.
- **Frontier Model Optimization**: Deeply tuned for late July 2026 frontier models including **Claude 5.1**, **GPT-5.5**, **Llama 4**, **Gemma 3**, and **Qwen 3.6**.

## Limitations
- **Architectural Complexity**: The emphasis on state-machines and explicit orchestration may feel overly complex for simple, linear agents.
- **Cloud-Centric Optimization**: While open-source, it is heavily optimized for the Google Cloud/Vertex AI ecosystem.
- **Learning Curve**: Requires understanding specific Google Cloud IAM roles, environment configurations, and state transition topologies.

## When to use it
- When building large-scale, multi-agent systems that require high reliability and clear state management.
- For enterprise projects where cross-language compatibility (e.g., a Go orchestrator with Python skills) is a requirement.
- When you are already utilizing the Vertex AI ecosystem and want native integration with its evaluation and monitoring tools.
- When building stateful long-horizon tasks ("Missions") using Google's **Anti-Gravity** framework or **Antigravity Agent**.

## When not to use it
- For quick, experimental prototypes where a lighter framework like [smolagents](https://github.com/huggingface/smolagents) or `instructor` would be faster.
- If you prefer a purely "vibe-based" or non-deterministic agent loop over structured state-machines.
- If you are building single-file scripts that do not require state persistence or formal orchestration.

## Getting started
The ADK is available via standard package managers.

### Python Installation
```bash
pip install google-adk
```

### TypeScript Installation
```bash
npm install @google/adk
```

## CLI examples

### 1. Initialize a New Project
```bash
adk init my-agentic-service --language python
```

### 2. Run Local Debugger
```bash
adk debug agent.yaml
```

### 3. Deploy to Vertex AI
```bash
adk deploy --project my-gcp-project --region us-central1
```

## API examples

### Defining a Standardized Skill (Python)
The ADK uses decorators to transform functions into discoverable agent skills.

```python
from google_adk import Skill

@Skill.define(
    name="get_stock_price",
    description="Fetches real-time stock pricing from the internal financial API."
)
def fetch_stock(ticker: str) -> float:
    # Logic to query internal API
    return 150.25

# Registering the skill with an agent
from google_adk import Agent
agent = Agent(name="FinanceAgent", model="gemini-3.5-pro", skills=[fetch_stock])
```

### Orchestrating a State-Machine Agent (TypeScript)
```typescript
import { Agent, StateMachine } from '@google/adk';

const sm = new StateMachine();
sm.addState('INITIAL', async (context) => {
  return context.input.includes('help') ? 'SUPPORT' : 'ROUTING';
});

const agent = new Agent({
  name: 'Orchestrator',
  workflow: sm
});
```

## Related tools / concepts
- [Gemini](../ai_knowledge/google-gemini.md) — The primary model backbone for ADK agents.
- [LangGraph](../frameworks/langgraph.md) — Competitive framework for stateful multi-agent systems.
- [CrewAI](../frameworks/crewai.md) — Popular alternative for multi-agent role-playing.
- [MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Integrated standard for tool connectivity.
- [Anti-Gravity](../development_ops/anti_gravity.md) — Google's runtime orchestration layer for autonomous agent Missions.
- [Jules](../ai_knowledge/jules.md) — Advanced agentic assistant developed by Google.
- [Firebase Genkit](../frameworks/firebase-genkit.md) — Google's framework for AI-integrated web apps.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The fundamental pattern the ADK implements.

## Sources / references
- [Google Cloud ADK Documentation](https://cloud.google.com/vertex-ai/docs/adk)
- [ADK GitHub Repository](https://github.com/google/adk)
- [Google Developers Blog: ADK General Availability](https://developers.googleblog.com/2026/06/adk-ga-launch)
- [Vertex AI Agent Runtime Guide](https://cloud.google.com/vertex-ai/docs/agents/runtime)

## Contribution Metadata
- Last reviewed: 2026-07-29
- Confidence: high
