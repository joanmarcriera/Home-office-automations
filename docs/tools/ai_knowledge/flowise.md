# Flowise

## What it is
Flowise is an open-source visual builder and low-code orchestrator for LLM applications and multi-agent systems. Built with Node.js and running on top of LangChain/LangGraph, it provides a drag-and-drop user interface to construct complex RAG pipelines, autonomous agent graphs, and automated cognitive workflows. As of late October / November 2026, Flowise includes native support for Model Context Protocol (MCP 3.1), FastMCP 3.1, and deep multi-agent coordination frameworks.

## What problem it solves
It bridges the gap between conceptual prompt engineering and production-grade software development. By offering a visual workspace, it enables engineers and business analysts to rapidly prototype, debug, and publish agentic systems. It handles the underlying complexities of state persistence, vector database upserts, and tool execution security (including native SSRF protection) with minimal boilerplate.

## Where it fits in the stack
**Orchestration / Builder Layer**. Sits above the [Inference & Providers](../providers/index.md) and [Vector Databases](../intake_storage/index.md) layers, serving as the visual "control plane" where cognitive logic, retrieval architectures, and autonomous tools are woven together.

## Typical use cases
- **Multi-Agent Flow Orchestration**: Designing stateful agent systems (e.g., Supervisor-Worker or Peer-to-Peer structures) where agents collaborate to solve complex research or coding problems.
- **Enterprise-Grade RAG Pipelines**: Connecting documents with advanced retrieval architectures like hybrid search, vector embeddings, reranking, and self-query retrievers.
- **MCP-Enabled Automation**: Equipping drag-and-drop agents with standardized local and cloud tools via MCP 3.1 integrations.
- **Secure Internal Tooling**: Deploying ready-to-use chatbots across interfaces like WhatsApp, Slack, Teams, or embedding them in corporate intranets.

## Strengths
- **Visual "AgentFlow" Designer**: Streamlines state machine configuration, decision loops, and task delegation without writing complex orchestration code.
- **SSRF & Network Hardening**: Out-of-the-box security guardrails to restrict agent actions, preventing unauthorized internal network scans or SSRF vulnerabilities.
- **MCP 3.1 standard compliance**: Seamless discovery and execution of standardized FastMCP 3.1 tool servers.
- **Human-in-the-Loop (HITL)**: Built-in nodes to halt execution, request human validation for sensitive actions (e.g., executing database writes), and resume dynamically.
- **Extensive Integrations**: Supports over 100+ components, including vector stores, document loaders, custom tools, and memory stores.

## Limitations
- **Visual Scaling**: When flows exceed dozens of interconnected nodes, the visual canvas can become complex and difficult to audit compared to modular code.
- **Underlying Engine Lock-in**: Deeply tied to the capabilities and paradigms of LangChain and LangGraph; extending beyond their supported structures can require custom JS nodes.
- **Server Overhead**: Visual server rendering and active WebSocket sessions require higher constant resources than lightweight code-native scripts.

## When to use it
- When you need to build, iterate, and visually audit complex agentic workflows and multi-step retrieval pipelines.
- For team environments where developers and non-technical stakeholders must collaborate on prompt flows and chatbot logic.
- When self-hosting a reliable, SSRF-hardened AI agent platform in local homelabs or corporate networks.

## When not to use it
- For ultra-high performance, sub-millisecond API endpoints where any framework-induced latency must be avoided.
- If you prefer code-first, highly mathematical declarative frameworks like [DSPy](../frameworks/dspy.md) or direct SDKs.

## Getting started

### 1. Docker Deployment
The safest and most isolated way to deploy Flowise in late 2026 is via Docker, with persistent storage and security variables enabled:

```bash
docker run -d \
  --name flowise \
  -p 3000:3000 \
  -e FLOWISE_USERNAME=admin \
  -e FLOWISE_PASSWORD=secure_password_2026 \
  -v ~/.flowise:/root/.flowise \
  flowiseai/flowise
```

