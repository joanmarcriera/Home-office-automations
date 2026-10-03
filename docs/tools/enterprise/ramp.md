# Ramp

## What it is
Ramp is a corporate finance platform, spending control engine, and automated accounting system that unifies corporate card issuance, expense management, invoice processing, and ERP integrations into an AI-powered interface. Built with **Ramp Intelligence**, Ramp employs autonomous financial agents driven by frontier models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4) to perform real-time receipt parsing, line-item SKU categorizations, ERP ledger reconciliations, and contract negotiation routines.

Ramp operates as an "Agentic Commerce and Corporate Governance Gateway." Enterprise developers and finance teams utilize Ramp's REST APIs and FastMCP 3.1 Model Context Protocol servers to grant AI agents (such as Claude Code or custom procurement workflows) autonomous spending capabilities constrained by programmatic velocity controls, merchant lockouts, pre-approved spending limits, and multi-tier manager approval flows.

```
+---------------------------------------------------------------------------------------------------+
|                                     RAMP FINANCE & AGENT ARCHITECTURE                             |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +-----------------------+     +-------------------------------+     +-------------------------+  |
|  | Enterprise AI Agents  |     | FastMCP 3.1 Gateway Server    |     | Ramp Developer API      |  |
|  | (Procurement Workers) | <-> | (mcp-server-ramp-finance)     | <-> | (OAuth2 / Developer API)|  |
|  +-----------------------+     +-------------------------------+     +-------------------------+  |
|              |                                 |                                  |               |
|              v                                 v                                  v               |
|  +---------------------------------------------------------------------------------------------+  |
|  |                                RAMP INTELLIGENCE REASONING ENGINE                          |  |
|  +---------------------------------------------------------------------------------------------+  |
|  | - Receipt OCR & SKU Matching           - Vendor Duplicate SaaS Audit Engine                 |  |
|  | - Dynamic Multi-Tier Policy Validator  - Real-Time AI Model Token Expense Tracking          |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                |                                                  |
|                                                v                                                  |
|  +---------------------------------------------------------------------------------------------+  |
|  |                               FINANCIAL SETTLEMENT & ENTERPRISE ERP                        |  |
|  +-------------------------------+-------------------------------+-----------------------------+  |
|  | Visa / Mastercard Card Rail   | Corporate Bank Clearing (ACH) | ERP Sync Engine             |  |
|  | (Virtual & Physical Cards)    | (Bill Pay & Invoice Wire)     | (NetSuite, QuickBooks, SAP) |  |
|  +-------------------------------+-------------------------------+-----------------------------+  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## What problem it solves
Managing corporate expenditure, software subscriptions, and employee expense reports in fast-scaling tech companies introduces significant administrative friction and budget leaks:

- **Manual Expense Processing Overhead**: Employees spend hours scanning receipts and writing expense descriptions, while accounting teams manually cross-reference transactions against GL account codes in NetSuite or SAP. Ramp Intelligence automates receipt matching and GL coding with 99%+ accuracy.
- **Unmonitored AI Token Spending**: Engineering teams deploying LLM applications across multiple AI providers (e.g., Anthropic, OpenAI, Google Cloud, Hugging Face) suffer from fragmented billing dashboards. Ramp unifies model API spend into real-time token tracking views.
- **Uncontrolled Agent Procurement**: Allowing autonomous software agents to purchase cloud compute or SaaS licenses risks runaway API charges. Ramp provides programmatic virtual card issuance with hard spending caps, expiration timestamps, and merchant category restrictions.
- **Duplicate SaaS Tool Bloat**: Enterprises frequently pay for redundant software subscriptions across distinct team silos. Ramp Intelligence scans vendor transactions to detect duplicate software licenses, underutilized seats, and contract price increases.

## Where it fits in the stack
**Category**: Enterprise AI / Finance Automation & Agent Procurement Gateway.

Ramp operates as the corporate spending governance gateway connecting autonomous agent workers to underlying banking rails and enterprise resource planning (ERP) databases:

```
+-----------------------------------------------------------------------------------+
|                             ENTERPRISE STACK PLACEMENT                            |
+-----------------------------------------------------------------------------------+
| Autonomous Agent Layer    | Procurement Agents, DevOps Runners, Claude Code       |
+---------------------------+-------------------------------------------------------+
| Agentic Governance Gateway| Ramp FastMCP 3.1 Server & Virtual Card Policy Controls|
+---------------------------+-------------------------------------------------------+
| Financial Processing Engine| Ramp Intelligence OCR, Line-Item Categorization, Audit|
+---------------------------+-------------------------------------------------------+
| ERP & Accounting Sync     | NetSuite, QuickBooks Online, SAP, Sage Intacct        |
+---------------------------+-------------------------------------------------------+
| Banking & Card Rails      | Visa / Mastercard Network, ACH / Wire Clearing House  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Automated Virtual Card Issuance for DevOps**: Dynamically issuing single-use or merchant-locked virtual cards to automated deployment scripts for cloud compute provisioning (Hetzner, Scaleway, AWS).
- **Enterprise AI Token Spend Tracking**: Monitoring real-time model API spending across [Anthropic](../providers/anthropic.md), [OpenAI](../../tools/ai_knowledge/openai.md), and [Google Gemini](../ai_knowledge/gemini.md) within a unified finance dashboard.
- **Automated Invoice Processing & Accounts Payable**: Ingesting PDF vendor invoices via email webhooks, extracting line-item line data with OCR, and queueing ACH bill payments for manager sign-off.
- **FastMCP 3.1 Financial Governance for Agents**: Registering tools that allow autonomous AI procurement agents to check department budget balances before executing card requests.

