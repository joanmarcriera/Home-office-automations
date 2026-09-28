# Habitica

## What it is
Habitica is an open-source, gamified task management and habit formation platform that transforms personal productivity into a retro 8-bit role-playing game (RPG). Operating on a flexible Node.js/Express backend with MongoDB storage, Habitica maps real-world habits, daily routines, and to-do items into RPG core loops: completing real-world tasks grants Experience Points (XP), Mana (MP), and Gold (GP), while neglecting daily habits deals damage to the user's Health Points (HP) or party members during multi-player boss quests.

In early 2027 enterprise personal automation and agentic coaching environments, Habitica serves as an active **behavioral incentive engine**. Featuring deep integration with the **Model Context Protocol (FastMCP 3.1)**, Habitica enables autonomous AI coaches—powered by **Claude 5.1**, **Claude 5.6**, **GPT-5.5**, **GPT-5.6**, **Gemini 4.0 Pro/Ultra**, and **Llama 4**—to dynamically analyze task velocity, adjust quest difficulty, auto-generate contextual subtasks, trigger smart home rewards, and orchestrate party strategy based on real-time life analytics.

## What problem it solves
Traditional task managers (such as basic check-lists or standard Kanban boards) suffer from acute "motivation decay"—the psychological drop-off in user engagement once novelty fades:

1. **Lack of Immediate Reinforcement Loops**: Real-world long-term goals (e.g., fitness, language acquisition, homelab refactoring) offer delayed rewards. Habitica bridges this gap by providing micro-dopamine feedback loops (XP, Gold, loot drops, pet hatching) immediately upon task scoring.
2. **Accountability Deficit in Isolated Work**: Individual productivity tools lack collaborative stakes. Habitica's "Party Quests" tie individual task completion directly to team survival: if a party member misses their Dailies, the quest boss inflicts area-of-effect damage on all party members.
3. **Disconnect Between Smart Home Data and Human Behavior**: Smart home hubs (**Home Assistant**) track physical milestones (e.g., exercise bike workouts, room cleaning completion), but lack a unified psychological reward ledger.
4. **Agentic Action Obstacles**: AI personal assistants can generate schedule plans, but lack a structured gamified API to enforce habit compliance and track long-term user momentum.

Habitica resolves these challenges by providing a robust RESTful API (v3/v4), webhook events, and FastMCP 3.1 tool wrappers, turning productivity data into gamified state parameters consumable by human users and AI agents alike.

```mermaid
graph TD
    subgraph Personal Automation & Intelligence Layer
        AI[Autonomous AI Coach / FastMCP 3.1]
        HA[Home Assistant Smart Home Events]
        N8N[n8n Workflow Automation Engine]
    end

    subgraph Habitica Gamified Core (Node.js Container)
        API[Habitica REST API v3 Gateway]
        ENGINE[RPG Game Engine / XP / Gold / HP Calculator]
        QUEST[Party Quest & Boss Battle State Machine]
        HOOK[Webhook Dispatcher]
    end

    subgraph Persistence Layer
        DB[(MongoDB Document Database)]
    end

    subgraph Social & Reward Layer
        PARTY[Habitica Party & Guild Members]
        NOTIF[Matrix / Element / Discord Alerts]
    end

    AI -->|FastMCP Tool: score_task / create_task| API
    HA -->|Gym Session Complete Event| N8N
    N8N -->|HTTP POST /api/v3/tasks/score| API

    API --> ENGINE
    ENGINE --> DB
    ENGINE --> QUEST
    ENGINE --> HOOK

    QUEST -->|Boss Damage Updates| PARTY
    HOOK -->|Level Up / Quest Reward Webhook| NOTIF
```

## Where it fits in the stack
**Category**: Service / Gamified Productivity & Behavioral Incentive.

Habitica operates as the **incentive and behavioral execution layer** of an automated personal management system. It connects raw physical sensors, task queues, and agentic planners with human psychology:

- **Network Topology**: Hosted on public infrastructure (`habitica.com`) or self-hosted via Docker containers on internal homelab networks.
- **Data Integration**: Connects downstream to smart devices via **Home Assistant** and **n8n**, upstream to agentic models (**Claude 5.1**, **GPT-5.5**) via FastMCP 3.1 server sidecars, and outward to messaging tools (**Element**, **Matrix**, **Discord**) via outbound webhooks.
- **State Management**: Consolidates user inventory (gear, potions, eggs, hatches), character stats (Str, Int, Con, Per), task definitions (Habits, Dailies, To-Dos, Rewards), and party quest progress in MongoDB.

