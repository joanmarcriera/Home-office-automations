# n8n

## What it is
n8n is an extendable workflow automation tool. It allows you to connect anything with an API to anything else, using a visual node-based interface.

## What problem it solves
It bridges the gap between disparate apps and services in your homelab. It handles complex data transformations and long-running logic that simpler automation tools might struggle with.

## Where it fits in the pipeline
**Orchestrate / Act**

## Typical use cases (in this homelab / family automation context)
- **Document Processing Pipeline**: Monitoring an email folder, sending attachments to Paperless-ngx, then extracting dates via AI and creating a calendar event.
- **Data Collection**: Scraping data from home devices and storing it in a database or Nextcloud.
- **Notification Hub**: Sending alerts from various home systems to Matrix or Signal.

## Related Playbooks
- [Email to Calendar](../../../playbooks/email-to-calendar.md)
- [Scan to Task](../../../playbooks/scan-to-task.md)
- [School Admin Intake](../../../playbooks/school-admin-intake.md)

## Integration points
- **AI Agents**: Using the AI nodes to integrate LLMs, memory, and tools directly into workflows.
- **Home Assistant**: Triggering automations or updating entities based on external data.
- **Paperless-ngx**: Ingesting and managing documents via the Paperless node.

## Licensing and cost
- **Open Source**: Fair-code (Sustainable use license)
- **Cost**: Free (Self-hosted for personal use)
- **Free tier**: Yes (Cloud version has limited free tier)
- **Self-hostable**: Yes

## Strengths
- Highly flexible with a massive library of pre-built nodes.
- Powerful JavaScript support for custom logic.
- Self-hosting ensures privacy and no "per-execution" costs.

## Limitations
- Steeper learning curve than Zapier.
- Requires some server maintenance when self-hosted.

## Alternatives / Related tools
- **Zapier**
- **Make.com**
- **Node-RED**

## Links
- [Official Website](https://n8n.io/)
- [GitHub](https://github.com/n8n-io/n8n)
