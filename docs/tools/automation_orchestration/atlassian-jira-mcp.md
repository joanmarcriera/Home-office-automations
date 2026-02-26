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

## ServiceNow MCP example
- [ServiceNow MCP Server](servicenow-mcp.md) — Existing ServiceNow canonical page in this repo.
- [ServiceNow MCP listing](https://mcpservers.org/servers/michaelbuckner/servicenow-mcp)

## Official MCP implementation resources
- [MCP Intro](https://modelcontextprotocol.io/docs/getting-started/intro)
- [ModelContextProtocol GitHub org](https://github.com/modelcontextprotocol)
- [TypeScript SDK: @modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
- [.NET SDK package: ModelContextProtocol](https://www.nuget.org/packages/ModelContextProtocol)

---

## Practical examples

### 1 — Configure the Atlassian MCP in Claude Desktop

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

---

### 2 — Useful prompts once the MCP is connected

The MCP exposes Jira as tools that Claude can call directly.
These natural-language prompts map to real tool calls:

| Goal | Example prompt |
|---|---|
| Fetch a specific issue | `Show me the details of PROJ-123` |
| Search with JQL | `Find all open bugs in project PROJ assigned to me` |
| Create an issue | `Create a Jira story in PROJ titled "Add dark mode toggle" with description "..."` |
| Transition an issue | `Move PROJ-456 to "In Progress"` |
| Add a comment | `Add a comment to PROJ-789: "Blocked on API access, following up tomorrow"` |
| Sprint report | `List all issues completed in the last sprint of PROJ` |

---

### 3 — JQL cheat-sheet for MCP search calls

The `searchJiraIssuesUsingJql` tool accepts standard JQL.
Copy-paste these into a prompt or pass them directly to the tool:

```jql
-- Open bugs assigned to me
project = PROJ AND issuetype = Bug AND assignee = currentUser() AND status != Done ORDER BY priority DESC

-- Issues updated in the last 7 days
project = PROJ AND updated >= -7d ORDER BY updated DESC

-- Unresolved issues in the current sprint
project = PROJ AND sprint in openSprints() AND resolution = Unresolved

-- High-priority blockers
project = PROJ AND priority in (Highest, High) AND issueType = Bug AND status != Done

-- Issues created this week by me
project = PROJ AND created >= startOfWeek() AND reporter = currentUser()
```

---

### 4 — Minimal custom MCP server (TypeScript)

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

// Tool: run a JQL search
server.tool(
  "search_issues",
  { jql: z.string().describe("JQL query string") },
  async ({ jql }) => {
    const res = await fetch(
      `https://your-org.atlassian.net/rest/api/3/search?jql=${encodeURIComponent(jql)}&maxResults=20`,
      {
        headers: {
          Authorization: `Basic ${Buffer.from(
            `${process.env.JIRA_EMAIL}:${process.env.JIRA_TOKEN}`
          ).toString("base64")}`,
        },
      }
    );
    const data = await res.json();
    const summary = data.issues.map((i: any) => `${i.key}: ${i.fields.summary}`);
    return {
      content: [{ type: "text", text: summary.join("\n") }],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

Run with:

```bash
JIRA_EMAIL=you@example.com JIRA_TOKEN=xxx npx ts-node index.ts
```

Register it in `claude_desktop_config.json` the same way as the hosted server (section 1), pointing `command` to `npx ts-node` and `args` to the script path.

---

### 5 — Playwright MCP: browser automation examples

The Playwright MCP (`@playwright/mcp`) lets Claude drive a real browser.
Configure it alongside the Atlassian MCP:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

Useful prompts once connected:

| Goal | Example prompt |
|---|---|
| Screenshot a page | `Take a screenshot of https://example.com` |
| Fill and submit a form | `Go to the login page at <url>, fill in the username and password fields, and click Login` |
| Extract table data | `Navigate to <url> and extract the data from the main table as JSON` |
| End-to-end test flow | `Open <url>, add item to cart, proceed to checkout, and confirm the order total shown` |

---

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
- Confidence: high
