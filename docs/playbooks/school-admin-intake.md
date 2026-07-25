# Playbook: School Admin Intake

## What it is

School Admin Intake is a specialized administrative automation playbook designed to handle the high volume of correspondence, permission slips, and scheduling requests from educational institutions. It uses OCR, RAG (Retrieval-Augmented Generation), and automated workflow triggers to ensure no school deadline is missed. By late August 2026, it utilizes [Llama 4](../tools/ai_knowledge/llama.md) (70B) or [Gemma 3](../tools/ai_knowledge/gemma.md) for privacy-first, local document processing.

## What problem it solves

It tackles the "backpack black hole" and "email fatigue" faced by parents and guardians. By automating the extraction of dates, consent requirements, and action items from school documents, it reduces manual data entry and prevents scheduling conflicts or missed field trip deadlines. It ensures that sensitive student information stays within the home network by prioritizing local LLM execution.

## Where it fits in the stack

**Category**: Personal Productivity / Family Admin. It integrates [Document Management](../services/paperless-ngx.md) with [Workflow Automation](../services/n8n.md) and [Calendar Services](../tools/calendar_tasks/google_calendar.md). It acts as a specialized instance of the [Family Admin Automation](family-admin-automation.md) playbook, focused on educational data contracts.

## Typical use cases

- **Field Trip Permission Slips**: Automatically extracting the date of the trip and creating a task to sign the form.
- **Weekly Newsletters**: Identifying key dates for school holidays, parent-teacher conferences, or special events.
- **Report Cards**: Archiving official academic records with appropriate metadata for long-term tracking.
- **Sports Physicals**: Tracking expiration dates for medical clearances required for extracurricular activities.

## Strengths

- **Error Reduction**: Minimizes human error in transcribing dates or forgetting deadlines.
- **Centralized Archive**: Keeps all school-related documents in a searchable, tagged repository in [Paperless-ngx](../services/paperless-ngx.md).
- **Privacy-First**: Natively supports [Llama 4](../tools/ai_knowledge/llama.md) for local processing of PII (Personally Identifiable Information).
- **Proactive Notifications**: Moves information from a passive inbox to an active calendar or task list.
- **RAG-Ready**: Uses [Paperless-AI](../services/paperless-ai.md) to answer natural language questions about school policies or events.

## Limitations

- **Handwriting Recognition**: May struggle with handwritten notes on scanned forms if OCR quality is low or ink is faded.
- **Complex Schedules**: Difficulty parsing multi-day events or rotating extracurricular schedules without fine-tuned RAG prompts.
- **Portal Fragmentation**: Some school data may be locked behind proprietary portals (e.g., ParentSquare) that lack easy API access.

## When to use it

- When you have multiple children in school and are overwhelmed by the volume of digital and physical paperwork.
- When you already use a self-hosted document management system like [Paperless-ngx](../services/paperless-ngx.md).
- When you need a highly reliable way to ensure consent forms are signed and returned on time.

## When not to use it

- If your school uses a centralized portal that already provides reliable calendar syncing and digital signatures.
- For very low-volume correspondence where manual entry is faster than maintaining the automation stack.
- If you lack the hardware (e.g., Mac Studio or RTX 4090) to run [Llama 4](../tools/ai_knowledge/llama.md) locally and have strict privacy rules against cloud LLMs.

## Getting started

To implement School Admin Intake:

1.  **Define Filtering**: Configure an [n8n](../services/n8n.md) IMAP filter for emails from `@school.edu` or containing keywords like "Permission" or "Activity".
2.  **Ingest to Paperless**: Route matched emails and scans to [Paperless-ngx](../services/paperless-ngx.md) with the `School` tag.
3.  **Deploy Paperless-AI**: Set up [Paperless-AI](../services/paperless-ai.md) with a [Llama 4](../tools/ai_knowledge/llama.md) backend.
4.  **Automate Actions**: Create n8n workflows to sync extracted dates to [Google Calendar](../tools/calendar_tasks/google_calendar.md) and tasks to [Vikunja](../services/vikunja.md).
5.  **Step-by-Step Flow**:
    ```mermaid
    flowchart TD
        A[School Email Inbox] --> B{n8n IMAP Filter}
        B -->|Match| C[Send to Paperless-ngx]
        B -->|No Match| Z[Skip]
        C --> D[Trigger Paperless-AI]
        D --> E[RAG Analysis & Extraction]
        E --> F{Extraction Successful?}
        F -->|Activity Date| G[Sync to Google Calendar]
        F -->|Consent Required| H[Create Vikunja Task]
        F -->|Low Confidence| I[Tag 'manual-verification']
    ```

## CLI examples

### Tagging School Documents via CLI
Manually applying school-specific tags to a document for reprocessing:
```bash
# Using the Paperless-ngx CLI (via docker exec)
docker exec paperless-ngx document_tagger --document_id 4567 --add_tag "School" --add_tag "Needs-Action"
```

### Creating a Vikunja Task for Consent
Using the Vikunja CLI to create a task for a school form:
```bash
# Create a task in the 'School' project
vikunja tasks create --project "School" --title "Sign Permission Slip: Zoo Field Trip" --due "2026-06-28"
```

## API examples

### Paperless-AI RAG Query (JSON)
Extracting consent requirements using the Paperless-AI API:
```json
{
  "document_id": "4567",
  "query": "Is parental consent required for this activity? If so, what is the deadline?",
  "model": "llama-4-70b-instruct",
  "temperature": 0
}
```

### n8n Google Calendar Sync (JSON)
Creating a school event from extracted data:
```json
{
  "node": "Google Calendar",
  "parameters": {
    "calendar": "Family",
    "summary": "School Activity: {{ $json.event_name }}",
    "start": "{{ $json.extracted_start_date }}",
    "end": "{{ $json.extracted_end_date }}",
    "description": "Auto-extracted from Paperless Doc ID: {{ $json.doc_id }}"
  }
}
```

## Related tools / concepts

- [Paperless-ngx](../services/paperless-ngx.md): Primary document storage.
- [n8n](../services/n8n.md): Workflow engine for email filtering and task creation.
- [Vikunja](../services/vikunja.md): Open-source task management for consent forms.
- [Google Calendar](../tools/calendar_tasks/google_calendar.md): Scheduling for school activities.
- [Paperless-AI](../services/paperless-ai.md): RAG-based analysis for complex forms.
- [Llama 4](../tools/ai_knowledge/llama.md): Recommended local LLM for privacy-first intake.
- [Family Admin Automation](family-admin-automation.md): The overarching household playbook.
- [Scan to Task](scan-to-task.md): Physical document ingestion strategy.

## Sources / References

- [Case Study: Automating School Admin (GitHub)](https://github.com/joanmarcriera/Home-office-automations)
- [Paperless-AI Documentation](https://github.com/the-paperless-project/paperless-ai)
- [n8n: Working with IMAP and Email](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.email-read-imap/)
- [Llama 4 Model Cards (HuggingFace)](https://huggingface.co/meta-llama)

## Contribution Metadata

- Last reviewed: 2026-08-26
- Confidence: high
