# OpenBB

## What it is
OpenBB is a financial data platform for analysts, quants, and AI agents. It provides a standardized interface to hundreds of financial data providers through a single Python SDK or CLI.

## What problem it solves
It eliminates the need for developers to build and maintain custom integrations for dozens of different financial data APIs (like Polygon, AlphaVantage, Fred, etc.). It normalizes data formats and provides a unified command set for market, fundamental, and macro data.

## Where it fits in the stack
**AI & Knowledge / Financial Intelligence Platform**. It serves as the data retrieval layer for financial agents, RAG systems focusing on market intelligence, and automated reporting pipelines.

## Typical use cases
- **Automated Market Reports**: Fetching daily sector performance and macro indicators.
- **Agentic Financial Analysis**: Providing LLMs with tools to "research" companies by fetching financial statements and news.
- **Quantitative Research**: Normalizing historical price data for backtesting.

## Strengths
- **Provider Agnostic**: Switch between data providers with minimal code changes.
- **Extensive Coverage**: Market data (stocks, crypto, forex), economics, fixed income, and more.
- **AI-Ready**: Designed to be used as a "tool" for agents through its structured output.

## Limitations
- **Domain Specific**: Limited utility outside of finance and economics.
- **API Key Management**: Still requires individual API keys from the underlying data providers for many endpoints.
- **Learning Curve**: The vastness of the available data commands can be overwhelming for new users.

## When to use it
- When your AI agent needs reliable, structured financial data beyond what generic web search can provide.
- When building internal dashboards that aggregate data from multiple financial sources.
- For high-fidelity RAG systems that require "ground truth" financial figures.

## When not to use it
- For general-purpose web search or news (use [Tavily](../providers/tavily.md)).
- If your application only requires very basic, infrequent stock price checks (where a simple API call might suffice).

## Getting started

OpenBB can be installed via pip:

```bash
pip install openbb
```

To use it in a script, you typically initialize the provider context:

```python
from openbb import obb

# Configure your API keys (can also be done via environment variables)
obb.account.credentials.polygon_api_key = "YOUR_KEY"

# Fetch daily stock data
data = obb.stocks.load(symbol="AAPL", start_date="2024-01-01", provider="polygon")
print(data.to_df().head())
```

## Technical examples

### Fetching Macro Economic Indicators
Agents can use OpenBB to monitor inflation or interest rate changes:

```python
from openbb import obb

# Fetch Consumer Price Index (CPI) data from FRED
cpi_data = obb.economy.cpi(countries=["united_states"], provider="fred")
df = cpi_data.to_df()
latest_cpi = df.iloc[-1]
print(f"Latest US CPI: {latest_cpi}")
```

### Sector Performance Analysis
Useful for automated "Daily Briefing" workflows:

```python
from openbb import obb

# Get US sector performance
sectors = obb.stocks.sector_performance(provider="fmp")
for sector in sectors.to_list():
    print(f"Sector: {sector.sector}, Performance: {sector.change_percentage}%")
```

### CLI: Fetching Market Snapshots
The OpenBB CLI allows for rapid data retrieval without writing code.

```bash
# Fetch daily price snapshot for a ticker
openbb stocks load --symbol NVDA --provider polygon

# Fetch latest news for a specific sector
openbb news --term "technology" --limit 5
```

## Example company use cases
- **Founder finance briefings**: pull macro indicators, sector news, and comparable-company signals into weekly strategy notes.
- **Investor relations prep**: support decks and updates with structured market context instead of ad hoc searching.
- **Sales and partnerships**: qualify target companies with financial and market context before outreach.

## Selection comments
- Use **OpenBB** when the workflow needs structured finance data.
- Use **Tavily** when the workflow needs broader web search and current unstructured signals.
- Use **OpenBB + n8n** when market or finance signals should trigger recurring reports.

## Related tools / concepts
- [Tavily](../providers/tavily.md)
- [n8n](../../services/n8n.md)
- [DeerFlow](../agents/deerflow.md)
- [LangChain](../ai_knowledge/langchain.md)
- [Data Copilot](../../architecture/data-copilot-text-to-sql.md)
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Financial Intelligence](../../knowledge_base/learning-map.md)

## Sources / References
- [Official Website](https://openbb.co/)
- [GitHub Repository](https://github.com/OpenBB-finance/OpenBB)
- [OpenBB Documentation](https://docs.openbb.co/)

## Contribution Metadata
- Last reviewed: 2026-06-02
- Confidence: high
