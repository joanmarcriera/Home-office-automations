# Google Agent Development Kit (ADK)

## What it is
The Google Agent Development Kit (ADK) is an open-source framework designed for building, debugging, and deploying enterprise-grade AI agents at scale. As of early January 2027, the ADK is in General Availability (GA), serving as the unified, stateful runtime orchestration layer for Google's agentic ecosystem. It is engineered to harness the advanced reasoning capabilities of the Gemini 4.0 series (Ultra, Pro, Flash), Gemini Spark (for planning and multi-agent coordination), and Gemini Omni (for multimodal stream processing), while maintaining full FastMCP 3.1 Task Protocol integration and cross-compatibility with other frontier models like Claude 5.6 and GPT-5.6.

## What problem it solves
While lightweight scripting libraries are suitable for single-agent chat loops, they fail to bridge the "Prototype-to-Production" gap for complex corporate workflows. They often lack strict state management, explicit orchestration, multi-language interoperability, and robust evaluation paths. The ADK addresses these enterprise requirements by providing reliable, deterministic state-machine orchestration, standardized "Skills" (tool-calling interfaces), FastMCP 3.1 Task Protocol execution loops, and integrated evaluation runtimes that ensure agent execution remains predictable, auditable, and SLA-compliant.

## Where it fits in the stack
**Category**: [Frameworks](index.md) / [Enterprise Agent Frameworks](../../knowledge_base/index.md).
It sits directly between the foundation model layer (Gemini, Claude, GPT) and the production application layer, acting as a structured, stateful middleware that coordinates business logic, session state, tool execution, FastMCP 3.1 tasks, and deployment orchestration.

## Typical use cases
- **Multi-Agent Enterprise Orchestration**: Coordinating complex, stateful workflows across specialized agents (e.g., an "Invoicing Agent" routing verified financial documents to a "Compliance Agent" for secondary legal audits).
- **Long-Horizon Stateful Missions**: Orchestrating autonomous tasks ("Missions") that require persisting and recovering state across asynchronous loops, API wait states, and human-in-the-loop approvals.
- **Skill-Based Capability Scaling**: Extending agent functionalities rapidly across multi-language microservices by deploying standardized, discoverable "Skills".
- **Vertex AI Production Deployment**: Scaling containerized agent runtimes natively to Google Cloud Platform (GCP) utilizing Cloud Run, Google Kubernetes Engine (GKE), and Vertex AI Agent Runtime.

## Strengths
- **Rigorous State-Machine Orchestration**: Prevents agents from entering infinite loops or executing unauthorized tools by enforcing explicit, deterministic state transitions.
- **First-Class Multi-Language Support**: Complete, feature-parity SDKs available for Python, TypeScript, Go, and Java, enabling polyglot enterprise architectures.
- **Native FastMCP 3.1 Integration**: Built-in support for FastMCP 3.1 client/server task protocol patterns, letting agents seamlessly query external tools, databases, and filesystem contexts.
- **Vertex AI Evaluation Integration**: Direct, out-of-the-box telemetry pipelines pointing to Vertex AI monitoring, logging, and evaluation frameworks to measure success and detect drift.
- **Standardized Skill Definitions**: A declarative paradigm that auto-generates schema parameters, enabling easy sharing of tool schemas across different internal teams.

## Limitations
- **Architectural Overhead**: The emphasis on explicit state transitions, strict schemas, and declarative configuration might feel unnecessarily verbose for simple, linear agent designs.
- **Ecosystem Gravity**: Although fully open-source and model-agnostic, the ADK delivers maximum optimization, security, and velocity when paired with Google Cloud, Vertex AI, and Gemini models.
- **Steep Learning Curve**: Developers must master state-machine concepts, context propagation boundaries, and skill schemas, rather than relying on intuitive, prompt-only steering.

## When to use it
- When building large-scale, multi-agent orchestrations that must run in robust, highly auditable production environments.
- For projects that require cross-language compatibility (e.g., coordinating a Go-based core system with Python-based ML skills and TypeScript frontend components).
- When leveraging Google Cloud Platform (GCP) and Vertex AI as the underlying hosting, logging, and model-inference infrastructure.
- For implementing FastMCP 3.1 Task Protocol execution loops across distributed agent networks.

## When not to use it
- For rapid, low-complexity prototyping or single-turn prompts where lightweight frameworks like `smolagents` or simple SDK scripts are more agile.
- If you prefer purely non-deterministic, agent-steered "vibe loops" where the LLM is given complete, unconstrained control over execution paths without state boundaries.

## Getting started
The Google ADK is distributed as highly optimized packages through all major package managers.

### Python Installation
```bash
pip install google-adk pydantic fastmcp
```

