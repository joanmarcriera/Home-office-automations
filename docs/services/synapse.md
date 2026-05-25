# Matrix Synapse

## What it is
Synapse is the reference "homeserver" implementation for Matrix, an open standard for decentralized, real-time communication.

## What problem it solves
It allows you to own your communication infrastructure. By hosting your own Synapse server, you control your messages, identity, and data, while remaining part of the global Matrix federation.

## Where it fits in the stack
**Category**: Services / Communication. It is the **backend coordination layer** for the [Element](element.md) client and Matrix-based automations.

## Typical use cases
- **Private Communication**: Hosting a server for family or a private community.
- **Automation Hub**: Acting as a central receiver for bot notifications (Home Assistant, n8n).
- **Federated Messaging**: Communicating with users on other Matrix servers (like `matrix.org`) without using a centralized service.

## Strengths
- **Reference Implementation**: Most feature-complete Matrix homeserver.
- **Robust Federation**: Reliable communication across the decentralized Matrix network.
- **Extensive Integration**: Support for bridges (Telegram, Discord, Slack) and numerous bots.
- **OIDC Support**: Native integration with [Authentik](authentik.md) for identity management.

## Limitations
- **Resource Intensive**: Requires significant RAM (1GB+ baseline) and a dedicated PostgreSQL database for performance.
- **Complexity**: Setting up federation and media repos requires careful DNS and reverse proxy configuration.

## When to use it
- When you want to self-host your own Matrix homeserver.
- When you need a reliable, federated communication backend for your homelab.
- When you want to integrate with [Authentik](authentik.md) for SSO across your chat apps.

## When not to use it
- On very low-resource hardware (consider [Dendrite](https://github.com/element-hq/dendrite) or [Conduit](https://conduit.rs/)).
- If you only need simple notifications without federation or multi-user support.

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

## OIDC Integration (Authentik)
To enable SSO via [Authentik](authentik.md), update your `homeserver.yaml`:

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
- [Vikunja](vikunja.md) — For task-based coordination.
- [PostgreSQL](https://www.postgresql.org/) — The required database for performance.

## Backlog
- [ ] Perform quarterly technical freshness audit.

## Sources / References
- [Synapse GitHub Repository](https://github.com/element-hq/synapse)
- [Official Documentation](https://element-hq.github.io/synapse/latest/)
- [Matrix.org](https://matrix.org/)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
