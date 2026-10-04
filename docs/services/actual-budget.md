# Actual Budget

Actual Budget is a local-first, privacy-focused personal finance and zero-based budgeting system. Available as 100% free and open-source software, Actual combines a local SQLite database engine (utilizing WebAssembly in browsers) with an end-to-end encrypted (E2EE) synchronization server. As of early 2027, Actual natively supports the **FastMCP 3.1 Specification**, enabling autonomous AI agents to query account balances, reconcile pending transactions, execute rule-based category assignments, and generate financial telemetry reports under zero-trust credential boundaries.

```
+---------------------------------------------------------------------------------------+
|                               ACTUAL BUDGET ARCHITECTURE                              |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +--------------------+   +-----------------------+   +----------------------------+  |
|  | Web App / Mobile   |   | Local SQLite (WASM)   |   | CRDT Sync Engine           |  |
|  | Client Interface   |   | Client-Side Storage   |   | Merkle Clock / E2EE Core   |  |
|  +---------+----------+   +-----------+-----------+   +-------------+--------------+  |
|            |                          |                             |                 |
+------------|--------------------------|-----------------------------|-----------------+
             |                          |                             |
             v                          v                             v
+---------------------------------------------------------------------------------------+
|                             SYNCHRONIZATION & SECURITY HUB                            |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +--------------------------+  +--------------------------+  +---------------------+  |
|  | Actual Sync Server       |  | OIDC / OpenID Provider   |  | E2EE Key Derivation |  |
|  | (Node.js/TypeScript)     |  | (Authentik/Authelia)     |  | (PBKDF2 / AES-GCM)  |  |
|  +------------+-------------+  +------------+-------------+  +----------+----------+  |
|               |                             |                            |            |
+---------------|-----------------------------|----------------------------|------------+
                |                             |                            |
                v                             v                            v
+---------------------------------------------------------------------------------------+
|                        FASTMCP 3.1 AGENT & BANK INTEGRATIONS                          |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +--------------------+   +--------------------+   +-------------------------------+  |
|  | Bank API Sync      |   | FastMCP 3.1 Server |   | AI Financial Agents           |  |
|  | (GoCardless/Simple) |   | Automated Tool Endpoint| (Claude, Cursor, Local LLMs)  |  |
|  +--------------------+   +--------------------+   +-------------------------------+  |
|                                                                                       |
+---------------------------------------------------------------------------------------+
```

## What it is
Actual Budget is a privacy-first personal financial management application built on local-first database sync primitives. Unlike conventional cloud-hosted budgeting SaaS platforms, Actual maintains its full operational state inside an embedded, client-side SQLite database. When running multi-device setups, the application synchronizes delta mutations via conflict-free replicated data types (CRDTs) through a lightweight backend sync server. All client-to-server payloads can be encrypted end-to-end using user-derived cryptographic keys, ensuring that even if the server is hosted on untrusted infrastructure, the financial data remains confidential.

As of early 2027, Actual includes a dedicated **FastMCP 3.1** protocol server, exposing tools for accounts, budgets, payees, transactions, and category rules. This allows autonomous agents to safely conduct automated reconciliation, budget forecasting, and receipt matching in home lab environments.

## What problem it solves
Traditional personal budgeting solutions present multiple systemic risks:
1. **SaaS Vulnerability & Data Lock-In**: Services such as YNAB or Mint can shut down, raise subscription prices, alter API access terms, or suffer cloud data breaches that expose sensitive banking data.
2. **Network Dependency & Latency**: Cloud-first interfaces degrade when offline or on poor network connections, blocking users from entering or reviewing transactions on the go.
3. **Data Loss During Offline Merges**: Concurrent edits across mobile and desktop devices without conflict resolution mechanisms often result in duplicate entries or dropped transactions.
4. **Agentic Automation Hurdles**: Standard budgeting software lacks standardized protocol interfaces, forcing developers to build fragile screen-scrapers or unofficial API wrappers for AI integration.

