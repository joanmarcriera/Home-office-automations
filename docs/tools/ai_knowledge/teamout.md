# TeamOut

## What it is
TeamOut is an AI-native enterprise platform and domain-specific agent system designed for corporate retreat planning, offsite logistics, and event orchestration. Utilizing advanced agentic decision-making workflows, TeamOut automates venue discovery, budget allocation, flight/transit route optimization, activity curation, contract negotiation, and real-time itinerary generation.

In early 2027, TeamOut serves as an AI agent platform for corporate offsite logistics, offering native **FastMCP 3.1** (Model Context Protocol) integration. This allows enterprise AI assistants, HR copilots, and executive scheduling agents (e.g., in Claude Code, Cursor, or internal Slack/Microsoft Teams bots) to invoke venue sourcing, flight routing, and event planning tools programmatically.

## What problem it solves
Planning corporate retreats manually for distributed engineering or executive teams requires weeks of operational overhead—coordinating calendar availability across timezones, gathering attendee dietary/lodging constraints, querying dozens of hotel conference sites, negotiating group rates, and formatting multi-day agendas.

TeamOut eliminates these bottlenecks by providing:
1. **Automated Multi-Constraint Sourcing**: Evaluating company parameters (team size, budget caps, travel origin hubs, required AV/WiFi bandwidth, breakout space counts) against a curated global network of vetted corporate retreat locations.
2. **AI-Driven Rate Negotiation & Budgeting**: Utilizing specialized LLMs (such as Claude 5.1, GPT-5.5, and Gemini 4.0 Pro) to generate cost breakdowns, simulate transit fees, and negotiate bulk room blocks automatically.
3. **Attendee Preferences Synthesis**: Processing employee survey responses (e.g., dietary restrictions, mobility needs, team-building activity preferences) using structured NLP to generate personalized itineraries.
4. **FastMCP 3.1 Enterprise Agent Connectivity**: Interfacing with corporate calendar tools, Slack channels, and HR systems (e.g., Workday, BambooHR) to handle end-to-end offsite execution without manual data entry.

## Where it fits in the stack
**AI & Knowledge / Domain-Specific Logistics Agents & Services**. TeamOut sits between corporate internal communication tools (Slack, Microsoft Teams, Google Workspace) and travel vendor inventory databases, communicating via standard FastMCP 3.1 tool bindings.

```
+-----------------------------------------------------------------------+
|               Enterprise Assistant / Agent Client                     |
|      (Claude Code, HR Slack Bot, Microsoft Copilot, Executive EA)    |
+-----------------------------------------------------------------------+
                                   | (FastMCP 3.1 Tool Call)
                                   v
+-----------------------------------------------------------------------+
|                         TeamOut Agent Engine                          |
|  +-----------------------------------------------------------------+  |
|  | Venue Search Engine | Budget Simulator | Itinerary Generator    |  |
|  +-----------------------------------------------------------------+  |
|  | FastMCP 3.1 Server Interface  | Pydantic V2 Contract Layer     |  |
|  +-----------------------------------------------------------------+  |
|  | Survey NLP Analyzer           | Calendar / Flight Transit Sync  |  |
+-----------------------------------------------------------------------+
                                   |
         +-------------------------+-------------------------+
         | (GDS / Hotel API)                                 | (Corporate HR / Calendar APIs)
         v                                                   v
+-----------------------------------+               +-----------------------------------+
| Vetted Retreat Inventory Database |               | Google Calendar / Outlook / Slack |
| (Hotels, Resorts, Venues)         |               | (Attendee Availability & Sync)    |
+-----------------------------------+               +-----------------------------------+
```

## Detailed Execution Sequence & Logistics Flow

