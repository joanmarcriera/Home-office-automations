# TeamOut

## What it is
TeamOut is an AI-native enterprise platform and domain-specific agent system designed for corporate retreat planning, offsite logistics, and large-scale event orchestration. Utilizing advanced agentic decision-making workflows, TeamOut automates venue discovery, budget allocation, flight and transit route optimization, vendor contract negotiation, attendee preference synthesis, and real-time itinerary generation.

In early 2027, TeamOut serves as an AI agent platform for corporate offsite logistics, offering native **FastMCP 3.1** (Model Context Protocol) integration. This allows enterprise AI assistants, HR copilots, and executive scheduling agents (e.g., in Claude Code, Cursor, or internal Slack/Microsoft Teams bots) to invoke venue sourcing, budget simulations, and event planning tools programmatically with zero manual data entry.

## What problem it solves
Planning corporate retreats manually for distributed engineering or executive teams requires weeks of operational overhead—coordinating calendar availability across timezones, gathering attendee dietary/lodging constraints, querying dozens of hotel conference sites, negotiating group rates, and formatting multi-day agendas.

TeamOut eliminates these bottlenecks by providing:
1. **Automated Multi-Constraint Sourcing**: Evaluating company parameters (team size, budget caps, travel origin hubs, required AV/WiFi bandwidth, breakout space counts) against a curated global network of vetted corporate retreat locations.
2. **AI-Driven Rate Negotiation & Budgeting**: Utilizing specialized LLMs (such as Claude 5.6, Claude 5.1, GPT-5.6, and Gemini 4.0 Pro) to generate cost breakdowns, simulate transit fees, and negotiate bulk room blocks automatically.
3. **Attendee Preferences Synthesis**: Processing employee survey responses (e.g., dietary restrictions, mobility needs, team-building activity preferences) using structured NLP to generate personalized itineraries.
4. **FastMCP 3.1 Enterprise Agent Connectivity**: Interfacing with corporate calendar tools, Slack channels, and HR systems (e.g., Workday, BambooHR) to handle end-to-end offsite execution without manual data entry.

## Where it fits in the stack
**Category**: AI & Knowledge / Domain-Specific Logistics Agents & Services. TeamOut sits between corporate internal communication tools (Slack, Microsoft Teams, Google Workspace) and travel vendor inventory databases, communicating via standard FastMCP 3.1 tool bindings.

```
+---------------------------------------------------------------------------------------------------------+
|                                  ENTERPRISE ASSISTANT / AGENT CLIENT LAYER                              |
|                                                                                                         |
|   +------------------------------------+             +----------------------------------------------+   |
|   |  Executive EA / HR Copilot Ingress |             |         FastMCP 3.1 Client Ingress           |   |
|   |  - Slack Bot / MS Teams / Email    |             |  - Structured Tool Invocations               |   |
|   |  - Web Portal / Form Submissions   |             |  - Resource Context Subscription             |   |
|   +-----------------+------------------+             +----------------------+-----------------------+   |
|                     |                                                       |                           |
|                     +--------------------------+----------------------------+                           |
|                                                | Authorized Event Query Payload                         |
|                                                v                                                        |
|   +-------------------------------------------------------------------------------------------------+   |
|   |                                  TEAMOUT ORCHESTRATION AGENT ENGINE                             |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   |  |                             Multi-Constraint Sourcing Engine                              |  |   |
|   |  |  - Venue Capacity & Layout Matcher               - Global Flight Cost Minimizer           |  |   |
|   |  |  - Fiber Internet / AV Bandwidth Verification     - Carbon Footprint Optimization          |  |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   |  |                             Budget & Contract Simulation Sandbox                          |  |   |
|   |  |  - Dynamic Rate Estimation                       - Seasonal Price Elasticity Adjuster     |  |   |
|   |  |  - Attrition & Cancellation Risk Model           - At-Scale Negotiation Draft Generator   |  |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   |  |                             Attendee Preference & Survey NLP Synthesizer                  |  |   |
|   |  |  - Dietary & Accessibility Constraint Aggregator - Team Dynamics & Activity Recommender   |  |   |
|   |  |  - Calendar Sync & Timezone Overlap Engine       - Pydantic v2 Contract Enforcement       |  |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   +--------------------------------------------+----------------------------------------------------+   |
|                                                |                                                        |
|                     +--------------------------+----------------------------+                           |
|                     | Global Distribution System (GDS)                      | Enterprise Data Sync      |
|                     v                                                       v                           |
|   +------------------------------------+             +----------------------------------------------+   |
|   |  Vetted Venue & Hotel Repositories |             |     Enterprise Productivity Connectors       |   |
|   |  - Amadeus / Sabre GDS Feeds       |             |  - Google Calendar / Outlook Graph API       |   |
|   |  - Direct Hotel API Partnerships   |             |  - Workday / BambooHR Roster Sync            |   |
|   |  - Dedicated Boutique Retreat Hubs |             |  - Slack Polling & Announcement Bot          |   |
|   +------------------------------------+             +----------------------------------------------+   |
+---------------------------------------------------------------------------------------------------------+
```

