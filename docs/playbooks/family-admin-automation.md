# Playbook: Family Admin Automation

## Objective
Automate the routing and notification of family-wide administrative tasks (bills, insurance, medical).

## Pre-requisites
- [Paperless-ngx](../services/paperless-ngx.md)
- [Home Assistant](../services/home-assistant.md)
- [Matrix/Signal](../architecture/component_map.md)

## Step-by-Step Flow
1.  **Ingest**: Document arrives via Email or Scan.
2.  **Classify**: Paperless matching rules categorize as `Insurance` or `Utility`.
3.  **Process**: n8n workflow triggers on tag application.
4.  **Notify**: Home Assistant sends a notification to the shared family chat: "New Insurance document received. Due: [Date]".
5.  **Dashboard**: The document appears in the "Unprocessed Admin" card on the Home Assistant dashboard.
6.  **Action**: Once a family member pays or acknowledges, they manually remove the `needs-action` tag in Paperless.

## Data Contract
JSON payload to Home Assistant:
- `doc_id`
- `category`
- `due_date`
- `summary`

## Failure Modes & Recovery
- **Missing Due Date**:
    - *Detection*: LLM returns null for `due_date`.
    - *Recovery*: Default to "ASAP" or 7 days from today.

## Variants
- **SMS Notifications**: Using [Signal-cli](../architecture/component_map.md) for urgent alerts.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/joanmarcriera/Home-office-automations
