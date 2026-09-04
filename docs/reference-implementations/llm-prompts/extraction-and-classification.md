# Reference Implementation: LLM Prompts for Extraction and Classification

## What it is
A collection of specialized prompt templates and schemas for Large Language Models (LLMs) to perform two core administrative tasks: **Task Extraction** (identifying actionable items from text) and **Document Classification** (categorizing documents into predefined buckets).

As of early January 2027, these prompts are optimized for SOTA frontier models such as **Claude 5.6**, **GPT-5.6**, **DeepSeek-V4**, and **Gemini 4.0 Ultra** utilizing **Model Context Protocol (MCP) 3.1** and **FastMCP 3.1** Task Protocol payloads for strict schema validation.

## What problem it solves
Managing a high volume of scanned documents requires significant cognitive effort to decide where each file belongs and what actions are required. Manual classification and task creation are major bottlenecks. These prompts turn raw OCR text into structured data, allowing for automated routing to [Vikunja](../../services/vikunja.md) and [Paperless-ngx](../../services/paperless-ngx.md).

## Where it fits in the stack
This implementation sits in the **Intelligent Processing Layer** of the ingestion pipeline. It acts as the "brain" that interprets the output of OCR tools before passing structured instructions to the **Task Management** (Vikunja) or **Document Storage** (Paperless) layers.

## Typical use cases
- **Inbox Zero for Paper**: Automatically creating tasks in Vikunja for every bill, appointment, or school flyer scanned into the system.
- **Auto-Archiving**: Categorizing documents (e.g., "Medical", "Finance", "School") to ensure they are stored with the correct tags and permissions in Paperless-ngx.
- **Meeting Minute Processing**: Extracting action items, owners, and deadlines from meeting transcripts or voice memos.
- **Smart Inbox**: Sorting documents automatically based on content rather than just filename or source directory.

## Strengths
- **Multi-Purpose**: Handles both the "what to do" (tasks) and "where to put it" (classification) in a single intelligent pipeline.
- **Priority Intelligence**: Uses heuristic definitions to assign consistent priorities (High/Medium/Low) better than simple keyword matching.
- **JSON Standardized**: Outputs data in a format ready for immediate API consumption or **MCP tool** invocation.
- **Local Model Friendly**: Includes optimized prompts for local **Gemma 4**, **Llama 4**, and **Qwen 3.6 VL** variants.

## Limitations
- **Classification Ambiguity**: Documents that span multiple categories (e.g., a "Medical Bill") may be classified inconsistently depending on model temperature.
- **Context Windows**: Extremely large documents may need to be summarized or chunked before classification to stay within token limits.
- **OCR Sensitivity**: Reliability is highly dependent on the quality of the upstream OCR (use **Omni Tools VLM** for best results).

## When to use it
- When you want to automate the transition from "digitized document" to "actionable task" in your productivity stack.
- When building a "smart inbox" that sorts documents automatically based on semantic content.
- For high-volume ingestion where manual metadata entry is not scalable.

## When not to use it
- For very high-security documents where LLM processing (if using a cloud provider) is restricted by privacy policies.
- For simple document types where the category can be determined by the source (e.g., all files from the "Bank" folder are "Finance").
- If the document volume is low enough that manual review is more cost-effective.

## Getting started

### 1. Ingestion Setup
Configure your scanner or phone to upload PDFs to a "To-Process" folder. Use **n8n** to trigger the extraction pipeline when a new file arrives.

### 2. Model Selection
Use **Claude 5.6** or **Gemini 4.0 Ultra** for high-precision extraction, or a local **Gemma 4** or **Qwen 3.6 VL** instance for privacy-sensitive documents.

### 3. Integration
Map the JSON output to the [Calendar Mapping Rules](../calendar/mapping-rules.md) for date-based events or directly to the Vikunja API for tasks.

## CLI examples
Test your extraction prompts using the following CLI commands.

```bash
# Extract tasks from an OCR text file using Claude Code
claude --prompt "$(cat task_extraction_prompt.txt)" --file ocr_text.txt

# Classify a document using a local Ollama instance
ollama run gemma-4 "Classify this text into [SCHOOL, ADMIN, FINANCE]: $(cat ocr_text.txt)"

# Validate extraction output against a schema
python3 scripts/validate_json.py --schema task_schema.json --data extraction_output.json
```

## API examples
The prompts are designed for structured output.

### Prompt Template: Task Extraction
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

### Task Extraction JSON Schema
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

### Pydantic v2 Parsing & Extraction Validation
The following code snippet demonstrates how to parse and validate extraction results programmatically using Pydantic v2:

```python
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, ValidationError, field_validator, TypeAdapter

class ActionableTask(BaseModel):
    task: str = Field(..., min_length=3, description="Actionable description of the task")
    due_date: Optional[date] = Field(None, description="Due date of the task in YYYY-MM-DD")
    priority: str = Field("medium", description="Priority level (low/medium/high)")
    owner: Optional[str] = Field(None, description="Assigned owner of the task")

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, value: str) -> str:
        normalized = value.lower().strip()
        if normalized not in {"low", "medium", "high"}:
            raise ValueError("Priority must be one of: 'low', 'medium', 'high'")
        return normalized

class TaskExtractionResult(BaseModel):
    tasks: List[ActionableTask] = Field(..., description="List of extracted actionable tasks")

# Example validation showing parsing using Pydantic v2 TypeAdapter and model_validate_json
json_data = """
{
  "tasks": [
    {
      "task": "Review and submit water bill",
      "due_date": "2027-01-07",
      "priority": "high",
      "owner": "Jules"
    }
  ]
}
"""

try:
    # Use Pydantic v2 TypeAdapter for advanced list/dict/model validation & parsing
    adapter = TypeAdapter(TaskExtractionResult)
    result = adapter.validate_json(json_data)
    for task in result.tasks:
        print(f"Parsed Task: {task.task} | Due: {task.due_date} | Priority: {task.priority} | Owner: {task.owner}")
except ValidationError as e:
    print(f"Strict schema validation failed: {e}")
```

## Related tools / concepts
- [Vikunja](../../services/vikunja.md): The target system for extracted tasks.
- [Paperless-ngx](../../services/paperless-ngx.md): The target system for classified documents.
- [Date Extraction](date-extraction.md): Specialized prompt for precise date handling and timezone normalization.
- [Warranty Extraction](warranty-extraction.md): For specific "High" priority warranty deadlines and purchase dates.
- [HITL UI Design](../hitl-ui-design.md): The interface for manual review of extraction and classification results.
- [n8n Error Handling](../../knowledge_base/patterns/n8n-error-handling.md): Pattern for retrying failed or low-confidence extractions.
- [Document Preparation](../../playbooks/document-preparation-for-llm-training.md): Enhancing OCR quality for better classification.
- [n8n Service](../../services/n8n.md): The primary orchestrator for these LLM prompts.
- [MCP](../../tools/automation_orchestration/mcp.md): Standardized protocol for model-tool interaction and schema management.

## Sources / references
- [Home Office Automations (GitHub)](https://github.com/joanmarcriera/Home-office-automations)
- [Pydantic Structured Outputs Documentation](https://docs.pydantic.dev/latest/concepts/json_schema/)
- [Model Context Protocol (MCP) 3.1 Specification](https://modelcontextprotocol.io/introduction)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
