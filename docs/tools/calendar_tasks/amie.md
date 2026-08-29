# Amie

Amie is a high-velocity, design-centric productivity platform that unifies calendar, tasks, and email into a single "joyful" interface. As of early January 2027, it has deepened its integration with frontier models like [Claude 5.6](../ai_knowledge/claude.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md), DeepSeek-V4, Qwen 3.6 VL, and [Gemma 4](../ai_knowledge/local_llms.md) to provide autonomous daily planning, multi-agent scheduling, and proactive time-blocking via the **FastMCP 3.1 Task Protocol**.

## What it is
Amie is an all-in-one AI-powered productivity app that combines your calendar, tasks, and emails into a single, cohesive interface. It focuses on reducing friction in the planning process through natural language and high-performance design.

## What problem it solves
It reduces context-switching by unifying personal and professional scheduling with task management. It addresses "planning fatigue" by using AI to automatically estimate task durations and find optimal slots in the user's schedule without manual intervention.

## Where it fits in the stack
**Calendar & Tasks**. It acts as a unified planning layer for users who want high-speed, integrated task and event management. It sits above the base calendar providers (Google, Outlook) and integrates directly with communication tools like Slack and GitHub.

## Typical use cases
- **AI-Powered Time Blocking**: Automatically scheduling tasks based on priority and typical user behavior patterns.
- **Natural Language Event Creation**: Using the `Cmd + K` palette to create complex events like "Coffee with Alex this Friday at 4pm at Starbucks".
- **Unified Email-to-Task**: Dragging emails onto the calendar to instantly convert them into time-blocked tasks.
- **Agentic Scheduling**: Using [Claude 5.6](../ai_knowledge/claude.md) via FastMCP 3.1 Task Protocol to query availability and propose meeting times to external partners.

## Strengths
- **Frontier AI Integration (Early January 2027)**: Native support for [Claude 5.6](../ai_knowledge/claude.md), GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Qwen 3.6 VL, and [Gemma 4](../ai_knowledge/local_llms.md) for advanced natural language scheduling.
- **Design-First UX**: Extremely polished interface with smooth animations and intuitive keyboard shortcuts.
- **High Performance**: One of the fastest applications in the productivity space for search and event creation.
- **Deep Integrations**: Robust connectors for Jira, GitHub, Slack, and Linear.

## Limitations
- **Proprietary SaaS**: No self-hosting or local-first option; requires full cloud access to calendar/email data.
- **Ecosystem Focus**: Primarily optimized for iOS and macOS; Android support is maturing.
- **API Access**: Public REST API is limited compared to enterprise-grade tools like Airflow or Dagster.

## When to use it
- If you value a premium UI/UX and want AI to handle the manual labor of time-blocking.
- If you want a unified view of tasks, events, and emails without maintaining a complex DIY stack.
- If you are a heavy user of the Apple ecosystem.

## When not to use it
- If you require a privacy-first, offline-only, or self-hosted solution (see [Vikunja](../../services/vikunja.md)).
- If your workflow depends on deep project management features with complex hierarchies (see [Linear](../agents/index.md)).
- If you need a fully open-source stack.

## Getting started
Amie is primarily a web and mobile-based application.

1. Visit [Amie.so](https://www.amie.so/) and sign in with Google or Outlook.
2. Complete the onboarding to sync your primary calendar and task sources.
3. Download the macOS or iOS app for the best experience with keyboard shortcuts.
4. Enable the **AI Planner** in settings to begin using autonomous time-blocking.

## CLI examples
Amie does not provide a traditional command-line binary. However, its "Command Bar" (`Cmd + K`) serves as a functional CLI within the app:

```bash
# Natural Language Commands in Cmd + K
"Plan my week" -> Triggers Gemma 4 / Qwen 3.6 VL to distribute backlog tasks.
"Meet with @Sarah tomorrow" -> Opens a scheduling link for Sarah.
"Remind me to call the bank at 10am" -> Creates a task with a reminder.
```

## API examples
Amie expands its developer access through a limited Beta API and **FastMCP 3.1 Task Protocol** integration.

**Triggering a Task Sync (cURL):**
```bash
curl -X POST "https://api.amie.so/v1/sync" \
  -H "Authorization: Bearer ${AMIE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"source": "github", "scope": "assigned_issues"}'
```

**Querying Availability via FastMCP 3.1 (Claude Desktop / FastMCP Server):**
Amie supports a "Read-Only Calendar" tool for AI agents. The following Python snippet demonstrates how an agentic script validates availability data returned by the Amie FastMCP server using **Pydantic v2**.

```python
import os
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class AvailabilitySlot(BaseModel):
    startTime: datetime = Field(..., description="Start of availability window.")
    endTime: datetime = Field(..., description="End of availability window.")
    status: str = Field(default="FREE", description="Status of the window.")

class AmieAvailabilityResponse(BaseModel):
    timezone: str = Field(default="UTC", description="Target timezone.")
    slots: List[AvailabilitySlot] = Field(..., description="List of free calendar slots.")

def validate_mcp_availability(raw_response: dict) -> AmieAvailabilityResponse:
    """
    Validates calendar availability payload using Pydantic v2.
    """
    try:
        # Programmatic schema enforcement
        validated_data = AmieAvailabilityResponse.model_validate(raw_response)
        print("Successfully validated Amie availability response using Pydantic v2.")
        return validated_data
    except ValidationError as e:
        print("Pydantic validation failed for Amie availability structure:")
        raise e

# Example payload returned by Amie's FastMCP 3.1 server to Claude 5.6
mcp_mock_payload = {
    "timezone": "Europe/London",
    "slots": [
        {
            "startTime": "2027-01-08T09:00:00Z",
            "endTime": "2027-01-08T10:30:00Z",
            "status": "FREE"
        },
        {
            "startTime": "2027-01-08T14:00:00Z",
            "endTime": "2027-01-08T15:00:00Z",
            "status": "FREE"
        }
    ]
}

validate_mcp_availability(mcp_mock_payload)
```

## Related tools / concepts
- [Sunsama](sunsama.md) (Alternative with deeper ritual focus)
- [Akiflow](akiflow.md) (Alternative for heavy task consolidation)
- [Notion Calendar](notion-calendar.md) (Alternative for Notion users)
- [Reclaim.ai](reclaim.md) (Alternative for automated time-blocking)
- [Morgen](morgen.md) (Unified calendar and task manager)
- [Motion](motion.md) (Algorithmic scheduling competitor)
- [SavvyCal](savvycal.md) (Interactive scheduling links)

## Sources / references
- [Amie Official Website](https://www.amie.so/)
- [Amie Help Center & FAQ](https://amie.so/help)
- [AI-Powered Planning Trends](https://www.usecarly.com/blog/best-ai-tools-daily-planning/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
