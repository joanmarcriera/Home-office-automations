# Atlassian Jira MCP Implementations

## What it is
A practical index of Model Context Protocol implementations for Jira/Atlassian workflows, plus official SDK resources used to build custom MCP servers.

## What problem it solves
Jira MCP implementations are fragmented across many repositories. This page provides a fast shortlist of viable options and the core SDK links needed to build or adapt your own server.

## Where it fits in the stack
**Automation / Orchestration Knowledge Page**. It supports tool selection and implementation planning for MCP-based Jira workflows.

## Example Jira MCP servers
- [cosmix/jira-mcp](https://mcpservers.org/servers/cosmix/jira-mcp) — Broad Jira Cloud/Server support with JQL-focused tooling.
- [InfinitIQ-Tech/mcp-jira](https://mcpservers.org/servers/InfinitIQ-Tech/mcp-jira) — Python/Jira-API style integration with issue CRUD and transitions.
- [1broseidon/mcp-jira-server](https://mcpservers.org/servers/1broseidon/mcp-jira-server) — REST-focused Jira issue operations.
- [Jongryong/jira_reporter](https://mcpservers.org/servers/Jongryong/jira_reporter) — Reporting-oriented Jira MCP workflow.

## ServiceNow MCP example
- [ServiceNow MCP Server](servicenow-mcp.md) — Existing ServiceNow canonical page in this repo.
- [ServiceNow MCP listing](https://mcpservers.org/servers/michaelbuckner/servicenow-mcp)

## Official MCP implementation resources
- [MCP Intro](https://modelcontextprotocol.io/docs/getting-started/intro)
- [ModelContextProtocol GitHub org](https://github.com/modelcontextprotocol)
- [TypeScript SDK: @modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
- [.NET SDK package: ModelContextProtocol](https://www.nuget.org/packages/ModelContextProtocol)

## Selection guidance
- Prefer server implementations with clear auth docs and active maintenance.
- Validate available tools against your required Jira workflows (search, create, transition, comments, reporting).
- For enterprise environments, test payload size, rate-limit behavior, and permission scoping before production use.

## Related tools / concepts
- [MCP Registry](mcp-registry.md)
- [ServiceNow MCP Server](servicenow-mcp.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)

## Sources / References
- [Issue source: requested MCP examples](https://github.com/joanmarcriera/Home-office-automations/issues/24)
- [Jira MCP example (cosmix)](https://mcpservers.org/servers/cosmix/jira-mcp)
- [Jira MCP example (InfinitIQ)](https://mcpservers.org/servers/InfinitIQ-Tech/mcp-jira)
- [Jira MCP example (1broseidon)](https://mcpservers.org/servers/1broseidon/mcp-jira-server)
- [Jira MCP reporter example](https://mcpservers.org/servers/Jongryong/jira_reporter)
- [ServiceNow MCP example](https://mcpservers.org/servers/michaelbuckner/servicenow-mcp)
- [MCP Intro docs](https://modelcontextprotocol.io/docs/getting-started/intro)
- [MCP TypeScript SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
- [MCP .NET SDK package](https://www.nuget.org/packages/ModelContextProtocol)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
