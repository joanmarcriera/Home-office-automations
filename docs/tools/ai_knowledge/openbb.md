# OpenBB

## What it is
OpenBB is a comprehensive, open-source financial data platform designed for financial analysts, quantitative researchers, and AI agents. It standardizes access to hundreds of financial data endpoints across diverse asset classes (equities, options, crypto, forex, macroeconomics, fixed income) using a single unified Python SDK, a Terminal (CLI), or a web-based dashboard. As of late October / November 2026, **OpenBB Platform v5.0** fully standardizes native Model Context Protocol (MCP 3.1 / FastMCP 3.1) integration, enabling AI agents and LLMs (such as Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, Gemma 3, and Qwen 3.6) to autonomously execute high-fidelity financial queries and synthesize market intelligence in real-time.

## What problem it solves
It eliminates the critical challenge of fragmentation in financial data acquisition. Traditional research requires maintaining separate API integrations, pipelines, and schema-normalizations for dozens of disparate financial data providers (e.g., FMP, Polygon, AlphaVantage, FRED, SEC EDGAR, Benzinga). OpenBB normalizes data schemas, provides a consistent command-and-query interface, and delivers structured, high-fidelity JSON data directly to LLMs, bypassing the latency, hallucinations, and unreliability associated with general web-scraping or unstructured searches.

## Where it fits in the stack
**AI & Knowledge / Financial Intelligence Layer**. OpenBB acts as the dedicated financial data retrieval engine. It operates directly between raw data/provider APIs and downstream AI agentic frameworks, multi-agent systems, and specialized RAG networks that require deterministic, quantitative grounding.

## Typical use cases
- **Agentic Financial Research**: Equipping LLMs with real-time tools to fetch balance sheets, cash flow statements, insider trading data, and company valuations.
- **Autonomous Market Monitoring**: Setting up scheduled triggers to generate sector performance updates or track macro indicators (e.g., CPI, unemployment rates, interest shifts).
- **Quantitative Workflow Grounding**: Standardizing historical and real-time pricing feeds for algorithmic backtesting and portfolio optimization.
- **Model Context Protocol (MCP) Integration**: Spinning up local or remote MCP servers to serve financial intelligence directly to chat environments like Claude Desktop, Cursor, or VS Code.

## Strengths
- **Native MCP Support**: The `openbb-mcp-server` Python library provides zero-code conversions of OpenBB installations into MCP 3.0-compliant servers.
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
OpenBB can be installed via pip. To enable full AI agentic and MCP integration, install the core platform alongside the dedicated MCP server extension:

```bash
pip install openbb openbb-mcp-server
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

### Python (Financial Data Schema Validation with Pydantic v2)
Ensure data integrity when fetching financial intelligence from OpenBB by validating raw API data outputs against clean, type-coerced Pydantic schemas:

```python
from datetime import date
from typing import Optional, List
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

### Custom MCP Server Instance (FastAPI)
Developers can wrap an existing FastAPI instance with OpenBB's MCP generator and configure custom tool behavior:

```python
from fastapi import FastAPI
from openbb_mcp_server.app import create_mcp_server
from openbb_mcp_server.models.mcp_config import MCPConfigModel

app = FastAPI(title="Custom Financial Tooling")

@app.get(
    "/custom/valuation",
    openapi_extra={
        "mcp_config": {
            "expose": True,
            "mcp_type": "tool",
            "exclude_args": ["debug_token"],
            "prompts": [
                {
                    "name": "valuation_summary_prompt",
                    "description": "Perform a baseline company valuation analysis.",
                    "content": "Evaluate the current financial valuation for {symbol} utilizing FMP endpoints.",
                }
            ]
        }
    }
)
def get_valuation(symbol: str, debug_token: str = "default"):
    return {"symbol": symbol, "status": "active", "valuation_score": 88}

# Instantiate the MCP-wrapped server
# mcp_server = create_mcp_server(settings=None, fastapi_app=app)
```

### Claude Desktop Integration
Connect your local OpenBB MCP server to Claude Desktop by updating your `claude_desktop_config.json` configuration file:

```json
{
  "mcpServers": {
    "openbb-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "openbb-mcp-server",
        "--with",
        "openbb",
        "openbb-mcp",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

## Related tools / concepts
- [Tavily](../providers/tavily.md) — Sibling search provider optimized for broad real-time unstructured queries.
- [n8n](../../services/n8n.md) — Workflow automation engine used to orchestrate OpenBB-triggered financial signals.
- [Data Copilot](../../architecture/data-copilot-text-to-sql.md) — Standardized architecture for natural-language interface with structured data.
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md) — Pattern of retrieval-augmented generation for financial environments.
- [OpenRouter](./openrouter.md) — Dynamic LLM routing engine utilized to delegate financial queries to specialized reasoning models.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Universal protocol connecting OpenBB's dataset with LLMs.
- [MCP Registry](../automation_orchestration/mcp-registry.md) — Directory for locating and coordinating diverse MCP servers.
- [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md) — CLI integration for feeding market intelligence directly into spreadsheets.
- [Agno](../agents/agno.md) — Lightweight agentic library natively orchestrating OpenBB financial tools.
- [Mastra](../frameworks/mastra.md) — Agent development framework utilizing MCP-based tool definitions.
- [Smolagents](../frameworks/smolagents.md) — Minimalist Python-native agentic framework.
- [Pydantic AI](../frameworks/pydantic-ai.md) — Schema-validated Python agent builder.
- [Mycelium](../frameworks/mycelium.md) — Clojure-based, state-machine agent harness enforcing strict data contracts.
- [Perplexity](../../knowledge_base/self-healing-agent-research.md) — Alternative source for low-fidelity real-time search and semantic grounding.

## Sources / references
- [OpenBB Official Website](https://openbb.co/)
- [OpenBB Documentation - Python SDK](https://docs.openbb.co/odp/python)
- [OpenBB Platform MCP Extension Guide](https://docs.openbb.co/odp/python/extensions/interface/openbb-mcp)
- [OpenBB Official Blog - APIs and MCP Integration](https://didierlopes.com/blog/)
- [OpenBB GitHub Repository](https://github.com/OpenBB-finance/OpenBB)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-11-24
- Confidence: high
