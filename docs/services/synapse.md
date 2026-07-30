# Matrix Synapse

Matrix Synapse is the reference "homeserver" implementation for Matrix, providing a decentralized, real-time communication backbone for the late October / November 2026 agentic ecosystem.

## What it is
Synapse is the reference "homeserver" implementation for Matrix, an open standard for decentralized, real-time communication. As of late October / November 2026, **v1.168.0** is the current stable release, featuring Matrix 1.14 compatibility, native support for Room v13, and optimized federation for low-latency agentic messaging and autonomous agent federation.

## What problem it solves
It allows you to own your communication infrastructure. By hosting your own Synapse server, you control your messages, identity, and data, while remaining part of the global Matrix federation. It specifically solves the privacy and control issues associated with centralized platforms, providing a secure substrate for agent-to-agent coordination without reliance on third-party API providers.

## Where it fits in the stack
**Category**: Services / Communication. It is the **backend coordination layer** for the [Element](element.md) client and Matrix-based automations. It serves as the primary transport layer for autonomous agents to communicate across different homelabs and organizations, often integrated with [Local LLMs](../tools/ai_knowledge/local_llms.md) for private inference.

## Typical use cases
- **Private Communication**: Hosting a secure, end-to-end encrypted (E2EE) chat server for families or teams.
- **Agentic Messaging**: Allowing agents like Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, Gemma 3, and Qwen 3.6 to send reports or receive instructions via Matrix.
- **Federated Automation**: Coordinating workflows across different homeservers using Matrix bots and the [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md).
- **Home Automation Hub**: Receiving notifications from [Home Assistant](home-assistant.md) or [n8n](n8n.md).

## Strengths
- **Reference Implementation**: Most feature-complete Matrix homeserver.
- **Robust Federation**: Reliable communication across the decentralized Matrix network.
- **Extensive Integration**: Support for bridges (Telegram, Discord, Slack) and numerous bots.
- **OIDC Support**: Native integration with [Authentik](authentik.md) for enterprise-grade identity management.
- **Agent Friendly**: Standardized APIs for automated message routing and room management.

## Limitations
- **Resource Intensive**: Requires significant RAM (1GB+ baseline) and a dedicated PostgreSQL database for production usage.
- **Complexity**: Setting up federation and media repos requires careful DNS and reverse proxy (Nginx/Traefik) configuration.
- **Disk Usage**: Media storage can grow rapidly without aggressive cleanup policies.

## When to use it
- When you want to self-host your own Matrix homeserver with full feature support.
- When you need a reliable, federated communication backend for your homelab.
- When coordinating multi-agent workflows using [MCP 3.1 Task Protocol](../tools/automation_orchestration/mcp.md) over decentralized channels.

## When not to use it
- On very low-resource hardware like a Raspberry Pi 3 (consider Conduit instead).
- If you only need simple, non-federated notifications where a lightweight [ntfy](https://ntfy.sh/) instance would suffice.

## Getting started

### Docker Compose Baseline
Synapse requires a PostgreSQL database for production usage.

```yaml
services:
  synapse:
    image: matrixdotorg/synapse:v1.168.0
    restart: unless-stopped
    environment:
      - SYNAPSE_CONFIG_PATH=/data/homeserver.yaml
    volumes:
      - ./data:/data
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_DB=synapse
      - POSTGRES_USER=synapse
      - POSTGRES_PASSWORD=your_password
    volumes:
      - ./pgdata:/var/lib/postgresql/data
```

### Initial Configuration
Generate the initial config file:
```bash
docker run -it --rm \
    -v ./data:/data \
    -e SYNAPSE_SERVER_NAME=my.matrix.host \
    -e SYNAPSE_REPORT_STATS=yes \
    matrixdotorg/synapse:v1.168.0 generate
```

## CLI examples

```bash
# Generate a new admin user (requires running inside the container)
docker exec -it synapse register_new_matrix_user -c /data/homeserver.yaml http://localhost:8008

# Check the Synapse version
docker exec -it synapse python3 -m synapse.app.homeserver --version

# Run the database maintenance tool
docker exec -it synapse synapse_review_recent_signups -c /data/homeserver.yaml
```

## API examples

### Python: Async Agentic Report with Pydantic v2 Validation
The following example demonstrates an asynchronous Python client sending an agentic message to a Synapse homeserver and validating the JSON response using Pydantic v2.

```python
import asyncio
import httpx
from pydantic import BaseModel, Field

# Define Pydantic v2 schemas for request and response validation
class MatrixEventResponse(BaseModel):
    event_id: str = Field(..., description="The unique ID of the sent event")

class AgentReportPayload(BaseModel):
    msgtype: str = Field("m.text", description="Matrix message type")
    body: str = Field(..., description="The body/content of the message")

HOMESERVER_URL = "https://matrix.example.com"
ACCESS_TOKEN = "your_access_token"
ROOM_ID = "!room_id:example.com"

async def send_agent_message_async(text: str) -> MatrixEventResponse:
    url = f"{HOMESERVER_URL}/_matrix/client/v3/rooms/{ROOM_ID}/send/m.room.message"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Validate payload structure using Pydantic v2
    payload = AgentReportPayload(body=f"[AGENT REPORT]: {text}")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=payload.model_dump(),
            timeout=10.0
        )
        response.raise_for_status()

        # Validate response structure using Pydantic v2
        validated_response = MatrixEventResponse.model_validate(response.json())
        return validated_response

async def main():
    try:
        res = await send_agent_message_async("Monthly storage audit complete. 2TB reclaimed under MCP 3.1 specifications.")
        print(f"Successfully sent event. Event ID: {res.event_id}")
    except Exception as e:
        print(f"Failed to send agentic message: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### OIDC Integration (Authentik)
Update your `homeserver.yaml` to delegate authentication to [Authentik](authentik.md):

```yaml
oidc_providers:
  - idp_id: authentik
    idp_name: "Authentik"
    issuer: "https://authentik.example.com/application/o/matrix/"
    client_id: "<client_id>"
    client_secret: "<client_secret>"
    scopes: ["openid", "profile", "email"]
    user_mapping_provider:
      config:
        localpart_template: "{{ user.preferred_username }}"
        display_name_template: "{{ user.name }}"
```

## Related tools / concepts
- [Element](element.md) — The recommended client for Synapse.
- [Authentik](authentik.md) — For SSO and identity management.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — For agentic task execution over Matrix (MCP 3.1 compatibility).
- [n8n](n8n.md) — For sending automated notifications to Matrix rooms.
- [Home Assistant](home-assistant.md) — For integrating smart home alerts.
- [Vikunja](vikunja.md) — For task-based coordination often synced via Matrix.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — For private inference-driven agents on Matrix.

## Sources / References
- [Synapse GitHub Repository](https://github.com/element-hq/synapse)
- [Official Documentation](https://element-hq.github.io/synapse/latest/)
- [Matrix.org](https://matrix.org/)
- [Synapse Workers Documentation](https://element-hq.github.io/synapse/latest/workers.html)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-11-05
