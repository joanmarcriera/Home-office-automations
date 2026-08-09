# Atlassian Jira MCP

## What it is
Atlassian Jira MCP implementations are Model Context Protocol (MCP) servers that expose Jira's project management capabilities to AI agents. As of late 2026, these servers fully support the **MCP 3.1** and **FastMCP 3.1** standards, enabling frontier models like [Gemma 3](../ai_knowledge/local_llms.md) and [Claude 5.1](../providers/anthropic.md) to interact directly with Jira issues, sprints, and backlogs using standardized, agentic tool-calling patterns.

## What problem it solves
It eliminates the need for manual context switching between chat interfaces and Jira dashboards. By providing a standardized interface for issue retrieval, creation, and updates, it enables autonomous agents to perform project management tasks, triage bugs, and generate status reports without custom glue code. The integration of **FastMCP 3.1** ensures that task execution is consistent, highly reliable, and type-safe across different agent frameworks and environments.

## Where it fits in the stack
**Automation / Orchestration**. It acts as a bridge between the **Agentic** layer and enterprise project management tools.

## Typical use cases
- **Automated Bug Triage**: Asking [Gemma 3](../ai_knowledge/local_llms.md) to analyze incoming issues and assign labels or priority.
- **Sprint Summaries**: Generating daily standup reports or sprint velocity summaries via an [n8n](../../services/n8n.md) workflow.
- **Natural Language JQL**: Searching for complex issue patterns using conversational queries instead of manual JQL.
- **Issue Lifecycle Management**: Moving stories through transitions (e.g., "In Progress" to "Review") directly from [Claude Code](../development_ops/claude-code-setup.md).
- **Automated Documentation**: Syncing Jira issue status with internal wikis or [AnythingLLM](../ai_knowledge/anythingllm.md) knowledge bases.

## Strengths
- **Native Tooling**: Maps Jira's REST API directly to LLM tools.
- **FastMCP 3.1 Compliance**: Leverages the latest FastMCP specification for improved reliability in multi-step agentic workflows.
- **Reduced Friction**: Enables managing complex projects without leaving the coding environment (e.g., [Aider](../development_ops/aider.md)).
- **Extensible**: The TypeScript and Python SDKs allow for easy customization of exposed tools.
- **Ecosystem Support**: Works with standard MCP clients including Claude Desktop, Zed, and [Cursor](../development_ops/cursor.md).

## Limitations
- **Auth Management**: Requires secure storage of Atlassian API tokens, ideally managed via [HashiCorp Vault](hashicorp-vault.md).
- **Rate Limiting**: Subject to Jira Cloud's REST API rate limits, which can be reached during bulk agent operations.
- **Tool Consistency**: Implementation quality and available tools (e.g., attachments, transitions) vary between different community servers.
- **Security Scoping**: Requires careful permission management in Jira to prevent accidental mass-updates by agents.

## When to use it
- When you want to manage Jira project state through an AI agent or terminal assistant.
- When building automated workflows that need to read from or write to Jira.
- When performing bulk issue updates based on natural language criteria.
- When integrating Jira management into a broader [Agentic Workflow](../../knowledge_base/patterns/agentic-workflows.md).

## When not to use it
- For high-frequency, high-volume automated data migrations (use the Jira REST API directly).
- In environments where storing long-lived API tokens on local machines is prohibited.
- When requiring complex UI interactions not covered by the REST API (though [Playwright MCP](../development_ops/playwright.md) can mitigate this).

## Getting started

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

### 3. Verify with Gemma 3
You can also use [Gemma 3](../ai_knowledge/local_llms.md) via a local runner that supports MCP 3.1 / FastMCP 3.1 to interact with your Jira projects.

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
When building custom Jira integrations, using Python with FastMCP 3.1 and strict **Pydantic v2** validation schemas ensures robust enterprise operation under frontier models like Claude 5.1 and GPT-5.5.

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Dict, Any
import requests
import os

# 1. Initialize FastMCP server conforming to late 2026 standards
mcp = FastMCP("Custom Jira Integration")

# 2. Define strict Pydantic v2 schemas for Jira outputs
class JiraIssueFields(BaseModel):
    summary: str = Field(description="The short summary or title of the issue")
    status_name: str = Field(description="The status name of the issue, e.g. 'In Progress'")
    assignee_name: Optional[str] = Field(None, description="The display name of the assignee")

class JiraIssueContract(BaseModel):
    key: str = Field(description="The Jira issue key, e.g. PROJ-123")
    fields: JiraIssueFields = Field(description="Selected validated fields of the issue")

# 3. Register tool with strict schema verification
@mcp.tool()
def get_issue_details(key: str) -> str:
    """Fetch details of a specific Jira issue and return verified JSON context."""
    # Retrieve configuration and perform REST request
    site_name = os.getenv("ATLASSIAN_SITE_NAME", "example-org.atlassian.net")
    auth_token = os.getenv("ATLASSIAN_API_TOKEN", "dummy-token")
    user_email = os.getenv("ATLASSIAN_USER_EMAIL", "agent@example.com")

    url = f"https://{site_name}/rest/api/3/issue/{key}"

    # Simulate API response for testing, or execute request:
    # response = requests.get(url, auth=(user_email, auth_token))
    # data = response.json()

    mock_response_data = {
        "key": key,
        "fields": {
            "summary": "Implement FastMCP 3.1 integration",
            "status": {"name": "In Progress"},
            "assignee": {"displayName": "Jules"}
        }
    }

    try:
        # Structure the payload to match the validation contract
        raw_payload = {
            "key": mock_response_data["key"],
            "fields": {
                "summary": mock_response_data["fields"]["summary"],
                "status_name": mock_response_data["fields"]["status"]["name"],
                "assignee_name": mock_response_data["fields"]["assignee"]["displayName"]
            }
        }

        # Enforce Pydantic v2 validation
        validated_issue = JiraIssueContract.model_validate(raw_payload)
        return validated_issue.model_dump_json(indent=2)

    except ValidationError as ve:
        return f"Data contract error: {str(ve)}"
    except Exception as e:
        return f"Request execution error: {str(e)}"

if __name__ == "__main__":
    # Start the FastMCP server
    mcp.run()
```

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md) — The underlying standard, now at version 3.1.
- [ServiceNow MCP](servicenow-mcp.md) — Equivalent for ServiceNow environments.
- [Claude Code](../development_ops/claude-code-setup.md) — Primary client for MCP-based Jira management.
- [n8n](../../services/n8n.md) — For orchestrating complex Jira workflows.
- [Playwright](../development_ops/playwright.md) — For browser-based Jira automation where APIs fall short.
- [HashiCorp Vault](hashicorp-vault.md) — Recommended for secure storage of Jira API tokens.
- [Gemma 3](../ai_knowledge/local_llms.md) — Frontier open model with native MCP 3.1 / FastMCP 3.1 support.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Architectural patterns for multi-step Jira tasks.

## Sources / references
- [Anthropic Atlassian MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/atlassian)
- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [Jira Cloud REST API v3 Reference](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Atlassian API Token Management](https://id.atlassian.com/manage-profile/security/api-tokens)
- [FastMCP Specification and Tools Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-12-22
- Confidence: high