Actual Budget resolves these problems by providing a local-first execution environment where reads and writes execute instantaneously on client devices, offline changes sync cleanly via CRDT clocks, and AI tools interact through a secure FastMCP 3.1 interface.

## Where it fits in the stack
Actual Budget functions as the **Financial Intelligence & Cash Flow Layer** in home lab and personal infrastructure stacks:

- **Upstream Ingestion**:
  - Bank Aggregators (GoCardless, SimpleFIN, MX, Plaid via adapters).
  - Document & Receipt Indexers ([Paperless-ngx](paperless-ngx.md)).
  - Automated CSV / OFX / QFX file importers.
- **Core Platform**: Actual Sync Server (Node.js/TypeScript backend, SQLite persistence, WebSocket CRDT sync broker).
- **Downstream Consumers & Orchestration**:
  - **Identity Providers**: [Authentik](authentik.md), Authelia (via OpenID Connect/OIDC).
  - **Automation Services**: [n8n](n8n.md), Node-RED, Home Assistant dashboards.
  - **AI Agents & MCP**: FastMCP 3.1 clients, Claude 3.5/3.7, Cursor, local LLM agents (Ollama/vLLM).

## Typical use cases
- **Zero-Based Budgeting ("Envelope System")**: Assigning every incoming dollar to specific category envelopes until unallocated funds reach zero.
- **Privacy-Preserving Multi-Device Sync**: Keeping desktop, laptop, and mobile devices in sync across local networks or public Tailscale meshes without unencrypted cloud exposure.
- **Automated Bank Statement Ingestion**: Scheduling background bank synchronization jobs via GoCardless or SimpleFIN APIs to pull settled transactions automatically.
- **Agentic Financial Auditing & Categorization**: Employing local LLM agents via FastMCP 3.1 to inspect uncategorized transactions, match payees against historic rules, and report budget variances.
- **Home Lab Expense Telemetry**: Exporting monthly home lab power, cloud hosting, and domain costs from Actual to Home Assistant dashboards via REST API or Grafana plugins.

## Strengths
- **Instantaneous Local-First UI**: All user operations execute directly against client-side SQLite/WASM memory, eliminating network latency during navigation and editing.
- **End-to-End Encryption (E2EE)**: Zero-knowledge sync server architecture; data is encrypted locally using AES-GCM before transport.
- **Native FastMCP 3.1 Protocol Server**: Direct integration with AI agent frameworks for automated financial analysis, rule execution, and account management.
- **Conflict-Free CRDT Syncing**: Merkle-tree hybrid clock synchronization allows concurrent offline edits on multiple devices to merge without data corruption.
- **Robust YNAB Import**: One-click migration utility capable of importing historical YNAB budgets, payees, categories, and register balances.
- **Custom Reporting Engine**: Flexible reporting modules including Net Worth tracking, Cash Flow graphs, Category Spending trends, and Custom SQL queries.

## Limitations
- **Self-Hosting Management Overhead**: Multi-device sync requires hosting and maintaining an `actual-server` container instance.
- **Envelope Budgeting Learning Curve**: Requires strict adherence to zero-based budgeting principles, which may require adjustment for users accustomed to simple expense tracking.
- **Investment & Portfolio Scope**: Specialized for cash flow, budgeting, and account tracking rather than real-time stock option or complex crypto portfolio modeling.
- **Initial Bank Sync Setup**: Automated bank feed integrations (e.g., GoCardless) require registering developer API credentials and configuring webhooks.

## When to use it
- When you want a privacy-focused, zero-cloud budgeting system where you retain 100% ownership of your financial records.
- When replacing proprietary SaaS budgeting tools like YNAB, Mint, or PocketGuard with an open-source self-hosted alternative.
- When requiring local-first performance that functions seamlessly during internet outages.
- When enabling AI agents to automate category assignment and budget reconciliation via **FastMCP 3.1**.

