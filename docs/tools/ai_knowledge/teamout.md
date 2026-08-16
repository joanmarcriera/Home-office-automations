# TeamOut

## What it is
TeamOut is an AI-native platform designed for corporate retreat planning, offsite logistics, and event orchestration. It employs specialized agentic workflows to automate venue discovery, budget management, activity curation, and itinerary generation. As of early January 2027, TeamOut natively supports **FastMCP 3.1** (Model Context Protocol), enabling AI assistants to interface directly with event planning pipelines.

## What problem it solves
Planning corporate retreats manually involves extensive email communication, venue negotiation, and schedule coordination over several weeks. TeamOut automates this process by evaluating company parameters (team headcount, budget caps, travel constraints, desired amenities) against a database of vetted corporate retreat locations. Powered by frontier models like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**, TeamOut delivers matched recommendations and optimized travel itineraries in minutes.

## Where it fits in the stack
**AI & Knowledge / Agents**. It operates as a domain-specific AI agent platform for corporate travel and event logistics, connecting to home-office and enterprise automation stacks via [FastMCP 3.1](../automation_orchestration/mcp.md).

## Typical use cases
- **Automated Venue Sourcing**: Locating retreat sites for groups of 10 to 500+ participants with high-speed internet, conference facilities, and lodging.
- **Budget & Logistics Optimization**: Simulating location, date, and transit options to maximize budget efficiency.
- **Team Interest Synthesis**: Processing internal survey data to tailor retreat activities and workshop schedules automatically.

## Strengths
- **Domain-Specific Logic**: Pre-trained on corporate travel logistics, contract terms, and venue capabilities.
- **Agentic Connectivity**: Native **FastMCP 3.1** integration allows external AI agents to trigger searches and retrieve itineraries.
- **Curated Inventory**: Accesses vetted databases of retreat-ready hotels and conference venues.

## Limitations
- **Specialized Scope**: Designed specifically for corporate offsites rather than general consumer travel or individual flight bookings.
- **Platform-Centric Access**: Advanced features require a TeamOut enterprise account, though integration APIs are available.

## When to use it
- When organizing company offsites, team retreats, or executive summits for 10 to 500+ attendees.
- When generating vetted location options and budget proposals on short notice.
- When incorporating corporate retreat scheduling into automated workflow pipelines.

## When not to use it
- For personal leisure travel or family vacations.
- For day-to-day office facilities or hot-desking management.

## Getting started

### Installation
TeamOut provides a web platform alongside developer integration libraries.

```bash
pip install teamout-sdk pydantic>=2.0
```

### Quick Start
1. Register an account on [TeamOut](https://app.teamout.com).
2. Configure company parameters and retreat preferences.
3. Utilize the web dashboard or API SDK to generate venue options and itineraries.

## CLI examples

### 1. Checking Retreat Task Status
Use the `teamout` CLI tool to inspect ongoing search tasks:
```bash
teamout status --retreat-id R_2027_0098
```

### 2. Exporting Itinerary to JSON
Export an approved itinerary to local storage for downstream automation:
```bash
teamout export --retreat-id R_2027_0098 --format json --output ./retreat_itinerary.json
```

## API examples

### Programmatic Retreat Sourcing with Pydantic v2
The following Python script illustrates querying the TeamOut API using strict **Pydantic v2** validation schemas:

```python
import os
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class RetreatQuerySchema(BaseModel):
    team_size: int = Field(..., gt=0, description="Total headcount")
    region: str = Field(..., description="Target geographic region")
    budget_cap_usd: float = Field(..., gt=0, description="Maximum total budget in USD")
    amenities: List[str] = Field(default_factory=list, description="Required facilities")

    @field_validator("team_size")
    @classmethod
    def validate_team_size(cls, v: int) -> int:
        if v > 2000:
            raise ValueError("Team size exceeds single retreat support limit (2000).")
        return v

def search_retreat_venues(query: RetreatQuerySchema) -> dict:
    api_key = os.getenv("TEAMOUT_API_KEY", "MOCK_KEY_2027")

    # Payload prepared from validated model
    payload = query.model_dump()
    print(f"Searching TeamOut venues with payload: {payload}")

    # Mock return structure matching API spec
    return {
        "status": "success",
        "matches_found": 3,
        "query": payload,
        "recommendations": [
            {
                "venue_name": "Pine Valley Conference Resort",
                "location": query.region,
                "est_cost_usd": query.budget_cap_usd * 0.85,
                "match_score": 0.96
            }
        ]
    }

# Execution example
if __name__ == "__main__":
    query = RetreatQuerySchema(
        team_size=45,
        region="Cascadia",
        budget_cap_usd=65000.0,
        amenities=["high-speed-wifi", "breakout-rooms", "catering"]
    )
    result = search_retreat_venues(query)
    print("Search Result:", result)
```

### FastMCP 3.1 Tool Request Schema
When an AI assistant powered by **Claude 5.1** or **GPT-5.5** triggers TeamOut via FastMCP 3.1:

```json
{
  "tool": "teamout_search_retreats",
  "arguments": {
    "team_size": 45,
    "region": "Cascadia",
    "budget_cap_usd": 65000.0,
    "amenities": ["high-speed-wifi", "breakout-rooms"]
  }
}
```

## Related tools / concepts
- [AI Agents](../agents/agency-agents.md) — Multi-agent frameworks and autonomous design patterns.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agentic tool access (FastMCP 3.1).
- [Claude 5.1](../providers/anthropic.md) — Frontier model utilized for complex travel reasoning.
- [GPT-5.5](openai.md) — LLM provider for logistics and proposal synthesis.
- [Make](../automation_orchestration/make.md) — Visual workflow automation for travel intake.

## Sources / references
- [TeamOut Platform Portal](https://app.teamout.com/)
- [TeamOut API Reference](https://docs.teamout.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
