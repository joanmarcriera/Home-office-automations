# Matrix Synapse

Matrix Synapse is the reference "homeserver" implementation for Matrix, providing a decentralized, real-time communication backbone for the June 2026 agentic ecosystem.

## What it is
Synapse is the reference "homeserver" implementation for Matrix, an open standard for decentralized, real-time communication. As of June 2026, **v1.155.0** is the current stable release, featuring Matrix 1.12 compatibility, native support for Room v12, and optimized federation for low-latency agentic messaging.

## What problem it solves
It allows you to own your communication infrastructure. By hosting your own Synapse server, you control your messages, identity, and data, while remaining part of the global Matrix federation. It specifically solves the privacy and control issues associated with centralized platforms like Discord or Slack.

## Where it fits in the stack
**Category**: Services / Communication. It is the **backend coordination layer** for the [Element](element.md) client and Matrix-based automations. It serves as the primary transport layer for autonomous agents to communicate across different homelabs and organizations.

## Typical use cases
- **Private Communication**: Hosting a secure, end-to-end encrypted (E2EE) chat server for families or teams.
- **Agentic Messaging**: Allowing agents like Claude 4.8 Opus to send reports or receive instructions via Matrix.
- **Federated Automation**: Coordinating workflows across different homeservers using Matrix bots.
- **Home Automation Hub**: Receiving notifications from [Home Assistant](home-assistant.md) or [n8n](n8n.md).

## Strengths
- **Reference Implementation**: Most feature-complete Matrix homeserver.
- **Robust Federation**: Reliable communication across the decentralized Matrix network.
- **Extensive Integration**: Support for bridges (Telegram, Discord, Slack) and numerous bots.
- **OIDC Support**: Native integration with [Authentik](authentik.md) for enterprise-grade identity management.
- **Scalability**: Supports worker-based scaling for high-concurrency environments.

## Limitations
- **Resource Intensive**: Requires significant RAM (1GB+ baseline) and a dedicated PostgreSQL database for production usage.
- **Complexity**: Setting up federation and media repos requires careful DNS and reverse proxy (Nginx/Traefik) configuration.
- **Disk Usage**: Media storage can grow rapidly without aggressive cleanup policies.

## When to use it
- When you want to self-host your own Matrix homeserver with full feature support.
- When you need a reliable, federated communication backend for your homelab.
- When you want to integrate with [Authentik](authentik.md) for SSO across your chat infrastructure.

## When not to use it
- On very low-resource hardware like a Raspberry Pi 3 (consider [Conduit](https://conduit.rs/) instead).
- If you only need simple, non-federated notifications (a simple Telegram bot might suffice).

## Getting started

### Docker Compose Baseline
Synapse requires a PostgreSQL database for production usage.

```yaml
services:
  synapse:
    image: matrixdotorg/synapse:latest
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
    matrixdotorg/synapse:latest generate
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

### Python: Sending an Agentic Report
```python
import requests
import json

HOMESERVER_URL = "https://matrix.example.com"
ACCESS_TOKEN = "your_access_token"
ROOM_ID = "!room_id:example.com"

def send_agent_message(text):
    url = f"{HOMESERVER_URL}/_matrix/client/v3/rooms/{ROOM_ID}/send/m.room.message"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {
        "msgtype": "m.text",
        "body": f"[AGENT]: {text}"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

print(send_agent_message("Monthly storage audit complete. 2TB reclaimed."))
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
- [Matrix Protocol](https://matrix.org/) — The underlying communication standard.
- [n8n](n8n.md) — For sending automated notifications to Matrix rooms.
- [Home Assistant](home-assistant.md) — For integrating smart home alerts.
- [Vikunja](vikunja.md) — For task-based coordination often synced via Matrix.
- [PostgreSQL](https://www.postgresql.org/) — The required database for performance.
- [Redis](https://redis.io/) — For high-performance worker scaling.

## Sources / References
- [Synapse GitHub Repository](https://github.com/element-hq/synapse)
- [Official Documentation](https://element-hq.github.io/synapse/latest/)
- [Matrix.org](https://matrix.org/)
- [Synapse Workers Documentation](https://element-hq.github.io/synapse/latest/workers.html)

## Backlog
- [x] Perform technical freshness audit (June 2026).

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-16
