# LLM Prompt: Family Daily Briefing

## What it is
The "Family Daily Briefing" is a structured LLM prompt designed to synthesize data from multiple household services into a concise, actionable morning summary. It acts as a personalized "morning news" for the family, delivered via chat or email.

## What problem it solves
Managing a household involves tracking disparate information across calendars, task managers, and weather apps. Checking each individually is time-consuming and often leads to missing important details. This prompt automates the synthesis, highlighting conflicts and priorities in a single, easy-to-read message.

## Where it fits in the stack
This prompt is part of the **AI Service** layer. It is typically executed by an LLM node (like **Ollama**, **GPT-5.5**, or **Claude 4.8**) within an **Orchestration** workflow (n8n), consuming data from the **Productivity** (Calendar/Tasks) and **Environmental** (Weather) layers. Modern integrations utilize the **Model Context Protocol (MCP 3.0)** to provide real-time, secure access to these data sources.

## Typical use cases
- **Morning Routine Automation**: Sending a briefing at 07:00 AM every morning.
- **Conflict Resolution**: Identifying and alerting the family if two members have overlapping commitments.
- **Activity Planning**: Using the weather summary to suggest outdoor vs. indoor activities for the day's tasks.

## Strengths
- **Centralization**: Consolidates multiple data sources into one location.
- **Personalization**: The tone and focus can be adjusted to suit the family's preferences.
- **Context Awareness**: Can correlate tasks with calendar events (e.g., "Don't forget the library books since you are going to the mall nearby").

## Limitations
- **Data Freshness**: Relies on the n8n workflow fetching the latest data at the time of execution.
- **LLM Cost/Latency**: Depending on the model used, there may be a small cost or a few seconds of delay in generating the briefing. Frontier models like **GPT-5.5** or **Claude 4.8** are faster but more expensive.
- **Hallucination Risk**: Small chance of misinterpreting times or priorities if the input data is messy. Local models like **Llama 4 Maverick** can mitigate privacy concerns but may have higher latency on modest hardware.

## When to use it
- When your family uses multiple digital tools to manage life and needs a unified view.
- When you want to gamify or encourage the completion of daily chores.
- To start the day with a "human-like" touch through the inclusion of memories.

## When not to use it
- For families with extremely static schedules that don't change day-to-day.
- If you have concerns about sharing personal calendar data with external LLM providers (use a local [Ollama](../../services/ollama.md) instance instead).
- If your source systems (Calendar/Tasks) are not consistently updated.

## Getting started
To implement the Family Daily Briefing:
1. Ensure your household data sources (Google Calendar, Vikunja, OpenWeatherMap) are accessible via n8n.
2. Use the **Aggregate** node in n8n to combine the data into a single JSON object.
3. Pass this object into the LLM prompt template provided below.

### Prompt Template
```markdown
# Role
You are the "Family Admin Assistant," a helpful, concise, and cheerful AI agent responsible for preparing the morning briefing for the family.

# Context
Today is {{ $today_date }}.
The weather today is {{ $weather_summary }}.

# Input Data
## Calendar Events (Google/Proton Calendar)
{{ $calendar_events }}

## Chores & Tasks (Vikunja/Habitica)
{{ $tasks }}

## "On This Day" Memories (Immich/Paperless)
{{ $memories }}

# Instructions
1. **Greeting**: Start with a warm, brief greeting and a mention of today's date and weather.
2. **Schedule**: Summarize the day's calendar events chronologically. Highlight any potential conflicts or busy periods.
3. **Tasks**: List the top 3-5 priority chores or tasks for today.
4. **Memories**: Briefly mention one "On This Day" memory to start the day with a smile.
5. **Tone**: Keep it helpful, concise, and upbeat. Avoid long-winded explanations.

# Output Format
Markdown-formatted text, suitable for delivery via Telegram or Email.
```

## CLI examples
You can test the synthesis logic using the `ollama` CLI with a local model.

```bash
# Testing the briefing with Ollama and Llama 4 Maverick
ollama run llama-4-maverick "Prepare a family briefing for 2026-06-26. Weather: Sunny, 25C. Tasks: Buy milk, Fix sink. Events: Dentist at 2PM."
```

## API examples
The briefing can be generated via a POST request to an LLM provider's API.

```bash
# Example API call to OpenAI (GPT-5.5) for briefing generation
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-5.5-preview",
    "messages": [
      {"role": "system", "content": "You are a helpful family assistant."},
      {"role": "user", "content": "Synthesis today'\''s data: [JSON DATA HERE]"}
    ]
  }'
```

## Related tools / concepts
- [Google Calendar](../../tools/calendar_tasks/google_calendar.md): Primary data source for the schedule.
- [Vikunja](../../services/vikunja.md): Primary data source for tasks and chores.
- [Habitica](../../services/habitica.md): Gamified task management alternative.
- [Immich](../../services/immich.md): Source for "On This Day" photo memories.
- [Paperless-ngx](../../services/paperless-ngx.md): Source for "On This Day" document memories.
- [n8n](../../services/n8n.md): The workflow engine that runs the entire process.
- [Ollama](../../services/ollama.md): Recommended for private, local execution.
- [MCP](../../tools/automation_orchestration/mcp.md) — Standardized protocol for model-tool interaction.

## Sources / references
- [n8n Documentation](https://docs.n8n.io/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Smart Home Briefing Patterns (GitHub)](https://github.com/n8n-io/n8n/tree/master/packages/nodes-base/nodes/LLM)

## Contribution Metadata
- Last reviewed: 2026-06-26
- Confidence: high
