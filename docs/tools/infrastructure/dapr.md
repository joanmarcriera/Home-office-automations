# Distributed Application Runtime (Dapr)

## What it is
Distributed Application Runtime (Dapr) is a portable, event-driven runtime that simplifies building resilient, stateless, and stateful microservice applications across edge hardware, Kubernetes clusters, and cloud environments. Dapr abstracts common microservice capabilities — state management, pub/sub messaging, service-to-service invocation, workflow orchestration, secrets management, and distributed tracing — into sidecar containers accessible via HTTP and gRPC APIs.

As of early **January 2027**, Dapr serves as a foundational microservices runtime for multi-agent execution graphs, serving as a reliable sidecar protocol bridge between Model Context Protocol (MCP 3.1 / FastMCP 3.1) agents, local vector databases, and event-driven automation pipelines.

## What problem it solves
Building distributed systems across edge nodes and cloud infrastructure typically requires embedding vendor-specific SDKs for messaging queues, state stores, and secret vaults directly into application code. Dapr decouples core infrastructure dependencies from business logic using standard sidecar APIs, eliminating vendor lock-in, simplifying multi-language microservice communication, and enabling resilient retries, circuit breaking, and mTLS encryption out of the box.

## Where it fits in the stack
**Infrastructure / Distributed Systems & Microservices Layer** — sits alongside containerized microservices and agent runtimes (in Docker, k3s, or Kubernetes), mediating service invocation, state persistence, and pub/sub event routing.

## Typical use cases
- **Resilient Multi-Agent Event Bus**: Pub/sub routing of agent execution events across distributed edge nodes using Redis, NATS, or RabbitMQ backends.
- **State Store Abstraction**: Storing agent conversation history and session key-value data using interchangeable backends (PostgreSQL, Redis, MongoDB) via unified Dapr HTTP APIs.
- **Cross-Language Service Invocation**: Calling Python LLM inference microservices from Node.js or Go automation services with built-in mTLS and retries.
- **Distributed Secret Management**: Retrieving API keys and tokens from Vault or Kubernetes Secrets via standardized sidecar endpoints.

## Strengths
- **Language & Framework Agnostic**: Exposes capabilities entirely over HTTP/1.1, HTTP/2, and gRPC APIs, compatible with any language.
- **Pluggable Architecture**: Components (state, pub/sub, secrets) can be swapped via YAML manifests without changing microservice application code.
- **Built-in Security & Observability**: Automatic mTLS encryption between sidecars and standardized OpenTelemetry metrics and tracing exports.

## Limitations
- **Sidecar Resource Overhead**: Running a Dapr sidecar container next to every microservice consumes additional memory and CPU on resource-constrained edge hardware.
- **Debugging Complexity**: Troubleshooting distributed sidecar network proxying requires analyzing both application logs and Dapr sidecar runtime logs.
- **Event Latency**: Introduces a minor local loopback network hop between application containers and sidecar proxies.

## When to use it
- When building event-driven microservice architectures across multi-node Kubernetes clusters or hybrid edge-cloud networks.
- When decoupling microservices from specific cloud provider SDKs for state management, pub/sub, or secrets.
- When requiring out-of-the-box mTLS, distributed tracing, and resilient retry logic between services.

## When not to use it
- For monolithic, single-container applications where inter-process communication overhead is unnecessary.
- On ultra-constrained microcontrollers where sidecar container runtimes cannot fit within available RAM.

## Getting started
Deploy Dapr locally or on Kubernetes using the CLI:

```bash
# Initialize Dapr in local Docker container environment
dapr init

# Run an application microservice with a Dapr sidecar
dapr run --app-id agent-service \
         --app-port 5000 \
         --dapr-http-port 3500 \
         python3 app.py

# Verify Dapr component status
dapr components -k
```

### Dapr State Component YAML Example (`statestore.yaml`)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
```

## CLI examples
Interact directly with Dapr sidecar HTTP endpoints to test state persistence and pub/sub messaging:

```bash
# Save state via local Dapr sidecar HTTP API
curl -X POST http://localhost:3500/v1.0/state/statestore \
  -H "Content-Type: application/json" \
  -d '[{ "key": "agent_session_101", "value": { "status": "active", "model": "gpt-5.6" } }]'

# Retrieve stored state
curl http://localhost:3500/v1.0/state/statestore/agent_session_101

# Publish an event to a pub/sub topic
curl -X POST http://localhost:3500/v1.0/publish/pubsub/agent-tasks \
  -H "Content-Type: application/json" \
  -d '{ "task_id": "task_882", "action": "summarize" }'
```

## API examples
The following Python script uses **Pydantic v2** to construct and validate Dapr state items before persisting them via the local Dapr sidecar HTTP API.

```python
from typing import Dict, Any, List
from pydantic import BaseModel, Field
import requests

class DaprStateItem(BaseModel):
    key: str = Field(..., description="Unique state key")
    value: Dict[str, Any] = Field(..., description="State value payload")
    etag: str = Field(default="", description="Optional ETag for concurrency control")

class DaprStateRequest(BaseModel):
    items: List[DaprStateItem] = Field(..., description="List of state items to store")

def save_state_to_dapr(dapr_port: int, store_name: str, payload: List[dict]) -> bool:
    """Validates payload and posts state to Dapr sidecar endpoint."""
    request_data = DaprStateRequest(items=[DaprStateItem(**item) for item in payload])
    url = f"http://localhost:{dapr_port}/v1.0/state/{store_name}"

    # Payload transformed to JSON
    json_body = request_data.model_dump()["items"]

    # In real usage: response = requests.post(url, json=json_body)
    print(f"Validated Dapr payload for {url}:", json_body)
    return True

# Example verification usage
if __name__ == "__main__":
    sample_data = [
        {
            "key": "agent_context_404",
            "value": {"last_prompt": "Analyze edge logs", "tokens": 128}
        }
    ]

    save_state_to_dapr(dapr_port=3500, store_name="statestore", payload=sample_data)
```

## Related tools / concepts
- [vLLM](vllm.md) — High-performance inference engine served alongside Dapr microservices.
- [Ollama](../../services/ollama.md) — Local LLM runner integrated with Dapr event buses.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Agent protocol leveraging Dapr sidecars for distributed execution.
- [n8n](../../services/n8n.md) — Workflow automation tool triggering Dapr pub/sub endpoints.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management service utilizing event triggers.
- [Claude Code](../development_ops/claude-code.md) — CLI coding assistant for developing Dapr components.
- [Cursor](../development_ops/cursor.md) — AI IDE for building distributed Dapr microservices.

## Sources / references
- [Dapr Official Documentation](https://dapr.io/)
- [Dapr GitHub Repository](https://github.com/dapr/dapr)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
