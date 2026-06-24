# TeamOut

## What it is
TeamOut is an AI-native platform designed for the end-to-end planning and logistics of company retreats, offsites, and corporate events. It utilizes specialized agents to automate venue sourcing, budget management, and itinerary generation.

## What problem it solves
Planning large-scale corporate events is traditionally a manual, months-long process involving thousands of emails. TeamOut reduces this to minutes by using AI to match company requirements (budget, team size, activities) with a global database of retreat-vetted venues.

## Where it fits in the stack
**AI & Knowledge / Agents**. It is a verticalized AI agent specialized in the corporate travel and logistics domain.

## Typical use cases
- **Automated Venue Sourcing**: Finding retreats that specifically accommodate 50+ people with high-speed internet and breakout rooms.
- **Budget Optimization**: Iteratively testing different dates and locations to find the most cost-effective offsite.
- **Team Sentiment Analysis**: Synthesizing survey data from employees to automatically recommend activities (e.g., hiking vs. workshops).

## Strengths
- **Domain-Specific Logic**: Unlike general-purpose agents, TeamOut is pre-trained on travel logistics and corporate venue data.
- **Workflow Integration**: Integrates directly with Slack and Google Calendar for team coordination.
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
pip install teamout-sdk
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
teamout export --retreat-id R_12345 --format json

# List all active retreat projects
teamout projects list
```

## API examples

### Programmatic Retreat Request
Using the SDK to trigger a search from a custom agent (e.g., a Claude 4.8-based assistant).

```python
from teamout import TeamOutClient

client = TeamOutClient(api_key="TO_SEC_XYZ")

# Request a venue search for a 25-person team in Portugal
retreat = client.search_venues(
    team_size=25,
    location="Portugal",
    budget_cap=35000,
    requirements=["meeting-rooms", "beach-access"]
)

for venue in retreat.recommendations:
    print(f"Found: {venue.name} - Score: {venue.match_score}%")
```

## Related tools / concepts
- [AI Agents](../agents/index.md)
- [ChatGPT](./chatgpt.md)
- [Claude 4.8](../providers/anthropic.md)
- [GPT-5.5](openai.md)
- [Event Management Automation](../automation_orchestration/index.md)
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md)
- [LangChain](./langchain.md)

## Sources / references
- [Official TeamOut AI Page](https://app.teamout.com/ai)
- [TeamOut API Documentation (Preview)](https://docs.teamout.com/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
