# Element

Element is a secure, decentralized communication app built on the [Matrix](../knowledge_base/patterns/communication.md) protocol.

## What it is
Element (formerly Riot) is the flagship client for the Matrix protocol, providing a user-friendly interface for end-to-end encrypted messaging, voice, and video calls. It operates in a decentralized manner, meaning users can choose their own "homeserver" while still communicating with users on other servers.

## What problem it solves
It solves the problem of "walled gardens" in communication (like WhatsApp or Slack) by using an open standard. It provides sovereign control over data without sacrificing modern features like multi-device sync, rich media sharing, and integrations.

## Where it fits in the stack
Element sits in the **Communication and Collaboration** layer. It serves as the primary interface for both human-to-human communication and bot-to-human notifications within a self-hosted ecosystem.

## Typical use cases
- **Personal Messaging**: Secure, E2EE alternative to commercial messaging apps.
- **Team Collaboration**: Organizing projects and discussions into "Spaces" and "Rooms".
- **Home Automation Notifications**: Receiving alerts from services like Home Assistant or custom scripts.
- **Bridging**: Acting as a unified interface for Discord, Telegram, and Slack via Matrix bridges.

## Strengths
- **Sovereignty**: Full control over your data when self-hosted.
- **E2EE**: High-grade end-to-end encryption for all conversations.
- **Extensibility**: Powerful API and "Widget" system for custom integrations.
- **Open Standard**: Interoperable with any other Matrix client or server.

## Limitations
- **UX Complexity**: The decentralized nature (homeservers, cross-signing) can be confusing for new users compared to centralized apps.
- **Resource Intensive**: Running a full Matrix homeserver (Synapse) can be resource-heavy for low-end hardware.

## When to use it
- When you need secure, encrypted communication that you fully control.
- When you want to bridge multiple messaging platforms (Discord, Telegram, Slack) into a single client.
- When you need a reliable notification channel for your home automation system.

## When not to use it
Do not use Element as a drop-in replacement for simple SMS-style family messaging if users are not ready to understand homeservers, key backup, and device verification. For large regulated organizations, validate Matrix retention, moderation, discovery, and e-discovery requirements before replacing Slack or Microsoft Teams.

## Getting started

### Web/Desktop App
The easiest way to start is by using the hosted version or the desktop client:
1. Download Element from [element.io](https://element.io/get-started).
2. Create an account on the default `matrix.org` server or specify your own.

### Docker (Self-Hosted Web Client)
To host the Element web interface yourself (requires a separate homeserver like Synapse):

```yaml
services:
  element:
    image: vectorim/element-web:latest
    ports:
      - "8080:80"
    restart: always
```

## CLI examples
While Element is a GUI, the Matrix ecosystem provides CLI tools like `matrix-commander` for automation:

```bash
# Install the CLI in an isolated Python environment
python3 -m pip install --user matrix-commander

# Log in interactively and store credentials for later commands
matrix-commander --login password

# Send a message using exported room configuration
: "${MATRIX_ROOM_ID:?set MATRIX_ROOM_ID to a Matrix room ID}"
matrix-commander --room "$MATRIX_ROOM_ID" --message "Hello from the home-office automation stack"

# Get room info for the same configured room
matrix-commander --room "$MATRIX_ROOM_ID" --room-info
```

## API examples
The Matrix Client-Server API allows direct programmatic interaction. The examples below are runnable after exporting real credentials from a bot or test account.

### Python (using `matrix-nio`)
```python
import asyncio
import os
from nio import AsyncClient

HOMESERVER = os.environ["MATRIX_HOMESERVER"]
USER_ID = os.environ["MATRIX_USER_ID"]
PASSWORD = os.environ["MATRIX_PASSWORD"]
ROOM_ID = os.environ["MATRIX_ROOM_ID"]

async def main():
    client = AsyncClient(HOMESERVER, USER_ID)
    login_response = await client.login(PASSWORD)
    if getattr(login_response, "access_token", None) is None:
        raise RuntimeError(f"Matrix login failed: {login_response}")
    await client.room_send(
        room_id=ROOM_ID,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": "Alert: Motion detected in the garden!"
        },
    )
    await client.close()

asyncio.run(main())
```

### Curl example
```bash
: "${MATRIX_HOMESERVER:=https://matrix.org}"
: "${MATRIX_ROOM_ID:?set MATRIX_ROOM_ID to a Matrix room ID}"
: "${MATRIX_ACCESS_TOKEN:?set MATRIX_ACCESS_TOKEN to a bot or user access token}"

curl -X POST \
  -H "Authorization: Bearer $MATRIX_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"msgtype":"m.text","body":"Hello from curl"}' \
  "$MATRIX_HOMESERVER/_matrix/client/v3/rooms/$MATRIX_ROOM_ID/send/m.room.message/$(date +%s)"
```

## Related tools / concepts
- [Synapse](https://github.com/element-hq/synapse) — The most common Matrix homeserver.
- [Dendrite](https://github.com/element-hq/dendrite) — A next-generation, high-performance Matrix homeserver.
- [Home Assistant](home-assistant.md) — Frequently integrated with Element for notifications.
- [Authentik](authentik.md) — Used for SSO authentication into Element/Matrix.
- [Bridges](https://matrix.org/bridges/) — Connect Matrix to other services like Telegram and Discord.
- [Nextcloud](nextcloud.md) — For file storage and cloud services alongside communication.
- [Gitea](gitea.md) — For hosting code and triggering notifications to Element.
- [Paperless-ngx](paperless-ngx.md) — For notifying users when new documents are indexed.
- [SearXNG](searXNG.md) — For secure search results sharing within Element rooms.
- [Vikunja](vikunja.md) — For task management notifications and team coordination.

## Links
- [Official Website](https://element.io/)
- [GitHub Repository](https://github.com/vector-im/element-web)
- [Matrix Protocol](https://matrix.org/)

## Backlog
- Set up Matrix Synapse homeserver for full self-hosting.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-08

## Sources / References
- https://element.io/
- https://github.com/vector-im/element-web
- https://matrix.org/docs/api/client-server/
- https://github.com/8go/matrix-commander
