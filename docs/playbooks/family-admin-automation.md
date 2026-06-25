# Playbook: Family Admin Automation

## What it is

Family Admin Automation is an architectural pattern for managing and routing household administrative tasks (bills, insurance, medical documents). It leverages [Paperless-ngx](../services/paperless-ngx.md) for classification, [n8n](../services/n8n.md) for workflow orchestration, and [Home Assistant](../services/home-assistant.md) for family-wide notifications and dashboarding. By June 2026, this has evolved into a "Self-Healing Agentic Loop" where [Claude 4.8](../tools/ai_knowledge/claude.md) or [GPT-5.5](../tools/ai_knowledge/openai.md) proactively manage household operations via [MCP 3.0](../knowledge_base/patterns/tool-calling-and-mcp.md).

## What problem it solves

Household administration is often fragmented across multiple family members, leading to missed due dates, lost paperwork, and redundant communication. This playbook solves the "coordination gap" by centralizing all documents in a searchable archive and automating the notification process. It ensures that everyone is aware of pending tasks without constant manual status updates, using AI to extract key dates and urgency from unstructured documents.

## Where it fits in the stack

**Category**: Playbook / Home Operations. It sits in the **actionable notification layer**, connecting the **document management system** (Paperless-ngx) to the **household control plane** (Home Assistant) and **communication channels** (Matrix/Signal). It utilizes [Model Context Protocol (MCP 3.0)](../knowledge_base/patterns/tool-calling-and-mcp.md) to allow agents to interact with both local and cloud-based administrative tools.

## Typical use cases

- **Bill Payment Alerts**: Automatically notifying the family chat when a new utility bill is scanned and due.
- **Insurance Document Archival**: Tagging and filing insurance policies and medical records for easy retrieval during emergencies.
- **School Form Routing**: Pushing new school forms to a shared "Action Required" dashboard in Home Assistant.
- **Home Maintenance Tracking**: Automating reminders for recurring maintenance tasks based on scanned service records.
- **Sentiment-Based Escalation**: Using [Claude 4.8](../tools/ai_knowledge/claude.md) to detect "Final Notice" language and trigger high-priority alerts.

## Strengths

- **High Visibility**: Centralizes task status on a shared dashboard that all family members can see.
- **Automatic Classification**: Uses Paperless-ngx matching rules and LLM-based reasoning (Claude 4.8) to route documents.
- **Multi-Channel**: Supports notifications via Matrix, Signal, or Home Assistant mobile alerts.
- **Archival Integrity**: Ensures every task is backed by a permanent, OCR'd digital record.
- **Agent-Ready**: Natively supports [MCP 3.0](../knowledge_base/patterns/tool-calling-and-mcp.md) for autonomous task resolution.

## Limitations

- **Entry Point Dependency**: Requires all documents (physical or digital) to be scanned or forwarded to the ingestion point.
- **Matching Rule Precision**: Complex or ambiguous documents may require initial manual tagging until LLM prompts are refined.
- **Home Assistant Configuration**: Requires some familiarity with Home Assistant YAML or UI-based dashboard creation.
- **Privacy Trade-offs**: Processing sensitive documents through cloud LLMs (unless using [Llama 4](../tools/ai_knowledge/llama.md) locally).

## When to use it

- When you have multiple family members sharing administrative responsibilities.
- When you want to eliminate the "Where is that bill?" conversation.
- When you are already using [Home Assistant](../services/home-assistant.md) for other household tasks and want a unified "Single Source of Truth."

## When not to use it

- For single-person households where a simple task manager or calendar is sufficient.
- If you do not have a reliable way to digitize physical mail (consider the [Scan to Task](scan-to-task.md) playbook first).
- If you prefer manual filing and do not want AI agents interacting with financial or medical data.

## Getting started

1.  **Configure Paperless**: Set up [Paperless-ngx](../services/paperless-ngx.md) with matching rules for tags like `Utility`, `Medical`, and `Insurance`.
2.  **Setup the Workflow**: Deploy an [n8n](../services/n8n.md) workflow that triggers on the `needs-action` tag.
3.  **Integrate LLM**: Use the [Claude 4.8](../tools/ai_knowledge/claude.md) node in n8n for document analysis.
4.  **Connect Home Assistant**: Link [Home Assistant](../services/home-assistant.md) to n8n to create notifications and update dashboard sensors.
5.  **Step-by-Step Flow**:
    ```mermaid
    flowchart TD
        A[Ingest: Email or Scan] --> B[Classify: Paperless Matching Rules]
        B --> C[Process: n8n Workflow]
        C --> D[LLM Reasoning: Claude 4.8/GPT-5.5]
        D --> E[Notify: Home Assistant Alert]
        E --> F[Dashboard: HA Unprocessed Admin Card]
        F --> G[Action: Manual Tag Removal]
    ```

## CLI examples

### Triggering n8n Execution
Manual trigger of a family admin workflow for a specific document ID:
```bash
# Execute n8n workflow via CLI (example uses a webhook)
curl -X POST https://n8n.local/webhook/process-family-doc \
     -H "Content-Type: application/json" \
     -d '{"document_id": 1234, "tag": "needs-action"}'
```

### Home Assistant Notification
Sending an urgent alert to the family mobile app via CLI:
```bash
# Using the Home Assistant CLI (hass-cli)
hass-cli service call notify.family_app \
         --arguments title="URGENT: Final Notice",message="A final notice for 'Water Bill' was detected in Paperless."
```

## API examples

### n8n Agent Node Configuration (JSON)
Extracting due dates and amounts from a Paperless document using Claude 4.8:
```json
{
  "node": "Claude 4.8 Agent",
  "parameters": {
    "prompt": "Analyze the following document text and extract the 'Due Date' and 'Amount Due'. Return only JSON.",
    "model": "claude-4-8-opus-20260528",
    "context": "{{$node[\"Paperless-ngx\"].json[\"content\"]}}"
  }
}
```

### Home Assistant REST API
Updating a dashboard sensor with the number of pending admin tasks:
```python
import requests

url = "http://homeassistant.local:8123/api/states/sensor.pending_admin_tasks"
headers = {
    "Authorization": "Bearer YOUR_LONG_LIVED_ACCESS_TOKEN",
    "content-type": "application/json",
}
data = {
    "state": "5",
    "attributes": {"unit_of_measurement": "tasks", "friendly_name": "Pending Admin"}
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
```

## Related tools / concepts

- [Paperless-ngx](../services/paperless-ngx.md): Primary document archive.
- [Home Assistant](../services/home-assistant.md): Family control plane and notification engine.
- [n8n](../services/n8n.md): The glue for administrative workflows.
- [Matrix](../services/element.md): Open communication standard for family alerts.
- [Signal-cli](../architecture/component_map.md): Secure messaging integration.
- [Scan to Task](scan-to-task.md): Hardware-centric ingestion playbook.
- [Email to Calendar](email-to-calendar.md): Complementary playbook for scheduling.
- [Vikunja](../services/vikunja.md): Open-source task management.
- [MCP 3.0](../knowledge_base/patterns/tool-calling-and-mcp.md): Protocol for agentic tool use.

## Sources / References

- [Family Admin Automation Case Study (GitHub)](https://github.com/joanmarcriera/Home-office-automations)
- [Home Assistant Notification Documentation](https://www.home-assistant.io/integrations/notify/)
- [n8n Documentation: Working with Documents](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.document/)
- [Paperless-ngx API Reference](https://docs.paperless-ngx.com/api/)

## Contribution Metadata

- Last reviewed: 2026-06-25
- Confidence: high
