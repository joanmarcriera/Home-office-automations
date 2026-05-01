# Webhook

## What it is
A Webhook is a standard method for an application to provide other applications with real-time information. It delivers data to other applications as it happens, meaning you get data immediately, rather than polling for it.

## What problem it solves
It enables event-driven architectures and real-time integrations between disparate systems without the need for constant, resource-heavy API polling. In the context of AI, it allows providers to "push" events (like log completion or trace generation) directly to your custom processing logic.

## Where it fits in the stack
**Category**: Process & Understanding / Integration Pattern

## Typical use cases
- **Real-Time Log Streaming**: Receiving JSON payloads from OpenRouter immediately after an LLM call is completed.
- **CI/CD Triggers**: Starting an automated test run when an AI agent pushes code to a repository.
- **Notifications**: Sending alerts to Discord or Slack when an anomaly is detected in an AI agent's performance.
- **Data Ingestion Pipelines**: Triggering a document parsing job when a new file is uploaded to S3.

## Strengths
- **Real-Time**: Low latency between the event and the notification.
- **Efficiency**: Reduces network traffic and server load compared to polling.
- **Simple Implementation**: Most webhooks use standard HTTP POST requests with JSON payloads.
- **Universal Support**: Almost every modern SaaS and AI tool supports webhooks.

## Limitations
- **Security**: Endpoint must be protected (e.g., via shared secrets or IP whitelisting) to prevent unauthorized data injection.
- **Reliability**: If the receiving server is down, the data may be lost (unless the provider implements retries).
- **One-Way**: Webhooks are typically "fire and forget"; the sender doesn't wait for a complex response.

## Getting started

### Basic Receiver (Python/FastAPI)
```python
from fastapi import FastAPI, Request, Header, HTTPException

app = FastAPI()

SECRET_TOKEN = "your-shared-secret"

@app.post("/webhook")
async def receive_webhook(request: Request, x_webhook_secret: str = Header(None)):
    if x_webhook_secret != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid secret")

    payload = await request.json()
    print(f"Received event: {payload}")
    return {"status": "success"}
```

## Related tools / concepts
- [n8n](../../services/n8n.md) (Excellent for receiving and processing webhooks)
- [Zapier](../automation_orchestration/zapier.md)
- [OpenRouter](../ai_knowledge/openrouter.md) (Log streaming destination)
- [Event-Driven Architecture](../../knowledge_base/patterns/index.md)

## Sources / references
- [Webhooks.fyi](https://webhooks.fyi/)
- [OpenRouter Webhook Broadcast Guide](https://openrouter.ai/docs/guides/features/broadcast/webhook)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