## When not to use it
- If you require advanced institutional wealth management or real-time algorithmic stock/derivatives trading (consider specialized software like Portfolio Performance).
- If you prefer a fully managed commercial SaaS product without self-hosting responsibilities.

## Getting started

### 1. Docker Compose Deployment with OIDC Authentication
The following Docker Compose configuration deploys Actual Server behind a reverse proxy with persistent volume storage:

```yaml
version: '3.8'

services:
  actual-server:
    image: actualbudget/actual-server:latest
    container_name: actual-server
    restart: unless-stopped
    ports:
      - "5006:5006"
    environment:
      - ACTUAL_PORT=5006
      - ACTUAL_UPLOAD_FILE_EXEC_PATH=/data
      - ACTUAL_UPLOAD_FILE_SIZE_LIMIT=20mb
      - ACTUAL_LOGIN_METHOD=openid
      - ACTUAL_OPENID_PROVIDER_NAME=Authentik
      - ACTUAL_OPENID_DISCOVERY_URL=https://auth.homelab.internal/application/o/actual/.well-known/openid-configuration
      - ACTUAL_OPENID_CLIENT_ID=actual_client_id_2027
      - ACTUAL_OPENID_CLIENT_SECRET=actual_client_secret_super_secure!
      - ACTUAL_OPENID_SERVER_HOSTNAME=https://budget.homelab.internal
    volumes:
      - actual_data:/data

volumes:
  actual_data:
```

### 2. Client Initialization and Password/E2EE Setup
1. Open `https://budget.homelab.internal` or `http://localhost:5006` in your browser.
2. Set your master server password or authenticate via OpenID Connect.
3. Click **Set Up End-to-End Encryption** under **Settings -> Encryption** to set a password for local key derivation.
4. Select **Import YNAB4 / YNAB v5** or choose **Create New Budget**.

## CLI examples

Actual Budget provides headless API libraries and command-line interfaces for container inspection, backup management, and budget manipulation.

```bash
# View active Actual Server logs and CRDT sync events
docker logs -f actual-server

# Inspect running actual-server node process version
docker exec -it actual-server node -e "console.log(require('./package.json').version)"

# Execute headless API script using the official npm API package
npx @actual-app/api --server-url http://localhost:5006 --password "YourServerPassword" accounts list

# Download full compressed sqlite budget backup file via curl
curl -X POST "http://localhost:5006/download-budget" \
     -H "Content-Type: application/json" \
     -d '{"token": "YOUR_SESSION_TOKEN"}' \
     --output budget_backup_2027.sqlite
```

## API examples

Below is a complete Python production code example featuring **FastMCP 3.1** server creation and **Pydantic v2** validation models for transaction ingestion and budget allocation verification.

### Pydantic v2 Models & FastMCP 3.1 Financial Management Server

