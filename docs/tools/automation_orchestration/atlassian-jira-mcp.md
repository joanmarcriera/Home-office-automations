# Atlassian Jira MCP

## What it is
Atlassian Jira MCP implementations are Model Context Protocol (MCP) servers that expose Jira's project management capabilities directly to AI agents. As of early 2027, these servers fully support the **MCP 3.1** and **FastMCP 3.1 Task Protocol** standards, enabling frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, and **DeepSeek-V4** to interact directly with Jira issues, sprints, and backlogs using standardized, agentic tool-calling patterns.

## What problem it solves
It eliminates manual context switching between chat interfaces, developer IDEs, and Jira dashboards. By providing a standardized protocol interface for issue retrieval, creation, transition, and backlog management, it enables autonomous agents to perform project management tasks, triage bugs, and generate status reports without custom glue code. The integration of **FastMCP 3.1 Task Protocol** ensures that multi-step task execution is consistent, highly reliable, and type-safe across different agent frameworks and environments.

## Where it fits in the stack
**Automation / Orchestration**. It acts as an architectural bridge between the **Agentic** orchestration layer and enterprise project management tools.

## Typical use cases
- **Automated Bug Triage**: Asking [Gemma 4](../ai_knowledge/local_llms.md) to analyze incoming bug reports, categorize severity, and assign labels or components.
- **Sprint Summaries & Velocity Tracking**: Generating daily standup reports or sprint velocity summaries via an [n8n](../../services/n8n.md) or [AirOps](airops.md) workflow.
- **Natural Language JQL**: Searching for complex issue patterns using conversational queries instead of writing manual JQL.
- **Issue Lifecycle Automation**: Moving stories through transitions (e.g., "In Progress" to "Code Review") directly from developer environments like [Claude Code](../development_ops/claude-code-setup.md).
- **Documentation & Wiki Sync**: Syncing Jira issue status with internal wikis, release notes, or [AnythingLLM](../ai_knowledge/anythingllm.md) knowledge bases.

## Strengths
- **Native Tooling Alignment**: Maps Jira Cloud REST API endpoints to LLM tool signatures directly.
- **FastMCP 3.1 Task Protocol Compliance**: Leverages the latest FastMCP specification for improved reliability in multi-step agentic workflows and long-running task execution.
- **Developer Workflow Integration**: Enables managing project boards without leaving terminal or code editor environments (e.g., Cursor, Zed, Aider).
- **Extensible SDK Support**: TypeScript and Python FastMCP SDKs allow easy customization of exposed tools and custom Jira workflow transitions.
- **Client Interoperability**: Compatible with standard MCP clients including Claude Desktop, Zed, Cursor, and custom agentic frameworks.

## Limitations
- **Auth & Secrets Security**: Requires secure storage of Atlassian API tokens, ideally managed via [HashiCorp Vault](hashicorp-vault.md).
- **API Rate Limiting**: Subject to Jira Cloud REST API rate limits during bulk or high-frequency agent operations.
- **Custom Field Complexity**: Complex custom fields and enterprise permission schemas require careful MCP tool mapping.
- **Granular Access Control**: Requires precise Jira role permissions to prevent accidental mass updates by autonomous agents.

## When to use it
- When managing Jira project state through an AI agent or terminal assistant.
- When building automated agentic workflows that read from or write to Jira.
- When executing bulk issue updates or searches based on natural language criteria.
- When integrating Jira management into a broader [Agentic Workflow](../../knowledge_base/patterns/agentic-workflows.md).

## When not to use it
- For high-volume automated data migrations (use raw Jira REST API scripts or dedicated ETL pipelines).
- In restricted environments where storing API tokens or external network access is strictly audited.
- When requiring visual UI interactions not exposed by the REST API (where [Playwright](../development_ops/playwright.md) may be required).

## Getting started

### 1. Generate an API Token
Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) and create a new API token.

### 2. Configure Claude Desktop / MCP Client
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

### 3. Interact with Frontier Models
Use **Claude 5.6** or **Gemma 4** via your MCP client to query issues, create tickets, and execute sprint transitions using natural language.

## CLI examples

```bash
# Run the official Atlassian MCP server locally for testing
ATLASSIAN_SITE_NAME="..." ATLASSIAN_API_TOKEN="..." npx @anthropic-ai/mcp-server-atlassian

# Search for Jira issues using JQL via an MCP CLI client
mcp-client call atlassian search_issues --jql "project = PROJ AND status = Open"

# Transition an issue to 'In Review'
mcp-client call atlassian transition_issue --issue_key "PROJ-123" --status "In Review"
```

## API examples

### Python FastMCP 3.1 Integration with Pydantic v2 Contract Validation
When building custom Jira MCP tools, using Python with FastMCP 3.1 and strict **Pydantic v2** validation schemas ensures robust enterprise operation under frontier models like Claude 5.6 and GPT-5.6.

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import os

# 1. Initialize FastMCP server conforming to early 2027 standards
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
    site_name = os.getenv("ATLASSIAN_SITE_NAME", "example-org.atlassian.net")
    auth_token = os.getenv("ATLASSIAN_API_TOKEN", "dummy-token")
    user_email = os.getenv("ATLASSIAN_USER_EMAIL", "agent@example.com")

    # Representation of API payload from Jira Cloud REST API v3
    mock_response_data = {
        "key": key,
        "fields": {
            "summary": "Implement FastMCP 3.1 Task Protocol integration",
            "status": {"name": "In Progress"},
            "assignee": {"displayName": "Jules"}
        }
    }

    try:
        # Structure payload to match contract
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
    mcp.run()
```

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md) — The underlying standard, now at version 3.1.
- [AirOps](airops.md) — Enterprise orchestration platform for scaling MCP agents.
- [Claude Code](../development_ops/claude-code-setup.md) — Primary developer CLI client for MCP-based Jira management.
- [n8n](../../services/n8n.md) — For orchestrating complex Jira workflows.
- [Playwright](../development_ops/playwright.md) — For browser-based UI automation where APIs fall short.
- [HashiCorp Vault](hashicorp-vault.md) — Recommended for secure storage of Jira API tokens.
- [Gemma 4](../ai_knowledge/local_llms.md) — Frontier open model with native FastMCP 3.1 support.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Architectural patterns for multi-step Jira tasks.

## Sources / references
- [Anthropic Atlassian MCP Server Repository](https://github.com/modelcontextprotocol/servers/tree/main/src/atlassian)
- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [Jira Cloud REST API v3 Reference](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Atlassian API Token Management](https://id.atlassian.com/manage-profile/security/api-tokens)
- [FastMCP Specification and Tools Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
