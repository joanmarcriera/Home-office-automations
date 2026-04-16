# Reference Implementation: Paperless-ngx Webhook Ingestion

This guide demonstrates how to bypass polling delays by pushing documents directly to Paperless-ngx using its REST API.

## Configuration

### API Endpoint
`POST /api/documents/post_document/`

### Authentication
Requires an `Authorization: Token <YOUR_API_TOKEN>` header.

### Multipart Form Data Fields
- `document`: The file to upload.
- `title` (optional): Override the filename.
- `created` (optional): ISO8601 date.
- `tags` (optional): List of tag IDs.

## cURL Example
```bash
curl -H "Authorization: Token your_token_here" \
     -F "document=@/path/to/your/document.pdf" \
     -F "title=Utility Bill" \
     -X POST http://your-paperless-ip:8000/api/documents/post_document/
```

## n8n Implementation
Use the **HTTP Request** node:
- **Method**: POST
- **URL**: `http://paperless:8000/api/documents/post_document/`
- **Authentication**: Header Auth (`Authorization`)
- **Send Binary Data**: Yes
- **Body Content Type**: Multipart Form-Data

## Sources / References
- [Paperless-ngx API Docs](https://docs.paperless-ngx.com/api/)

## Contribution Metadata
- Last reviewed: 2026-04-06
- Confidence: high