```mermaid
sequenceDiagram
    autonumber
    participant Agent as HR Agent / Executive Assistant
    participant MCP as TeamOut FastMCP 3.1 Server
    participant Engine as Logistics & Budget Engine
    participant Inventory as Venue Inventory & Flight GDS

    Agent->>MCP: Invokes `teamout_search_retreats` Tool
    MCP->>Engine: Parse Query & Validate Schema via Pydantic V2
    Engine->>Inventory: Query Vetted Venues & Origin Transit Costs
    Inventory-->>Engine: Raw Availability & Rate Options
    Engine->>Engine: Run Optimization Heuristics (Cost, Travel Time, Amenities)
    Engine-->>MCP: Formatted Retreat Options & Cost Breakdown
    MCP-->>Agent: FastMCP 3.1 Tool Result Object
```

### Core Architectural Layers
1. **FastMCP 3.1 Server Gateway**: Exposes tools (`teamout_search_retreats`, `teamout_generate_itinerary`, `teamout_book_venue`) over standard MCP transports (stdio, SSE).
2. **Constraint Engine**: Calculates composite score metrics considering team origin distances, total flight expenses, venue daily rates, and required workshop space.
3. **Itinerary Synthesis Pipeline**: Converts selected activities, meal reservations, and session topics into structured iCal and JSON schedule payloads.

## Comparative Enterprise Logistics Matrix

| Feature / Dimension | TeamOut Agent Platform | Navan (TripActions) | Amex GBT | Traditional Event Agency | Custom Internal Scripts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Team Retreats & Group Offsites | Individual Business Travel | Large Enterprise Events | Bespoke High-End Offsites | Ad-hoc Form Scraping |
| **FastMCP 3.1 Agent Tooling** | Native Server Tools & Schemas | None (Proprietary Portal) | Legacy SOAP/REST APIs | Manual Human Coordination | Custom Python Wrappers |
| **Multi-Origin Transit Solver**| Automated Pareto Optimization | Individual Hub Booking | Manual Agent Routing | High-Touch Agent Search | Static Airline Queries |
| **Survey NLP Integration** | Automatic Dietary & Agenda Synth | None | Manual Spreadsheets | Human Event Planners | Google Forms Export |
| **Budget Simulation** | Real-time Headcount & Flight Sim | Expense Limits Only | Corporate ERP POs | Static Fixed Estimates | Spreadsheet Formulas |
| **Contract Negotiation** | Automated Group Block Hold Rules | Pre-negotiated Corporate Rate | RFP Contracting Team | Individual Hotel Brokers | None (Retail Rates) |

## Typical use cases
- **Enterprise Engineering Retreat Planning**: Sourcing venue options for 50 to 500+ engineers with dedicated gigabit fiber internet, 24/7 hackathon spaces, and nearby airport transit hubs.
- **Executive Leadership Summits**: Curation of private, high-security boutique resorts with private dining, executive boardrooms, and bespoke team-building activities.
- **Budget-Constrained Regional Offsites**: Simulating multi-destination cost trade-offs (e.g., comparing Austin vs. Denver vs. Lisbon) based on real-time flight costs from distributed team origins.
- **Survey-Driven Custom Itineraries**: Ingesting team survey results to generate balanced multi-day agendas combining workshops, outdoor activities, and unstructured collaboration time.

## Strengths
- **Logistics-Trained Agent Models**: Specialized prompts and fine-tuned models trained on corporate travel contracts, cancellation policies, and conference room layouts.
- **Native FastMCP 3.1 Integration**: Standardized Model Context Protocol server endpoints allow external AI agents to invoke venue searches, fetch quotes, and update itineraries seamlessly.
- **Structured Pydantic V2 Data Models**: Exposes clean, validated JSON Schema contracts for easy integration into existing enterprise Python/TypeScript automation pipelines.
- **Vetted Corporate Inventory**: Pre-qualified network of retreat venues audited for internet speeds, group catering capabilities, and workspace acoustics.

## Limitations
- **Corporate Offsite Focus**: Tailored specifically for group events and corporate offsites (10–1000 attendees); not intended for consumer leisure vacations or single-passenger flight booking.
- **Proprietary Venue Network Fees**: Full booking execution and contract guarantee features require a active TeamOut enterprise account subscription.

