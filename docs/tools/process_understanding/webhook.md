# Webhook

## What it is
A Webhook is a standard, lightweight method for an application to deliver real-time data payloads to another application immediately upon the occurrence of a specific event. Unlike polling, which involves repeated and resource-heavy queries to an API, webhooks employ an event-driven "push" pattern over standard HTTP POST. In early January 2027, webhooks serve as the vital "nervous system" linking inference engines (like [Ollama](../../services/ollama.md)) to external automated triggers and FastMCP 3.1 Task Protocol event buses.

## What problem it solves
In an ecosystem dominated by long-running or asynchronous agentic processes, polling introduces unacceptable latency and wastes valuable CPU and network resources. Webhooks solve this "latency gap." For instance, when an autonomous agent triggers a long-running research or parsing pipeline using models like Claude 5.6, GPT-5.6, or Gemini 4.0 Ultra, downstream tools do not need to repeatedly query the status; the processing service simply dispatches an HTTP POST request containing verified results directly to the orchestrator (e.g., [n8n](../../services/n8n.md)) the moment it completes.

## Where it fits in the stack
**Integration & Orchestration**. Sitting between the **Inference Plane** (LLMs and Agent Runtimes) and the **Execution Plane** (Home Automation and local services), webhooks facilitate clean, asynchronous, event-driven communications across the home lab and enterprise infrastructure.

## Typical use cases
- **Paperless-ngx AI Ingestion**: Post-consumption hooks triggering an LLM to analyze a newly parsed receipt and auto-classify tags.
- **Asynchronous Agent Hand-offs**: An agent utilizing the [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) FastMCP 3.1 Task Protocol triggers a webhook to notify a human-in-the-loop when confirmation is required.
- **GitOps and CI/CD Pipelines**: A Gitea webhook firing a local container deployment flow upon a push event on a specific branch.
- **Live System Alerts**: Emitting JSON telemetry payloads from [Sentry](sentry.md) or [Datadog](datadog.md) directly to an AI self-healing daemon.

## Strengths
- **Near-Instantaneous**: Ensures immediate data transport and execution reaction times without any polling lag.
- **High Resource Efficiency**: Minimal network and compute footprint, executing code only when an actual event is broadcast.
- **Broad Compatibility**: Operates on universal, standard HTTP/JSON structures supported by every modern framework and language.
- **Decoupled Architecture**: Allows senders and receivers to evolve independently without requiring shared database structures.

## Limitations
- **Exposed Attack Surface**: Receiving endpoints must be reachable from the internet or internal networks, necessitating strict security (HMAC signatures).
- **Transient Delivery Failures**: If the receiving endpoint is briefly offline, the webhook payload can be lost permanently unless retry/dead-letter queues are configured.
- **Unpredictable Spikes**: High-volume systems can generate sudden bursts of event deliveries, which can overwhelm unprepared receivers.

## When to use it
- When you require real-time synchronization between independent, self-hosted services.
- To handle asynchronous notifications from long-running agent tasks without locking up execution threads.
- When designing scalable, decoupled event-driven workflows inside visual orchestrators like [n8n](../../services/n8n.md).

## When not to use it
- For continuous, high-frequency streaming (e.g., real-time microphone audio feeds or camera video frames) where WebSockets or gRPC are more appropriate.
- When absolute, guaranteed sequential delivery is required and the emitting system does not support transactional queuing.

## Getting started

### Exposing Local Ports
For local homelab development behind firewalls, you can temporarily expose a port to receive public webhook callbacks (e.g., from OpenRouter or GitHub):
```bash
# Using modern secure tunnels
npm install -g localtunnel
lt --port 8000
```

### Receiving Webhooks (Docker)
For running a dedicated, secure webhook receiver daemon that executes bash files or Docker triggers:
```bash
docker run -d -p 9000:9000 -v /path/to/hooks:/etc/webhook adnanh/webhook:latest
```

## CLI examples