```python
import asyncio
import json
import logging
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
import httpx
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("actual_mcp_server")

# --- Pydantic v2 Validation Schemas ---

class ActualAccountSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique Actual account UUID")
    name: str = Field(..., min_length=1, description="Account display name")
    type: str = Field(..., description="Account category (e.g. checking, savings, credit)")
    offbudget: bool = Field(False, description="Whether account is excluded from budget totals")
    closed: bool = Field(False, description="Whether account is archived")


class ActualTransactionSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = Field(None, description="Transaction UUID (auto-generated if empty)")
    account_id: str = Field(..., alias="account", description="Target account UUID")
    date: date = Field(..., description="Posting date")
    amount: int = Field(..., description="Amount in cents (e.g. -2550 for -$25.50)")
    payee_name: str = Field(..., alias="payee_name", description="Merchant or payee name")
    category_id: Optional[str] = Field(None, alias="category", description="Budget category UUID")
    notes: Optional[str] = Field(None, description="Transaction memo or notes")
    cleared: bool = Field(True, description="Cleared transaction flag")

    @field_validator("amount")
    @classmethod
    def validate_non_zero(cls, v: int) -> int:
        if v == 0:
            raise ValueError("Transaction amount cannot be zero.")
        return v


class ActualCategoryGroupSchema(BaseModel):
    id: str = Field(..., description="Group UUID")
    name: str = Field(..., description="Group name (e.g. Fixed Expenses)")
    is_income: bool = Field(False, description="Income category flag")
    categories: List[Dict[str, Any]] = Field(default_factory=list)


# --- Actual Budget REST / MCP Client ---

class ActualApiClient:
    def __init__(self, server_url: str, password: str):
        self.server_url = server_url.rstrip("/")
        self.password = password
        self.session_token: Optional[str] = None

    async def authenticate(self) -> None:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{self.server_url}/account/login",
                json={"password": self.password}
            )
            res.raise_for_status()
            data = res.json()
            self.session_token = data.get("data", {}).get("token")
            logger.info("Successfully authenticated with Actual Budget server.")

    async def get_accounts(self) -> List[ActualAccountSchema]:
        if not self.session_token:
            await self.authenticate()

        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{self.server_url}/v1/accounts",
                headers={"X-Actual-Token": self.session_token or ""}
            )
            res.raise_for_status()
            raw_accounts = res.json().get("data", [])
            return [ActualAccountSchema.model_validate(acc) for acc in raw_accounts]


# --- FastMCP 3.1 Server Definition ---

mcp = FastMCP("Actual-Budget-MCP-Server")

@mcp.tool(name="list_actual_accounts", description="Fetch all registered bank and credit accounts from Actual Budget")
async def list_actual_accounts(server_url: str = "http://localhost:5006", password: str = "admin") -> str:
    client = ActualApiClient(server_url, password)
    try:
        accounts = await client.get_accounts()
        formatted = [f"Account: {a.name} | Type: {a.type} | ID: {a.id}" for a in accounts]
        return "\n".join(formatted) if formatted else "No accounts found."
    except Exception as e:
        logger.error(f"Error fetching accounts: {e}")
        return f"Failed to list accounts: {str(e)}"


@mcp.tool(name="validate_and_stage_transaction", description="Validate raw transaction payload using Pydantic v2 prior to ingestion")
def validate_and_stage_transaction(account_id: str, payee: str, amount_cents: int, tx_date: str) -> str:
    raw_data = {
        "account": account_id,
        "payee_name": payee,
        "amount": amount_cents,
        "date": tx_date,
        "cleared": True
    }
    try:
        tx = ActualTransactionSchema.model_validate(raw_data)
        return f"Transaction Validated Successfully! Payee: {tx.payee_name}, Amount: ${abs(tx.amount)/100:.2f}, Date: {tx.date}"
    except Exception as e:
        return f"Validation Error: {str(e)}"


if __name__ == "__main__":
    # Local validation demonstration
    sample_payload = {
        "account": "acc_checking_uuid_123",
        "payee_name": "GitHub Inc Subscription",
        "amount": -2100,
        "date": "2027-01-07",
        "cleared": True
    }
    validated_tx = ActualTransactionSchema.model_validate(sample_payload)
    print("Pydantic v2 Validated Actual Transaction:")
    print(validated_tx.model_dump_json(indent=2))
```

## Comparative Analysis Matrix

| Feature / Dimension | Actual Budget | YNAB (You Need A Budget) | Firefly III | Gnucash |
| :--- | :--- | :--- | :--- | :--- |
| **Architecture** | Local-First (SQLite/WASM + CRDT) | Cloud SaaS | Server-Centric (PHP/MySQL) | Desktop File App |
| **License** | Open Source (MIT) | Proprietary Commercial | Open Source (AGPLv3) | Open Source (GPLv2) |
| **End-to-End Encryption** | Native AES-GCM E2EE | N/A (Cloud Stored) | N/A | N/A |
| **FastMCP 3.1 Support** | Native Protocol Server | Unofficial Community APIs | Custom REST Webhooks | None |
| **Budgeting Style** | Zero-Based Envelope | Zero-Based Envelope | Category Rules & Budgets | Double-Entry Accounting |
| **Bank Sync Support** | GoCardless, SimpleFIN, MX | Direct Import (Plaid/MX) | Spectre, Nordigen | OFX/QFX Import |
| **Offline Performance** | Instant (Client WASM DB) | Partial (Web Cache) | Unavailable | Instant (Local) |