## Detailed Execution Sequence Flow

The operational flow when an autonomous agent schedules a retreat via TeamOut is illustrated below:

```
[HR Assistant / Claude Code Agent]
        |
        v
[FastMCP 3.1 Gateway Tool: teamout_search_retreats]
        |
        +---> [1. Request Validation via Strict Pydantic v2 Contract]
        |        |
        |        +--> Verifies headcount (> 0), budget per attendee (>= $300/head)
        |        +--> Confirms region and mandatory technical amenity criteria
        |
        +---> [2. Multi-Airport Flight Transit Simulation]
        |        |
        |        +--> Pulls employee home airport distribution from HRIS connector
        |        +--> Calculates aggregate travel time and cost matrix across candidates
        |
        +---> [3. Venue Availability & Workspace Acoustic Scoring]
        |        |
        |        +--> Queries vetted retreat inventory with verified gigabit fiber
        |        +--> Checks private breakout room and plenary hall availability
        |
        +---> [4. AI-Driven Cost Simulation & Contract Generation]
        |        |
        |        +--> Models seasonal tier discounts and calculates total savings
        |        +--> Generates custom multi-day agenda with balanced workshop blocks
        |
        +---> [5. Structured Result Packaging]
        |
        v
[Return Validated Retreat Proposal & Booking Links to Invoking Agent]
```

## Typical use cases
- **Global Engineering Hackathons**: Sourcing private retreat campuses capable of hosting 50 to 500+ developers with 24/7 dedicated high-speed fiber, backup power, plenary auditoriums, and ergonomic seating.
- **Executive Leadership Summits**: Booking private, high-security boutique retreats with executive dining, private meeting spaces, and bespoke team-building activities.
- **Multi-Origin Cost Optimization**: Running automated simulations to determine whether hosting a 60-person distributed team in Lisbon, Denver, or Austin yields the lowest total travel cost and flight duration.
- **Survey-Driven Custom Itineraries**: Ingesting attendee dietary restrictions, physical accessibility requirements, and survey feedback to generate personalized daily schedules.

## Strengths
- **Domain-Specific Logistics Agents**: Prompts and optimization models fine-tuned on corporate travel contracts, cancellation policies, and conference room layouts.
- **Native FastMCP 3.1 Protocol Server**: Exposes standardized tools (`teamout_search_retreats`, `teamout_generate_itinerary`, `teamout_book_venue`) directly to AI assistants.
- **Strict Pydantic v2 Schema Enforcement**: Zero-tolerance contract validation ensures external callers receive predictable, strongly typed JSON payloads.
- **Vetted Corporate Inventory**: Curated network of properties pre-audited for verified internet bandwidth, AV infrastructure, and professional catering capabilities.

### 7-Dimension Platform Comparison

