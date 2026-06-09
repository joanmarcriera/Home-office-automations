# Reference Implementation: LLM Prompts for Extraction and Classification

## What it is
A collection of specialized prompt templates and schemas for Large Language Models (LLMs) to perform two core administrative tasks: **Task Extraction** (identifying actionable items from text) and **Document Classification** (categorizing documents into predefined buckets).

## What problem it solves
Managing a high volume of scanned documents requires significant cognitive effort to decide where each file belongs and what actions are required. Manual classification and task creation are bottlenecks in a truly automated homelab. These prompts turn raw OCR text into structured data, allowing for automated routing to [Vikunja](../../services/vikunja.md) and [Paperless-ngx](../../services/paperless-ngx.md).

## Where it fits in the stack
This implementation sits in the **intelligent processing layer** of the ingestion pipeline. It acts as the "brain" that interprets the output of OCR tools before passing structured instructions to the **task management** (Vikunja) or **document storage** (Paperless) layers.

## Typical use cases
- **Inbox Zero for Paper**: Automatically creating tasks in Vikunja for every bill, appointment, or school flyer scanned into the system.
- **Auto-Archiving**: Categorizing documents (e.g., "Medical", "Finance", "School") to ensure they are stored with the correct tags and permissions in Paperless-ngx.
- **Meeting Minute Processing**: Extracting action items, owners, and deadlines from meeting transcripts or notes.

## Strengths
- **Multi-Purpose**: Handles both the "what to do" (tasks) and "where to put it" (classification) in a single pipeline.
- **Priority Intelligence**: Uses heuristic definitions to assign consistent priorities (High/Medium/Low) better than simple keyword matching.
- **JSON Standardized**: Outputs data in a format ready for immediate API consumption.

## Limitations
- **Classification Ambiguity**: Documents that span multiple categories (e.g., a "Medical Bill") may be classified inconsistently depending on model temperature.
- **Context Windows**: Extremely large documents may need to be summarized or chunked before classification to stay within token limits.
- **Model Dependency**: Smaller local models may struggle with complex schema adherence compared to frontier models like **GPT-5.5** or **Claude 4.7**.

## When to use it
- When you want to automate the transition from "digitized document" to "actionable task".
- When building a "smart inbox" that sorts documents automatically based on content rather than just filename.

## When not to use it
- For very high-security documents where LLM processing (if using a cloud provider) is restricted.
- For simple document types where the category can be determined by the source (e.g., all files from a specific scanner folder are "Admin").

## Prompt Template: Task Extraction
```text
Extract actionable tasks from the following text.

Text:
{{ocr_text}}

Return a list of JSON objects:
[
  {
    "task": "string",
    "due_date": "YYYY-MM-DD or null",
    "priority": "low/medium/high",
    "owner": "string (if mentioned)"
  }
]
```

## Prompt Template: Document Classification
```text
Classify the following document into one of these categories:
[SCHOOL, ADMIN, FINANCE, MEDICAL, TECHNICAL, MISC]

Text:
{{ocr_text}}

Response: One word only.
```

## JSON Schema for Structured Output
To improve reliability with local models (e.g. `Qwen3-Coder-Next` or **Llama 4 Maverick**), use **JSON Mode** or **Constrained Output** by providing a formal schema. Modern models support **Model Context Protocol (MCP)** to dynamically pull these schemas from a central registry.

### Task Extraction Schema
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "task": { "type": "string" },
      "due_date": { "type": ["string", "null"], "format": "date" },
      "priority": { "enum": ["low", "medium", "high"] },
      "owner": { "type": ["string", "null"] }
    },
    "required": ["task", "due_date", "priority", "owner"]
  }
}
```

### Token-Efficiency Tip
When using local models, prefer a **minimal schema**. Removing the `owner` field or `reasoning` can reduce output tokens by 20-30% in high-volume ingestion workflows.

## Priority Selection Logic
To ensure consistent priority detection with local LLMs, use the following definitions in your system prompt or instruction block:

- **HIGH**:
    - **Deadlines**: Tasks with a due date of today or tomorrow.
    - **Keywords**: Presence of urgency keywords: `urgent`, `asap`, `immediately`, `critical`, `deadline`.
    - **Consequences**: Legal, financial, or medical requirements that have immediate consequences (e.g., "pay by", "court date", "appointment tomorrow").
    - **Blocked Work**: Tasks that are blocking multiple other people or critical infrastructure repairs.
- **MEDIUM**:
    - **Weekly Horizon**: Tasks with a due date within the next 7 days.
    - **Routine/Business**: Routine business or household tasks that are time-sensitive but not immediate (e.g., "schedule appointment", "weekly report").
    - **Meeting Actions**: Action items mentioned in meeting summaries without explicit deadlines.
- **LOW**:
    - **Future/Someday**: Tasks with no due date or a date more than 7 days away.
    - **Non-Critical**: "Nice-to-have" items, reading lists, or long-term research goals.
    - **Inspirational**: General suggestions or ideas (e.g., "maybe we should", "someday").

## Improved Prompt for Local LLMs (Example)
To ensure the best results from models like `Qwen3-Coder-Next`, `Llama-3.1`, or **Llama 4 Maverick**, use a **Few-Shot** approach:

```text
Extract actionable tasks from the following text. Use the priority definitions provided below.

### Priority Definitions
- HIGH: Due today/tomorrow, urgent keywords, or immediate legal/financial consequences.
- MEDIUM: Due within 7 days or routine time-sensitive business.
- LOW: No due date, due > 7 days, or "nice-to-have" items.

### Examples
Input: "Please pay the electricity bill by tomorrow or they will cut the power."
Output: [{"task": "Pay electricity bill", "due_date": "2026-04-21", "priority": "high", "owner": null}]

Input: "We should think about painting the fence this summer."
Output: [{"task": "Paint the fence", "due_date": null, "priority": "low", "owner": null}]

### Text to Process
{{ocr_text}}

### Response (JSON Only)
```

## Related tools / concepts
- [Vikunja](../../services/vikunja.md) — The target system for extracted tasks.
- [Paperless-ngx](../../services/paperless-ngx.md) — The target system for classified documents.
- [Date Extraction](date-extraction.md) — Specialized prompt for precise date handling.
- [Warranty Extraction](warranty-extraction.md) — For specific "High" priority warranty deadlines.
- [HITL UI Design](../hitl-ui-design.md) — For manual review of extraction and classification.
- [n8n Error Handling](../../knowledge_base/patterns/n8n-error-handling.md) — Pattern for retrying failed extractions.
- [Document Preparation](../../playbooks/document-preparation-for-llm-training.md) — Enhancing OCR quality for better classification.
- [n8n Service](../../services/n8n.md) — Orchestrator for these LLM prompts.
- [MCP](../../tools/automation_orchestration/mcp.md) — Standardized protocol for model-tool interaction.

## Sources / References
- [Home Office Automations](https://github.com/joanmarcriera/Home-office-automations)
- [Pydantic Structured Outputs](https://docs.pydantic.dev/latest/concepts/json_schema/)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-08