```mermaid
sequenceDiagram
    autonumber
    participant SmartHome as Home Assistant / Fitness Sensor
    participant Workflow as n8n Automation Engine
    participant MCP as FastMCP 3.1 Habitica Bridge
    participant Habitica as Habitica REST API v3
    participant Agent as Claude 5.1 Behavioral Coach

    SmartHome->>Workflow: Webhook: "Workout Completed (45 mins)"
    Workflow->>MCP: Trigger Task Score ("workout_daily_id")
    MCP->>Habitica: POST /api/v3/tasks/workout_daily_id/score/up
    Habitica-->>MCP: 200 OK {delta: +15 XP, +2.5 Gold, bossDamage: 45.2}
    MCP->>Agent: Stream Gamified Outcome & Character Health
    Agent->>MCP: call_tool("habitica_cast_skill", {skillId: "fireball"})
    MCP->>Habitica: POST /api/v3/user/class/cast/fireball
    Habitica-->>MCP: 200 OK {mp: -10, partyDamage: 120}
    MCP-->>Agent: Quest Boss Defeated Event
```

## Typical use cases

1. **Automated Fitness & Health Gamification**:
   Linking Home Assistant workout sensors or smartwatch activity metrics to Habitica task completion triggers via n8n, granting instant XP and Gold upon completing physical exercise.

2. **Autonomous AI Habit Coaching via FastMCP 3.1**:
   Deploying an AI agent (Claude 5.1 / GPT-5.5) that monitors daily task completion rates, dynamically adds contextual sub-tasks for missed habits, purchases gear upgrades, and casts class skills during party quests.

3. **Homelab Maintenance Discipline**:
   Converting routine infrastructure maintenance tasks (e.g., verifying backups, applying OS patches, reviewing audit logs) into recurring Habitica "Dailies" with real health penalties if skipped.

4. **Shared Family & Group Accountability**:
   Forming a Habitica "Party" with family members or homelab team members to embark on boss quests where real-world task completion directly damages monsters and earns shared loot.

5. **Financial Savings & Reward Discipline**:
   Linking financial tracking applications (**Actual Budget**) to Habitica Custom Rewards—locking real-world discretionary purchases behind gold earned through completed to-dos.

## Strengths

- **Proven Psychological RPG Loops**: Highly engaging gamification mechanics (classes like Warrior, Mage, Rogue, Healer; pet collection; quest lines; equipment stats).
- **Extensive & Stable REST API (v3)**: Clean RESTful endpoints exposing complete control over tasks, user inventory, party state, skills, and tags.
- **Native Webhook System**: Outbound webhooks trigger immediately on task creation, task scoring, level up, and quest events.
- **Self-Hostable & Open Source**: Full Node.js codebase and MongoDB schemas available for self-hosting on private infrastructure.
- **Ecosystem Interoperability**: First-class integration with n8n, Home Assistant, Node-RED, and FastMCP 3.1 sidecars.

## Limitations

- **Pixel-Art Aesthetic**: The retro pixel-art interface may not suit corporate or ultra-minimalist preference environments.
- **Self-Report Trust Model**: By default, task completion relies on manual checking unless locked behind automated API triggers.
- **Character Class Complexity**: Managing equipment attributes, Mana points, and spell casting adds minor operational overhead compared to bare-bones todo list apps.

## When to use it

- When standard productivity apps fail to maintain user engagement and long-term task consistency.
- When you want to combine smart home automation data with psychological habit incentives.
- When creating automated AI agent workflows that coach users, assign tasks, and manage personal schedules.
- When building team or family productivity games where group accountability drives task completion.

## When not to use it

- For high-stakes enterprise project management requiring Gantt charts, critical path calculations, and formal SLAs (use **OpenProject** or **Jira**).
- When a strictly minimalist, text-only task interface is required (evaluate **Vikunja** or **Todo.txt**).
- For pure expense or financial accounting (use **Actual Budget** or **Firefly III**).

## Getting started

### Enterprise Self-Hosted Docker Compose Setup

While many users utilize the official hosted cloud platform (`habitica.com`), the configuration below deploys a complete local instance of Habitica with MongoDB.

