# Actual Budget

Actual is a local-first personal finance tool, a 100% free and open-source application. Since the **v26.11.0 (late October / November 2026)** release, it features enhanced multi-user orchestration and native support for the **Model Context Protocol (MCP) 3.1 / FastMCP** standard.

## What it is
Actual is a privacy-focused personal finance manager that uses a local-first architecture. It provides a robust, fast interface for budgeting, transaction tracking, and account management, originally developed as a commercial product before being open-sourced. It relies on a local SQLite database for performance and privacy, with optional end-to-end encrypted synchronization.

## What problem it solves
It solves the problem of "cloud-dependency" and "data-decay" in personal finance. Traditional apps like YNAB or Mint can shut down, change pricing, or suffer from data breaches. Actual ensures your financial data stays on your device, working offline while offering secure synchronization that prevents the server from reading your data.

## Where it fits in the stack
In a home-automation stack, Actual serves as the **Financial Intelligence Layer**. It can ingest data from automated bank scrapers or manual CSV exports and provide a clean API for other home-office agents to query budget status or transaction history. It often integrates with [Authentik](authentik.md) for OIDC-based identity management and [n8n](n8n.md) for automated workflows.

## Typical use cases
- **Zero-Based Budgeting**: Implementing the "Give Every Dollar a Job" philosophy.
- **Privacy-First Finance**: Managing sensitive financial data without uploading it to a third-party cloud.
- **Multi-Device Syncing**: Keeping budget data in sync between a desktop and mobile device via a self-hosted synchronization server.
- **Agentic Auditing**: Using [Claude 5.1](../tools/providers/anthropic.md) or [Gemma 3](../tools/ai_knowledge/local_llms.md) to analyze transaction patterns via the Actual MCP 3.1 server.

## Strengths
- **Local-First Performance**: Extremely fast UI because all data is stored locally.
- **End-to-End Encryption**: Secure synchronization that ensures privacy even on public or shared servers.
- **Active Community**: Rapidly evolving since going open-source.
- **YNAB Migration**: Excellent compatibility for users moving from YNAB.
- **Advanced Reporting**: Built-in support for Age of Money, Sankey Diagrams, and custom budget analysis.
- **MCP 3.1 / FastMCP Support**: Native support for autonomous agent interaction, tool execution, and structured data retrieval.

## Limitations
- **Self-Hosting Required**: Requires a server (Docker) for multi-device sync and automated bank integration.
- **Learning Curve**: Zero-based budgeting requires a specific mindset and initial setup effort.
- **Limited Investment Tracking**: Primarily focused on budgeting and cash flow rather than complex portfolio or derivatives analysis.

## When to use it
- When you want a privacy-focused, local-first budgeting tool.
- For users who want full control over their financial data and its storage location.
- When you need a 100% free and open-source alternative to YNAB or other SaaS budgeting tools.
- To integrate financial data into [Agentic Workflows](../knowledge_base/patterns/agentic-workflows.md).

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
Actual Budget is primarily a web application, but you can manage the container or use the **Actual CLI** (v26.11.0+).

### Container Management
```bash
# View server logs
docker logs actual_server

# Check version
docker exec actual_server node src/app.js --version

# Restart the synchronization server
docker restart actual_server
```

### Actual CLI
The Actual CLI allows for headless interaction with your budget.
```bash
# Initialize the CLI
npx @actual-app/api --server-url http://localhost:5006 --password YOUR_PASSWORD

# List accounts and their balances
npx @actual-app/api accounts
```

## API examples
Actual Budget provides a REST API and an [MCP 3.1](../tools/automation_orchestration/mcp.md) server for programmatic interaction:

```bash
# Get server info
curl http://localhost:5006/info
```

### Automated Bank Synchronization & Pydantic Validation
Actual Budget supports automated transaction ingestion from banks via the GoCardless API and programmatic parsing.

Here is a Python example using **Pydantic v2** to validate transaction payloads prior to importing or syncing them into the Actual Budget API:

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ActualBudgetTransactionModel(BaseModel):
    """
    Pydantic v2 model representing an Actual Budget synchronized transaction
    via the bank sync or REST API.
    """
    id: str = Field(..., description="Unique transaction identifier")
    account_id: str = Field(..., description="Target account ID within Actual Budget")
    amount: int = Field(..., description="Transaction amount in cents (e.g., -1000 for -$10.00)")
    payee: str = Field(..., min_length=1, description="The merchant or payee name")
    category: Optional[str] = Field(None, description="Inferred or matched budget category name")
    date: date = Field(..., description="Transaction posting date")
    cleared: bool = Field(default=False, description="Whether the transaction has cleared")

# Example payload validation
raw_payload = {
    "id": "tx_890123",
    "account_id": "acc_savings_01",
    "amount": -2499,
    "payee": "Target Stores Inc.",
    "category": "Household Supplies",
    "date": "2026-11-06",
    "cleared": True
}

transaction = ActualBudgetTransactionModel.model_validate(raw_payload)
print(f"Validated Transaction for {transaction.payee}: ${abs(transaction.amount)/100:.2f}")
```

To trigger a bank sync:
```bash
# Trigger a bank sync for a specific account via API
curl -X POST "http://localhost:5006/api/v1/accounts/YOUR_ACCOUNT_ID/sync" \
     -H "X-Actual-Token: YOUR_API_TOKEN"
```

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md) — For archiving receipts and matching them to transactions.
- [n8n](n8n.md) — For automating bank exports or budgeting alerts.
- [Home Assistant](home-assistant.md) — To display budget status on home dashboards.
- [Authentik](authentik.md) — For OIDC multi-user authentication.
- [Claude 5.1](../tools/providers/anthropic.md) — For analyzing complex spending trends.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — For local AI analysis of financial data.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — For standardizing financial data access for agents.
- [Agentic Workflows](../knowledge_base/patterns/agentic-workflows.md) — Patterns for autonomous financial management.

## Sources / references
- [Actual Budget Official Site](https://actualbudget.com/)
- [GitHub Repository](https://github.com/actualbudget/actual)
- [Actual Budget MCP Server](https://github.com/actualbudget/mcp-server-actual)
- [GoCardless API Documentation](https://developer.gocardless.com/bank-account-data/)

## Contribution Metadata
- Last reviewed: 2026-11-06
- Confidence: high
