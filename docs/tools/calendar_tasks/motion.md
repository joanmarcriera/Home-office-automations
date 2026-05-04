# Motion

## What it is
An all-in-one productivity tool that uses AI to build a daily schedule based on your tasks, meetings, and project deadlines.

## What problem it solves
Eliminates the need for manual scheduling by automatically prioritizing tasks and fitting them into your calendar gaps.

## Where it fits in the stack
**Category**: Calendar & Tasks / AI Productivity

## Typical use cases
- Automated daily planning
- Project management integrated with calendar
- Team-wide automated scheduling

## Strengths
- "Intelligent Calendar" that moves tasks automatically when meetings are added
- Integrated task and project management
- Meeting booking links that respect task deadlines

## Limitations
- Higher cost compared to other scheduling tools
- Can feel restrictive if you prefer full manual control

## When to use it
- When you have a high volume of tasks and meetings and lack time to plan
- For teams that want to automate work distribution

## When not to use it
- If you have a simple schedule with few tasks
- If you are on a tight budget

## Getting started

### n8n Automation
Motion provides a public API that allows you to create tasks from external triggers (e.g., a "high priority" email or a new GitHub issue).

**Example: Creating a task via HTTP Request**
- **Endpoint**: `POST https://api.usemotion.com/v1/tasks`
- **Headers**:
  - `X-API-Key`: `YOUR_API_KEY`
  - `Content-Type`: `application/json`
- **Payload**:
```json
{
  "name": "Review Project Proposal",
  "dueDate": "2026-06-05T17:00:00Z",
  "duration": 60,
  "priority": "ASAP",
  "workspaceId": "YOUR_WORKSPACE_ID"
}
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription)
- **Self-hostable**: No

## Related tools / concepts
- [Reclaim.ai](reclaim.md)
- [Akiflow](akiflow.md)
- [Google Calendar](google_calendar.md)
- [Sunsama](sunsama.md)
- [n8n](../../services/n8n.md)

## Sources / References
- [Motion Official Site](https://www.usemotion.com/)
- [Motion API Documentation](https://docs.usemotion.com/)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
