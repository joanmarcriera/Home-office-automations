# Habitica

## What it is

Habitica is an open-source habit-building and productivity app that treats your real life like a game. It transforms your daily tasks and habits into RPG quests, rewarding completion with experience points and gold, and penalizing neglect with health loss.

## What problem it solves

Traditional to-do lists often lack the motivation required for long-term habit formation. Habitica solves this by using gamification (rewards, social accountability, and RPG mechanics) to make productivity engaging and fun.

## Where it fits in the stack
**Category**: Service / Productivity

## Typical use cases
- Gamified habit tracking and task management.
- Team-based productivity challenges.
- Automated habit scoring via API.

## Strengths
- Highly engaging gamification mechanics.
- Strong community and social features.
- Robust API for third-party integrations.

## Limitations
- Visual style might be too "noisy" for some users.
- RPG elements can be distracting for pure focus.

## When to use it
- When traditional to-do lists fail to motivate you.
- When you want to combine habit tracking with social accountability.

## When not to use it
- For strictly professional or minimalist project management.
- If you find RPG mechanics distracting.

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

## Related tools / concepts
- [SuperBetter](https://www.superbetter.com/)
- [Vikunja](vikunja.md)
- [Mealie](mealie.md)
- [Grocy](grocy.md)
- [Home Assistant](home-assistant.md)
- [Actual Budget](actual-budget.md)

## Backlog
- API integration for automated habit scoring based on n8n workflows.

## Sources / References
- [Official Website](https://habitica.com/)
- [Habitica API Documentation](https://github.com/HabitRPG/habitica/blob/develop/API-reference.md)
- [SuperBetter](https://www.superbetter.com/)

## Contribution Metadata
- Last reviewed: 2026-07-15
- Confidence: high