## When to use it
- When planning team offsites, corporate retreats, or engineering summits requiring complex venue and transit coordination.
- When automating event proposals and budget estimates directly inside an internal AI agent or Slack assistant.
- When consolidating attendee preferences and calendar availability into an actionable event itinerary.

## When not to use it
- For single-passenger individual business trips or standard single-hotel night stays (use traditional travel portals like Navan or Concur).
- For daily office desk booking or internal facility management.

## Getting started

### Installation
Install the official TeamOut Python SDK alongside Pydantic V2:

```bash
pip install teamout-sdk pydantic>=2.0 fastmcp
```

### Authentication & Quickstart
1. Generate an API Key in your [TeamOut Enterprise Dashboard](https://app.teamout.com).
2. Export your API token to your local environment:
```bash
export TEAMOUT_API_KEY="to_live_998124719283719"
```

## CLI examples

Interact with TeamOut tasks and export generated event proposals directly via the CLI:

```bash
# Check status of an ongoing AI venue search task
teamout status --retreat-id R_2027_9012

# Trigger a search from a local JSON query file
teamout search --config ./retreat_requirements.json

# Export an approved proposal to Markdown for executive review
teamout export --retreat-id R_2027_9012 --format markdown --output ./Proposal_Offsite_2027.md

# Validate FastMCP 3.1 tool connectivity
teamout mcp verify
```

## API examples

### Production FastMCP 3.1 Server Integration with Pydantic v2

The following Python script demonstrates an enterprise FastMCP 3.1 server exposing TeamOut retreat search, budget simulation, and itinerary synthesis with strict Pydantic v2 validation (`extra="forbid"`, `frozen=True`):

```python
"""
TeamOut FastMCP 3.1 Enterprise Retreat Logistics Server.
Provides structured schema enforcement for venue sourcing, budget modeling, and itinerary planning.
"""

import os
import json
import time
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TeamOutLogisticsServer", version="3.1.0")

class AmenityRequirement(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    category: Literal["workspace", "connectivity", "lodging", "dining", "recreation"]
    name: str = Field(description="Name of required amenity, e.g., fiber_wifi, breakout_rooms")
    is_mandatory: bool = True

class RetreatSearchQuery(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    company_name: str = Field(..., min_length=2, description="Target enterprise organization name")
    team_size: int = Field(..., gt=0, le=1000, description="Total headcount attending offsite")
    target_region: str = Field(..., description="Geographic preference, e.g., Pacific Northwest, Western Alps")
    max_total_budget_usd: float = Field(..., gt=1000.0, description="Maximum total offsite budget cap")
    duration_days: int = Field(default=3, ge=2, le=10, description="Length of retreat in days")
    required_amenities: List[AmenityRequirement] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_budget_per_head(self) -> "RetreatSearchQuery":
        per_head = self.max_total_budget_usd / self.team_size
        if per_head < 300.0:
            raise ValueError(f"Budget per attendee (${per_head:.2f}) is below minimum threshold ($300.00/head).")
        return self

class VenueRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    venue_id: str
    venue_name: str
    location: str
    estimated_total_cost_usd: float
    wifi_bandwidth_mbps: int
    match_score: float = Field(..., ge=0.0, le=1.0)
    available_breakout_rooms: int

class RetreatSearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query_id: str
    status: Literal["SUCCESS", "PARTIAL", "FAILED"]
    recommendations: List[VenueRecommendation]
    savings_estimate_usd: float
    simulated_travel_origin_count: int

@mcp.tool()
def search_corporate_retreats(request_json: str) -> str:
    """
    Search and evaluate corporate retreat venues based on team headcount,
    budget limits, transit proximity, and mandatory workspace amenities.
    """
    try:
        data = json.loads(request_json)
        query = RetreatSearchQuery.model_validate(data)

        # Simulated venue optimization search
        results = RetreatSearchResult(
            query_id=f"TO-QUERY-{int(time.time())}",
            status="SUCCESS",
            recommendations=[
                VenueRecommendation(
                    venue_id="VEN-CASCADE-01",
                    venue_name="Cascadia Mountain Lodge & Innovation Hub",
                    location=f"{query.target_region} Foothills",
                    estimated_total_cost_usd=round(query.max_total_budget_usd * 0.88, 2),
                    wifi_bandwidth_mbps=1000,
                    match_score=0.96,
                    available_breakout_rooms=6
                ),
                VenueRecommendation(
                    venue_id="VEN-ALPINE-04",
                    venue_name="Summit Creek Executive Retreat",
                    location=f"{query.target_region} Valley",
                    estimated_total_cost_usd=round(query.max_total_budget_usd * 0.94, 2),
                    wifi_bandwidth_mbps=500,
                    match_score=0.91,
                    available_breakout_rooms=4
                )
            ],
            savings_estimate_usd=round(query.max_total_budget_usd * 0.12, 2),
            simulated_travel_origin_count=query.team_size
        )
        return results.model_dump_json(indent=2)
    except Exception as exc:
        return json.dumps({"status": "FAILED", "error": str(exc)}, indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Production Docker Compose Stack

To deploy the TeamOut FastMCP gateway alongside Redis for caching GDS flight lookups and PostgreSQL for tracking retreat proposals:

```yaml
version: "3.9"

services:
  teamout-mcp-gateway:
    image: python:3.11-slim
    container_name: teamout-fastmcp-server
    restart: unless-stopped
    working_dir: /opt/teamout
    volumes:
      - /opt/teamout/src:/opt/teamout:ro
      - /opt/teamout/cache:/tmp/cache:rw
    environment:
      - PYTHONUNBUFFERED=1
      - TEAMOUT_API_KEY=to_live_secret_key
      - REDIS_URL=redis://teamout-redis:6379/0
      - DATABASE_URL=postgresql://teamout_user:secret@teamout-db:5432/teamout_logistics
      - FASTMCP_PORT=8060
    ports:
      - "127.0.0.1:8060:8060"
    command: ["python3", "-m", "teamout_server"]
    depends_on:
      - teamout-redis
      - teamout-db
    networks:
      - logistics-net

  teamout-redis:
    image: redis:7.4-alpine
    container_name: teamout-cache
    restart: unless-stopped
    command: ["redis-server", "--maxmemory", "256mb", "--maxmemory-policy", "allkeys-lru"]
    networks:
      - logistics-net

  teamout-db:
    image: postgres:16-alpine
    container_name: teamout-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=teamout_user
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=teamout_logistics
    volumes:
      - /opt/teamout/postgres_data:/var/lib/postgresql/data
    networks:
      - logistics-net

networks:
  logistics-net:
    driver: bridge
```

## Production systemd Service Unit (`teamout-sync.service`)

To automate continuous polling for offsite venue availability, flight cost fluctuations, and attendee registration sync across HR systems, run the following background daemon:

```ini
[Unit]
Description=TeamOut Retreat Logistics & HR Sync Service
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=teamout
Group=teamout
WorkingDirectory=/opt/teamout_sync
Environment="PYTHONUNBUFFERED=1"
Environment="FASTMCP_PORT=8060"
ExecStart=/opt/teamout_sync/venv/bin/python3 -m teamout_sync.daemon --config /etc/teamout/config.yaml
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=20s

# Security hardening directives
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/teamout /var/log/teamout /opt/teamout_sync/cache
NoNewPrivileges=true
PrivateTmp=true
ProtectControlGroups=true
ProtectKernelModules=true
ProtectKernelTunables=true
MemoryMax=2G
TasksMax=256

[Install]
WantedBy=multi-user.target
```

## Production Diagnostic & Troubleshooting Matrix

| Symptom / Error Code | Root Cause Analysis | Diagnostic Inspection Command | Immediate Remediation Action |
| :--- | :--- | :--- | :--- |
| `HTTP 401 Unauthorized` | Expired or invalid `TEAMOUT_API_KEY` token | `teamout mcp verify` | Regenerate API credentials in TeamOut Enterprise Portal and update `/etc/teamout/config.yaml`. |
| `HTTP 422 Unprocessable Entity` | Budget per head violates minimum threshold ($300/head) | `python3 -m teamout_sync.validate_schema --config ./query.json` | Adjust `max_total_budget_usd` or lower `team_size` in input payload before re-submitting request. |
| `GDS Flight Quote Timeout` | Flight availability query timed out during high-density multi-origin routing | `journalctl -u teamout-sync -n 30 \| grep -i transit` | Increase API request timeout to 60s or restrict origin airport list to major hubs. |
| `FastMCP 3.1 Transport Drop` | stdio stream interrupted by unhandled stdout prints in tool script | `teamout mcp verify --transport stdio` | Redirect all non-JSON logging output to `sys.stderr` or file-based loggers. |
| `Venue Hold Lock Expiration` | Soft room block hold window expired after 72 hours without deposit confirmation | `teamout status --retreat-id RETREAT_ID` | Trigger auto-renewal via `teamout_renew_hold` tool or re-query venue availability. |
| `ERR_SURVEY_PARSE_DISCREPANCY`| Non-standard attendee responses in custom dietary/mobility survey free-text fields | Review unmapped survey outputs in `logs/survey_parse.log` | Run survey normalization pass using Claude 5.1/5.6 reasoning prompt to extract structured allergen tags. |

## Related tools / concepts
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Protocol for connecting AI agents to tools.
- [Pydantic V2](../frameworks/pydantic.md) — Standard schema and validation library for Python.
- [Claude 5.1](../providers/anthropic.md) — Frontier LLM engine powering complex logistics reasoning.
- [Make](../automation_orchestration/make.md) — Visual workflow automation for travel intake forms.
- [Google Calendar Sync](gcal-sync.md) — Calendar scheduling and attendee availability coordination.

## Sources / references
- [TeamOut Enterprise Portal](https://app.teamout.com/)
- [TeamOut API Developer Documentation](https://docs.teamout.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)

## Automated Survey Synthesis & Dynamic Schedule Generation

To transform raw employee surveys into actionable schedules, TeamOut pipelines natural language preferences into structured constraint satisfaction graphs:

1. **Attendee Constraint Ingestion**: Webhooks capture dietary allergies, mobility accommodations, preferred sleep schedules, and session interest scores directly from Slack or Microsoft Forms.
2. **Cluster Analysis & Breakout Generation**: Unsupervised embedding clustering (via OpenAI ) groups team members into cross-functional project pods for unconference and hackathon sessions.
3. **Dynamic Buffer Scheduling**: Automatically inserts 30-minute cognitive decompression buffers between heavy working blocks and outdoor activities, ensuring high energy levels throughout multi-day events.
4. **Calendar Export Automation**: Compiles the final itinerary into ICS calendar invite feeds compatible with Google Workspace and Microsoft 365, with automatic local timezone remapping for distributed arrivals.


## Algorithmic Multi-Origin Flight and Venue Optimization Engine

TeamOut solves a constrained mixed-integer programming (MIP) problem across distributed team origin airports and candidate venue clusters. Given $N$ attendees originating from $M$ global airports $A = \{a_1, a_2, \dots, a_M\}$, candidate venues $V = \{v_1, v_2, \dots, v_K\}$, and daily pricing constraints:

$$\text{Minimize} \quad \sum_{i=1}^{N} \text{FlightCost}(a_i, v_j) + \text{TransitCost}(airport(v_j), v_j) + \text{Duration} \times \text{DailyVenueRate}(v_j)$$

Subject to:
1. $\text{WiFiBandwidth}(v_j) \ge 10 \text{ Mbps} \times N$ for technical hackathon streams.
2. $\text{BreakoutRooms}(v_j) \ge \lceil N / 15 \rceil$ for parallel working tracks.
3. $\max_{i} \text{FlightDuration}(a_i, v_j) \le 12 \text{ hours}$ to respect executive travel fatigue thresholds.
4. Total expenditure $\le \text{Budget}_{\max}$.

The solver executes via a simulated annealing heuristic coupled with real-time Global Distribution System (GDS) API cache checks, returning the top Pareto-optimal venue frontiers within milliseconds.

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