```yaml
version: "3.8"

networks:
  habitica-net:
    driver: bridge

services:
  habitica-db:
    image: mongo:5.0
    container_name: habitica-mongo
    restart: unless-stopped
    volumes:
      - ./mongo-data:/data/db
    networks:
      - habitica-net

  habitica-app:
    image: habitrpg/habitica:latest
    container_name: habitica-app
    restart: unless-stopped
    environment:
      - NODE_ENV=production
      - PORT=3000
      - AMQP_URL=amqp://guest:guest@localhost:5672
      - MONGODB_URI=mongodb://habitica-db:27017/habitica
      - BASE_URL=http://localhost:3000
      - API_CONNECT_TIMEOUT=5000
    ports:
      - "3000:3000"
    depends_on:
      - habitica-db
    networks:
      - habitica-net
```

### API Credentials Retrieval

1. Login to your Habitica account (cloud or local instance).
2. Go to **Settings -> API**.
3. Copy your **User ID** and **API Token**.
4. Pass these values via `x-api-user` and `x-api-key` HTTP request headers.

## CLI examples

```bash
# Verify API connection and retrieve user character stats via cURL
curl -s -H "x-api-user: YOUR_USER_ID" \
        -H "x-api-key: YOUR_API_TOKEN" \
        https://habitica.com/api/v3/user | jq '.data.stats'

# Fetch active Dailies list
curl -s -H "x-api-user: YOUR_USER_ID" \
        -H "x-api-key: YOUR_API_TOKEN" \
        "https://habitica.com/api/v3/tasks/user?type=dailies" | jq '.data[] | {id: .id, text: .text, completed: .completed}'

# Score up a task ("workout") by task ID
curl -s -X POST \
     -H "x-api-user: YOUR_USER_ID" \
     -H "x-api-key: YOUR_API_TOKEN" \
     https://habitica.com/api/v3/tasks/YOUR_TASK_ID/score/up | jq '.data | {delta: .delta, hp: .hp, exp: .exp, mp: .mp, gp: .gp}'

# Cast class skill ("Fireball") on active quest boss
curl -s -X POST \
     -H "x-api-user: YOUR_USER_ID" \
     -H "x-api-key: YOUR_API_TOKEN" \
     https://habitica.com/api/v3/user/class/cast/fireball | jq '.data'
```

## API examples

### FastMCP 3.1 Habitica Server & Pydantic v2 Schema Validation

The following Python script provides a production-ready **FastMCP 3.1** server that wraps Habitica's API. It allows AI agents to query character stats, score tasks, and handle quest strategy with strict **Pydantic v2** validation.

