# Zapier

## What it is
Zapier is a cloud-based automation tool that connects thousands of different web applications to automate tasks between them.

## What problem it solves
It allows non-technical users to build automations (Zaps) between cloud services without writing code. It is the largest ecosystem for connecting SaaS applications.

## Where it fits in the pipeline
**Orchestrate / Act**

## Typical use cases (in this homelab / family automation context)
- **Cloud-to-Home Sync**: Triggering an n8n webhook when a new Gmail arrives with a specific attachment.
- **Task Management**: Creating a task in Vikunja when a specific event is added to a Google Calendar.
- **Social Media Notifications**: Sending a home automation status update to a private group.

## Integration points
- **Webhooks**: Common integration point for connecting self-hosted tools (like n8n) to the cloud.
- **Google Calendar / Gmail**: Deep native integrations with all major cloud productivity suites.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (with a free tier)
- **Free tier**: Yes (Limited tasks per month and single-step Zaps).
- **Self-hostable**: No

## Strengths
- Massive library of supported apps (5,000+).
- Very user-friendly and intuitive interface.
- Reliable cloud execution.

## Limitations
- Costs can scale quickly with task volume.
- Less powerful for complex data manipulation compared to n8n or Make.
- No self-hosted option; requires data to leave your network.

## Alternatives / Related tools
- **n8n**
- **Make.com**
- **IFTTT**

## Links
- [Official Website](https://zapier.com/)
