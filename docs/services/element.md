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
While Element is a GUI, the Matrix ecosystem provides powerful CLI tools like `matrix-commander` for automation:

```bash
# Send a message to a room via CLI
matrix-commander --room "!roomid:matrix.org" --message "Hello from the CLI!"

# Listen for messages and trigger a local script
matrix-commander --listen --on-message "./handle_message.sh"

# Get room info
matrix-commander --room "!roomid:matrix.org" --info
```

## API examples
The Matrix Client-Server API allows for direct programmatic interaction.

### Python (using `matrix-nio`)
```python
import asyncio
from nio import AsyncClient

async def main():
    client = AsyncClient("https://matrix.org", "@your_user:matrix.org")
    await client.login("your_password")

    await client.room_send(
        room_id="!your_room_id:matrix.org",
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": "Alert: Motion detected in the garden!"
        }
    )
    await client.close()

asyncio.run(main())
```

### Curl Example
```bash
# Send a simple text message via API
curl -XPOST -d '{"msgtype":"m.text", "body":"Hello World"}' \
     "https://matrix.org/_matrix/client/r0/rooms/!roomid:matrix.org/send/m.room.message?access_token=YOUR_ACCESS_TOKEN"
```

## Related tools / concepts
- [Synapse](https://github.com/element-hq/synapse) — The most common Matrix homeserver.
- [Dendrite](https://github.com/element-hq/dendrite) — A next-generation, high-performance Matrix homeserver.
- [Home Assistant](home-assistant.md) — Frequently integrated with Element for notifications.
- [Authentik](authentik.md) — Used for SSO authentication into Element/Matrix.
- [Bridges](https://matrix.org/bridges/) — Connect Matrix to other services like Telegram and Discord.
- [Nextcloud](nextcloud.md) — For file storage and cloud services alongside communication.
- [Gitea](gitea.md) — For hosting code and triggering notifications to Element.

## Links
- [Official Website](https://element.io/)
- [GitHub Repository](https://github.com/vector-im/element-web)
- [Matrix Protocol](https://matrix.org/)

## Backlog
- Set up Matrix Synapse homeserver for full self-hosting.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-20

## Sources / References
- https://element.io/
- https://github.com/vector-im/element-web
- https://matrix.org/docs/api/client-server/
- https://github.com/8go/matrix-commander
