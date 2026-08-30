# AirOps

## What it is
AirOps is an enterprise AI platform for building, testing, and scaling AI-powered applications, agentic workflows, and MCP tool orchestrations. It provides a collaborative studio for enterprise teams to design complex prompt chains, test them against state-of-the-art models, and deploy them as scalable microservices and tools. As of early 2027, AirOps fully integrates with the **MCP 3.1** and **FastMCP 3.1 Task Protocol** standards, enabling seamless orchestration of autonomous workflows using frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**.

## What problem it solves
AirOps addresses the challenge of moving AI from simple prototyping to robust, production-grade business operations. It provides enterprise infrastructure for prompt versioning, multi-model orchestration, evaluations, and secure data handling, allowing organizations to build internal AI tools that are reliable, auditable, and scalable. It eliminates the need for managing underlying compute resources, custom container clusters, or complex API integrations manually.

## Where it fits in the stack
**Automation & Orchestration / Enterprise AI Platform**. It acts as the enterprise-grade orchestration layer between foundation models and core business applications, often serving as the central execution engine for complex [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- **Enterprise RAG & Knowledge Systems**: Implementing high-accuracy Retrieval-Augmented Generation across massive internal data warehouses with human-in-the-loop validation checkpoints.
- **Custom AI SaaS Products**: Building and hosting multi-tenant, white-labeled AI applications for external customers with strict tenant isolation.
- **Intelligent Process Automation (IPA)**: Automating complex multi-step enterprise workflows like insurance claims triage, compliance audits, or legal contract analysis.
- **Autonomous Market & Sales Intelligence**: Creating autonomous research agents that analyze market trends, track competitor movements, and draft personalized outreach using search tools like [Tavily](../providers/tavily.md).
- **Enterprise Knowledge Integration**: Centralizing company intelligence into queryable agents integrated with [AnythingLLM](../ai_knowledge/anythingllm.md) or [mem0](../agents/mem0.md).

## Strengths
- **Collaborative Studio & Workspace**: Enables product managers, domain experts, and engineers to collaborate on prompt engineering, evaluation sets, and workflow design in real time.
- **FastMCP 3.1 & Task Protocol Native**: Native support for Model Context Protocol (MCP) 3.1 and FastMCP 3.1 task management specifications for standardized agent-to-tool interactions.
- **Enterprise-Grade Scaling & SLA**: Engineered to process millions of requests daily with high availability, low-latency execution routing, and real-time performance monitoring.
- **Rich Connector Ecosystem**: Native connectors for Postgres, Snowflake, BigQuery, and major SaaS applications, along with custom OpenAPI endpoints.
- **Built-in Guardrails & Audit Trails**: Enterprise governance including automated PII detection, continuous evaluations, [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md), and detailed audit logs.

## Limitations
- **Platform Pricing**: Primarily designed for mid-market and enterprise teams, with pricing models that may be prohibitive for individual developers.
- **Learning Curve**: The extensive feature set for prompt versioning, evaluations, and complex multi-agent flows requires initial team onboarding.
- **Managed Ecosystem**: While highly flexible, the core orchestration logic runs within the managed AirOps environment, introducing vendor managed dependencies.

## When to use it
- When building mission-critical AI applications requiring enterprise-grade security, scalability, continuous evaluations, and auditability.
- For teams requiring a collaborative, no-code/low-code studio to rapidly iterate on complex prompt logic and agentic reasoning.
- When orchestrating multi-step AI tasks that leverage the **FastMCP 3.1 Task Protocol** ecosystem.
- For implementing RAG patterns that require high retrieval accuracy, hybrid search, and custom re-ranking strategies.

## When not to use it
- For simple, single-prompt automations that can be handled by basic scripts or standard webhook triggers.
- If the application strictly mandates air-gapped, on-premises deployment without external cloud connectivity (consider [LocalAI](../infrastructure/localai.md) or self-hosted [Dify](../ai_knowledge/dify.md)).
- For ultra-low latency real-time voice streaming where direct websocket connections to frontier models are necessary.

## Getting started

### 1. Workspace Setup
Sign up at [AirOps.com](https://www.airops.com/) and configure your enterprise workspace.

### 2. Configure API Keys & Secrets
Generate an API Key in your workspace settings and securely store it, ideally using [HashiCorp Vault](hashicorp-vault.md).

### 3. Build & Evaluate a Workflow
Use the AirOps Studio to visually design your workflow, connecting nodes for LLMs (e.g., **Claude 5.6**, **Gemma 4**), vector stores, and logic nodes. Run automated evaluations against test suites before deployment.

### 4. Deploy and Integrate
Publish your workflow and execute it via webhooks or the REST API within your software stack.

## CLI examples

```bash
# Execute an AirOps workflow via POST request (Webhook Execution)
curl --request POST \
  --url 'https://app.airops.com/public_api/airops_apps/YOUR_APP_UUID/webhook_async_execute?auth_token=YOUR_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{ "input_query": "Analyze market trends for Q1 2027", "mode": "fast_mcp_3_1" }'

# Retrieve results from a specific execution ID
curl -G 'https://app.airops.com/public_api/airops_apps/YOUR_APP_UUID/executions/YOUR_EXECUTION_UUID' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

## API examples

### Executing an AirOps App with Pydantic v2 Contract Validation
In early 2027 enterprise integrations, responses received from AirOps webhook executions must be strictly verified against a schema contract before propagating to downstream microservices or vector indices. This ensures high data reliability when invoking frontier models such as Claude 5.6 or GPT-5.6.

```python
import os
import requests
from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError

# 1. Define the validation contract using Pydantic v2
class AirOpsOutput(BaseModel):
    summary: str = Field(description="The primary summary returned by the execution")
    confidence_score: float = Field(ge=0.0, le=1.0, description="The reliability confidence score of the extracted info")
    key_entities: List[str] = Field(default_factory=list, description="Extracted enterprise entities")

class AirOpsExecutionResponse(BaseModel):
    execution_id: str = Field(description="The unique identifier of the AirOps execution")
    status: str = Field(description="State of the webhook run (e.g., success, queued)")
    result: AirOpsOutput = Field(description="The validated output object from the execution")

def trigger_and_validate_airops(app_uuid: str, query: str) -> Optional[AirOpsExecutionResponse]:
    api_key = os.getenv("AIROPS_API_KEY", "dummy-key")
    endpoint = f"https://app.airops.com/public_api/airops_apps/{app_uuid}/webhook_async_execute"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "query": query,
        "depth": "comprehensive"
    }

    try:
        # Example representation of a successful response payload from AirOps running Claude 5.6
        mock_response_data = {
            "execution_id": "exec-abc-987654",
            "status": "success",
            "result": {
                "summary": "AI integration patterns for Gemma 4 and FastMCP 3.1 completed.",
                "confidence_score": 0.99,
                "key_entities": ["Gemma 4", "FastMCP 3.1 Task Protocol", "Enterprise RAG"]
            }
        }

        # 2. Enforce strict Pydantic v2 validation contract
        validated_response = AirOpsExecutionResponse.model_validate(mock_response_data)
        return validated_response

    except ValidationError as ve:
        print(f"AirOps response schema validation failed: {ve}")
    except Exception as e:
        print(f"Network or execution error: {e}")

    return None

if __name__ == "__main__":
    app_id = "YOUR_APP_UUID"
    validated_run = trigger_and_validate_airops(app_id, "Synthesize enterprise RAG patterns")
    if validated_run:
        print("AirOps response matched the enterprise data contract!")
        print(f"Execution ID: {validated_run.execution_id}")
        print(f"Result Summary: {validated_run.result.summary}")
```

## Related tools / concepts
- [Gumloop](gumloop.md) — Visual AI automation for agile teams and rapid prototyping.
- [Model Context Protocol (MCP)](mcp.md) — The standard for connecting AI agents to enterprise tools.
- [Gemma 4](../ai_knowledge/local_llms.md) — Frontier open model often orchestrated via AirOps workflows.
- [n8n](../../services/n8n.md) — Self-hosted workflow automation alternative.
- [AnythingLLM](../ai_knowledge/anythingllm.md) — Enterprise-grade local knowledge base.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Patterns for multi-step reasoning and execution.
- [Tavily](../providers/tavily.md) — Specialized search engine for AI agents.
- [Langfuse](../process_understanding/langfuse.md) — Observability for complex LLM applications.

## Sources / references
- [AirOps Official Website](https://www.airops.com/)
- [AirOps Documentation](https://docs.airops.com/)
- [AirOps API Reference](https://docs.airops.com/api-reference)
- [FastMCP Specification and Tools Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
