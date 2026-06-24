# Atlassian Jira MCP Implementations

## What it is
A practical index of Model Context Protocol implementations for Jira/Atlassian workflows, plus official SDK resources used to build custom MCP servers.

## What problem it solves
Jira MCP implementations are fragmented across many repositories. This page provides a fast shortlist of viable options and the core SDK links needed to build or adapt your own server.

## Where it fits in the stack
**Automation / Orchestration Knowledge Page**. It supports tool selection and implementation planning for MCP-based Jira workflows.

## Typical use cases
- Ask Claude to triage a sprint backlog using natural language
- Automate daily issue status summaries via an n8n → MCP workflow
- Let Claude create, update, or close Jira issues from a chat interface
- Build a custom MCP server that bridges an internal system to Jira
- Drive browser-based Jira actions via Playwright MCP when no REST API exists
- Assist frontier models (Claude 4.8 Opus, GPT-5.5) in project management tasks

## Strengths
- No custom integration code needed for common Jira operations
- Natural-language interface hides JQL complexity from end users
- MCP SDK (TypeScript / Python / .NET) is well-documented and actively maintained
- Tools compose well: combine Jira MCP + Slack MCP for automated standup reports

## Limitations
- Hosted MCP servers require storing Atlassian API tokens in config files
- Tool coverage varies per server — not all implementations expose transitions or attachments
- Rate limits on the Jira Cloud REST API apply to all MCP calls underneath
- Playwright MCP adds browser overhead; not suitable for high-frequency automation

## When to use it
- You want to control Jira from a Claude chat session without writing glue code
- You need a quick proof-of-concept for AI-assisted project management
- You are building a custom MCP server to expose an internal system

## When not to use it
- High-volume batch operations (use Jira REST API directly or Automation for Jira)
- Environments where API token storage in config files is not allowed
- When Jira Server/Data Center REST API v2 compatibility is required (check each server's docs)

## Example Jira MCP servers
- [cosmix/jira-mcp](https://mcpservers.org/servers/cosmix/jira-mcp) — Broad Jira Cloud/Server support with JQL-focused tooling.
- [InfinitIQ-Tech/mcp-jira](https://mcpservers.org/servers/InfinitIQ-Tech/mcp-jira) — Python/Jira-API style integration with issue CRUD and transitions.
- [1broseidon/mcp-jira-server](https://mcpservers.org/servers/1broseidon/mcp-jira-server) — REST-focused Jira issue operations.
- [Jongryong/jira_reporter](https://mcpservers.org/servers/Jongryong/jira_reporter) — Reporting-oriented Jira MCP workflow.
- [cyan-24/mcp-server-jira](https://github.com/cyan-24/mcp-server-jira) — Comprehensive Jira Cloud implementation with advanced search and transition support.

## ServiceNow MCP example
- [ServiceNow MCP Server](servicenow-mcp.md) — Existing ServiceNow canonical page in this repo.
- [ServiceNow MCP listing](https://mcpservers.org/servers/michaelbuckner/servicenow-mcp)

## Official MCP implementation resources
- [MCP Intro](https://modelcontextprotocol.io/docs/getting-started/intro)
- [ModelContextProtocol GitHub org](https://github.com/modelcontextprotocol)
- [TypeScript SDK: @modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
- [.NET SDK package: ModelContextProtocol](https://www.nuget.org/packages/ModelContextProtocol)

## Getting started

Atlassian MCP requires an API token and can be configured in Claude Desktop.

### 1. Configure the Atlassian MCP in Claude Desktop
Add the following block to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS).
Replace the placeholder values with your actual Atlassian credentials.

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-atlassian"],
      "env": {
        "ATLASSIAN_SITE_NAME": "your-org.atlassian.net",
        "ATLASSIAN_USER_EMAIL": "you@example.com",
        "ATLASSIAN_API_TOKEN": "YOUR_API_TOKEN_HERE"
      }
    }
  }
}
```

Generate an API token at: `https://id.atlassian.com/manage-profile/security/api-tokens`

### 2. Verify Connection
Once connected, try a simple prompt to verify:
`claude --prompt "Show me the details of PROJ-123"`

## CLI examples

### 1. Useful prompts once the MCP is connected
The MCP exposes Jira as tools that Claude can call directly via terminal-like prompts:

```bash
# Fetch a specific issue
claude --prompt "Show me the details of PROJ-123"

# Search with JQL
claude --prompt "Find all open bugs in project PROJ assigned to me"

# Create an issue
claude --prompt "Create a Jira story in PROJ titled 'Add dark mode toggle' with description '...'"
```

### 2. JQL search via CLI
```bash
claude --prompt "Search Jira using JQL: project = PROJ AND issuetype = Bug AND status != Done"
```

### 3. Transition an issue
```bash
claude --prompt "Move PROJ-456 to 'In Progress'"
```

## API examples

### 1. Minimal custom MCP server (TypeScript)
Use this as a starting point to expose any internal system to Claude as an MCP tool.

```typescript
// my-jira-mcp/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-jira-mcp", version: "1.0.0" });

// Tool: fetch a Jira issue by key
server.tool(
  "get_issue",
  { key: z.string().describe("Jira issue key, e.g. PROJ-123") },
  async ({ key }) => {
    const res = await fetch(
      `https://your-org.atlassian.net/rest/api/3/issue/${key}`,
      {
        headers: {
          Authorization: `Basic ${Buffer.from(
            `${process.env.JIRA_EMAIL}:${process.env.JIRA_TOKEN}`
          ).toString("base64")}`,
          "Content-Type": "application/json",
        },
      }
    );
    const data = await res.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data.fields, null, 2) }],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 2. Playwright MCP: browser automation
```bash
# Register Playwright MCP
claude mcp add playwright -- npx -y @playwright/mcp
```

### 3. Screenshot a page via API/Tool call
```bash
claude --prompt "Take a screenshot of https://your-org.atlassian.net"
```

---

## Selection guidance
- Prefer server implementations with clear auth docs and active maintenance.
- Validate available tools against your required Jira workflows (search, create, transition, comments, reporting).
- For enterprise environments, test payload size, rate-limit behavior, and permission scoping before production use.

## Related tools / concepts
- [MCP Registry](mcp-registry.md)
- [ServiceNow MCP Server](servicenow-mcp.md)
- [Playwright MCP Server](playwright-mcp.md)
- [Model Context Protocol (MCP)](mcp.md)
- [n8n](../../services/n8n.md)
- [Aider](../development_ops/aider.md)
- [GitHub Copilot](../development_ops/github_copilot.md)
- [Claude Code](../development_ops/claude-code-setup.md)

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

- Last reviewed: 2026-06-12
- Confidence: high