### 2. Building a Stateful Flow
1. Open `http://localhost:3000` in your browser and log in.
2. Select **AgentFlows** and click **Create New**.
3. Drag a **Supervisor Agent** and two **Worker Agents** (e.g., "Web Researcher" and "Code Execution") onto the canvas.
4. Add an **MCP 3.1 Tool Node**, pointing it to your local FastMCP server.
5. Link the Workers to the Supervisor, specify a model like `claude-5.1-sonnet` or `gpt-5.5-preview` as the brain, and hit **Save**.

## CLI examples
Flowise includes an interactive CLI for running migrations, exporting chatflows, and adjusting server configurations.

```bash
# Start Flowise with customized execution paths and logging level
npx flowise start --databasePath ~/.flowise/db --uploadsPath ~/.flowise/uploads --logLevel debug

# Export all visual flows into a portable backup folder
flowise export --output ./backup-flows/

# Force DB schema migrations after major 2026 core updates
npx flowise-db migrate
```

## API examples
Every Flowise flow is immediately exposed as a standardized REST API. Below is a Python script utilizing `pydantic` (v2) to construct and validate payloads for querying a Flowise visual flow asynchronously.

```python
import asyncio
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl

class NodeParameterConfig(BaseModel):
    node_id: str = Field(..., alias="nodeId")
    node_type: str = Field(..., alias="nodeType")
    parameters: Dict[str, Any] = Field(default_factory=dict)

class FlowisePredictionPayload(BaseModel):
    question: str = Field(..., min_length=1, description="The user prompt to inject into the visual flow")
    override_config: Optional[Dict[str, Any]] = Field(None, alias="overrideConfig", description="Override parameters dynamically")
    history: Optional[List[Dict[str, str]]] = Field(None, description="Previous conversational history blocks")
    nodes: Optional[List[NodeParameterConfig]] = Field(None, description="Dynamically inject node overrides")

async def trigger_flow_prediction():
    # Constructing a complex visual flow execution request
    raw_payload = {
        "question": "Run a system health check and audit our Postgres DB indexes.",
        "overrideConfig": {
            "temperature": 0.2,
            "systemPrompt": "You are a senior DevOps SRE.",
            "mcpServerUrl": "http://host.docker.internal:8000/mcp"
        },
        "nodes": [
            {
                "nodeId": "agent_worker_1",
                "nodeType": "workerAgentNode",
                "parameters": {"maxIterations": 10}
            }
        ]
    }

    # Validate payload under Pydantic v2 schemas
    validated_payload = FlowisePredictionPayload.model_validate(raw_payload)
    print(f"Payload successfully validated for Flowise.")
    print(f"Target query: {validated_payload.question}")

    # Example simulated POST request
    # async with httpx.AsyncClient() as client:
    #     response = await client.post("http://localhost:3000/api/v1/prediction/<FLOW_ID>", json=validated_payload.model_dump(by_alias=True))
    #     print(response.json())

if __name__ == "__main__":
    asyncio.run(trigger_flow_prediction())
```

## Related tools / concepts
- [LangFlow](../frameworks/langflow.md) — The leading visual orchestrator competitor.
- [Dify](dify.md) — Advanced full-suite LLMOps workspace platform.
- [n8n](../../services/n8n.md) — General workflow automation with modular agent extensions.
- [Rivet](../frameworks/rivet.md) — Node-based builder targeting complex, conditional logic networks.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Core tool protocol powering Flowise integration.
- [CrewAI](../frameworks/crewai.md) — High-productivity code-native multi-agent framework.
- [LangGraph](../frameworks/langgraph.md) — Visual state framework built upon LangGraph concepts.

## Sources / references
- [Flowise Official Documentation](https://docs.flowiseai.com/)
- [Flowise Multi-Agent Architecture Specifications](https://docs.flowiseai.com/multi-agents/agentflows)
- [SSRF Network Security and Hardening in Flowise (2026 Update)](https://docs.flowiseai.com/security/ssrf-protection)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
