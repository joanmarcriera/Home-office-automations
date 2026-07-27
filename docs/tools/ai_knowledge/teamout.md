# TeamOut

## What it is
TeamOut is an AI-native platform designed for the end-to-end planning and logistics of company retreats, offsites, and corporate events. It utilizes specialized agentic networks to automate venue sourcing, budget management, and itinerary generation, fully supporting the Model Context Protocol (MCP 3.1) standard.

## What problem it solves
Planning large-scale corporate events is traditionally a manual, months-long process involving thousands of emails. TeamOut reduces this to minutes by using AI to match company requirements (budget, team size, activities) with a global database of retreat-vetted venues. It leverages Claude 5.1 and GPT-5.5 for high-precision semantic matching and deep reasoning.

## Where it fits in the stack
**AI & Knowledge / Agents**. It is a verticalized AI agent specialized in the corporate travel and logistics domain, integrating with the home-office stack via [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).

## Typical use cases
- **Automated Venue Sourcing**: Finding retreats that specifically accommodate 50+ people with high-speed internet and breakout rooms.
- **Budget Optimization**: Iteratively testing different dates and locations to find the most cost-effective offsite.
- **Team Sentiment Analysis**: Synthesizing survey data from employees to automatically recommend activities (e.g., hiking vs. workshops).

## Strengths
- **Domain-Specific Logic**: Unlike general-purpose agents, TeamOut is pre-trained on travel logistics and corporate venue data.
- **Workflow Integration**: Integrates directly with Slack, Google Calendar, and MCP 3.1-compliant clients for team coordination.
- **High Signal Data**: Uses proprietary datasets of "retreat-ready" hotels that aren't always prioritized in general search engines.

## Limitations
- **Niche Focus**: Cannot be used for general travel (like individual flight booking) or general coding/task automation.
- **Platform Dependent**: Best experienced through the TeamOut web platform; external API access for custom agents is currently in early preview.

## When to use it
- When tasked with organizing a company offsite for 10 to 500+ people.
- When you need to provide multiple, budget-vetted options to leadership within a short timeframe.

## When not to use it
- For personal travel or small family vacations.
- For managing day-to-day office logistics or facilities management.

## Getting started

### Installation
TeamOut primarily operates as a managed service. To use the integration SDK for agents:

```bash
pip install teamout-sdk pydantic>=2.0
```

### Quick Start
You can interact with the TeamOut planning engine via their web interface or by sending a structured prompt to your integrated assistant:

1. Create an account at [teamout.com](https://app.teamout.com).
2. Define your "Retreat Profile" (Team size, preferred regions).
3. The TeamOut agent will generate 3-5 complete itineraries.

## CLI examples
While TeamOut is platform-first, the `teamout` CLI allows for programmatic status checks and profile management.

```bash
# Check the status of an ongoing retreat search
teamout status --retreat-id R_12345

# Export a draft itinerary to JSON for local review
teamout export --retreat-id R_12345 --format json --output ./itinerary.json

# List all active retreat projects with verbose logging
teamout projects list --verbose
```

## API examples

### Programmatic Retreat Request
Using the Python SDK with Pydantic v2 validation to trigger a search from a custom agent (e.g., a Claude 5.1-based assistant).

```python
from typing import List, Optional
from pydantic import BaseModel, Field
from teamout import TeamOutClient

# Define payload schema for strict Pydantic v2 validation
class RetreatSearchQuery(BaseModel):
    team_size: int = Field(..., gt=0, description="Number of participants")
    location: str = Field(..., description="Target region or country")
    budget_cap: float = Field(..., gt=0, description="Maximum budget in USD")
    requirements: List[str] = Field(default_factory=list, description="Core requirements")

client = TeamOutClient(api_key="TO_SEC_XYZ")

# Validate input parameters
query = RetreatSearchQuery(
    team_size=25,
    location="Portugal",
    budget_cap=35000.0,
    requirements=["meeting-rooms", "beach-access"]
)

# Request a venue search
retreat = client.search_venues(
    team_size=query.team_size,
    location=query.location,
    budget_cap=query.budget_cap,
    requirements=query.requirements
)

for venue in retreat.recommendations:
    print(f"Found: {venue.name} - Match Score: {venue.match_score}% - Est. Cost: ${venue.estimated_cost}")
```

## Related tools / concepts
- [AI Agents](../agents/agency-agents.md) — Broader context on AI agent frameworks.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for agentic communication.
- [Claude 5.1](../providers/anthropic.md) — Frontier model used for retreat reasoning.
- [GPT-5.5](openai.md) — LLM provider for travel logistics synthesis.
- [Make](../automation_orchestration/make.md) — Used for automating retreat workflows.
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) — Framework for building agentic travel apps.
- [LangChain](langchain.md) — Library for orchestrating travel planning agents.
- [Event Management Automation](../automation_orchestration/index.md) — General category for event tools.

## Sources / references
- [Official TeamOut AI Page](https://app.teamout.com/ai)
- [TeamOut API Documentation (Preview)](https://docs.teamout.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-09-25
- Confidence: high
