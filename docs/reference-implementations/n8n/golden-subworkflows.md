# n8n Golden Sub-workflows

This reference implementation defines standardized, reusable sub-workflows for common home-office automation patterns.

## 1. Email Triage (`email-triage`)
**Purpose**: Classifies incoming emails and extracts structured metadata.

### Logic Flow
1. **Input**: Raw email body and headers.
2. **LLM Analysis**: Categorizes as `personal`, `bill`, `notification`, or `spam`.
3. **Extraction**: Pulls `sender`, `amount_due` (if applicable), and `due_date`.
4. **Output**: JSON object for downstream routing.

### AI Prompt Pattern
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

## 2. Risk Gating (`risk-gating`)
**Purpose**: Intercepts high-risk actions (e.g., bank transfers, deleting files) and requires secondary validation.

### Logic Flow
1. **Input**: Proposed action and data.
2. **Risk Assessment**: Checks against `high_risk_keywords` or dollar thresholds.
3. **Branching**:
   - **Low Risk**: Proceeds automatically.
   - **High Risk**: Routes to `human-approval` sub-workflow.

## 3. Human Approval (`human-approval`)
**Purpose**: Pauses execution and waits for a human to approve or reject an action via a messaging interface (e.g., Element or Telegram).

### Logic Flow
1. **Input**: Approval message and unique execution ID.
2. **Notification**: Sends message with "Approve" and "Reject" buttons (using `Wait for Webhook` node).
3. **Wait**: Workflow enters "Waiting" state.
4. **Resume**: Continues based on the webhook payload from the button click.

## Usage in n8n
To use these patterns:
1. Create a new workflow for each pattern above.
2. Use the **Execute Workflow** node in your primary flows to call these sub-workflows.
3. Pass data via the **Node Input** and receive results via the **Output**.

---
- Status: Reference Implementation
- Last reviewed: 2026-05-13
