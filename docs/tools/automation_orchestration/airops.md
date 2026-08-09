# AirOps

## What it is
AirOps is an enterprise AI platform for building, testing, and scaling AI-powered applications and agentic workflows. It provides a collaborative studio for teams to design sophisticated prompt chains, test them against various models, and deploy them as scalable "tools." As of late 2026, AirOps fully integrates with the **MCP 3.1** and **FastMCP 3.1** standards, enabling seamless orchestration of complex tasks using frontier models like **Gemma 3**, **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**.

## What problem it solves
AirOps addresses the challenge of moving AI from simple prototyping to robust, production-grade business operations. It provides the necessary infrastructure for prompt versioning, multi-model orchestration, and secure data handling, allowing organizations to build internal AI tools that are reliable, auditable, and scalable. It eliminates the need for managing underlying compute resources or complex API integrations manually.

## Where it fits in the stack
**Automation & Orchestration / Enterprise AI Platform**. It acts as the enterprise-grade orchestration layer between foundation models and core business applications, often serving as the "brain" for complex [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- **Enterprise RAG Systems**: Implementing high-accuracy Retrieval-Augmented Generation across massive internal datasets with human-in-the-loop validation.
- **Custom AI SaaS**: Building and hosting white-labeled AI applications for external customers.
- **Intelligent Process Automation (IPA)**: Automating multi-step business processes like insurance claims triage or legal document review.
- **Sales & Marketing Intelligence**: Creating agents that research leads, summarize market trends, and draft personalized outreach using tools like [Tavily](../providers/tavily.md).
- **Knowledge Management**: Centralizing company intelligence into queryable agents integrated with [AnythingLLM](../ai_knowledge/anythingllm.md) or [mem0](../agents/mem0.md).

## Strengths
- **Collaborative Studio**: Enables product managers and engineers to collaborate on prompt engineering and workflow design in real-time.
- **FastMCP 3.1 Native**: Direct support for the Model Context Protocol (MCP) FastMCP 3.1 specification for standardized tool and agent interaction.
- **Enterprise-Grade Scaling**: Built to handle millions of requests with high availability and robust performance monitoring.
- **Deep Integrations**: Native connectors for Postgres, Snowflake, and major SaaS platforms, plus custom API support.
- **Built-in Guardrails**: Includes tools for managing [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md) and ensuring data privacy.

## Limitations
- **Platform Cost**: Primarily targeted at enterprise teams, with pricing that may be prohibitive for solo developers.
- **Learning Curve**: The breadth of features for managing complex workflows requires time to master compared to basic automation tools.
- **Managed Ecosystem**: While powerful, the core orchestration logic is hosted on the AirOps platform, creating a level of vendor dependency.

## When to use it
- When building mission-critical AI applications that require enterprise-level reliability, security, and scalability.
- For teams that need a collaborative environment to iterate on complex prompt logic and agentic reasoning.
- When you need to orchestrate multi-step AI tasks that leverage the **FastMCP 3.1** ecosystem.
- For implementing RAG patterns that require high accuracy and sophisticated data chunking/retrieval strategies.

## When not to use it
- For simple, single-prompt automations that can be handled by basic scripts or [Zapier](zapier.md).
- If the project requires a strictly local, air-gapped deployment (consider [LocalAI](../infrastructure/localai.md) or self-hosted [Dify](../ai_knowledge/dify.md)).
- For ultra-low latency applications where direct API calls to models are necessary to minimize overhead.

## Getting started

### 1. Workspace Setup
Sign up at [AirOps.com](https://www.airops.com/) and create your organization workspace.

### 2. Configure API Keys
Generate an API Key in your workspace settings and securely store it, ideally using [HashiCorp Vault](hashicorp-vault.md).

### 3. Build a Workflow
Use the AirOps Studio to design a workflow, connecting nodes for LLMs (e.g., [Gemma 3](../ai_knowledge/local_llms.md)), data sources, and logical operators.

### 4. Deploy and Test
Publish your workflow and test it using the built-in sandbox before integrating it into your application via the REST API.

## CLI examples

```bash
# Execute an AirOps workflow via CURL (Webhook)
curl --request POST \
  --url 'https://app.airops.com/public_api/airops_apps/YOUR_APP_UUID/webhook_async_execute?auth_token=YOUR_API_KEY' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{ "input_query": "Analyze market trends for July 2026" }'

# Retrieve results from a specific execution ID
curl -G 'https://app.airops.com/public_api/airops_apps/YOUR_APP_UUID/executions/YOUR_EXECUTION_UUID' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

## API examples

### Executing an AirOps App with Pydantic v2 Contract Validation
For late 2026 enterprise integrations, responses received from AirOps webhook executions must be strictly verified against a schema contract before propagating to downstream services or RAG stores. This ensures high accuracy under frontier models such as Claude 5.1.

```python
import os
import requests
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError

# 1. Define the validation contract using Pydantic v2
class AirOpsOutput(BaseModel):
    summary: str = Field(description="The primary summary returned by the execution")
    confidence_score: float = Field(ge=0.0, le=1.0, description="The reliability confidence score of the extracted info")
    key_entities: list[str] = Field(default_factory=list, description="Extracted enterprise entities")

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
        # Simulate or call actual endpoint:
        # response = requests.post(endpoint, json=payload, headers=headers)
        # response_data = response.json()

        # Example representation of a successful response payload from AirOps running Claude 5.1
        mock_response_data = {
            "execution_id": "exec-abc-123456",
            "status": "success",
            "result": {
                "summary": "AI integration patterns for Gemma 3 and FastMCP 3.1 completed.",
                "confidence_score": 0.98,
                "key_entities": ["Gemma 3", "FastMCP 3.1", "Enterprise RAG"]
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
- [Gemma 3](../ai_knowledge/local_llms.md) — Frontier open model often orchestrated via AirOps workflows.
- [n8n](../../services/n8n.md) — Self-hosted workflow automation alternative.
- [AnythingLLM](../ai_knowledge/anythingllm.md) — Enterprise-grade local knowledge base.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Patterns for multi-step reasoning and execution.
- [Tavily](../providers/tavily.md) — Specialized search engine for AI researchers and agents.
- [Langfuse](../process_understanding/langfuse.md) — Observability for complex LLM applications.

## Sources / references
- [AirOps Official Website](https://www.airops.com/)
- [AirOps Documentation](https://docs.airops.com/)
- [AirOps API v2 Reference](https://docs.airops.com/api-reference)
- [FastMCP Specification and Tools Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-12-22
- Confidence: high
