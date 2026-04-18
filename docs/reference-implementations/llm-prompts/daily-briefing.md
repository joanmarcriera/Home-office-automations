# LLM Prompt: Family Daily Briefing

## Purpose
This prompt is designed to synthesize data from various family services (calendar, tasks, weather) into a concise, encouraging morning briefing. It is intended to be used in an n8n workflow that triggers every morning.

## Prompt Template

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

## Integration Details

### 1. Data Fetching Strategy
- **Google Calendar Node**:
    - **Resource**: Event
    - **Operation**: Get Many
    - **Filter**: Set `Time Min` to `{{ $now.set({ hour: 0, minute: 0, second: 0 }).toISO() }}` and `Time Max` to `{{ $now.set({ hour: 23, minute: 59, second: 59 }).toISO() }}` to fetch only today's events.
- **Vikunja Node**:
    - **Resource**: Task
    - **Operation**: Get Many
    - **Filters**: Filter by `due_date` (today) and `done` (false).
- **OpenWeatherMap Node**:
    - **Resource**: Current Weather or 5-Day Forecast.
    - **Operation**: Get
    - **Location**: Your home city.

### 2. Aggregation & Synthesis
- **Aggregate Node**: Use the **Aggregate** node to combine the arrays of events and tasks into a single object.
- **LLM Node**:
    - **Synthesis**: Pass the aggregated data into this prompt using an LLM node (e.g., Ollama or OpenAI).
- **Delivery**: Send the output to the family Telegram group or via email.

## Sources / References
- [n8n Documentation](https://docs.n8n.io/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high
