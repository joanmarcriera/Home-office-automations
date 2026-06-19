# Webhook

## What it is
A Webhook is a standard method for an application to provide other applications with real-time information. It delivers data to other applications as it happens, meaning you get data immediately, rather than polling for it. In 2026, webhooks are the primary "nervous system" of agentic workflows, connecting LLM events to system actions.

## What problem it solves
It enables event-driven architectures and real-time integrations between disparate systems without the need for constant, resource-heavy API polling. In the context of AI, it allows providers to "push" events (like log completion, trace generation, or tool-use results) directly to your custom processing logic.

## Where it fits in the stack
**Category**: Process & Understanding / Integration Pattern. It acts as the trigger mechanism for [n8n](../../services/n8n.md) workflows and custom MCP (Model Context Protocol) servers.

## Typical use cases
- **Real-Time Log Streaming**: Receiving JSON payloads from OpenRouter immediately after an LLM call is completed.
- **Agentic Triggers**: Starting an automated test run or deployment when an AI agent pushes code to a repository.
- **Smart Notifications**: Sending filtered alerts to Discord or Slack based on anomaly detection in an AI agent's reasoning traces.
- **Inbound Data Ingestion**: Triggering a document parsing job (e.g., via OCRmyPDF) when a new file is uploaded to storage.

## Strengths
- **Real-Time**: Minimizes latency between an event occurring and the system responding.
- **Efficiency**: Significantly reduces network traffic and server load compared to high-frequency polling.
- **Standardized**: Most webhooks use standard HTTP POST requests with JSON payloads, making them language-agnostic.
- **Scalability**: Decouples the producer of information from the consumer, allowing for asynchronous processing.

## Limitations
- **Security**: The receiving endpoint must be robustly protected (e.g., via shared secrets, signature verification, or IP whitelisting).
- **Reliability**: If the receiving server is down, data may be lost unless the provider implements an exponential backoff retry policy.
- **Order of Delivery**: Webhooks do not always guarantee that events will arrive in the exact order they occurred.

## When to use it
- When you need real-time data synchronization between two independent systems.
- When building event-driven architectures where actions should be triggered by external state changes.
- To avoid the performance overhead and rate-limiting issues associated with constant API polling.

## When not to use it
- When the order of events is strictly critical and the provider does not offer sequencing guarantees.
- For extremely high-frequency data streams (e.g., sensor data) where WebSockets or a message bus (like Kafka) are more efficient.
- If the receiving infrastructure cannot handle sudden, massive bursts of traffic.

## Getting started

### Basic Concept
Webhooks are passive receivers. To use them, you typically provide an endpoint URL to a service provider (like GitHub, OpenRouter, or a self-hosted service).

### Testing Tools
- **Webhook.site**: For instant visual inspection of incoming payloads.
- **ngrok / localtunnel**: To expose your local development server to the public internet for testing.

## CLI examples

### Mocking a Webhook Request
```bash
# Test a local webhook endpoint with a mock JSON payload
curl -X POST http://localhost:8000/webhook \
     -H "Content-Type: application/json" \
     -H "X-Webhook-Secret: my-secret" \
     -d '{"event": "agent_started", "data": {"id": "jules-01", "task": "audit"}}'
```

### Exposing Local Port
```bash
# Use localtunnel to expose a local port for receiving external webhooks
npx localtunnel --port 8000
```

## API examples

### FastAPI Receiver (Python)
```python
from fastapi import FastAPI, Request, Header, HTTPException

app = FastAPI()
SECRET_TOKEN = "your-shared-secret"

@app.post("/webhook")
async def receive_webhook(request: Request, x_webhook_secret: str = Header(None)):
    # Validate the request source
    if x_webhook_secret != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid secret")

    # Process the incoming JSON payload
    payload = await request.json()
    print(f"Received event: {payload.get('event')}")
    return {"status": "accepted"}
```

## Related tools / concepts
- [n8n](../../services/n8n.md) (The industry standard for processing webhooks in 2026)
- [Zapier](../automation_orchestration/zapier.md) (Cloud-based webhook automation)
- [OpenRouter](../ai_knowledge/openrouter.md) (Log streaming destination)
- [FastAPI](https://fastapi.tiangolo.com/) (Preferred framework for high-performance receivers)
- [Event-Driven Architecture](../../knowledge_base/patterns/index.md)
- [REST API](../../standards.md)
- [Model Context Protocol (MCP)](../frameworks/microsoft-agent-framework.md) (Often triggered by webhook events)
- [Cloudflare Mesh](../../services/cloudflare-mesh.md) (Securely routing webhooks through tunnels)

## Sources / references
- [Webhooks.fyi - The Webhook Standard Guide](https://webhooks.fyi/)
- [OpenRouter Webhook Guide](https://openrouter.ai/docs/guides/features/broadcast/webhook)
- [GitHub Webhooks Documentation](https://docs.github.com/webhooks)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