## Strengths
- **Native Ramp Intelligence**: Integrated vision models and LLMs perform automatic receipt line-item extraction and SKU matching without manual template rules.
- **Granular Spend Rules**: Virtual cards support merchant category locking, daily/monthly rolling velocity limits, and auto-termination dates.
- **Sub-Second Accounting Sync**: Instant bi-directional sync with major enterprise accounting engines (NetSuite, QuickBooks, Sage Intacct, Workday).
- **Comprehensive API & MCP Extensions**: REST endpoints and FastMCP 3.1 server tools enable seamless integration into agentic workflows.

## Limitations
- **Corporate Card Qualification Thresholds**: Requires businesses to meet specific cash balance thresholds and revenue metrics for approval.
- **Regional Banking Restrictions**: Primary issuance and banking rail features are optimized for US, UK, and EU corporate entities, requiring specialized local setups for other regions.

## When to use it
- When managing multi-million dollar R&D budgets across distributed cloud AI provider accounts.
- When enabling AI agents to purchase third-party APIs or software licenses under strict, programmatic policy bounds.
- When replacing manual expense reports with automated receipt matching and ERP reconciliations.

## When not to use it
- For personal finance or small side project expense tracking (use [Actual Budget](../../services/actual-budget.md) instead).
- For consumer-facing peer-to-peer payment processing.

## Getting started

### Enabling Ramp Developer API Access
1. Log into your **Ramp Developer Dashboard** as an administrator.
2. Navigate to **Settings > Developer API & Integrations** and generate an OAuth2 or API Token with required read/write scopes (`cards:write`, `transactions:read`, `bills:write`).
3. Set environment variables in your secure vault or container runner:

```bash
export RAMP_CLIENT_ID="ramp_client_id_2027_production"
export RAMP_CLIENT_SECRET="ramp_client_secret_secret_key"
export RAMP_API_TOKEN="ramp_dev_access_token_2027"
```

## CLI examples

```bash
# 1. Inspect enterprise AI provider transaction list via cURL
curl -s -X GET "https://api.ramp.com/developer/v1/transactions?merchant_name=Anthropic" \
  -H "Authorization: Bearer $RAMP_API_TOKEN" \
  -H "Content-Type: application/json" | jq .

# 2. Issue a virtual card for an automated cloud runner with a $500 monthly cap
curl -s -X POST "https://api.ramp.com/developer/v1/cards/virtual" \
  -H "Authorization: Bearer $RAMP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "DevOps Scaleway Runner Card",
    "cardholder_id": "usr_devops_001",
    "amount": {"amount": 50000, "currency": "USD"},
    "fulfillment": {"type": "VIRTUAL"},
    "spending_restrictions": {
      "interval": "MONTHLY",
      "allowed_merchant_categories": ["COMPUTER_SOFTWARE", "CLOUD_SERVICES"]
    }
  }' | jq .

# 3. Query Ramp Intelligence SaaS duplicate subscription recommendations
curl -s -X GET "https://api.ramp.com/developer/v1/insights/subscriptions" \
  -H "Authorization: Bearer $RAMP_API_TOKEN" | jq '.data[] | select(.potential_savings > 1000)'

# 4. Fetch department budget usage summaries
curl -s -X GET "https://api.ramp.com/developer/v1/departments/dept_eng_01/budget" \
  -H "Authorization: Bearer $RAMP_API_TOKEN" | jq .
```

