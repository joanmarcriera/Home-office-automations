# Habitica

## What it is

Habitica is an open-source habit-building and productivity app that treats your real life like a game. It transforms your daily tasks and habits into RPG quests, rewarding completion with experience points and gold, and penalizing neglect with health loss.

## What problem it solves

Traditional to-do lists often lack the motivation required for long-term habit formation. Habitica solves this by using gamification (rewards, social accountability, and RPG mechanics) to make productivity engaging and fun.

## Where it fits in the stack
**Category**: Service / Productivity. It serves as the **gamified behavioral layer** of the personal organization stack.

## Typical use cases
- Gamified habit tracking and task management.
- Team-based productivity challenges and social accountability.
- Automated habit scoring via API based on external triggers (e.g., GitHub commits).
- Visualizing productivity progress through RPG-style character development.

## Strengths
- **Engaging Gamification**: Highly effective for users motivated by rewards and social mechanics.
- **Robust Community**: Strong social features including parties, guilds, and global challenges.
- **Stable API**: (v3/v4) Allows for deep integration with automation tools and custom clients.
- **Cross-Platform**: Consistent experience across Web, iOS, and Android.

## Limitations
- **Visual Noise**: The RPG interface may be too cluttered for users seeking a minimalist workflow.
- **RPG Distraction**: Game mechanics can occasionally overshadow the actual tasks.
- **Manual Overhead**: Requires consistent manual updates unless heavily automated via API.

## When to use it
- When traditional productivity tools fail to maintain long-term motivation.
- When you enjoy RPG mechanics and want to integrate them into your daily routine.
- For groups or families looking for a shared, gamified productivity experience.

## When not to use it
- For strictly professional project management requiring Gantt charts or complex dependencies.
- If you find RPG elements and "game-like" notifications distracting.
- When a local-first, offline-primary tool is required (Habitica is cloud-sync primary).

## Getting started

Habitica can be used via the web app, mobile apps, or the API. For developers, getting started involves obtaining your User ID and API Token from **Settings > API**.

### Installation (CLI Tool)
You can use the community-maintained CLI to interact with Habitica:
```bash
npm install -g habitica-tools
```

## CLI examples

### Check status
```bash
habitica status
```

### List tasks
```bash
habitica tasks
```

## API examples

### Scoring a task (Python)
```python
import requests

USER_ID = 'your-user-id'
API_TOKEN = 'your-api-token'
TASK_ID = 'your-task-id'

headers = {
    'x-api-user': USER_ID,
    'x-api-key': API_TOKEN
}

# Score up a task
response = requests.post(
    f'https://habitica.com/api/v3/tasks/{TASK_ID}/score/up',
    headers=headers
)
print(response.json())
```

## n8n Integration: Automated Habit Scoring

Habitica can be integrated with [n8n](n8n.md) to automatically score habits based on external events. This allows for "invisible" habit tracking where your character levels up as you perform real-world actions.

### Workflow Pattern: Automated Task Scoring
1.  **Trigger**: Watch for a specific event (e.g., a new row in a Google Sheet, a finished Toggl timer, or a [GitHub](gitea.md) commit).
2.  **HTTP Request Node (Habitica API)**:
    - **Method**: `POST`
    - **URL**: `https://habitica.com/api/v3/tasks/{{$json["task_id"]}}/score/up`
    - **Headers**:
        - `x-api-user`: `{{$env["HABITICA_USER_ID"]}}`
        - `x-api-key`: `{{$env["HABITICA_API_TOKEN"]}}`
3.  **Notification Node**: Send a message to [Element](element.md) or [Home Assistant](home-assistant.md) confirming the XP gain.

## Related tools / concepts
- [SuperBetter](https://www.superbetter.com/) — Alternative gamification framework.
- [Vikunja](vikunja.md) — For managing the tasks that aren't gamified.
- [Mealie](mealie.md) — For nutritional habit tracking and meal planning.
- [Grocy](grocy.md) — For household chore integration and inventory.
- [Home Assistant](home-assistant.md) — For real-life trigger-based scoring.
- [Actual Budget](actual-budget.md) — For financial habit gamification.
- [Authentik](authentik.md) — For managing external access to Habitica data tools.
- [n8n](n8n.md) — For orchestrating complex automated scoring workflows.
- [Element](element.md) — For receiving habit-related notifications.

## Sources / References
- [Official Website](https://habitica.com/)
- [Habitica API Documentation](https://github.com/HabitRPG/habitica/blob/develop/API-reference.md)
- [Habitica Wiki](https://habitica.fandom.com/wiki/Habitica_Wiki)

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