### Mocking a Webhook Dispatch (cURL)
To test a receiving endpoint, you can mock an incoming POST delivery with a customized JSON payload:
```bash
curl -X POST http://localhost:8000/webhook \
     -H "Content-Type: application/json" \
     -H "X-Hub-Signature-256: sha256=abcdef1234567890" \
     -d '{"event": "agent_task_completed", "agent_id": "claude-5.6"}'
```

### Inspecting Local Webhook Traffic
```bash
# Verify active ports listening for incoming HTTP callback requests
ss -tlnp | grep 8000
```

## API examples

### Secure Webhook Receiver (FastAPI) with HMAC Cryptographic Verification and Pydantic v2 Validation
This example showcases a production-grade FastAPI receiver in Python. It parses incoming payloads, performs strict SHA256 HMAC cryptographic signature validation to ensure the requests originate from a trusted sender, and validates the event metadata structures against a strict Pydantic v2 schema.

```python
import hmac
import hashlib
import json
from datetime import datetime
from typing import Dict, Any, Optional, Literal
from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI()
WEBHOOK_SHARED_SECRET = b"homelab_super_secure_webhook_key"

# 1. Define strict Pydantic v2 schema for incoming event payloads
class WebhookPayload(BaseModel):
    event_type: Literal["agent_task_completed", "document_ingested", "alert_triggered"]
    timestamp: datetime
    sender_id: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$")
    payload: Dict[str, Any]
    priority: int = Field(1, ge=1, le=5)

    @field_validator("payload")
    @classmethod
    def validate_payload_non_empty(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        if not v:
            raise ValueError("Event payload dictionary cannot be empty")
        return v

# 2. Secure Route Handler with HMAC validation
@app.post("/webhook")
async def receive_webhook(request: Request, x_signature_256: str = Header(None)):
    if not x_signature_256:
        raise HTTPException(status_code=401, detail="Missing required security signature header")

    # Read raw body to perform cryptographic HMAC verification
    raw_body = await request.body()

    # Calculate expected HMAC SHA256 signature
    expected_signature = hmac.new(
        WEBHOOK_SHARED_SECRET,
        raw_body,
        hashlib.sha256
    ).hexdigest()

    # Prevent timing attacks using compare_digest
    if not hmac.compare_digest(f"sha256={expected_signature}", x_signature_256):
        raise HTTPException(status_code=403, detail="Cryptographic verification failed: Invalid signature")

    # Parse JSON and validate utilizing strict Pydantic v2 schemas
    try:
        json_data = json.loads(raw_body.decode("utf-8"))
        validated_event = WebhookPayload.model_validate(json_data)

        # In a real pipeline, dispatch tasks based on validated_event.event_type
        print(f"Verified event '{validated_event.event_type}' received from '{validated_event.sender_id}'")
        return {"status": "accepted", "message": "Event processed successfully"}

    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Payload validation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting secure Webhook receiver on port 8000...")
    # uvicorn.run(app, host="127.0.0.1", port=8000)
```

## Related tools / concepts
- [n8n](../../services/n8n.md) — Self-hosted automation orchestrator natively driven by inbound webhooks.
- [Zapier](../automation_orchestration/zapier.md) — Enterprise workflow manager that utilizes cloud webhook receivers.
- [Make](../automation_orchestration/make.md) — Visual automation service supporting high-throughput webhook routes.
- [OpenRouter](../ai_knowledge/openrouter.md) — LLM router capable of streaming agentic events via Webhooks.
- [Sentry](sentry.md) — Application monitoring platform triggering automated webhooks on error thresholds.
- [Gitea](../../services/gitea.md) — Git manager supporting deep post-receive and pre-receive webhook hooks.
- [Standards and Conventions](../../standards.md) — Taxonomy standards for secure payload designs.
- [Event-Driven Architecture](../../knowledge_base/patterns/index.md) — Foundational homelab blueprint utilizing decoupled webhook events.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Communication protocols utilizing async JSON events.

## Sources / references
- [Webhooks.fyi Comprehensive Guide](https://webhooks.fyi/)
- [FastAPI Webhook Security Guidelines](https://fastapi.tiangolo.com/advanced/using-request-directly/)
- [n8n Webhook Node Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
