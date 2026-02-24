# Paperless-ngx

## What it is
Paperless-ngx is a community-supported open-source document management system. It transforms your physical documents into a searchable online archive.

## What problem it solves
It eliminates paper clutter by providing a centralized, digital repository for all household and office documents. It handles OCR, indexing, and tagging automatically.

## Where it fits in the pipeline
**Store / Process**

## Typical use cases (in this homelab / family automation context)
- **School/Admin documents**: Scanning report cards and permission slips for quick retrieval.
- **Utility Bills**: Automatically ingesting bills from email and tagging them by provider.
- **Tax Records**: Organizing receipts and financial statements for tax season.

## Related Playbooks
- [Email to Calendar](../../../playbooks/email-to-calendar.md)
- [Scan to Task](../../../playbooks/scan-to-task.md)
- [School Admin Intake](../../../playbooks/school-admin-intake.md)

## Integration points
- **Email ingestion**: Connects via IMAP to monitor specific folders for new documents.
- **File System**: Monitors a "consumption" directory for new scans.
- **REST API**: Allows AI agents and automation tools (n8n) to retrieve documents and metadata.

## Licensing and cost
- **Open Source**: Yes (GPL-3.0)
- **Cost**: Free
- **Free tier**: N/A (Self-hosted)
- **Self-hostable**: Yes

## Strengths
- Powerful OCR via Tesseract.
- Automatic matching and tagging.
- Web UI is fast and responsive.

## Limitations
- Mobile app experience is primarily via 3rd party apps or web.
- Requires some setup for optimal OCR performance (e.g., Tika/Gotenberg).

## Alternatives / Related tools
- **Nextcloud** (for general file storage)
- **DocuWare** (Commercial)

## Links
- [Official Website](https://docs.paperless-ngx.com/)
- [GitHub](https://github.com/paperless-ngx/paperless-ngx)
