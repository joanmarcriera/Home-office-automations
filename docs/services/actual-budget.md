# Actual Budget

Actual is a local-first personal finance tool, a 100% free and open-source application. Since the **v26.6.0 (June 2026)** release, it features enhanced multi-user orchestration and native support for the Model Context Protocol (MCP).

## What it is
Actual is a privacy-focused personal finance manager that uses a local-first architecture. It provides a robust, fast interface for budgeting, transaction tracking, and account management, originally developed as a commercial product before being open-sourced. It relies on a local SQLite database for performance and privacy, with optional end-to-end encrypted synchronization.

## What problem it solves
It solves the problem of "cloud-dependency" and "data-decay" in personal finance. Traditional apps like YNAB or Mint can shut down, change pricing, or suffer from data breaches. Actual ensures your financial data stays on your device, working offline while offering secure synchronization that prevents the server from reading your data.

## Where it fits in the stack
In a home-automation stack, Actual serves as the **Financial Intelligence Layer**. It can ingest data from automated bank scrapers or manual CSV exports and provide a clean API for other home-office agents to query budget status or transaction history. It often integrates with [Authentik](authentik.md) for OIDC-based identity management in multi-user labs.

## Typical use cases
- **Zero-Based Budgeting**: Implementing the "Give Every Dollar a Job" philosophy.
- **Privacy-First Finance**: Managing sensitive financial data without uploading it to a third-party cloud.
- **Multi-Device Syncing**: Keeping budget data in sync between a desktop and mobile device via a self-hosted synchronization server.
- **Agentic Auditing**: Using Claude 4.8 Opus or GPT-5.5 to analyze transaction patterns via the Actual API.

## Strengths
- **Local-First Performance**: Extremely fast UI because all data is stored locally.
- **End-to-End Encryption**: Secure synchronization that ensures privacy even on public or shared servers.
- **Active Community**: Rapidly evolving since going open-source.
- **YNAB Migration**: Excellent compatibility for users moving from YNAB.
- **Advanced Reporting**: Built-in support for Age of Money, Sankey Diagrams, and custom budget analysis.
- **Multi-User Support**: Native OIDC integration for multi-user environments.

## Limitations
- **Self-Hosting Required**: Requires a server (Docker) for multi-device sync and automated bank integration.
- **Learning Curve**: Zero-based budgeting requires a specific mindset and initial setup effort.
- **Limited Investment Tracking**: Primarily focused on budgeting and cash flow rather than complex portfolio or derivatives analysis.

## When to use it
- When you want a privacy-focused, local-first budgeting tool.
- For users who want full control over their financial data and its storage location.
- When you need a 100% free and open-source alternative to YNAB or other SaaS budgeting tools.

## When not to use it
- If you require advanced investment tracking or complex portfolio management (consider specialized tools like Portfolio Performance).
- If you are not comfortable managing a self-hosted server for synchronization or bank API secrets.

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
Actual Budget is primarily a web application, but you can manage the container or use the experimental **Actual CLI** (v26.6.0+).

### Container Management
```bash
# View server logs
docker logs actual_server

# Check version
docker exec actual_server node src/app.js --version

# Restart the synchronization server
docker restart actual_server
```

### Actual CLI (Experimental)
The Actual CLI allows for headless interaction with your budget.
```bash
# Initialize the CLI
npx @actual-app/api --server-url http://localhost:5006 --password YOUR_PASSWORD

# List accounts and their balances
npx @actual-app/api accounts
```

## API examples
Actual Budget provides a REST API for programmatic interaction:

```bash
# Get server info
curl http://localhost:5006/info
```

### Automated Bank Synchronization
Actual Budget supports automated transaction ingestion from banks via the GoCardless (formerly Nordigen) API.

```bash
# Example: Trigger a bank sync for a specific account via API
curl -X POST "http://localhost:5006/api/v1/accounts/YOUR_ACCOUNT_ID/sync" \
     -H "X-Actual-Token: YOUR_API_TOKEN"
```

## Related tools / concepts
- [Firefly III](https://www.firefly-iii.org/) — A web-based personal finance manager (alternative).
- [n8n](n8n.md) — For automating bank exports or budgeting alerts.
- [Vikunja](vikunja.md) — For managing financial tasks and goals.
- [Paperless-ngx](paperless-ngx.md) — For archiving receipts and matching them to transactions.
- [Home Assistant](home-assistant.md) — To display budget status on home dashboards.
- [Authentik](authentik.md) — For OIDC multi-user authentication.
- [Syncthing](syncthing.md) — For manual file-based budget synchronization.
- [Gitea](gitea.md) — For version-controlling budget exports and backups.
- [Claude 4.8 Opus](../tools/ai_knowledge/claude.md) — For analyzing complex spending trends.

## Bank Synchronization Setup

### GoCardless Configuration
1. Create a free account at [GoCardless (Bank Account Data)](https://gocardless.com/bank-account-data/).
2. Generate a **Secret ID** and **Secret Key** in the GoCardless dashboard.
3. In Actual Budget, navigate to **Settings > GoCardless** and enter your credentials.

### Linking Accounts
1. Once configured, click **Add Account** in the sidebar.
2. Select **Link Bank Account**.
3. Follow the secure OAUTH flow provided by GoCardless to authorize Actual to read your transaction history.
4. Map the discovered bank accounts to your internal Actual budget accounts.

### Manual CSV Imports
For banks not supported by GoCardless, Actual provides a robust CSV import tool with "Import Rules" that can automatically categorize transactions based on descriptions or amounts.

## Sources / references
- [Actual Budget Official Site](https://actualbudget.com/)
- [GitHub Repository](https://github.com/actualbudget/actual)
- [Firefly III Official Site](https://www.firefly-iii.org/)
- [GoCardless API Documentation](https://developer.gocardless.com/bank-account-data/)

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).
- [ ] Document the new Sankey Diagram configuration options added in v26.5.0.

## Contribution Metadata
- Last reviewed: 2026-06-17
- Confidence: high
