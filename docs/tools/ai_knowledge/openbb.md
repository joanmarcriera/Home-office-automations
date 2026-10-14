# OpenBB

## What it is
OpenBB is a comprehensive, open-source financial data platform designed for financial analysts, quantitative researchers, and AI agents. It standardizes access to hundreds of financial data endpoints across diverse asset classes (equities, options, crypto, forex, macroeconomics, fixed income) using a single unified Python SDK, a Terminal (CLI), or a web-based dashboard. As of early 2027, **OpenBB Platform v5.2** fully standardizes native Model Context Protocol (MCP 3.1 / FastMCP 3.1) integration via streamable-http and stdio transports, enabling AI agents and LLMs (such as Claude 5.6, GPT-5.6, Gemini 4.0, Llama 4, Gemma 4, and Qwen 3.6) to autonomously execute high-fidelity financial queries and synthesize market intelligence in real-time.

## What problem it solves
It eliminates the critical challenge of fragmentation in financial data acquisition. Traditional research requires maintaining separate API integrations, pipelines, and schema-normalizations for dozens of disparate financial data providers (e.g., FMP, Polygon, AlphaVantage, FRED, SEC EDGAR, Benzinga). OpenBB normalizes data schemas, provides a consistent command-and-query interface, and delivers structured, high-fidelity JSON data directly to LLMs, bypassing the latency, hallucinations, and unreliability associated with general web-scraping or unstructured searches.

## Where it fits in the stack
**AI & Knowledge / Financial Intelligence Layer**. OpenBB acts as the dedicated financial data retrieval engine. It operates directly between raw data/provider APIs and downstream AI agentic frameworks, multi-agent systems, and specialized RAG networks that require deterministic, quantitative grounding.

```
┌────────────────────────────────────────┐
│      Agentic Framework / Gateway       │
│     (Claude 5.6, FastMCP 3.1, n8n)     │
└───────────────────┬────────────────────┘
                    │ FastMCP 3.1 Streamable-HTTP
┌───────────────────▼────────────────────┐
│         OPENBB PLATFORM CORE           │
│         (SDK v5.2 / MCP Server)        │
└───────────────────┬────────────────────┘
                    │ Normalized API Queries
┌───────────────────▼────────────────────┐
│ Financial Data Providers (FMP, FRED)   │
└────────────────────────────────────────┘
```

## Typical use cases
- **Agentic Financial Research**: Equipping LLMs with real-time tools to fetch balance sheets, cash flow statements, insider trading data, and company valuations.
- **Autonomous Market Monitoring**: Setting up scheduled triggers to generate sector performance updates or track macro indicators (e.g., CPI, unemployment rates, interest shifts).
- **Quantitative Workflow Grounding**: Standardizing historical and real-time pricing feeds for algorithmic backtesting and portfolio optimization.
- **Model Context Protocol (MCP) Integration**: Spinning up local or remote MCP servers to serve financial intelligence directly to chat environments like Claude Desktop, Cursor, or VS Code.

## Strengths
- **Native FastMCP Support**: The `openbb-mcp-server` library provides zero-code conversions of OpenBB installations into MCP 3.1-compliant servers.
- **Provider Independence**: Seamlessly switch downstream data providers (e.g., swapping historical data from Yahoo Finance to Polygon) via simple parameter modifications with zero schema changes.
- **Dynamic Tool Discovery**: Minimizes model context bloat by starting with core discovery tools and dynamically enabling/disabling specific endpoints on the fly.
- **Enterprise-Grade Security**: Supports robust Bearer Authentication (Base64-encoded username/password) and granular API key management at the user profile level.

## Limitations
- **Domain Specialization**: Tailored exclusively for financial and macroeconomic workflows; offers no utility outside of these spaces.
- **Provider Subscriptions**: While the OpenBB engine is open-source and free, advanced endpoints require individual user API keys and associated paid subscriptions from downstream data providers.
- **API Complexity**: The presence of hundreds of unique command endpoints can overwhelm smaller models without explicit system prompts and server-side route filtering.