| Feature / Dimension | TeamOut | Navan (TripActions) | TravelPerk | Traditional Event Agency | Custom Internal Scripts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Domain Focus** | Corporate Retreats & Offsites | Individual Corporate Travel | Business Travel & Events | Bespoke Event Production | Ad-hoc Venue Booking |
| **FastMCP 3.1 Tool Server** | Native First-Class Server | None (Proprietary REST) | REST Webhooks Only | None | Manual Implementation |
| **Flight Matrix Minimizer** | Automatic Multi-Origin Engine | Single-Origin Booking | Group Travel Add-on | Manual Travel Agent Quotes| Google Flights Scraping |
| **Workspace & Tech Vetting**| Verified Fiber / AV Audits | Standard Hotel Star Rating | Hotel Filter Tags | Site Visit Verification | Unverified Reviews |
| **Contract Automation** | AI Rate Simulation & Clauses | Standard Corporate Rates | Standard Rates | Human Negotiation | None |
| **Itinerary Generation** | Agentic Survey-to-Agenda | Basic Itinerary List | Static Calendar Invite | PDF Deck | Manual Spreadsheet |
| **Pydantic v2 Schemas** | Strict Contract Validation | None | OpenAPI JSON | None | Custom DTOs |

## Limitations
- **Retreat & Group Focus**: Optimized specifically for groups (10 to 1,000+ attendees); unsuitable for individual business traveler overnight stays.
- **Subscription & Booking Tiers**: Full contract negotiation execution and locked group rates require an active TeamOut enterprise license.
- **Inventory Geographic Concentration**: Highest density of pre-vetted corporate retreat hubs is concentrated across North America and Europe, with growing coverage in APAC and Latin America.

## When to use it
- When planning team offsites, corporate retreats, or engineering summits requiring complex venue and transit coordination.
- When automating event proposals and budget estimates directly inside an internal AI agent or Slack assistant.
- When consolidating attendee preferences and calendar availability into an actionable event itinerary.

## When not to use it
- For single-passenger individual business trips or standard single-hotel night stays (use traditional travel portals like Navan or Concur).
- For daily office desk booking or internal facility management.

## Getting started

### Installation
Install the TeamOut Python SDK alongside FastMCP 3.1 and Pydantic v2:

```bash
pip install teamout-sdk "mcp[cli]>=3.1.0" "pydantic>=2.6.0"
```

### Authentication & Quickstart
1. Generate an API Key in your [TeamOut Enterprise Dashboard](https://app.teamout.com).
2. Set your environment variable:
```bash
export TEAMOUT_API_KEY="to_live_998124719283719"
```

## CLI examples

```bash
# Check status of an ongoing AI venue search task
teamout status --retreat-id R_2027_9012

# Trigger a search from a local JSON query file
teamout search --config ./retreat_requirements.json

# Export an approved proposal to Markdown for executive review
teamout export --retreat-id R_2027_9012 --format markdown --output ./Proposal_Offsite_2027.md

# Verify FastMCP 3.1 tool connectivity
teamout mcp verify
```

## API examples

### Production FastMCP 3.1 Logistics Server Implementation

The following complete, production-grade FastMCP 3.1 server exposes retreat sourcing and budget simulation tools. It implements strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) and returns validated proposal payloads:

```python
"""
Production TeamOut FastMCP 3.1 Enterprise Retreat Logistics Server
Provides multi-constraint venue sourcing and budget simulation with strict Pydantic v2 models.
"""

import os
import sys
import json
import time
import logging
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("TeamOut-Retreat-Logistics", version="3.1.0")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("teamout_mcp")

class AmenityRequirement(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    category: Literal["workspace", "connectivity", "lodging", "dining", "recreation"] = Field(
        ...,
        description="Functional amenity category"
    )
    name: str = Field(..., description="Specific amenity requirement (e.g. gigabit_fiber, plenary_room)")
    is_mandatory: bool = Field(default=True, description="Whether amenity is strictly required")

class RetreatSearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    company_name: str = Field(..., min_length=2, description="Target enterprise organization name")
    team_size: int = Field(..., gt=0, le=1000, description="Total headcount attending retreat")
    target_region: str = Field(..., description="Geographic region preference (e.g. Pacific Northwest, Western Alps)")
    max_total_budget_usd: float = Field(..., gt=1000.0, description="Maximum total offsite budget ceiling")
    duration_days: int = Field(default=3, ge=2, le=14, description="Retreat duration in calendar days")
    required_amenities: List[AmenityRequirement] = Field(default_factory=list, description="Mandatory amenities")

    @field_validator("company_name", "target_region")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("String fields cannot be empty or whitespace only")
        return clean

    @model_validator(mode="after")
    def validate_budget_adequacy(self) -> "RetreatSearchRequest":
        per_head = self.max_total_budget_usd / self.team_size
        if per_head < 300.0:
            raise ValueError(f"Budget per attendee (${per_head:.2f}) is below minimum threshold of $300.00/head.")
        return self

class VenueOption(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    venue_id: str = Field(..., description="Unique vetted venue identifier")
    venue_name: str = Field(..., description="Full marketing name of the property")
    location: str = Field(..., description="City and country location")
    estimated_cost_usd: float = Field(..., ge=0.0, description="Total estimated property expense")
    per_attendee_cost_usd: float = Field(..., ge=0.0, description="Cost per attendee")
    wifi_bandwidth_mbps: int = Field(..., ge=50, description="Verified fiber internet download bandwidth")
    match_score: float = Field(..., ge=0.0, le=1.0, description="Heuristic compatibility score")
    breakout_rooms_available: int = Field(..., ge=1, description="Dedicated private conference breakout spaces")

class RetreatSearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["SUCCESS", "NO_VENUES_FOUND"] = Field(..., description="Search execution status")
    query_id: str = Field(..., description="Unique search query trace ID")
    company_name: str = Field(..., description="Requesting enterprise")
    recommended_venues: List[VenueOption] = Field(default_factory=list, description="Ranked venue recommendations")
    estimated_savings_usd: float = Field(..., ge=0.0, description="Projected savings via TeamOut group rates")
    execution_time_ms: float = Field(..., ge=0.0, description="Processing duration in milliseconds")

@mcp.tool()
def search_corporate_retreats(request_json: str) -> str:
    """
    Evaluates retreat venue availability and transit optimization, returning a validated
    Pydantic v2 structured recommendation proposal with verified amenities and budget models.
    """
    start_time = time.time()
    try:
        raw_input = json.loads(request_json)
        req = RetreatSearchRequest.model_validate(raw_input)

        logger.info(f"Processing retreat search for '{req.company_name}' ({req.team_size} attendees) in {req.target_region}")

        # In production, this queries the TeamOut GDS inventory and flight transit API
        per_head = round(req.max_total_budget_usd / req.team_size, 2)
        simulated_cost = round(req.max_total_budget_usd * 0.88, 2)

        options = [
            VenueOption(
                venue_id="VEN-CASCADE-01",
                venue_name="Cascadia Mountain Lodge & Tech Hub",
                location=f"{req.target_region} - Cle Elum, WA",
                estimated_cost_usd=simulated_cost,
                per_attendee_cost_usd=round(simulated_cost / req.team_size, 2),
                wifi_bandwidth_mbps=1000,
                match_score=0.96,
                breakout_rooms_available=6
            )
        ]

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        response = RetreatSearchResponse(
            status="SUCCESS",
            query_id=f"TO-REQ-{int(time.time())}",
            company_name=req.company_name,
            recommended_venues=options,
            estimated_savings_usd=round(req.max_total_budget_usd * 0.12, 2),
            execution_time_ms=elapsed_ms
        )
        return response.model_dump_json(indent=2)

    except Exception as exc:
        logger.error(f"Retreat search execution error: {str(exc)}", exc_info=True)
        return json.dumps({
            "status": "NO_VENUES_FOUND",
            "error_type": exc.__class__.__name__,
            "message": str(exc),
            "execution_time_ms": round((time.time() - start_time) * 1000, 2)
        }, indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Production Docker Compose Stack

Deploy the TeamOut FastMCP logistics engine alongside a Redis cache sidecar:

```yaml
version: "3.8"

