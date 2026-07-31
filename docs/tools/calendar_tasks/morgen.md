# Morgen

## What it is
Morgen is a cross-platform calendar, task manager, and meeting scheduler that aggregates all your calendars into one place. It is built as a unified interface for managing multiple scheduling providers, including Google, Outlook, iCloud, Exchange, and CalDAV.

In the late October / November 2026 AI orchestration landscape, Morgen is widely utilized as a unified calendar and task hub that can be controlled by autonomous AI agents (such as Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, and Qwen 3.6). By acting as a single gateway to fragmented calendars, Morgen simplifies the tool definitions needed for agentic schedule planning and time-blocking.

## What problem it solves
It eliminates the "multiple calendar" problem by consolidating disparate scheduling sources into a single, cohesive interface on desktop and mobile. It also addresses the friction of scheduling meetings by providing integrated scheduling links and allowing users to time-block tasks directly onto their calendar.

Furthermore, it simplifies agentic tool use. Instead of writing custom calendar synchronization and scheduling modules for Google Calendar, Outlook, and self-hosted CalDAV instances separately, developers and AI agents can target Morgen's unified, developer-friendly local and cloud APIs.

## Where it fits in the stack
**Category**: Calendar & Tasks / Unified Scheduling. It serves as the primary daily scheduling interface for users who operate across multiple ecosystems (e.g., a mix of Windows, macOS, and Linux).

## Typical use cases
- **Unified Personal and Work Scheduling**: Viewing an iCloud personal calendar alongside a corporate Exchange calendar.
- **Task Time-Blocking**: Syncing tasks from providers like Todoist or Microsoft To-Do and dragging them into calendar slots.
- **Meeting Scheduling**: Creating and sharing scheduling links that automatically respect the availability across all connected calendars.
- **CalDAV Management**: Providing a modern UI for self-hosted calendars like [Radicale](../../services/radicale-automation.md).
- **Agentic Schedule Planning**: Enabling an AI agent to inspect availability across Google and Exchange calendars via the Morgen API, negotiate times, and block slots for work.

## Strengths
- **Broad Provider Support**: One of the few modern apps with robust support for iCloud, Exchange, and CalDAV simultaneously.
- **Cross-Platform**: Native applications for Windows, macOS, Linux, iOS, and Android.
- **Privacy-Conscious**: Offers local-only calendar options and clear data handling policies.
- **Integrated Scheduling**: Combines calendar management with meeting links and task time-blocking in one app.

## Limitations
- **Subscription Required**: Advanced features, such as multiple scheduling links and deep task integrations, require a paid plan.
- **No Web Interface**: Unlike competitors, Morgen focuses on native apps, which may be a limitation for users who cannot install software on certain machines.
- **UI Density**: The interface can become crowded when many calendars and tasks are displayed at once.

## When to use it
- If you use a mix of operating systems and need a high-quality, unified calendar app that works everywhere.
- If you need to manage self-hosted CalDAV servers alongside standard cloud providers.
- If you want an all-in-one tool for scheduling meetings, managing tasks, and viewing your calendar.
- When configuring AI-driven time-blocking workflows across diverse calendar systems.

## When not to use it
- If you only use a single calendar provider (e.g., only Google Calendar) and don't need task integration.
- If you prefer a web-based scheduling workflow without installing local applications.
- If you require a purely open-source solution for your calendar management.

## Getting started

### Installation
Download the Morgen application for your platform from the [official website](https://www.morgen.so/download).

**macOS (Homebrew)**
```bash
brew install --cask morgen
```

**Linux (AppImage/Deb/RPM)**
Morgen provides native packages for most Linux distributions.

```bash
# Example for Debian/Ubuntu
sudo dpkg -i morgen-*.deb
```

### Connecting Calendars
1. Launch Morgen and follow the setup wizard.
2. Select your providers (Google, Outlook, iCloud, etc.).
3. For CalDAV (e.g., Radicale or Nextcloud), select "CalDAV" and provide your server URL, username, and password.

### Setting up Scheduling Links
- Navigate to the "Scheduling" tab (calendar icon with a link).
- Create a new "Booking Page" or "Quick Meeting".
- Customize your availability and share the generated link.

## CLI examples
While Morgen is primarily a GUI-driven application, the desktop app can be controlled via CLI on some platforms or interacted with through local protocols.

```bash
# Check if Morgen is running on macOS
pgrep Morgen

# Open Morgen to a specific date (Deep link example)
open "morgen://calendar/2026-11-05"
```

## API examples

### Creating a Task
```bash
: "${MORGEN_API_KEY:?set your Morgen API key}"

curl -X POST https://api.morgen.so/v3/tasks/create \
  -H "Authorization: ApiKey $MORGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review Daily Knowledge Expansion PR",
    "description": "Ensure all code examples are runnable.",
    "priority": 1,
    "dueDate": "2026-11-05"
  }'
```

### Programmatic Task Validation with Pydantic v2 (Python)
Validating payloads programmatically before calling the Morgen API.

```python
import os
import requests
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class MorgenTaskPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(..., description="Task title", min_length=1)
    description: Optional[str] = Field(default=None, description="Detailed task description")
    priority: int = Field(default=2, description="Task priority (1=high, 2=medium, 3=low)", ge=1, le=3)
    due_date: Optional[date] = Field(default=None, alias="dueDate")

    @field_validator("due_date")
    @classmethod
    def validate_future_date(cls, v: Optional[date]) -> Optional[date]:
        if v and v < date.today():
            raise ValueError("Due date cannot be in the past")
        return v

# Example usage validating a payload
try:
    payload = MorgenTaskPayload(
        title="Audit Morgen Documentation",
        description="Verify 13 section standards and references.",
        priority=1,
        dueDate="2026-11-05"
    )
    print("Validated Payload:", payload.model_dump(by_alias=True))

    # Send to Morgen API
    api_key = os.environ.get("MORGEN_API_KEY")
    if api_key:
        response = requests.post(
            "https://api.morgen.so/v3/tasks/create",
            headers={"Authorization": f"ApiKey {api_key}", "Content-Type": "application/json"},
            json=payload.model_dump(by_alias=True)
        )
        print("API Response:", response.json())
except Exception as e:
    print("Validation or API error:", e)
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Basic version is free; Pro features require a subscription).
- **Self-hostable**: No (Cloud-based service with native clients).

## Related tools / concepts
- [Akiflow](akiflow.md) (Task-focused command center alternative)
- [Fantastical](fantastical.md) (Calendar-centric alternative)
- [Calendly](calendly.md) (Specialized scheduling links)
- [Radicale](../../services/radicale-automation.md) (Self-hosted CalDAV backend)
- [Nextcloud](../intake_storage/caldav.md) (Self-hosted cloud with calendar support)
- [Todoist](todoist.md) (Task integration source)
- [Microsoft To-Do](microsoft-todo.md) (Task integration source)
- [CalDAV](../intake_storage/caldav.md) (Underlying protocol)
- [Homebox](../../services/homebox.md) (Inventory management often used in parallel)

## Sources / References
- [Morgen Official Site](https://www.morgen.so/)
- [Morgen Help Center](https://morgen.notion.site/Morgen-Help-Center-885474c3e86c4a85a4f66453f6316278)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
