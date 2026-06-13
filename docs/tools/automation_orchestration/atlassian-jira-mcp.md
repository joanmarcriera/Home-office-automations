# Atlassian Jira MCP

## What it is
Atlassian Jira MCP implementations are Model Context Protocol (MCP) servers that expose Jira's project management capabilities to AI agents. They allow frontier models like [Claude 4.8 Opus](../providers/anthropic.md) to interact directly with Jira issues, sprints, and backlogs using natural language.

## What problem it solves
It eliminates the need for manual context switching between chat interfaces and Jira dashboards. By providing a standardized interface for issue retrieval, creation, and updates, it enables autonomous agents to perform project management tasks, triage bugs, and generate status reports without custom glue code.

## Where it fits in the stack
**Automation / Orchestration**. It acts as a bridge between the **Agentic** layer and enterprise project management tools.

## Typical use cases
- **Automated Bug Triage**: Asking Claude to analyze incoming issues and assign labels or priority.
- **Sprint Summaries**: Generating daily standup reports or sprint velocity summaries via an n8n workflow.
- **Natural Language JQL**: Searching for complex issue patterns using conversational queries instead of manual JQL.
- **Issue Lifecycle Management**: Moving stories through transitions (e.g., "In Progress" to "Review") directly from the terminal.

## Strengths
- **Native Tooling**: Maps Jira's REST API directly to LLM tools.
- **Reduced Friction**: Enables managing complex projects without leaving the coding environment (e.g., [Claude Code](../development_ops/claude-code-setup.md)).
- **Extensible**: The TypeScript and Python SDKs allow for easy customization of exposed tools.
- **Ecosystem Support**: Works with standard MCP clients including Claude Desktop and Zed.

## Limitations
- **Auth Management**: Requires secure storage of Atlassian API tokens in configuration files.
- **Rate Limiting**: Subject to Jira Cloud's REST API rate limits.
- **Tool Consistency**: Implementation quality and available tools (e.g., attachments, transitions) vary between different community servers.
- **Security Scoping**: Requires careful permission management in Jira to prevent accidental mass-updates by agents.

## When to use it
- When you want to manage Jira project state through an AI agent or terminal assistant.
- When building automated workflows that need to read from or write to Jira.
- When performing bulk issue updates based on natural language criteria.

## When not to use it
- For high-frequency, high-volume automated data migrations (use the Jira REST API directly).
- In environments where storing long-lived API tokens on local machines is prohibited.
- When requiring complex UI interactions not covered by the REST API (though Playwright MCP can mitigate this).

## Getting started
Most Jira MCP servers are distributed via `npm` or `pip`.

### 1. Generate an API Token
Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) and create a new token.

### 2. Configure Claude Desktop
Add the following to your `claude_desktop_config.json`:
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

## CLI examples
You can interact with Jira MCP servers using `npx` or custom runners.

```bash
# Run the official Anthropic Jira MCP server locally for testing
ATLASSIAN_SITE_NAME="..." ATLASSIAN_API_TOKEN="..." npx @anthropic-ai/mcp-server-atlassian

# Search for Jira issues using JQL from the command line (via an MCP client)
mcp-client call atlassian search_issues --jql "project = PROJ AND status = Open"

# Transition an issue to 'Done'
mcp-client call atlassian transition_issue --issue_key "PROJ-123" --status "Done"
```

## API examples
Building a custom Jira MCP tool using the TypeScript SDK.

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({ name: "custom-jira", version: "1.0.0" });

server.tool(
  "get_issue_details",
  { key: z.string().describe("Jira issue key, e.g., PROJ-123") },
  async ({ key }) => {
    // Fetch issue from Jira API
    const response = await fetch(`https://your-org.atlassian.net/rest/api/3/issue/${key}`, {
      headers: { "Authorization": `Basic ${process.env.AUTH_TOKEN}` }
    });
    const data = await response.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data.fields.summary) }]
    };
  }
);
```

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md) — The underlying standard.
- [ServiceNow MCP](servicenow-mcp.md) — Equivalent for ServiceNow environments.
- [Claude Code](../development_ops/claude-code-setup.md) — Primary client for MCP-based Jira management.
- [n8n](../../services/n8n.md) — For orchestrating complex Jira workflows.
- [Playwright MCP](playwright-mcp.md) — For browser-based Jira automation.
- [FastMCP 3.0](mcp.md) — Modern framework for building MCP servers.
- [GitHub Copilot](../development_ops/github_copilot.md) — Supports similar extensions for GitHub issues.
- [Aider](../development_ops/aider.md) — Terminal-based agent that can leverage MCP.

## Sources / references
- [Anthropic Atlassian MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/atlassian)
- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [Jira Cloud REST API Reference](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Atlassian API Token Management](https://id.atlassian.com/manage-profile/security/api-tokens)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
