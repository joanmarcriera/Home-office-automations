# Standards and Conventions

This document defines the technical standards for tools to interoperate within this automation stack.

## Naming Conventions
- **Tags (Paperless)**: `kebab-case`. Lowercase only. Prefix status tags with `s:` and category tags with `c:`.
- **Workflows (n8n)**: `[Trigger Source] -> [Primary Action]`. Example: `IMAP -> Paperless Intake`.
- **Prompts**: Versioned using SemVer. Store as Markdown files in `reference-implementations/llm-prompts/`.

## Document Lifecycle States
1.  **Ingested**: Raw file received by the system.
2.  **OCRed**: Searchable layer added (via [OCRmyPDF](./tools/process_understanding/ocrmypdf.md)).
3.  **Classified**: Assigned a document type and category tags.
4.  **Actioned**: Any extracted tasks/events have been synced to external systems.
5.  **Archived**: Document is moved to long-term storage or its final tag state.

## Minimal Metadata Schema
Every document processed by AI should attempt to populate:
- `extraction_date`: ISO8601 of when AI ran.
- `source_origin`: Email, Scan, Webhook.
- `action_required`: Boolean.
- `due_date`: If applicable.
- `confidence_score`: 0.0 to 1.0 (from LLM).

## Interoperability
- **Data Format**: All cross-tool communication should prefer **JSON**.
- **Dates**: Always use **ISO8601** with UTC offsets.
- **IDs**: Use the internal ID of the source system (e.g. Paperless `document_id`) in the metadata of the destination system (e.g. GCal event description).

## What "Done" Means
An automated flow is considered "done" when:
1.  The primary action is completed (Event created/Task synced).
2.  The source document is updated with a `processed` or `actioned` tag.
3.  No errors were logged in the orchestration engine (n8n).
4.  If a critical failure occurred, a notification was sent to a human review channel.
