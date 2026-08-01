# Habitica

Habitica is an open-source habit-building and productivity app that treats your real life like a game. It transforms your daily tasks and habits into RPG quests, rewarding completion with experience points and gold, and penalizing neglect with health loss.

## What it is
Habitica is a gamified task management platform that leverages RPG mechanics (Experience, Gold, Health, Pets, and Quests) to motivate users toward habit formation and goal completion. In late October / November 2026, it has evolved into a primary target for agentic habit coaching, with native support for the Model Context Protocol (MCP 3.1 / FastMCP 3.1).

## What problem it solves
Traditional productivity tools often suffer from "motivation decay." Habitica solves this by applying game theory to real-world tasks, providing immediate feedback loops through virtual rewards and social accountability (Parties and Guilds), which are essential for long-term behavior change.

## Where it fits in the stack
**Category**: Service / Gamified Productivity. It serves as the **incentive layer** for the personal automation stack, bridging the gap between raw data (e.g., from Home Assistant or n8n) and psychological reward.

## Typical use cases
- **Gamified Habit Formation**: Tracking daily routines like exercise, meditation, or hydration.
- **Agentic Coaching**: Using Gemma 3, Claude 5.1, or GPT-5.5 to analyze task completion patterns and suggest quest strategies.
- **Automated Reward Systems**: Linking smart home completions (e.g., finishing a workout on a Peloton) to Habitica XP gain via FastMCP 3.1.
- **Social Productivity**: Collaborating with a "Party" to defeat bosses by completing real-world tasks.

## Strengths
- **Proven Gamification**: Deeply integrated RPG mechanics that provide genuine dopamine hits.
- **Robust API**: Stable v3/v4 API with extensive documentation and community wrappers.
- **Extensibility**: Native integration with n8n, Zapier, and now FastMCP 3.1 for agentic interaction.
- **Cross-Platform**: Seamless sync between Web, iOS, and Android clients.

## Limitations
- **Visual Noise**: The pixel-art RPG aesthetic can be distracting for users preferring minimalist interfaces.
- **Self-Report Bias**: Relies on user honesty unless integrated with automated triggers.
- **Learning Curve**: Managing equipment, skills, and quests adds overhead compared to simple to-do lists.

## When to use it
- When you struggle with the "boredom" of standard to-do lists.
- When you want to gamify your self-improvement journey with friends or family.
- When you need a productivity tool that offers a robust API for automation.

## When not to use it
- For high-stakes corporate project management where RPG elements are inappropriate.
- If you find pixel art or "gaming" terminology (XP, HP, Mana) confusing or annoying.

## Getting started
To begin, create an account at [Habitica.com](https://habitica.com/). Developers should navigate to **Settings > API** to retrieve their `User ID` and `API Token`.

### Integration with Gemma 3
To use Habitica with Gemma 3, Claude 5.1, or GPT-5.5, install the `habitica-mcp` server:
```bash
npm install -g @habitica/mcp-server
# Add to your Agent config
{
  "mcpServers": {
    "habitica": {
      "command": "habitica-mcp",
      "env": {
        "HABITICA_USER_ID": "your-id",
        "HABITICA_API_TOKEN": "your-token"
      }
    }
  }
}
```

## CLI examples

### Official/Community CLI
The community CLI provides quick access to your tasks.
```bash
# Installation
npm install -g habitica

# Check status and stats
habitica stats

# List active Dailies
habitica list dailies
```

### Direct API via Curl
```bash
# Score up a task
curl -X POST "https://habitica.com/api/v3/tasks/TASK_ID/score/up" \
     -H "x-api-user: YOUR_USER_ID" \
     -H "x-api-key: YOUR_API_TOKEN"
```

## API examples

### Python (Scoring a task with Pydantic v2 Validation)
The following script utilizes **Pydantic v2** to validate payloads and structures before invoking the Habitica API, ensuring safety and data integrity when driven by frontier models (Claude 5.1, GPT-5.5, Gemini 4.0).

```python
import requests
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any

class HabiticaTaskScore(BaseModel):
    user_id: str = Field(..., description="The user's unique Habitica ID")
    api_token: str = Field(..., description="The user's Habitica API Token")
    task_id: str = Field(..., description="The ID of the task to be scored")
    direction: str = Field(default="up", description="The score direction ('up' or 'down')")

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, v: str) -> str:
        if v not in ("up", "down"):
            raise ValueError("direction must be 'up' or 'down'")
        return v

class HabiticaResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

def score_task(config: HabiticaTaskScore) -> HabiticaResponse:
    url = f"https://habitica.com/api/v3/tasks/{config.task_id}/score/{config.direction}"
    headers = {
        "x-api-user": config.user_id,
        "x-api-key": config.api_token
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        raw_data = response.json()
        return HabiticaResponse(success=raw_data.get("success", False), data=raw_data.get("data"))
    except Exception as e:
        return HabiticaResponse(success=False, error=str(e))

# Example usage:
# task_config = HabiticaTaskScore(user_id="my-id", api_token="my-token", task_id="habit-123")
# result = score_task(task_config)
# print(result.success)
```

### n8n Workflow Integration
Habitica is a first-class citizen in [n8n](n8n.md). A common pattern is:
1. **Trigger**: [Home Assistant](home-assistant.md) detects a "Gym Session Complete" event.
2. **HTTP Request**: POST to `https://habitica.com/api/v3/tasks/:id/score/up`.
3. **Notification**: Send a message to [Element](element.md) with the XP earned.

## Related tools / concepts
- [SuperBetter](https://www.superbetter.com/) — Scientific gamification.
- [Vikunja](vikunja.md) — For professional task management.
- [Mealie](mealie.md) — Gamifying nutritional habits.
- [Home Assistant](home-assistant.md) — For automating real-world task triggers.
- [n8n](n8n.md) — For orchestrating complex habit workflows.
- [Actual Budget](actual-budget.md) — Gamifying financial discipline.
- [Element](element.md) — For receiving habit notifications and party chats.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — For agentic coaching and strategy in late 2026.
- [Claude 5.1](../tools/ai_knowledge/claude.md) — For advanced behavior analysis.
- [GPT-5.5](../tools/providers/huggingface.md) — For generating habit recommendation plans.

## Sources / references
- [Official Habitica Website](https://habitica.com/)
- [Habitica API Reference](https://github.com/HabitRPG/habitica/blob/develop/API-reference.md)
- [Habitica Wiki](https://habitica.fandom.com/wiki/Habitica_Wiki)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-11-12
- Confidence: high
