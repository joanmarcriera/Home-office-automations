# Make

## What it is
Make (formerly Integromat) is a visual automation platform that allows you to design, build, and automate complex workflows between cloud apps.

## What problem it solves
It provides a more advanced and visual alternative to Zapier, allowing for complex branching, filtering, and data processing in a drag-and-drop interface.

## Where it fits in the pipeline
**Orchestrate / Act**

## Typical use cases (in this homelab / family automation context)
- **Complex Email Processing**: Parsing multipart emails and conditionally sending different attachments to Paperless-ngx or Nextcloud.
- **Cross-Calendar Sync**: Implementing complex logic to sync specific event types between Google and a private CalDAV server.
- **System Monitoring**: Aggregating logs from multiple cloud services and sending a summary report to a local Matrix channel.

## Integration points
- **HTTP/Webhooks**: Used to bridge the gap between cloud scenarios and self-hosted automation hubs like n8n.
- **Databases**: Native support for connecting to MySQL, PostgreSQL, and other data stores.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (with a free tier)
- **Free tier**: Yes (Limited data transfer and operations per month).
- **Self-hostable**: No

## Strengths
- Beautiful and powerful visual builder.
- Detailed execution history and debugging tools.
- Advanced data manipulation features (iterators, aggregators).

## Limitations
- Steeper learning curve than Zapier.
- Operation-based pricing can be tricky to manage.
- Cloud-only; data leaves your network.

## Alternatives / Related tools
- **n8n**
- **Zapier**
- **Pipedream**

## Links
- [Official Website](https://www.make.com/)
