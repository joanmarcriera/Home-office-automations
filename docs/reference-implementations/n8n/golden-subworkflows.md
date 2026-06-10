# n8n Golden Sub-workflows

## What it is
n8n Golden Sub-workflows are a library of standardized, reusable automation building blocks designed to handle common, high-value tasks across the homelab and home-office stack. They encapsulate complex logic into single "Execute Workflow" nodes. As of June 2026, these sub-workflows have been optimized for integration with [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) servers.

## What problem it solves
Reduces duplication of logic across multiple workflows, ensures consistent handling of sensitive data (like risk gating or human approval), and simplifies the creation of new automations by providing pre-validated patterns for common operations. It also ensures that advanced models like Claude 4.8 and GPT-5.5 have a predictable execution environment for complex multi-step tasks.

## Where it fits in the stack
Orchestration Layer — serves as the "standard library" for all n8n-based automations, connecting intake sources (Email, Webhooks) to destination services (Vikunja, Google Calendar). It bridges the gap between raw API calls and high-level [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- **Automated Triage**: Classifying incoming emails or documents before they are processed by specialized agents.
- **Safety Checks**: Implementing a "Human-in-the-Loop" gate for any automation that could cause destructive changes.
- **Workflow Resilience**: Standardizing how errors and approvals are handled globally.
- **MCP Integration**: Acting as a middleware that exposes n8n logic as tools to MCP-compatible agents.

## Strengths
- **Reusability**: Write once, use in dozens of production workflows.
- **Consistency**: Ensures every automation follows the same rules for security and data extraction.
- **Maintainability**: Updating a "Golden" sub-workflow automatically improves all parent workflows that use it.
- **Observability**: Standardized logging makes it easier to trace errors across nested workflows.

## Limitations
- **Complexity**: Debugging nested workflows can be more challenging than single-layer flows.
- **State Management**: Care must be taken when passing large payloads between workflows to avoid memory issues in small n8n instances.
- **Version Control**: Requires disciplined naming and versioning to avoid breaking parent workflows during updates.

## When to use it
- When you find yourself rebuilding the same logic (e.g., "Send to Telegram and wait for a reply") in multiple places.
- For high-stakes operations that require a standardized risk-gating or approval step.
- When you need to expose complex n8n logic to an external agent via MCP.

## When not to use it
- For one-off, highly specific tasks that are unlikely to be repeated.
- When the overhead of calling a sub-workflow exceeds the simplicity of keeping the logic local.

## Core Implementation Patterns

### 1. Email Triage (`email-triage`)
**Purpose**: Classifies incoming emails and extracts structured metadata using Claude 4.8.

#### Logic Flow
1. **Input**: Raw email body and headers.
2. **LLM Analysis**: Categorizes as `personal`, `bill`, `notification`, or `spam`.
3. **Extraction**: Pulls `sender`, `amount_due` (if applicable), and `due_date`.
4. **Output**: JSON object for downstream routing.

#### AI Prompt Pattern
```text
Analyze the following email and return a JSON object:
{
  "category": "invoice|personal|update|spam",
  "urgency": "low|medium|high",
  "summary": "one sentence summary",
  "action_required": true|false
}
Email Content: {{ $json.body }}
```

### 2. Risk Gating (`risk-gating`)
**Purpose**: Intercepts high-risk actions (e.g., bank transfers, deleting files) and requires secondary validation.

#### Logic Flow
1. **Input**: Proposed action and data.
2. **Risk Assessment**: Checks against `high_risk_keywords` or dollar thresholds using a predefined list.
3. **Branching**:
   - **Low Risk**: Proceeds automatically.
   - **High Risk**: Routes to `human-approval` sub-workflow.

### 3. Human Approval (`human-approval`)
**Purpose**: Pauses execution and waits for a human to approve or reject an action via a messaging interface (e.g., Element or Telegram).

#### Logic Flow
1. **Input**: Approval message and unique execution ID.
2. **Notification**: Sends message with "Approve" and "Reject" buttons (using `Wait for Webhook` node).
3. **Wait**: Workflow enters "Waiting" state.
4. **Resume**: Continues based on the webhook payload from the button click.

## Getting started
1. **Identify the Pattern**: Choose one of the sub-workflows above (e.g., `human-approval`).
2. **Create the Sub-workflow**: In n8n, create a new workflow using the "Execute Workflow Trigger".
3. **Define Inputs**: Use the "Set" node to define the required variables (e.g., `action_name`, `severity`).
4. **Implement the Logic**: Add the specific nodes for notification, LLM analysis, or branching.
5. **Call from Parent**: In your main workflow, add an "Execute Workflow" node and select the sub-workflow you just created.

## CLI examples
> [!NOTE]
> n8n sub-workflows are managed via the web UI, but you can interact with the n8n CLI for management tasks.

```bash
# Export all workflows to a backup directory
n8n export:workflow --all --output=./backups/

# Import a golden sub-workflow from a file
n8n import:workflow ./golden-subworkflows/email-triage.json

# List all active workflows to verify sub-workflow presence
n8n list:workflow
```

## API examples
Example of calling an n8n sub-workflow via its webhook trigger using Python:

```python
import requests

N8N_URL = "https://n8n.your-homelab.com/webhook/email-triage"
API_TOKEN = "your_secure_token"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "body": "Your invoice for June is $50.00, due on 2026-06-15.",
    "sender": "billing@utility.com"
}

response = requests.post(N8N_URL, json=data, headers=headers)
print(response.json())
```

## Related tools / concepts
- [n8n Service](../../services/n8n.md)
- [n8n Error Handling Pattern](../../knowledge_base/patterns/n8n-error-handling.md)
- [Human-in-the-Loop UI Design](../../reference-implementations/hitl-ui-design.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Webhook Ingestion](../../reference-implementations/paperless/webhook-ingestion.md)
- [Telegram Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.telegram/)
- [Wait Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/)
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / References
- [n8n Execution Logs Documentation](https://docs.n8n.io/hosting/scaling-n8n/execution-logs/)
- [n8n Sub-workflows Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/)
- [Advanced n8n Patterns for AI Agents (June 2026)](https://n8n.io/blog/ai-agent-patterns)

---
- Status: Reference Implementation
- Last reviewed: 2026-06-10
- Confidence: high