```python
import os
from typing import List, Optional, Dict, Any
import requests
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Habitica-Gamified-Coach", version="3.1.0")

HABITICA_BASE_URL = os.getenv("HABITICA_BASE_URL", "https://habitica.com")
HABITICA_USER_ID = os.getenv("HABITICA_USER_ID", "your-user-id")
HABITICA_API_TOKEN = os.getenv("HABITICA_API_TOKEN", "your-api-token")

# --- Pydantic v2 Data Schemas ---

class CharacterStats(BaseModel):
    hp: float = Field(..., description="Current Health Points")
    max_hp: float = Field(50.0, alias="maxHealth", description="Maximum Health Points")
    mp: float = Field(..., description="Current Mana Points")
    max_mp: float = Field(..., alias="maxMP", description="Maximum Mana Points")
    exp: float = Field(..., description="Current Experience Points")
    to_next_level: float = Field(..., alias="toNextLevel", description="XP required for next level")
    gp: float = Field(..., description="Current Gold balance")
    level: int = Field(..., alias="lvl", description="Character level")
    character_class: str = Field("habitican", alias="class", description="Character class (warrior, mage, rogue, healer)")

class HabiticaTask(BaseModel):
    id: str = Field(..., description="Unique task GUID")
    text: str = Field(..., description="Task title or description")
    task_type: str = Field(..., alias="type", description="Task category: habit, daily, todo, reward")
    completed: Optional[bool] = Field(False, description="Completion status for dailies and todos")
    value: float = Field(0.0, description="Task difficulty score/color scale")
    priority: float = Field(1.0, description="Task priority value (0.1: Trivial, 1.0: Easy, 1.5: Medium, 2.0: Hard)")

class TaskScoreResponse(BaseModel):
    delta: float = Field(..., description="Change in task score value")
    hp: float = Field(..., description="Updated character HP")
    exp: float = Field(..., description="Updated character Experience")
    mp: float = Field(..., description="Updated character Mana")
    gp: float = Field(..., description="Updated character Gold balance")

class HabiticaUserResponse(BaseModel):
    stats: CharacterStats
    tasks: List[HabiticaTask] = Field(default_factory=list)


# --- Helper Headers Function ---

def get_habitica_headers() -> Dict[str, str]:
    return {
        "x-api-user": HABITICA_USER_ID,
        "x-api-key": HABITICA_API_TOKEN,
        "x-client": "FastMCP-3.1-HabiticaAgent"
    }


# --- FastMCP 3.1 Tools ---

@mcp.tool(
    name="habitica_get_character_profile",
    description="Retrieve current character stats (HP, MP, Level, Gold) and active task inventory."
)
def habitica_get_character_profile() -> str:
    """Fetch user character stats from Habitica API."""
    url = f"{HABITICA_BASE_URL}/api/v3/user"
    try:
        resp = requests.get(url, headers=get_habitica_headers(), timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", {})

        # Parse stats via Pydantic v2
        stats_raw = data.get("stats", {})
        stats = CharacterStats.model_validate(stats_raw)

        return f"Character Profile (Level {stats.level} {stats.character_class.capitalize()}):\n" \
               f"HP: {stats.hp:.1f}/{stats.max_hp} | MP: {stats.mp:.1f}/{stats.max_mp}\n" \
               f"XP: {stats.exp:.1f}/{stats.to_next_level} | Gold: {stats.gp:.2f} GP"
    except Exception as err:
        return f"Failed to retrieve character profile: {str(err)}"


@mcp.tool(
    name="habitica_score_task",
    description="Score a habit, daily, or to-do task 'up' (completed/positive) or 'down' (negative habit)."
)
def habitica_score_task(task_id: str, direction: str = "up") -> str:
    """Score a Habitica task up or down."""
    if direction not in ("up", "down"):
        return "Invalid direction. Must be 'up' or 'down'."

    url = f"{HABITICA_BASE_URL}/api/v3/tasks/{task_id}/score/{direction}"
    try:
        resp = requests.post(url, headers=get_habitica_headers(), timeout=10)
        resp.raise_for_status()
        raw_data = resp.json().get("data", {})

        score_data = TaskScoreResponse.model_validate(raw_data)
        return f"Task scored '{direction}' successfully!\n" \
               f"HP: {score_data.hp:.1f} | XP: {score_data.exp:.1f} | GP: {score_data.gp:.2f}"
    except Exception as err:
        return f"Error scoring task {task_id}: {str(err)}"


@mcp.tool(
    name="habitica_create_todo",
    description="Create a new To-Do task with optional priority level."
)
def habitica_create_todo(text: str, priority: float = 1.0, notes: str = "") -> str:
    """Create a new To-Do item in Habitica."""
    url = f"{HABITICA_BASE_URL}/api/v3/tasks/user"
    payload = {
        "text": text,
        "type": "todo",
        "priority": priority,
        "notes": notes
    }
    try:
        resp = requests.post(url, headers=get_habitica_headers(), json=payload, timeout=10)
        resp.raise_for_status()
        created_task = resp.json().get("data", {})
        return f"Successfully created To-Do '{created_task.get('text')}' (ID: {created_task.get('id')})"
    except Exception as err:
        return f"Failed to create task: {str(err)}"


if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts

- [Vikunja](vikunja.md) — Self-hosted task management application for structured, non-gamified Kanban project tracking.
- [Home Assistant](home-assistant.md) — Smart home automation engine for executing real-world task triggers.
- [n8n](n8n.md) — Workflow engine connecting external service events to Habitica API endpoints.
- [Actual Budget](actual-budget.md) — Financial budgeting application for linking real-world rewards to Habitica Gold balances.
- [Element](element.md) — Secure messaging client for receiving party quest notifications and level-up webhooks.
- [Mealie](mealie.md) — Recipe and meal planning tool for tracking nutrition habits.

## Sources / references

- [Official Habitica Platform](https://habitica.com/)
- [Habitica REST API v3 Documentation](https://habitica.com/apidoc/)
- [Habitica GitHub Organization & Source Repositories](https://github.com/HabitRPG/habitica)
- [FastMCP 3.1 & Model Context Protocol Docs](https://modelcontextprotocol.io/protocol/tasks)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
