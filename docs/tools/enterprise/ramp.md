# Ramp

## What it is
Ramp is a finance automation platform that combines corporate cards, expense management, bill payments, and accounting integrations into a single, AI-powered interface. It is designed to help businesses control spend, automate manual tasks, and close their books faster.

## What problem it solves
It eliminates the friction of traditional expense reporting and manual data entry. By using AI to categorize transactions, extract data from receipts, and flag policy violations in real-time, Ramp reduces the operational burden on finance teams and employees.

## Where it fits in the stack
**Category**: Enterprise AI / Finance Automation. It sits at the intersection of corporate spend and automated accounting workflows.

## Typical use cases
- **AI Spend Intelligence**: Consolidating token usage and costs from providers like Anthropic (Claude 4.7) and OpenAI (GPT-5.5) into a single finance dashboard.
- **Automated Expense Management**: Using "Ramp Intelligence" to automatically match receipts to transactions and categorize spend.
- **Smart Bill Pay**: Using OCR and AI to extract invoice details and automate approval workflows.
- **Ramp Stack**: Deploying AI agents that handle reconciliations, journal entries, and variance analysis end-to-end.

## Key Features
- **Native AI (Ramp Intelligence)**: Deeply integrated AI for receipt parsing, categorization, and anomaly detection.
- **AI Token Spend Management**: Direct API integrations with LLM providers to track unit economics (cost-per-token) alongside corporate spend.
- **Ramp Agents**: Finance-specific agents built to act like a thousand controllers, handling complex accounting tasks around the clock.
- **Speed**: Built for efficiency, often allowing companies to close their books in days rather than weeks.
- **Seamless Integrations**: Strong connectors for major accounting software (NetSuite, Sage Intacct, QuickBooks, Xero).

## Strengths
- **Agentic Commerce**: Employs AI agents to research, compare, and buy for the organization.
- **AI Cost Visibility**: Real-time tracking of AI provider spend, essential for managing model-heavy R&D budgets.
- **Global Expansion**: Expanding support for Europe and the UK with regulatory authorization (via Billhop acquisition).
- **Proactive Spend Control**: Setting proactive spend limits and automated policy enforcement at the card level.

## Limitations
- **Geographic Focus**: Historically optimized for US-based businesses, though international support is rapidly expanding in 2026.
- **Credit Requirements**: As a corporate card provider, it requires businesses to meet certain financial thresholds for approval.
- **Closed Ecosystem**: While it has great integrations, the core experience is tied to the Ramp platform and card.

## When to use it
- When you want to automate expense reports and eliminate manual receipt submission for employees.
- When you need granular control over company spend via virtual cards with category-specific limits.
- When you want an AI-powered assistant (GPT-5.5 or Claude 4.7 optimized) to automatically identify duplicate SaaS subscriptions.

## When not to use it
- For personal finance or small "side hustle" projects (use [Actual Budget](../../services/actual-budget.md) for self-hosted personal finance).
- If your business is based entirely outside of the US/UK/EU and requires specialized localized tax compliance in other regions.
- If you prefer a traditional bank with a physical branch presence for all your business operations.

## Getting started

### Enabling AI Spend Intelligence
1.  **Early Access**: Toggle on "AI Spend Intelligence" in your Ramp settings.
2.  **Connect Providers**: Obtain an **Admin API Key** (read-only) from your AI providers.
    - **Anthropic**: Create a key in `Settings > Organization > Admin API Keys`.
    - **OpenAI**: Create a `read_only` key in `Organization > Admin API Keys`.
3.  **Monitor**: View consolidated AI costs by model, team, and user within the Ramp dashboard.

## CLI examples
> [!NOTE]
> Ramp is primarily a SaaS platform and API. There is no official public CLI tool for general users as of June 2026.

## API examples
While Ramp is primarily a SaaS platform, developers can interact with its API to trigger payments or sync data.

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
- [Glean](glean.md) (Enterprise search/discovery)
- [Fyxer AI](fyxer.md) (Administrative AI)
- [OpenRouter (Logging Support)](../ai_knowledge/openrouter.md)
- [Zapier (Automation)](../automation_orchestration/zapier.md)
- [Hebbia](hebbia.md) (Analytical synthesis for complex documents)
- [tldv](tldv.md) (Meeting transcription and extraction)
- [Actual Budget](../../services/actual-budget.md) (Self-hosted personal finance)
- [n8n](../../services/n8n.md) (Workflow automation for finance)
- [Langfuse](../process_understanding/langfuse.md) (Observability for custom LLM integrations)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) (Standard for connecting tools to agents)

## Sources / references
- [Ramp Official Website](https://ramp.com/)
- [Ramp AI Spend Intelligence](https://support.ramp.com/hc/en-us/articles/50665591644051-AI-Spend-Intelligence)
- [Ramp Stack: The question every accountant should ask](https://ramp.com/blog/ramp-stack-launch)
- [OpenRouter Log Integration (Context)](../../reports/openrouter-logs-backlog.md)

## Contribution Metadata
- Last reviewed: 2026-06-07
- Confidence: high