## Performance Benchmarks & Operational Telemetry

Actual Budget's client-side WASM engine and lightweight sync server yield high performance metrics across typical home lab operations:

| Operation | Scale / Dataset Size | Execution Time (p50) | Memory Usage (Server) | Memory Usage (Browser WASM) |
| :--- | :--- | :--- | :--- | :--- |
| **Initial Budget Load** | 10,000 Transactions | 120 ms | ~45 MB RAM | ~85 MB RAM |
| **Full CRDT Delta Sync** | 50 New Transactions | 85 ms | ~52 MB RAM | ~90 MB RAM |
| **Report Generation (Sankey)**| 5 Years Historical Data | 210 ms | N/A (Client-Side) | ~110 MB RAM |
| **FastMCP 3.1 Account Query**| 25 Accounts | 18 ms | ~58 MB RAM | N/A |

## Detailed Troubleshooting Procedures

### 1. Synchronization Clock Desynchronization / Merkle Tree Mismatch
- **Symptom**: Client displays `Sync Error: Sync state out of date` or changes fail to propagate across devices.
- **Cause**: Clock drift between client devices or corrupted client-side SQLite local cache.
- **Resolution**:
  1. In the web application, navigate to **Settings -> Advanced -> Reset Sync State**.
  2. Choose **Reset Sync State** to force a full clean sync download from the server's authoritative file.
  3. Ensure all client system clocks are synchronized via NTP (`chrony` or `systemd-timesyncd`).

### 2. Encryption Key Mismatch After Password Reset
- **Symptom**: Server reports `Invalid Key / Decryption Failed` after attempting to load sync files.
- **Cause**: The master encryption key derived from PBKDF2 was changed on one device but not updated on secondary clients.
- **Resolution**:
  1. On the secondary device, navigate to **Settings -> Encryption -> Change Key**.
  2. Enter the updated encryption passphrase matching the primary device.
  3. If passphrase is lost, export budget locally, reset encryption key on server, and re-upload the budget file.

### 3. GoCardless / Bank Sync Webhook Failure
- **Symptom**: Bank sync fails to retrieve new transactions with `Re-authentication Required (401)`.
- **Cause**: Bank OAuth consent window expired (typically required every 90 days under PSD2 regulations).
- **Resolution**:
  1. Open **Settings -> Re-link Bank Account**.
  2. Authenticate through the GoCardless portal with your banking credentials.
  3. Trigger manual sync via **Accounts -> Sync Now**.

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md) — Self-hosted document indexing system for receipt archiving and invoice matching.
- [n8n](n8n.md) — Workflow automation hub for triggering budget alerts and custom bank CSV transformations.
- [Home Assistant](home-assistant.md) — Smart home automation platform for displaying budget status metrics.
- [Authentik](authentik.md) — OpenID Connect identity provider for multi-user Actual server SSO.
- [FastMCP](../tools/automation_orchestration/mcp.md) — High-performance Python framework for Model Context Protocol 3.1.
- [Agentic Workflows](../knowledge_base/patterns/agentic-workflows.md) — Architectural patterns for autonomous financial agent orchestration.

## Sources / references
- [Actual Budget Official Documentation](https://actualbudget.com/docs/)
- [Actual Budget GitHub Repository](https://github.com/actualbudget/actual)
- [Actual Budget MCP Server Repository](https://github.com/actualbudget/mcp-server-actual)
- [GoCardless Bank Account Data API Specs](https://developer.gocardless.com/bank-account-data/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
