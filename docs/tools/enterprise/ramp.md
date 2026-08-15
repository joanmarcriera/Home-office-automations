# Ramp

## What it is
Ramp is a finance automation platform that combines corporate cards, expense management, bill payments, and accounting integrations into a single, AI-powered interface. It is designed to help businesses control spend, automate manual tasks, and close their books faster. As of early January 2027, it features deeply integrated **Ramp Intelligence** for autonomous finance operations, driven by frontier models (Claude 5.1, GPT-5.5).

## What problem it solves
It eliminates the friction of traditional expense reporting and manual data entry. By using AI to categorize transactions, extract data from receipts, and flag policy violations in real-time, Ramp reduces the operational burden on finance teams and employees, while providing real-time visibility into AI provider costs (e.g., token usage).

## Where it fits in the stack
**Category**: Enterprise AI / Finance Automation. It sits at the intersection of corporate spend and automated accounting workflows, acting as an "Agentic Finance" layer.

## Typical use cases
- **AI Spend Intelligence**: Consolidating token usage and costs from providers like [Anthropic](../providers/anthropic.md) and [OpenAI](../../tools/ai_knowledge/openai.md) into a single finance dashboard.
- **Automated Expense Management**: Using Ramp Intelligence to automatically match receipts to transactions and categorize spend.
- **Smart Bill Pay**: Using OCR and AI to extract invoice details and automate approval workflows.
- **Agentic Reconciliations**: Deploying **Ramp Agents** that handle journal entries and variance analysis end-to-end.

## Strengths
- **Native AI (Ramp Intelligence)**: Deeply integrated AI for receipt parsing, categorization, and anomaly detection.
- **AI Cost Visibility**: Real-time tracking of AI provider spend (Claude 5.1, GPT-5.5), essential for managing model-heavy R&D budgets.
- **Agentic Commerce**: Employs AI agents to research, compare, and buy for the organization.
- **Speed**: Built for efficiency, often allowing companies to close their books in days rather than weeks.
- **Global Expansion**: Strong support for US, UK, and EU markets with localized tax compliance.

## Limitations
- **Credit Requirements**: As a corporate card provider, it requires businesses to meet certain financial thresholds for approval.
- **Closed Ecosystem**: While it has great integrations, the core experience is tied to the Ramp platform and card.
- **SaaS Overhead**: Managing multiple virtual cards and automated policies requires initial setup and governance.

## When to use it
- When you want to automate expense reports and eliminate manual receipt submission for employees.
- When you need granular control over company spend via virtual cards with category-specific limits.
- When you want an AI-powered assistant to automatically identify duplicate SaaS subscriptions or redundant AI tool spend.

## When not to use it
- For personal finance or small "side hustle" projects (use [Actual Budget](../../services/actual-budget.md) for self-hosted personal finance).
- If your business is based entirely outside of supported regions (US/UK/EU) and requires specialized localized tax compliance.

## Getting started

### Enabling AI Spend Intelligence
1. **Early Access**: Toggle on "AI Spend Intelligence" in your Ramp settings.
2. **Connect Providers**: Obtain an **Admin API Key** (read-only) from your AI providers (Anthropic, OpenAI).
3. **Monitor**: View consolidated AI costs by model, team, and user within the Ramp dashboard.

## CLI examples
> [!NOTE]
> Ramp is primarily a SaaS platform and API. There is no official public CLI tool for general users as of early January 2027. However, developer teams can interact with Ramp API endpoints using custom Curl or CLI scripts for automated virtual card management.

### CLI Virtual Card Issuance via Curl
```bash
curl -X POST "https://api.ramp.com/developer/v1/cards" \
  -H "Authorization: Bearer $RAMP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cardholder_id": "usr_908123", "amount_limit": 50000, "spending_interval": "MONTHLY"}'
```

## API examples

### Python (Listing AI Provider Transactions with Pydantic v2 Validation)
Audit AI provider spend (e.g. Anthropic, OpenAI) and validate transaction payloads using Pydantic v2 schemas:

```python
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class RampTransaction(BaseModel):
    id: str = Field(description="Unique Ramp transaction ID")
    merchant_name: str = Field(description="Merchant name, e.g. OpenAI or Anthropic")
    amount: float = Field(description="Transaction amount in USD")
    user_id: str = Field(description="Cardholder or user ID")
    category: str = Field(default="Software & Cloud Services")

class RampTransactionList(BaseModel):
    data: List[RampTransaction] = Field(default_factory=list)

def filter_ai_spend(raw_api_response: Dict[str, Any]) -> List[RampTransaction]:
    # Validate raw payload using Pydantic v2
    validated = RampTransactionList(**raw_api_response)
    ai_providers = ['OpenAI', 'Anthropic', 'Azure OpenAI', 'Bedrock']
    return [
        tx for tx in validated.data
        if any(provider in tx.merchant_name for provider in ai_providers)
    ]

if __name__ == "__main__":
    mock_response = {
        "data": [
            {"id": "tx_101", "merchant_name": "Anthropic", "amount": 1250.00, "user_id": "usr_901"},
            {"id": "tx_102", "merchant_name": "Coffee Shop", "amount": 4.50, "user_id": "usr_902"},
            {"id": "tx_103", "merchant_name": "OpenAI", "amount": 3400.00, "user_id": "usr_901"}
        ]
    }
    ai_txs = filter_ai_spend(mock_response)
    print(f"Found {len(ai_txs)} AI provider transactions totaling ${sum(tx.amount for tx in ai_txs):.2f}")
```

### FastMCP 3.1 Integration Snippet
Expose virtual card issuance and Ramp ERP controls as a FastMCP 3.1 tool endpoint:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("RampFinanceControl")

class IssueVirtualCardRequest(BaseModel):
    cardholder_id: str = Field(description="Ramp user or employee ID")
    monthly_limit_usd: float = Field(gt=0, description="Monthly spending limit in USD")
    purpose: str = Field(default="AI Compute Budget", description="Reason or tag for card issue")

@mcp.tool()
def issue_virtual_card(request: IssueVirtualCardRequest) -> dict:
    """Issue an agentic virtual card via Ramp Developer API."""
    return {
        "status": "issued",
        "card_id": "card_2027_0192",
        "cardholder_id": request.cardholder_id,
        "monthly_limit_usd": request.monthly_limit_usd,
        "purpose": request.purpose
    }

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Glean](glean.md)
- [Fyxer AI](fyxer.md)
- [Hebbia](hebbia.md)
- [tldv](tldv.md)
- [Actual Budget](../../services/actual-budget.md)
- [n8n](../../services/n8n.md)
- [Langfuse](../process_understanding/langfuse.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Anthropic](../providers/anthropic.md)
- [OpenAI](../../tools/ai_knowledge/openai.md)

## Sources / References
- [Ramp Official Website](https://ramp.com/)
- [Ramp AI Spend Intelligence](https://support.ramp.com/hc/en-us/articles/50665591644051-AI-Spend-Intelligence)
- [Ramp Stack: The question every accountant should ask](https://ramp.com/blog/ramp-stack-launch)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