## API examples

### FastMCP 3.1 Autonomous Finance Server
The following Python server implements a **FastMCP 3.1** protocol gateway allowing agentic systems to query budget balances and request virtual cards under strict financial policies:

```python
"""
Ramp Autonomous Finance FastMCP 3.1 Server
Exposes tools for AI agents to check budgets and request card issuance within governance rules.
"""

import json
import logging
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ramp-mcp")

# Initialize FastMCP Server
mcp = FastMCP(
    "Ramp Finance Governance Server",
    version="3.1.0",
    description="FastMCP server for agentic procurement, card issuance, and spend auditing"
)

class CardRequestSpec(BaseModel):
    agent_id: str = Field(..., description="Unique agent identifier requesting card")
    purpose_description: str = Field(..., description="Justification for card issuance")
    monthly_limit_usd: float = Field(..., ge=10.0, le=5000.0, description="Monthly spending cap in USD")
    merchant_category: str = Field("CLOUD_INFRASTRUCTURE", description="Allowed merchant classification")
    expiration_days: int = Field(30, ge=1, le=90, description="Card lifespan in days")

class CardIssuanceResponse(BaseModel):
    success: bool
    card_id: Optional[str] = None
    masked_card_number: Optional[str] = None
    monthly_limit_usd: float
    expiration_date: str
    status_message: str

class SpendAuditQuery(BaseModel):
    department_id: str = Field(..., description="Department identifier (e.g. dept_engineering)")
    include_ai_token_breakdown: bool = Field(True, description="Filter for LLM provider transactions")

@mcp.tool()
def issue_agent_virtual_card(spec: CardRequestSpec) -> str:
    """
    Issue a virtual corporate card for an AI agent worker subject to policy limit checks.
    """
    logger.info(f"Agent {spec.agent_id} requested virtual card for '{spec.purpose_description}' with cap ${spec.monthly_limit_usd}")

    # Enforce policy limit checks
    if spec.monthly_limit_usd > 2500.0:
        response = CardIssuanceResponse(
            success=False,
            monthly_limit_usd=spec.monthly_limit_usd,
            expiration_date="",
            status_message="Card limit exceeds automated agent threshold ($2,500.00 USD). Manager approval required."
        )
        return response.model_dump_json(indent=2)

    response = CardIssuanceResponse(
        success=True,
        card_id=f"card_v_{spec.agent_id}_2027",
        masked_card_number="•••• •••• •••• 4892",
        monthly_limit_usd=spec.monthly_limit_usd,
        expiration_date="2027-02-07",
        status_message="Virtual card successfully provisioned and locked to CLOUD_INFRASTRUCTURE."
    )
    return response.model_dump_json(indent=2)

@mcp.tool()
def audit_ai_model_spend(query: SpendAuditQuery) -> str:
    """
    Audit current monthly AI provider expenditure (Anthropic, OpenAI, Gemini) for a department.
    """
    logger.info(f"Auditing AI spend for {query.department_id}")

    audit_data = {
        "department_id": query.department_id,
        "billing_period": "2027-01",
        "total_ai_spend_usd": 8420.50,
        "provider_breakdown": [
            {"provider": "Anthropic PBC", "amount_usd": 4850.00, "models": ["Claude 5.6"]},
            {"provider": "OpenAI Inc", "amount_usd": 2420.50, "models": ["GPT-5.6"]},
            {"provider": "Google Cloud (Vertex AI)", "amount_usd": 1150.00, "models": ["Gemini 4.0 Pro"]}
        ],
        "policy_compliant": True
    }
    return json.dumps(audit_data, indent=2)

if __name__ == "__main__":
    mcp.run()
```

### Financial Transaction Schema Validation using Pydantic v2
This production script parses and validates Ramp card transaction feeds and line-item receipt objects:

