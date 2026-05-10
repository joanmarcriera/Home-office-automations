# Ramp

## What it is
Ramp is a finance automation platform that combines corporate cards, expense management, bill payments, and accounting integrations into a single, AI-powered interface. It is designed to help businesses control spend, automate manual tasks, and close their books faster.

## What problem it solves
It eliminates the friction of traditional expense reporting and manual data entry. By using AI to categorize transactions, extract data from receipts, and flag policy violations in real-time, Ramp reduces the operational burden on finance teams and employees.

## Where it fits in the stack
**Category**: Enterprise AI / Finance Automation. It sits at the intersection of corporate spend and automated accounting workflows.

## Typical use cases
- **AI Spend Intelligence**: Consolidating token usage and costs from providers like Anthropic and OpenAI into a single finance dashboard.
- **Automated Expense Management**: Using "Ramp Intelligence" to automatically match receipts to transactions and categorize spend.
- **Smart Bill Pay**: Using OCR and AI to extract invoice details and automate approval workflows.
- **Real-time Spend Control**: Setting proactive spend limits and automated policy enforcement at the card level.

## Strengths
- **Native AI (Ramp Intelligence)**: Deeply integrated AI for receipt parsing, categorization, and anomaly detection.
- **AI Cost Visibility**: Direct API integrations with LLM providers to track unit economics (cost-per-token) alongside corporate spend.
- **Speed**: Built for efficiency, often allowing companies to close their books in days rather than weeks.
- **Seamless Integrations**: Strong connectors for major accounting software (NetSuite, Sage Intacct, QuickBooks, Xero).

## Limitations
- **Geographic Focus**: Primarily optimized for US-based businesses, though international support is expanding.
- **Credit Requirements**: As a corporate card provider, it requires businesses to meet certain financial thresholds for approval.
- **Closed Ecosystem**: While it has great integrations, the core experience is tied to the Ramp platform and card.

## When to use it
- When you want to automate expense reports and eliminate manual receipt submission for employees.
- When you need granular control over company spend via virtual cards with category-specific limits.
- When you want an AI-powered assistant to automatically identify duplicate SaaS subscriptions or negotiate better rates.

## When not to use it
- For personal finance or small "side hustle" projects (use [Actual Budget](../../services/actual-budget.md) for self-hosted personal finance).
- If your business is based entirely outside of the US and requires localized tax and banking compliance in multiple non-US regions.
- If you prefer a traditional bank with a physical branch presence for all your business operations.

## Getting started

### Enabling AI Spend Intelligence
1.  **Early Access**: Toggle on "AI Spend Intelligence" in your Ramp settings.
2.  **Connect Providers**: Obtain an **Admin API Key** (read-only) from your AI providers.
    - **Anthropic**: Create a key in `Settings > Organization > Admin API Keys`.
    - **OpenAI**: Create a `read_only` key in `Organization > Admin API Keys`.
3.  **Monitor**: View consolidated AI costs by model, team, and user within the Ramp dashboard.

### Automating Bill Pay (API Example)
While Ramp is primarily a SaaS platform, developers can interact with its API to trigger payments or sync data.

```python
import requests

# Example: List recent transactions to audit AI provider spend
url = "https://api.ramp.com/developer/v1/transactions"
headers = {
    "Authorization": "Bearer <YOUR_ACCESS_TOKEN>",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
transactions = response.json()

# Filter for AI providers
ai_spend = [tx for tx in transactions['data'] if 'OpenAI' in tx['merchant_name']]
for tx in ai_spend:
    print(f"Date: {tx['user_transaction_time']}, Amount: ${tx['amount']/100:.2f}")
```

## Related tools / concepts
- [Glean](glean.md) (Enterprise search/discovery)
- [Fyxer AI](fyxer.md) (Administrative AI)
- [OpenRouter (Logging Support)](../ai_knowledge/openrouter.md)
- [Zapier (Automation)](../automation_orchestration/zapier.md)
- [Hebbia](hebbia.md) (Analytical synthesis for complex documents)
- [tldv](tldv.md) (Meeting transcription and extraction)
- [Actual Budget](../../services/actual-budget.md) (Self-hosted personal finance)
- [n8n](../../services/n8n.md) (Workflow automation for finance)
- [Langfuse](../process_understanding/langfuse.md) (Observability for custom LLM integrations)

## Sources / references
- [Ramp Official Website](https://ramp.com/)
- [Ramp AI Spend Intelligence](https://support.ramp.com/hc/en-us/articles/50665591644051-AI-Spend-Intelligence)
- [OpenRouter Log Integration (Context)](../../reports/openrouter-logs-backlog.md)

## Contribution Metadata
- Last reviewed: 2026-05-10
- Confidence: high
