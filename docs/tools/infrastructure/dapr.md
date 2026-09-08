# Dapr (Distributed Application Runtime)

## What it is
Dapr (Distributed Application Runtime) is an open-source, portable, event-driven runtime that simplifies building resilient, microservices-based, and distributed applications. Dapr provides developer-friendly building block APIs—such as State Management, Service-to-Service Invocation, Pub/Sub Messaging, Workflow Orchestration, Secrets Management, and Distributed Locking—exposed via HTTP and gRPC sidecar proxies.

In cloud-native infrastructure, Kubernetes clusters (K3s), and distributed AI agent architectures, Dapr abstracts underlying cloud infrastructure and message brokers, allowing applications to run seamlessly across local edge hardware, hybrid cloud, and Kubernetes environments.

## What problem it solves
Developing distributed microservice applications and multi-agent AI execution pipelines requires complex code for handling retry policies, state serialization, service discovery, pub/sub message brokers, and secret retrieval. Dapr decouples this infrastructure boilerplate from application code by providing standardized sidecar APIs, enabling language-agnostic service communication and effortless switching between backend providers (e.g., Redis, Kafka, PostgreSQL, or HashiCorp Vault) without code changes.

## Where it fits in the stack
**Infrastructure / Distributed Middleware & Service Mesh** — operates as a sidecar application runtime layer in Kubernetes (K3s) or containerized environments.

## Typical use cases
- **Multi-Agent State & Memory Management**: Managing agent execution state, session history, and key-value memory across distributed LLM workers using Dapr State Management APIs.
- **Event-Driven AI Pipelines**: Triggering downstream document processing or vector indexing tasks asynchronously using Dapr Pub/Sub messaging.
- **Microservice Service Discovery & Resiliency**: Enabling secure, mTLS-encrypted inter-service invocation and automatic retry logic between microservices on K3s.

## Strengths
- **Language Agnostic**: Exposed via standard HTTP/1.1 and gRPC endpoints, accessible from Python, Go, Node.js, Rust, or C++.
- **Pluggable Components**: Easily swap underlying state stores, message queues, or secret stores via declarative YAML manifests.
- **Built-in Resiliency & Observability**: Includes mTLS encryption, circuit breaking, automatic retries, and OpenTelemetry tracing out of the box.

## Limitations
- **Sidecar Overhead**: Adds a minor CPU and memory footprint per pod/container for running the Dapr sidecar process (`daprd`).
- **Learning Curve for Component Schemas**: Requires understanding Dapr YAML component resource definitions and custom resource definitions (CRDs) in Kubernetes.
- **Event Ordering Trade-offs**: Asynchronous pub/sub event processing requires careful design if strict global event ordering is needed.

## When to use it
- When building distributed, containerized microservice stacks on Kubernetes (K3s) or Docker Compose.
- When decoupling application code from specific cloud vendor databases, key-value stores, or message queues.
- When orchestrating asynchronous distributed AI agent workflows and event streams.

## When not to use it
- For monolithic, single-process applications running on a single server without distributed components.
- In ultra-resource-constrained microcontrollers where sidecar process overhead cannot be accommodated.

## Getting started
### Installing Dapr CLI & Initializing Local Environment
Install the Dapr CLI and initialize local Docker sidecars:

```bash
# Install Dapr CLI
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | bash

# Initialize Dapr in local standalone mode (launches Redis and Zipkin)
dapr init

# Verify Dapr runtime components
dapr components
```

### Declarative Component Definition (`statestore.yaml`)
Define a Redis state store component manifest:

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
Running an application with a Dapr sidecar and invoking state management:

```bash
# Run a Python microservice with a Dapr sidecar proxy listening on HTTP port 3500
dapr run --app-id agent-worker --app-port 5000 --dapr-http-port 3500 python3 app.py

# Save state directly via the Dapr HTTP sidecar API
curl -X POST http://localhost:3500/v1.0/state/statestore \
  -H "Content-Type: application/json" \
  -d '[{"key": "agent_session_1", "value": {"status": "active", "task": "indexing"}}]'

# Get state via Dapr HTTP API
curl http://localhost:3500/v1.0/state/statestore/agent_session_1
```

## API examples
The following Python script demonstrates storing and retrieving state using the official `dapr-sdk` client library.

```python
from dapr.clients import DaprClient
import json

STATE_STORE_NAME = "statestore"

def manage_agent_state(session_id: str, payload: dict):
    """Interacts with Dapr State Management API via Python SDK."""
    with DaprClient() as client:
        # Save state
        client.save_state(
            store_name=STATE_STORE_NAME,
            key=session_id,
            value=json.dumps(payload)
        )
        print(f"Saved state for session '{session_id}' via Dapr.")

        # Read state back
        state_response = client.get_state(store_name=STATE_STORE_NAME, key=session_id)
        if state_response.data:
            retrieved_data = json.loads(state_response.data.decode("utf-8"))
            print("Retrieved state payload:", retrieved_data)
            return retrieved_data
        return None

if __name__ == "__main__":
    sample_data = {"agent": "copilot", "status": "idle", "step": 42}
    manage_agent_state("session_99", sample_data)
```

## Related tools / concepts
- [Diagrid Catalyst](diagrid-catalyst.md)
- [Kubernetes (K3s)](k3s.md)
- [Docker](docker.md)
- [Temporal](../orchestration/temporal.md)
- [Argo Workflows](../orchestration/argo-workflows.md)
- [OpenTelemetry Collector](../process_understanding/opentelemetry-collector.md)
- [HashiCorp Vault](../automation_orchestration/hashicorp-vault.md)

## Sources / references
- [Dapr Official Documentation](https://dapr.io/)
- [Dapr GitHub Repository](https://github.com/dapr/dapr)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