## When to use it
- When your AI agents or RAG pipelines require absolute, verified quantitative accuracy for financial analysis rather than soft web grounding.
- When building multi-tenant financial terminals or dashboards that aggregate data from multiple provider API keys.
- When integrating real-time market data retrieval into IDE chat environments (e.g., Windsurf, Cursor, VS Code) via Model Context Protocol.

## When not to use it
- For general-purpose web search or unstructured real-time web search (use [Tavily](../providers/tavily.md) or [Perplexity](../../knowledge_base/self-healing-agent-research.md)).
- If your application only requires simple, occasional, or static stock price lookups where a lightweight, direct API fetch is more appropriate.
- When you require deterministic, real-time microsecond-level algorithmic trading pipelines where API normalization introduces minor routing overhead.

## Getting started

### Installation
OpenBB can be installed via pip. To enable full AI agentic and FastMCP integration, install the core platform alongside the dedicated MCP server extension:

```bash
pip install openbb openbb-mcp-server pydantic
```

### Initial Configuration
Setup your provider API credentials using the OpenBB configuration files or dynamically in your script:

```python
from openbb import obb

# Configure Polygon and Financial Modeling Prep (FMP) credentials
obb.account.credentials.polygon_api_key = "YOUR_POLYGON_API_KEY"
obb.account.credentials.fmp_api_key = "YOUR_FMP_API_KEY"
```

To run the MCP server with proper authentication, define your Bearer credentials in your environment:

```bash
export OPENBB_MCP_SERVER_AUTH='["myuser", "mypassword123"]'
```

## CLI examples

### Fetching Market Snapshots
Using the OpenBB command-line interface to pull normalized historical price data:

```bash
# Fetch daily price data for NVDA from Polygon
openbb stocks load --symbol NVDA --provider polygon

# Pull recent news headlines on macro topics
openbb news --term "inflation" --limit 5
```

### Starting the OpenBB MCP Server
Launch the native Model Context Protocol server directly from the command line:

```bash
# Start the MCP server using standard HTTP transport on port 8001
openbb-mcp --host 127.0.0.1 --port 8001 --transport streamable-http

# Restrict the server to only expose macroeconomic and news categories
openbb-mcp --allowed-categories economy,news --port 8080

# Disable dynamic tool discovery for fixed, immutable multi-client deployments
openbb-mcp --no-tool-discovery
```

## API examples

### Programmatic Python Retrieval
Using the OpenBB SDK within a custom agent function to supply structured financial data:

```python
from openbb import obb

def analyze_company_fundamentals(symbol: str) -> dict:
    # Fetch income statement from FMP
    income_stmt = obb.stocks.fa.income(symbol=symbol, provider="fmp")
    # Fetch recent company-specific news
    news_feed = obb.news(term=symbol, limit=3, provider="benzinga")

    return {
        "fundamentals": income_stmt.to_df().iloc[0].to_dict(),
        "recent_headlines": [item.title for item in news_feed.to_list()]
    }

# Execute retrieval
print(analyze_company_fundamentals("MSFT"))
```

### FastMCP 3.1 Financial Intelligence Server Tool Implementation
Expose OpenBB's multi-provider SDK endpoints directly to autonomous AI agents using a native FastMCP 3.1 streamable-http / stdio server pattern:

