# Webhook

## What it is
A Webhook is a mechanism for one application to provide another application with real-time data. It is often referred to as "reverse API" or "push API" because it sends data automatically when an event occurs, rather than requiring the receiving application to poll for updates.

## What problem it solves
It solves the inefficiency of polling. Instead of an application constantly asking "is there new data?" (which wastes resources and causes delays), Webhooks allow the source application to push data immediately as soon as an event happens (e.g., a new document is scanned, a payment is processed, or a GitHub issue is opened).

## Where it fits in the stack
**Category**: Automation & Orchestration / Communication Pattern

## Typical use cases
- **Automation Triggers**: Triggering an [n8n](../../services/n8n.md) or Zapier workflow when a specific event occurs in an external service.
- **Real-time Notifications**: Sending a message to Telegram or Slack when a server alert is triggered.
- **Data Ingestion**: Pushing documents from a cloud service directly to [Paperless-ngx](../../services/paperless-ngx.md).
- **CI/CD Pipelines**: Triggering a build in GitHub Actions or Gitea when code is pushed.

## Strengths
- **Real-time**: Data is delivered almost instantaneously after an event.
- **Efficient**: Reduces server load and network traffic compared to polling.
- **Universal**: Supported by almost all modern SaaS platforms and automation tools.
- **Simple**: Easy to implement using standard HTTP protocols.

## Limitations
- **Reliability**: If the receiving server is down, the data may be lost unless the sender implements a retry mechanism.
- **Security**: Requires the receiving endpoint to be public or accessible to the sender, necessitating authentication (e.g., API keys, HMAC signatures) to prevent unauthorized requests.
- **Debugging**: Can be harder to debug than standard APIs since you are the receiver and don't always control the source of the request.

## When to use it
- When you need low-latency reactions to events in external systems.
- To connect disparate services that don't have a direct integration.
- To build event-driven architectures.

## When not to use it
- If the sender does not support webhooks (polling may be the only option).
- If the receiving system cannot be made accessible to the sender.
- For transmitting extremely sensitive data without robust encryption and authentication.

## Licensing and cost
- **Protocol**: Webhooks are a pattern based on HTTP standards; there is no license.
- **Service Cost**: Many services include webhook support in their free tiers, but some may gate advanced webhook features (e.g., retries, high volume) behind paid plans.

## Getting started

### Implementation (Receiver)
In an automation tool like [n8n](../../services/n8n.md), you simply add a "Webhook" node, select the HTTP method (usually POST), and copy the generated URL.

### Basic usage (Sender)
In the source application (e.g., GitHub, Stripe), you paste the Webhook URL into the configuration settings and select which events should trigger the request.

## CLI examples
You can test a webhook endpoint using `curl`:

```bash
curl -X POST https://your-webhook-url.com/endpoint \
     -H "Content-Type: application/json" \
     -d '{"event": "test", "data": "hello world"}'
```

## API examples
**Simple Python Receiver (using Flask):**
```python
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    if request.method == 'POST':
        data = request.json
        print(f"Received webhook: {data}")
        return 'Success', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(port=5000)
```

## Related tools / concepts
- [n8n](../../services/n8n.md)
- [Zapier](zapier.md)
- [Model Context Protocol (MCP)](mcp.md)
- [OpenRouter](../ai_knowledge/openrouter.md) (for log streaming via Webhooks)

## Sources / references
- [Webhooks.pb](https://webhooks.pb.design/)
- [n8n Webhook Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