services:
  teamout-logistics-engine:
    image: python:3.11-slim-bookworm
    container_name: teamout-fastmcp-engine
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1
      - FASTMCP_PORT=8060
      - TEAMOUT_API_KEY=${TEAMOUT_API_KEY}
      - REDIS_CACHE_URL=redis://teamout-cache:6379/0
    volumes:
      - ./teamout_service:/opt/teamout:ro
      - teamout_proposals:/data/proposals:rw
    working_dir: /opt/teamout
    command: ["python3", "-m", "service.mcp_daemon", "--port", "8060", "--host", "0.0.0.0"]
    ports:
      - "8060:8060"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8060/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    networks:
      - teamout_net

  teamout-cache:
    image: redis:7.4-alpine
    container_name: teamout-redis-cache
    restart: unless-stopped
    volumes:
      - teamout_redis_data:/data
    networks:
      - teamout_net

volumes:
  teamout_proposals:
    driver: local
  teamout_redis_data:
    driver: local

networks:
  teamout_net:
    driver: bridge
```

## Production Hardened Systemd Service Unit

To run the TeamOut FastMCP 3.1 daemon as a background service on a dedicated Linux host:

```ini
# /etc/systemd/system/teamout-mcp.service
[Unit]
Description=TeamOut Retreat Logistics FastMCP 3.1 Gateway Service
Documentation=https://docs.teamout.com/
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=teamout
Group=teamout
WorkingDirectory=/opt/teamout-service
ExecStart=/opt/teamout-service/venv/bin/python -m service.server --port 8060 --host 127.0.0.1
Restart=always
RestartSec=10s

# Process Environment & Security
Environment="PYTHONUNBUFFERED=1"
Environment="FASTMCP_PORT=8060"
EnvironmentFile=/etc/teamout/teamout.env

# Sandboxing
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
NoNewPrivileges=true
ReadWritePaths=/var/log/teamout /data/proposals

# Resource Allocations
LimitNOFILE=65535
MemoryHigh=2G
MemoryMax=3G

[Install]
WantedBy=multi-user.target
```

## Production Diagnostic & Troubleshooting Matrix

| Error Code / Symptom | Root Cause | Diagnostic Verification | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| `HTTP 401 Unauthorized` | Invalid or expired `TEAMOUT_API_KEY` token in service environment. | Run `teamout mcp verify`; check journalctl for authentication rejection. | Regenerate API credentials in TeamOut Enterprise Portal and update `/etc/teamout/teamout.env`. |
| `HTTP 422 Unprocessable Entity` | Budget per head violates minimum threshold ($300/head) in Pydantic validation. | Review server logs for `ValueError: Budget per attendee is below minimum threshold`. | Adjust `max_total_budget_usd` or reduce `team_size` in input payload before re-submitting. |
| `GDS Flight Quote Timeout` | Flight transit query timed out during high-density multi-origin routing. | Journal logs show `TransitGatewayTimeout: Amadeus API latency > 30s`. | Increase API request timeout to 60s or configure origin airport list to major international hubs. |
| `FastMCP Transport Drop` | Standard I/O stream corrupted by unbuffered stdout prints in Python child process. | Client reports `JSONRPCResponseError: Invalid JSON payload received`. | Ensure all non-protocol logging is redirected to `sys.stderr` or file-based logging handlers. |
| `Pydantic ValidationError` | Client submitted invalid keys or extra properties violating strict model schema. | Server logs report `ValidationError: Extra inputs are not permitted`. | Conclude client payload strictly adheres to `RetreatSearchRequest` schema (`extra="forbid"`). |

## Related tools / concepts
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Protocol for connecting AI agents to tools.
- [Pydantic V2](../frameworks/pydantic.md) — Standard schema and validation library for Python.
- [Claude 5.6](../providers/anthropic.md) — Frontier LLM engine powering complex logistics reasoning.
- [Make](../automation_orchestration/make.md) — Visual workflow automation for travel intake forms.
- [Obsidian](../ai_knowledge/obsidian.md) — Documentation store for corporate offsite runbooks.

## Sources / references
- [TeamOut Enterprise Portal](https://app.teamout.com/)
- [TeamOut API Developer Documentation](https://docs.teamout.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
