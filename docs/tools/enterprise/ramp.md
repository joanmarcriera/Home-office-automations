# Ramp

## What it is
Ramp is a finance automation platform that combines corporate cards, expense management, bill payments, and accounting integrations into a single, AI-powered interface. It is designed to help businesses control spend, automate manual tasks, and close their books faster. As of June 2026, it features deeply integrated **Ramp Intelligence** for autonomous finance operations.

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
- **AI Cost Visibility**: Real-time tracking of AI provider spend (Claude 4.8, GPT-5.5), essential for managing model-heavy R&D budgets.
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
1.  **Early Access**: Toggle on "AI Spend Intelligence" in your Ramp settings.
2.  **Connect Providers**: Obtain an **Admin API Key** (read-only) from your AI providers (Anthropic, OpenAI).
3.  **Monitor**: View consolidated AI costs by model, team, and user within the Ramp dashboard.

## CLI examples
> [!NOTE]
> Ramp is primarily a SaaS platform and API. There is no official public CLI tool for general users as of June 2026.

## API examples

### Python (Listing AI Provider Transactions)
```python
import requests

# Example: List recent transactions to audit AI provider spend (v1 API)
API_URL = "https://api.ramp.com/developer/v1/transactions"
API_TOKEN = "<YOUR_ACCESS_TOKEN>"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

response = requests.get(API_URL, headers=headers)
transactions = response.json()

# Filter for AI providers (e.g., Anthropic or OpenAI)
ai_spend = [tx for tx in transactions['data'] if any(p in tx['merchant_name'] for p in ['OpenAI', 'Anthropic'])]
for tx in ai_spend:
    print(f"Date: {tx['user_transaction_time']}, Amount: ${tx['amount']/100:.2f}")
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
- Last reviewed: 2026-06-26
- Confidence: high
