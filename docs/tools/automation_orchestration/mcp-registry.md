# MCP Registry

## What it is
The official central repository and discovery platform for Model Context Protocol (MCP) servers. It acts as a standardized directory for tools and integrations that follow the MCP specification.

## What problem it solves
It addresses the fragmentation in the MCP ecosystem by providing a single, authoritative source for discovering publicly available MCP servers. It standardizes server metadata using the `server.json` format, enabling easier publishing and discovery for developers and users.

## Where it fits in the stack
**Infra / Router**: It provides the infrastructure for tool discovery and acts as a registry for routing agent requests to the correct tools.

## Typical use cases
- **Extending Agent Capabilities**: Discovering new MCP servers to add features like calendar access, database management, or smart home control to AI agents.
- **Developer Publishing**: Providing a standardized way for developers to share their custom MCP servers with the community.
- **Protocol Compliance**: Ensuring that tools follow the official MCP standards for metadata and communication.

## Strengths
- **Authoritative Source**: Official central hub for the MCP ecosystem.
- **Community-Owned**: Managed by the open-source community with backing from major AI industry players.
- **Standardized Format**: Enforces the use of `server.json` for consistent tool representation.
- **Unified Discovery**: Creators publish once, and all consumers can reference the same canonical data.

## Limitations
- **Early Stage**: Currently in preview, with the ecosystem and server list still actively growing.
- **Metadata Only**: Does not host the server binaries or code directly, acting instead as a pointer to other registries (NPM, PyPI, Docker Hub).

## When to use it
- When looking for pre-built integrations for MCP-compatible agents (like Claude Desktop).
- When developing a new MCP server and wanting to ensure it is discoverable by the community.

## When not to use it
- When requiring private or internal-only tool integrations that should not be public.
- When using non-MCP compliant tool-calling frameworks.

## Related tools / concepts
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [Claude Desktop](../development_ops/vscode.md) (as a primary MCP client)
- [PulseMCP](https://pulsemcp.com/) (community alternative)

## Sources / references
- [Official MCP Registry Announcement](https://modelcontextprotocol.info/tools/registry/)
- [Registry Browser](https://registry.modelcontextprotocol.io/)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
