# Webhook

## What it is
A Webhook is a standard method for an application to provide other applications with real-time information. It delivers data to other applications as it happens, meaning you get data immediately, rather than polling for it. In the June 2026 agentic ecosystem, webhooks serve as the "nervous system" for event-driven automation, enabling Claude 4.8 Opus and GPT-5.5 agents to react to external triggers instantly.

## What problem it solves
It enables event-driven architectures and real-time integrations between disparate systems without the need for constant, resource-heavy API polling. For autonomous agents, webhooks solve the "latency gap" in multi-step reasoning, allowing a long-running process (like a deep research task) to notify the agent or a downstream service as soon as results are available.

## Where it fits in the stack
**Category**: Process & Understanding / Integration Pattern. It sits between the **Inference Plane** (LLMs) and the **Execution Plane** (Automations), facilitating asynchronous communication.

## Typical use cases
- **Real-Time Log Streaming**: Receiving JSON payloads from OpenRouter immediately after an LLM call is completed for observability.
- **Agentic CI/CD**: Triggering an [OpenHands](../development_ops/openhands.md) environment when a webhook signals a new PR on Gitea.
- **Proactive Maintenance**: Sending alerts to [Sentry](sentry.md) when an AI agent's self-healing script fails.
- **Automated Ingestion**: Triggering [OCRmyPDF](ocrmypdf.md) when a document is uploaded to [MinIO](../intake_storage/minio.md).

## Strengths
- **Instantaneous**: Eliminates the delay inherent in polling intervals.
- **Resource Efficient**: Only consumes compute resources when an actual event occurs.
- **Scalable**: Modern providers like OpenRouter and Cloudflare support high-throughput webhook broadcasting.
- **Standardized**: Uses universal HTTP POST/JSON patterns compatible with all major frameworks.

## Limitations
- **Exposed Surface**: Receiving endpoints must be public or reachable via a tunnel, requiring strict security (HMAC signatures).
- **Delivery Guarantees**: Without a retry mechanism on the sender's side, transient network failures can lead to missed events.
- **Statelessness**: Individual webhooks carry no state; the receiver must handle session management or persistence.

## When to use it
- When you need real-time data synchronization between independent systems.
- For long-running agentic tasks where the model cannot wait for a synchronous response.
- When building event-driven workflows in [n8n](../../services/n8n.md) or [Zapier](../automation_orchestration/zapier.md).

## When not to use it
- For high-frequency streaming (e.g., raw audio/video frames) where WebSockets or gRPC are more efficient.
- When strict ordering of events is required and not guaranteed by the provider.
- If the receiving system cannot handle spiky, unpredictable bursts of traffic.

## Getting started

### Local Setup
For local development, you need a way to receive webhooks behind a firewall.
```bash
# Install localtunnel to expose a local port
npm install -g localtunnel
lt --port 8000
```

### Docker Setup
Use a generic webhook receiver like `adnanh/webhook` for simple shell script execution:
```bash
docker run -d -p 9000:9000 -v /path/to/config:/etc/webhook adnanh/webhook:latest
```

## CLI examples

### Testing an Endpoint
```bash
# Mock a webhook delivery to a local FastAPI server
curl -X POST http://localhost:8000/webhook \
     -H "Content-Type: application/json" \
     -H "X-Hub-Signature-256: sha256=..." \
     -d '{"event": "agent_task_completed", "agent_id": "claude-4.8-opus"}'
```

### Exposing Local Ports
```bash
# Use ngrok for more advanced features like inspection and replay
ngrok http 8000
```

## API examples

### Secure Receiver (Python/FastAPI)
Using HMAC verification for June 2026 security standards.
```python
import hmac
import hashlib
from fastapi import FastAPI, Request, Header, HTTPException

app = FastAPI()
WEBHOOK_SECRET = b"your_secure_secret"

@app.post("/webhook")
async def handle_webhook(request: Request, x_signature: str = Header(None)):
    payload = await request.body()

    # Verify HMAC signature
    signature = hmac.new(WEBHOOK_SECRET, payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(f"sha256={signature}", x_signature or ""):
        raise HTTPException(status_code=403, detail="Invalid signature")

    data = await request.json()
    print(f"Verified event: {data['event']}")
    return {"status": "accepted"}
```

## Related tools / concepts
- [n8n](../../services/n8n.md) — Primary platform for webhook-driven agentic workflows.
- [Zapier](../automation_orchestration/zapier.md) — Enterprise-grade webhook orchestration.
- [Make](../automation_orchestration/make.md) — Visual workflow automation with native webhook support.
- [OpenRouter](../ai_knowledge/openrouter.md) — Supports real-time broadcast of agent logs.
- [Sentry](sentry.md) — Observability via error-triggered webhooks.
- [Gitea](../../services/gitea.md) — Source control with extensive webhook integration for CI/CD.
- [REST API](../../standards.md) — The underlying protocol for most webhook deliveries.
- [Event-Driven Architecture](../../knowledge_base/patterns/index.md) — The design pattern powered by webhooks.
- [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Model Context Protocol, often integrated with webhook notifications.

## Sources / references
- [Webhooks.fyi Guide](https://webhooks.fyi/)
- [OpenRouter Webhook Features (June 2026)](https://openrouter.ai/docs/guides/features/broadcast)
- [FastAPI Webhook Documentation](https://fastapi.tiangolo.com/advanced/using-request-directly/)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