```python
import asyncio
from typing import List, Optional, Dict, Any
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
from openbb import obb

# Initialize FastMCP 3.1 server for OpenBB financial tools
mcp = FastMCP(
    name="OpenBB Financial Intelligence Gateway",
    version="3.1.0",
    description="Standardized FastMCP server exposing multi-asset market data and corporate fundamentals"
)

class TickerQueryInput(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol (e.g. NVDA, AAPL, MSFT)")
    provider: Optional[str] = Field("fmp", description="Downstream financial provider (fmp, polygon, yfinance)")
    limit: Optional[int] = Field(5, ge=1, le=50, description="Max result items")

class MacroQueryInput(BaseModel):
    indicator: str = Field(..., description="Macroeconomic indicator ID or search query (e.g., CPI, UNRATE, GDP)")
    provider: Optional[str] = Field("fred", description="Macro provider (fred, eia, ecb)")

@mcp.tool(
    name="get_corporate_income_statement",
    description="Fetch normalized audited corporate income statements and top-line figures."
)
async def get_corporate_income_statement(query: TickerQueryInput, ctx: Context) -> Dict[str, Any]:
    await ctx.info(f"Querying OpenBB income statement for {query.symbol} via {query.provider}")
    try:
        data = obb.stocks.fa.income(symbol=query.symbol, provider=query.provider)
        df = data.to_df()
        if df.empty:
            return {"status": "empty", "symbol": query.symbol, "records": []}
        records = df.head(query.limit).reset_index().to_dict(orient="records")
        return {
            "status": "success",
            "symbol": query.symbol.upper(),
            "provider_used": query.provider,
            "record_count": len(records),
            "data": records
        }
    except Exception as e:
        await ctx.error(f"OpenBB income statement retrieval failed: {str(e)}")
        return {"status": "error", "error_message": str(e), "symbol": query.symbol}

@mcp.tool(
    name="get_macroeconomic_series",
    description="Fetch standardized macroeconomic time series data from Federal Reserve (FRED) or EIA."
)
async def get_macroeconomic_series(query: MacroQueryInput, ctx: Context) -> Dict[str, Any]:
    await ctx.info(f"Fetching macro series {query.indicator} from {query.provider}")
    try:
        data = obb.economy.fred_series(symbol=query.indicator)
        df = data.to_df()
        records = df.tail(12).reset_index().to_dict(orient="records")
        return {
            "status": "success",
            "indicator": query.indicator.upper(),
            "recent_observations": records
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e), "indicator": query.indicator}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Python (Financial Data Schema Validation with Pydantic v2)
Ensure data integrity when fetching financial intelligence from OpenBB by validating raw API data outputs against clean, type-coerced Pydantic schemas:

```python
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class CorporateFundamentals(BaseModel):
    symbol: str = Field(..., description="Standardized stock ticker symbol")
    fiscal_date: date = Field(..., description="Ending date of the audited period")
    net_income: int = Field(..., description="Net income in USD")
    revenue: int = Field(..., description="Total top-line revenue in USD")
    eps: float = Field(..., description="Diluted earnings per share")
    mcp_discovery_token: Optional[str] = Field(None, description="MCP 3.1 session identifier")

    @field_validator("symbol")
    @classmethod
    def normalize_ticker(cls, v: str) -> str:
        return v.upper().strip()

class ValuationProfile(BaseModel):
    company_name: str = Field(..., description="Legal company name")
    metrics: CorporateFundamentals = Field(..., description="Corporate fundamental metrics")
    valuation_score: int = Field(..., ge=0, le=100)

# Example parsing of raw data received from OpenBB's stocks.fa.income endpoint
raw_response = {
    "company_name": "Microsoft Corporation",
    "metrics": {
        "symbol": " msft ",
        "fiscal_date": "2026-09-30",
        "net_income": 22000000000,
        "revenue": 56000000000,
        "eps": 2.95
    },
    "valuation_score": 92
}