```python
"""
Ramp Transaction Feed Schema Validator
Validates transaction feeds and Line-Item OCR metadata using Pydantic v2.
"""

import json
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator

class LineItemSKU(BaseModel):
    sku_description: str = Field(..., description="Line-item product description")
    quantity: int = Field(1, ge=1, description="Quantity purchased")
    unit_price: float = Field(..., ge=0.0, description="Unit cost in transaction currency")

class MerchantInfo(BaseModel):
    merchant_name: str = Field(..., description="Vendor trading name")
    merchant_category_code: str = Field(..., description="MCC code string")
    country_code: str = Field("US", min_length=2, max_length=2, description="Vendor country code")

class RampTransactionRecord(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction ID (tx_...)")
    card_id: str = Field(..., description="Associated Ramp card ID")
    cardholder_email: str = Field(..., description="Employee or agent email owner")
    amount_usd: float = Field(..., gt=0.0, description="Transaction amount in USD")
    merchant: MerchantInfo = Field(..., description="Vendor details")
    skus: List[LineItemSKU] = Field(default_factory=list, description="Extracted receipt line items")
    receipt_attached: bool = Field(False, description="Whether receipt is attached")
    flagged_for_review: bool = Field(False, description="Flagged by Ramp Intelligence for policy violation")
    transaction_timestamp: datetime = Field(..., description="ISO timestamp of transaction")

class TransactionAuditBatchPayload(BaseModel):
    batch_id: str = Field(..., description="Batch execution identifier")
    records: List[RampTransactionRecord] = Field(..., min_items=1, description="List of validated records")

def validate_transaction_batch(raw_json: str) -> Optional[TransactionAuditBatchPayload]:
    try:
        data = json.loads(raw_json)
        batch = TransactionAuditBatchPayload.model_validate(data)
        print(f"Batch '{batch.batch_id}' successfully validated {len(batch.records)} transactions.")
        total_value = sum(tx.amount_usd for tx in batch.records)
        print(f" - Total Transaction Value: ${total_value:.2f} USD")
        return batch
    except ValidationError as err:
        print("Ramp Transaction Validation Error:")
        print(err.json(indent=2))
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON payload.")
        return None

if __name__ == "__main__":
    sample_payload = json.dumps({
        "batch_id": "batch-ramp-20270107-01",
        "records": [
            {
                "transaction_id": "tx_ramp_908123",
                "card_id": "card_v_devops_runner",
                "cardholder_email": "agent_runner@company.com",
                "amount_usd": 1250.00,
                "merchant": {
                    "merchant_name": "Anthropic PBC",
                    "merchant_category_code": "5734",
                    "country_code": "US"
                },
                "skus": [
                    {
                        "sku_description": "Claude 5.6 API Token Batch Usage",
                        "quantity": 1,
                        "unit_price": 1250.00
                    }
                ],
                "receipt_attached": True,
                "flagged_for_review": False,
                "transaction_timestamp": "2027-01-07T14:30:00Z"
            }
        ]
    })

    validate_transaction_batch(sample_payload)
```

## Related tools / concepts
- [Glean](glean.md) — Enterprise search and AI knowledge management system.
- [Fyxer AI](fyxer.md) — AI assistant for automated executive workflows.
- [Hebbia](hebbia.md) — AI document analysis matrix engine for finance.
- [tldv](tldv.md) — AI meeting capture and transcription tool.
- [Actual Budget](../../services/actual-budget.md) — Self-hosted personal budget engine.
- [n8n](../../services/n8n.md) — Workflow engine connecting Ramp webhooks to enterprise systems.
- [Langfuse](../process_understanding/langfuse.md) — LLM observability and token tracking platform.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open protocol for FastMCP 3.1 integrations.
- [Anthropic](../providers/anthropic.md) — Frontier AI provider for Claude models.
- [OpenAI](../../tools/ai_knowledge/openai.md) — Frontier AI provider for GPT models.

## Sources / references
- [Ramp Official Portal](https://ramp.com/)
- [Ramp Intelligence Product Documentation](https://support.ramp.com/hc/en-us/articles/50665591644051-AI-Spend-Intelligence)
- [Ramp Developer API Portal](https://ramp.com/developer)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