### TypeScript Installation
```bash
npm install @google/adk
```

## CLI examples
The ADK command-line interface streamlines project scaffolding, local diagnostic execution, and production cloud deployment.

```bash
# Initialize a new, structured ADK project
adk init my-agentic-service --language python

# Run the local debugger to trace state-machine execution and variable states
adk debug agent.yaml --port 8080

# Run evaluation runs against a local test dataset
adk test --dataset ./eval-queries.json --agent agent.yaml

# Package and deploy the agent to Vertex AI Agent Runtime
adk deploy --project enterprise-gcp-prod --region us-central1 --tag v2.4
```

## API examples

### 1. Declaring and Registering a FastMCP 3.1 Skill with Pydantic v2 Payload Validation (Python)
The ADK leverages decorators to extract signatures and can be coupled with strict **Pydantic v2** validation parameters to enforce payload verification at runtime.

```python
import os
from pydantic import BaseModel, Field, field_validator
from google_adk import Skill, Agent

# Define a strict FastMCP 3.1 parameter validation schema using Pydantic v2
class InventoryQuery(BaseModel):
    task_id: str = Field(..., description="FastMCP 3.1 execution task identifier")
    sku: str = Field(..., description="Unique product stock-keeping unit (format: SKU-XXXXX)")
    warehouse_id: str = Field(default="us-east-1", description="Target fulfillment center identifier")

    @field_validator("sku")
    @classmethod
    def validate_sku_format(cls, v: str) -> str:
        if not v.startswith("SKU-") or len(v) < 6:
            raise ValueError("SKU must start with 'SKU-' followed by alphanumeric characters")
        return v

# Define a secure, standardized Skill
@Skill.define(
    name="get_inventory_status",
    description="Fetches real-time stock levels and warehouse availability for a validated inventory query under FastMCP 3.1."
)
def fetch_inventory(query_payload: dict) -> dict:
    # Strictly validate payload inputs before processing ERP logic
    validated_query = InventoryQuery.model_validate(query_payload)
    return {
        "task_id": validated_query.task_id,
        "sku": validated_query.sku,
        "status": "In Stock",
        "quantity": 142,
        "warehouse": validated_query.warehouse_id
    }

# Initialize the Gemini-powered agent and register the Skill
agent = Agent(
    name="LogisticsAgent",
    model="gemini-4.0-pro",
    api_key=os.environ.get("GEMINI_API_KEY"),
    skills=[fetch_inventory]
)

# Run the agent with structured payload query context
response = agent.run("Check inventory status for task task_inv_01 and SKU-90812 in warehouse us-east-1")
print("Agent Response:", response.text)
```

### 2. State-Machine Orchestration with Context Propagation (TypeScript)
Define deterministic transitions between state blocks using the TypeScript SDK.

```typescript
import { Agent, StateMachine, Context } from '@google/adk';

const sm = new StateMachine();

// Define states with explicit transitions
sm.addState('INITIAL', async (context: Context) => {
  if (context.input.includes('billing')) {
    return 'BILLING_FLOW';
  }
  return 'GENERAL_ROUTE';
});

sm.addState('BILLING_FLOW', async (context: Context) => {
  // Logic to process billing queries via secure payment gateways
  return 'COMPLETE';
});

sm.addState('GENERAL_ROUTE', async (context: Context) => {
  // Logic to route general queries to Gemini 4.0 Flash
  return 'COMPLETE';
});

const orchestratorAgent = new Agent({
  name: 'EnterpriseRouter',
  workflow: sm
});
```

## Related tools / concepts
- [Gemini](../ai_knowledge/gemini.md) — The core model backbone optimized for ADK's native context caching and planning.
- [LangGraph](../frameworks/langgraph.md) — Multi-agent state-graph orchestration framework.
- [CrewAI](../frameworks/crewai.md) — High-level role-playing multi-agent execution framework.
- [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) — The unified protocol the ADK uses to communicate with external data servers.
- [Supabase](../infrastructure/supabase.md) — Frequently utilized alongside ADK for managing session state storage and user authentication.
- [Firebase Genkit](../frameworks/firebase-genkit.md) — Google's application developer framework for integrating AI into web and mobile backends.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The state-machine patterns and paradigms implemented by the ADK.

## Sources / references
- [Google Vertex AI Agent SDK Guides](https://cloud.google.com/vertex-ai/docs/adk)
- [Official Google ADK GitHub Repository](https://github.com/google/adk)
- [Google Cloud Developers Blog: Launching ADK General Availability](https://developers.googleblog.com/2026/06/adk-ga-launch)
- [Vertex AI Agent Runtime Guide](https://cloud.google.com/vertex-ai/docs/agents/runtime)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