profile = ValuationProfile.model_validate(raw_response)
print(f"Validated financial profile for {profile.company_name} (Ticker: {profile.metrics.symbol})")
```

## Architectural Comparison & Provider Matrix

| Platform / Engine | Primary Focus | MCP 3.1 Integration | Schema Normalization | Cost Model | Best Agentic Deployment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenBB Platform v5.2** | Multi-asset financial & macro quantitative data | Native (`openbb-mcp-server`) | Universal Pydantic / DataFrame normalization across 50+ sources | Free core framework; downstream provider API keys required | Production Agentic Financial Research & Trading Copilots |
| **Bloomberg Terminal API / BLPAPI** | Enterprise institutional financial trading & analysis | Custom wrapper required | Proprietary C++/Java SDK structures | High ($27,000+/user/year) | Wall St institutional desks with dedicated Bloomberg subscriptions |
| **Direct FMP / Polygon REST APIs** | Single-provider financial endpoint access | Manual FastMCP implementation needed per vendor | Vendor-specific raw JSON | Paid per-request or tier-based monthly | Simple single-source data fetching scripts |
| **Tavily / Perplexity Web Search** | Unstructured web search & unstructured news rag | Native or standard tools | Unstructured text snippets / Markdown | Tiered per-query pricing | Broad qualitative web grounding & press release discovery |

## Operational Hardening & Security Best Practices
- **Credential Segregation**: Store API provider keys (e.g. Polygon, FMP, AlphaVantage, FRED) in encrypted secrets managers or environment variables (`.env`) rather than hardcoding in scripts or agent system prompts.
- **Dynamic Tool Throttling**: Configure `openbb-mcp-server` rate-limit rules to prevent LLM retry loops from exhausting downstream provider quota limits during complex multi-step reasoning runs.
- **Filter Unused Endpoints**: Restrict exposed MCP tools via the `--allowed-categories` flag (e.g. `--allowed-categories economy,news`) to prevent context bloat and hallucinated API parameter combinations in smaller models (e.g., Llama 3 8B, Qwen 2.5 7B).
- **Bearer Auth Enforcements**: Enable Base64 Bearer authentication when deploying `openbb-mcp` over HTTP/streamable-http endpoints in shared network environments or Kubernetes ingress routes.

## Diagnostic & Troubleshooting Guide

| Issue / Symptom | Root Cause | Resolution Strategy |
| :--- | :--- | :--- |
| `Exception: Empty Dataframe` returned from `obb.stocks.fa.income` | Invalid ticker symbol or insufficient access tier for selected downstream provider | Verify symbol formatting and ensure valid API key is set under `obb.account.credentials` for the requested provider. |
| `401 Unauthorized` on FastMCP HTTP connection | Missing or invalid Bearer credentials passed in request headers | Set `OPENBB_MCP_SERVER_AUTH` environment variable and pass correct Base64 Bearer header in client config. |
| Agent context window exhaustion during tool selection | Exposing hundreds of OpenBB endpoints simultaneously to client LLM | Launch `openbb-mcp` with `--allowed-categories` or enable dynamic tool discovery to lazily expose tools. |
| Rate-limit `429 Too Many Requests` from FRED / Polygon | Rapid agent loop issuing unthrottled API calls | Wrap OpenBB tool invocations in an async queue or implement client-side caching with Redis for historical daily prices. |

## Related tools / concepts
- [Tavily](../providers/tavily.md) — Sibling search provider optimized for broad real-time unstructured queries.
- [n8n](../../services/n8n.md) — Workflow automation engine used to orchestrate OpenBB-triggered financial signals.
- [Data Copilot](../../architecture/data-copilot-text-to-sql.md) — Standardized architecture for natural-language interface with structured data.
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md) — Pattern of retrieval-augmented generation for financial environments.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Universal protocol connecting OpenBB's dataset with LLMs.
- [MCP Registry](../automation_orchestration/mcp-registry.md) — Directory for locating and coordinating diverse MCP servers.

## Sources / references
- [OpenBB Official Website](https://openbb.co/)
- [OpenBB Documentation - Python SDK](https://docs.openbb.co/odp/python)
- [OpenBB Platform MCP Extension Guide](https://docs.openbb.co/odp/python/extensions/interface/openbb-mcp)
- [OpenBB GitHub Repository](https://github.com/OpenBB-finance/OpenBB)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
