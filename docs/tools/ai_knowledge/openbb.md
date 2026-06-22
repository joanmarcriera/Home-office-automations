# OpenBB

## What it is
OpenBB is a financial data platform for analysts, quants, and AI agents. It provides a standardized interface to hundreds of financial data providers through a single Python SDK, a Terminal (CLI), or a web-based dashboard. As of June 2026, **OpenBB Terminal v4.5** introduces deep agentic integration, allowing LLMs to natively execute financial data commands and synthesize market intelligence.

## What problem it solves
It eliminates the need for developers to build and maintain custom integrations for dozens of disparate financial data APIs (e.g., Polygon, AlphaVantage, FRED, SEC EDGAR). It normalizes data formats, provides unified command sets, and ensures that AI agents have access to "ground truth" financial figures rather than unreliable web-scraped data.

## Where it fits in the stack
**AI & Knowledge / Financial Intelligence Layer**. It serves as the data retrieval engine for financial agents, RAG systems focusing on market intelligence, and automated quantitative research pipelines.

## Typical use cases
- **Agentic Financial Research**: Providing LLMs with tools to "deep-dive" into a company by fetching financial statements, insider trades, and real-time news.
- **Automated Market Briefings**: Generating daily sector performance reports and macro indicator summaries for stakeholders.
- **Quantitative Backtesting**: Fetching normalized historical price data across different asset classes (stocks, crypto, forex).
- **Founder & VC Intelligence**: Monitoring competitor financial signals and macro-economic shifts (e.g., CPI or interest rate changes) via automated triggers.

## Strengths
- **Provider Agnostic**: Switch between data providers (e.g., from IEX to Polygon) with zero code changes.
- **Extensive Coverage**: Support for equities, options, crypto, forex, macroeconomics, and fixed income.
- **AI-Native Design**: Features like structured JSON outputs and the OpenBB Agent framework make it highly compatible with LLM tool-calling.
- **Open Source Foundation**: High transparency and community-driven expansion of data providers.

## Limitations
- **Domain Specificity**: Extremely powerful for finance and economics, but has limited utility outside these fields.
- **API Key Management**: While the interface is unified, users still need to provide individual API keys for many premium data sources.
- **Complexity**: The sheer volume of available commands (hundreds of endpoints) can be overwhelming without proper documentation or agent orchestration.

## When to use it
- When your AI agent needs reliable, structured financial data beyond what generic web search can provide.
- When building internal financial dashboards that aggregate data from multiple sources.
- For high-fidelity RAG systems that require exact financial figures for quantitative analysis.

## When not to use it
- For general-purpose web search or unstructured news (use [Tavily](../providers/tavily.md) or [Perplexity](../../knowledge_base/self-healing-agent-research.md)).
- If your application only requires very basic, infrequent stock price checks where a simple fetch from a single API is sufficient.

## Getting started

### Installation
OpenBB can be installed via pip. It is recommended to use a virtual environment.

```bash
pip install openbb
```

### Initial Configuration
You can set your API keys via the OpenBB Hub or directly in your script:

```python
from openbb import obb

# Configure your provider keys
obb.account.credentials.polygon_api_key = "YOUR_KEY"
obb.account.credentials.fmp_api_key = "YOUR_KEY"
```

## CLI examples

### Fetching Market Snapshots
The OpenBB Terminal (CLI) allows for rapid data retrieval:

```bash
# Get daily price data for a specific ticker
openbb stocks load --symbol NVDA --provider polygon

# Fetch latest news related to "Artificial Intelligence"
openbb news --term "AI" --limit 10
```

### Macro Economic Analysis
Quickly check macro indicators from the terminal:
```bash
# Fetch latest US CPI data from FRED
openbb economy cpi --countries united_states --provider fred
```

## API examples

### Agentic Data Retrieval (Python)
Using the OpenBB SDK to provide data to an agentic workflow:

```python
from openbb import obb

def get_company_health(symbol: str):
    # Fetch income statement
    income = obb.stocks.fa.income(symbol=symbol, provider="fmp")
    # Fetch latest news
    news = obb.news(term=symbol, limit=5, provider="benzinga")

    return {
        "financials": income.to_df().iloc[0].to_dict(),
        "recent_headlines": [n.title for n in news.to_list()]
    }

print(get_company_health("AAPL"))
```

### Quantitative Analysis Workflow
```python
from openbb import obb

# Fetch historical data for multiple symbols
data = obb.equity.price.historical(
    symbol="AAPL,MSFT,GOOGL",
    start_date="2024-01-01",
    provider="yfinance"
)

# Convert to DataFrame for analysis
df = data.to_df()
print(df.groupby('symbol').mean())
```

## Related tools / concepts
- [Tavily](../providers/tavily.md) — Broader web search for unstructured signals.
- [n8n](../../services/n8n.md) — Automating OpenBB signals into workflows.
- [Data Copilot](../../architecture/data-copilot-text-to-sql.md) — Pattern for structured data interaction.
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md) — Financial context for RAG.
- [OpenRouter](../ai_knowledge/openrouter.md) — Routing financial queries to best-fit models.
- [LangChain](../ai_knowledge/langchain.md) — Orchestrating financial agents.
- [Perplexity](../../knowledge_base/self-healing-agent-research.md) — Real-time web grounding.

## Sources / references
- [OpenBB Official Website](https://openbb.co/)
- [OpenBB Documentation (v4.5)](https://docs.openbb.co/)
- [OpenBB GitHub Repository](https://github.com/OpenBB-finance/OpenBB)
- [OpenBB Agent Framework](https://github.com/OpenBB-finance/openbb-agents)
- [Financial Intelligence Learning Map](../../knowledge_base/learning-map.md)
- [Quantitative Finance with OpenBB](https://openbb.co/blog/quantitative-finance-open-source)
- [SEC EDGAR API Access](https://www.sec.gov/edgar/sec-api-documentation)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
