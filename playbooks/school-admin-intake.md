# Playbook: School Admin Intake

## Objective
Streamline the processing of school-related correspondence, extracting dates for school activities and archiving official documents.

## Pre-requisites
- [Paperless-ngx](../docs/services/paperless-ngx.md)
- [n8n](../docs/services/n8n.md)
- [Google Calendar](../docs/tools/calendar_tasks/google_calendar.md)

## Step-by-Step Flow
1.  **Filter**: n8n monitors the `Inbox` via IMAP for emails from `@school.edu` or containing keywords like "Activity", "Field Trip", "Grade".
2.  **Archive**: The email and any attachments are sent to Paperless-ngx with the document type `SchoolCorrespondence` and the tag `School`.
3.  **Analyze**: [Paperless-AI](../docs/services/paperless-ai.md) triggers on the document creation to perform a RAG-based analysis.
4.  **Extract**: Specifically look for:
    - Activity Date/Time
    - Consent required (Yes/No)
    - Deadline for consent
5.  **Sync**:
    - If an activity date is found, add it to the `School Calendar` in Google Calendar.
    - If consent is required, create a task in [Vikunja](../docs/services/vikunja.md) tagged `Consent`.

## Data Contract
Defined in [Classification Standards](../standards-and-conventions.md).

## Failure Modes & Recovery
- **Ambiguous Dates**: "Next Friday" extraction issues.
    - *Detection*: LLM confidence score < 0.8.
    - *Recovery*: Tag document as `manual-verification`.

## Variants
- **Direct Scan**: Scanning a physical permission slip brought home by the student.
