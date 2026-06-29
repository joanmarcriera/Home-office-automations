# AnyType

## What it is
AnyType is an open-source, decentralized, and local-first personal knowledge management application. It is built on the Anysync protocol, which enables peer-to-peer data synchronization and end-to-end encryption.

## What problem it solves
It provides a unified "operating system for your life," allowing you to store notes, tasks, files, and data in a structured, private environment. It eliminates reliance on centralized cloud providers by keeping your data on your own devices while still offering seamless synchronization.

## Where it fits in the stack
**Category**: Tool / Knowledge Management. It serves as a local-first alternative to Notion or Obsidian, particularly for users who require high privacy and offline-first capabilities.

## Typical use cases
- Organizing personal projects and databases.
- Creating a secure, private digital vault for sensitive information.
- Building custom information workflows without third-party trackers.
- Managing complex personal wikis using an object-oriented data model.

## Strengths
- **Local-first architecture**: Ensures high speed and full offline functionality.
- **Privacy & Security**: End-to-end encryption (E2EE) and peer-to-peer sync.
- **Object-based model**: Highly flexible data structure where everything (tasks, notes, people) is an "Object".
- **Cross-platform**: Available on macOS, Windows, Linux, iOS, and Android.

## Limitations
- **Collaborative features**: While evolving, multi-user real-time collaboration is more complex than centralized alternatives.
- **Learning Curve**: The object-oriented model can be less intuitive for users accustomed to simple folders or flat files.
- **Storage Limits**: While data is local, the free tier of their encrypted sync backup has limits.

## When to use it
- When privacy and data ownership are top priorities.
- If you need a powerful, structured knowledge base that works perfectly without an internet connection.
- When you want an all-in-one workspace that you can truly own.

## When not to use it
- If you need real-time, multi-user simultaneous editing on the same document (like Google Docs).
- If you prefer a simple, plain-text-only workflow (consider [Obsidian](../ai_knowledge/obsidian.md) or [Logseq](../ai_knowledge/logseq.md) instead).

## Getting started

### 1. Installation
Install the Anytype CLI to run a headless server for automation:
```bash
/usr/bin/env bash -c "$(curl -fsSL https://raw.githubusercontent.com/anyproto/anytype-cli/HEAD/install.sh)"
```

### 2. Basic Setup
Initialize a bot account and verify the connection:
```bash
# Create a bot account for automation
anytype auth create my-automation-bot

# Start the headless server
anytype serve
```

### Self-Hosting (Anysync)
For advanced users who want full control over their sync environment, AnyType allows self-hosting the synchronization nodes.

```bash
# Example: Deploying an AnyType node via Docker (Conceptual)
docker run -d \
  --name anytype-node \
  -v ./config:/anytype/config \
  -p 8080:8080 \
  anyproto/any-sync-node:latest
```

Detailed self-hosting instructions for the Anysync protocol components (node, filenode, coordinator) are available in the [Anyproto GitHub](https://github.com/anyproto).

## CLI examples
The Anytype CLI allows running Anytype as a headless server for automation.

```bash
# Start the headless server
anytype serve

# Create a bot account for automation
anytype auth create my-automation-bot

# Generate an API key
anytype auth apikey create "Local Integration"
```

## API examples
Anytype exposes an HTTP API (typically at `http://127.0.0.1:31012`) when running via the CLI or desktop app with API access enabled.

### List Spaces (Python)
```python
import requests

url = "http://127.0.0.1:31012/spaces"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Anytype-Version": "2025-11-08"
}

response = requests.get(url, headers=headers)
spaces = response.json()

for space in spaces.get("spaces", []):
    print(f"Space: {space['name']} (ID: {space['id']})")
```

## Licensing and cost
- **Open Source**: Yes (Any Source Code License / GPL-3.0)
- **Cost**: Free for local use and basic sync; paid tiers for increased encrypted backup storage.
- **Self-hostable**: Yes (Anysync protocol components).

## Related tools / concepts
- [Obsidian](../ai_knowledge/obsidian.md) (Markdown-based alternative)
- [Logseq](../ai_knowledge/logseq.md) (Privacy-focused outliner)
- [SilverBullet](silverbullet.md) (Markdown-based programmable wiki)
- [Nextcloud](../../services/nextcloud.md) (Self-hosted cloud suite)
- [Syncthing](../../services/syncthing.md) (P2P file synchronization)
- [Local LLMs](../ai_knowledge/local_llms.md) (Can be used to process local AnyType data)
- [KnowledgeOps Standards](../../standards.md) (Governance for local knowledge)

## Sources / References
- [Official Website](https://anytype.io/)
- [Anyproto GitHub](https://github.com/anyproto)
- [AnyType Documentation](https://doc.anytype.io/)

## Contribution Metadata
- Last reviewed: 2026-07-20
- Confidence: high
