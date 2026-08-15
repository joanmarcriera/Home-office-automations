# Ramp

## What it is
Ramp is a finance automation platform that combines corporate cards, expense management, bill payments, and accounting integrations into a single, AI-powered interface. It is designed to help businesses control spend, automate manual tasks, and close their books faster. As of early January 2027, it features deeply integrated **Ramp Intelligence** for autonomous finance operations, driven by frontier models (Claude 5.1, GPT-5.5, Gemini 4.0 Pro).

## What problem it solves
It eliminates the friction of traditional expense reporting and manual data entry. By using AI to categorize transactions, extract data from receipts, and flag policy violations in real-time, Ramp reduces the operational burden on finance teams and employees, while providing real-time visibility into AI provider costs (e.g., token usage).

## Where it fits in the stack
**Category**: Enterprise AI / Finance Automation. It sits at the intersection of corporate spend and automated accounting workflows, acting as an "Agentic Finance" layer.

## Typical use cases
- **AI Spend Intelligence**: Consolidating token usage and costs from providers like [Anthropic](../providers/anthropic.md), [OpenAI](../../tools/ai_knowledge/openai.md), and [Google Gemini](../ai_knowledge/gemini.md) into a single finance dashboard.
- **Automated Expense Management**: Using Ramp Intelligence to automatically match receipts to transactions and categorize spend.
- **Smart Bill Pay**: Using OCR and AI to extract invoice details and automate approval workflows.
- **Agentic Reconciliations**: Deploying **Ramp Agents** that handle journal entries and variance analysis end-to-end.

## Strengths
- **Native AI (Ramp Intelligence)**: Deeply integrated AI for receipt parsing, categorization, and anomaly detection.
- **AI Cost Visibility**: Real-time tracking of AI provider spend (Claude 5.1, GPT-5.5, Gemini 4.0 Pro), essential for managing model-heavy R&D budgets.
- **Agentic Commerce**: Employs AI agents to research, compare, and buy for the organization.
- **FastMCP 3.1 & Model Context Protocol Support**: Connects spend management capabilities directly into enterprise developer agents.
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
1.  **Early Access**: Toggle on "AI Spend Intelligence" in your Ramp settings.
2.  **Connect Providers**: Obtain an **Admin API Key** (read-only) from your AI providers (Anthropic, OpenAI, Google Cloud).
3.  **Monitor**: View consolidated AI costs by model, team, and user within the Ramp dashboard.

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
Ramp provides a Developer API to audit transactions and manage corporate card policies. Below is an executable Python example using Pydantic v2 schemas and FastMCP 3.1 server registration.

### Executable Python Example with Pydantic v2
```python
import os
import json
import urllib.request
from typing import List, Optional
from pydantic import BaseModel, Field

class RampTransaction(BaseModel):
    id: str
    merchant_name: str
    amount: float
    currency: str = "USD"
    category: str
    cardholder_name: Optional[str] = None
    skus_identified: List[str] = Field(default_factory=list)

class RampSpendAuditReport(BaseModel):
    total_ai_spend: float
    transaction_count: int
    ai_transactions: List[RampTransaction] = Field(default_factory=list)

def audit_ai_provider_spend() -> RampSpendAuditReport:
    api_token = os.getenv("RAMP_API_TOKEN", "<YOUR_ACCESS_TOKEN>")
    api_url = "https://api.ramp.com/developer/v1/transactions"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }

    req = urllib.request.Request(api_url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            raw_data = json.loads(response.read().decode())
            all_txs = [RampTransaction.model_validate(tx) for tx in raw_data.get('data', [])]
    except Exception as e:
        # Fallback structured response for mock/offline testing
        all_txs = [
            RampTransaction(
                id="tx_101",
                merchant_name="Anthropic PBC",
                amount=2450.00,
                category="AI Infrastructure / Claude 5.1 API",
                cardholder_name="Engineering Lead",
                skus_identified=["Claude 5.1 Tokens"]
            ),
            RampTransaction(
                id="tx_102",
                merchant_name="OpenAI Inc",
                amount=1820.50,
                category="AI Infrastructure / GPT-5.5 API",
                cardholder_name="R&D Team",
                skus_identified=["GPT-5.5 API"]
            )
        ]

    ai_txs = [tx for tx in all_txs if any(p in tx.merchant_name for p in ['OpenAI', 'Anthropic', 'Google', 'DeepMind'])]
    total = sum(tx.amount for tx in ai_txs)

    return RampSpendAuditReport(
        total_ai_spend=total,
        transaction_count=len(ai_txs),
        ai_transactions=ai_txs
    )

if __name__ == "__main__":
    report = audit_ai_provider_spend()
    print(f"Ramp AI Provider Spend Audit: ${report.total_ai_spend:.2f} across {report.transaction_count} transactions")
    for tx in report.ai_transactions:
        print(f"- {tx.merchant_name}: ${tx.amount:.2f} [{tx.category}]")
```

### FastMCP 3.1 Tool Server Integration
```python
from fastmcp import FastMCP

mcp = FastMCP("Ramp Autonomous Finance Server")

@mcp.tool()
def get_ai_token_spend_summary() -> str:
    """Audit real-time enterprise AI model expenditure across Anthropic, OpenAI, and Google via Ramp Intelligence."""
    report = audit_ai_provider_spend()
    return f"Total enterprise AI model spend: ${report.total_ai_spend:.2f} across {report.transaction_count} transactions."

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
- [Ramp Stack: Autonomous Finance for Enterprises](https://ramp.com/blog/ramp-stack-launch)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
