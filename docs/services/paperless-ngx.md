# Paperless-ngx

Paperless-ngx is a community-supported document management system.

## Description
It transforms your physical documents into a searchable online archive. It handles OCR, tagging, and indexing.

## Typical workflows
- **Consumption Folder**: Drop files into a monitored directory for automatic ingestion.
- **Webhook-based Ingestion**: Use the REST API to push documents directly. This is preferred for cloud-to-local automations or when low-latency ingestion is required.
    - **Endpoint**: `POST /api/documents/post_document/`
    - **Payload**: Multipart form data with `document` (file) and optional metadata like `title`, `tags`, or `created`.
    - **Benefit**: Avoids polling delays and allows for immediate confirmation of document receipt.

## Links
- [Official Website](https://docs.paperless-ngx.com/)
- [GitHub Repository](https://github.com/paperless-ngx/paperless-ngx)

## Alternatives
- [Docspell](https://docspell.org/)
- [Teedy](https://teedy.io/)

## Backlog
- Configure multi-user permissions.
- Setup automated email ingestion.

## Sources / References

- [Reference](https://docs.paperless-ngx.com/)
- [Reference](https://github.com/paperless-ngx/paperless-ngx)
- [Reference](https://docspell.org/)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
