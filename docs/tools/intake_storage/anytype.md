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
Download the desktop client for your platform from the [official downloads page](https://anytype.io/download).

### 2. Enable API Access
Anytype provides a local API (typically on port 31009). To use it with AI agents:
1. Open Anytype Settings > API Keys.
2. Create a new API Key.
3. Use the provided credentials to connect via [Model Context Protocol](../automation_orchestration/mcp.md).

### Hello World Example
Verify your local API is reachable and retrieve your API key via the CLI:
```bash
npx -y @anyproto/anytype-mcp get-key
```

## CLI examples
```bash
# Start the Anytype MCP server (requires ANYTYPE_API_BASE_URL and OPENAPI_MCP_HEADERS)
npx -y @anyproto/anytype-mcp

# List available spaces via the local CLI tool (if installed)
anytype-cli spaces list

# Sync local data with your self-hosted node
any-sync-node --config ./config.yml
```

## API examples
Anytype is best automated via its [MCP server](https://github.com/anyproto/anytype-mcp). Below is a conceptual tool call for an AI agent:

```json
// Create a new 'Note' object in a specific space
anytype.create_object({
  "spaceId": "YOUR_SPACE_ID",
  "body": {
    "name": "Meeting Notes 2026-07-21",
    "type": "Note",
    "folder": "Work"
  }
})
```

For direct local API access (REST):
```bash
curl -X GET "http://127.0.0.1:31009/api/v1/spaces" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Anytype-Version: 2025-11-08"
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
