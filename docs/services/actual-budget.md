# Actual Budget

Actual is a local-first personal finance tool, a 100% free and open-source application.

## What it is
Actual is a privacy-focused personal finance manager that uses a local-first architecture. It provides a robust, fast interface for budgeting, transaction tracking, and account management, originally developed as a commercial product before being open-sourced.

## What problem it solves
It solves the problem of "cloud-dependency" in personal finance. Traditional apps like YNAB or Mint can shut down, change pricing, or suffer from data breaches. Actual ensures your financial data stays on your device, working offline while offering optional end-to-end encrypted synchronization.

## Where it fits in the stack
In a home-automation stack, Actual serves as the **Financial Intelligence Layer**. It can ingest data from automated bank scrapers or manual CSV exports and provide a clean API for other home-office agents to query budget status or transaction history.

## Typical use cases
- **Zero-Based Budgeting**: Implementing the "Give Every Dollar a Job" philosophy.
- **Privacy-First Finance**: Managing sensitive financial data without uploading it to a third-party cloud.
- **Multi-Device Syncing**: Keeping budget data in sync between a desktop and mobile device via a self-hosted synchronization server.

## Strengths
- **Local-First Performance**: Extremely fast UI because all data is local.
- **End-to-End Encryption**: Secure synchronization that the server cannot read.
- **Active Community**: Rapidly evolving since going open-source.
- **YNAB Migration**: Excellent compatibility for users moving from YNAB.

## Limitations
- **Self-Hosting Required**: Requires a server (Docker) for multi-device sync.
- **Learning Curve**: Zero-based budgeting requires a specific mindset and setup.
- **Limited Investment Tracking**: Primarily focused on budgeting rather than complex portfolio analysis.

## When to use it
- When you want a privacy-focused, local-first budgeting tool.
- For users who want full control over their financial data.
- When you need a 100% free and open-source alternative to YNAB.

## When not to use it
- If you require advanced investment tracking or complex portfolio management.
- If you are not comfortable managing a self-hosted server for synchronization.

## Getting started

### Docker
To run Actual Budget using Docker:

```bash
docker run -d \
  --name actual_server \
  -p 5006:5006 \
  -v actual-data:/data \
  --restart unless-stopped \
  actualbudget/actual-server:latest
```

Access the web interface at `http://localhost:5006`.

## CLI examples
Actual Budget is primarily a web application, but you can manage the container:

```bash
# View server logs
docker logs actual_server

# Check version (if supported by the image)
docker exec actual_server node src/app.js --version

# Restart the synchronization server
docker restart actual_server
```

## API examples
Actual Budget provides a REST API for programmatic interaction:

```bash
# Get server info
curl http://localhost:5006/info
```

## Related tools / concepts
- [Firefly III](https://www.firefly-iii.org/)
- [n8n](n8n.md)
- [Vikunja](vikunja.md)
- [Paperless-ngx](paperless-ngx.md)
- [Home Assistant](home-assistant.md)

## Backlog
- Set up automated bank synchronization via GoCardless/Nordigen.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-15

## Sources / References
- [Actual Budget Official Site](https://actualbudget.com/)
- [GitHub Repository](https://github.com/actualbudget/actual)
- [Firefly III Official Site](https://www.firefly-iii.org/)
