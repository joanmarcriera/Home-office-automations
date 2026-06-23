# Gemini Canvas

## What it is
Gemini Canvas is a collaborative, infinite-workspace interface within the Gemini ecosystem designed for multi-step AI orchestration and visual content creation. By June 2026, it has evolved into a primary interface for **Antigravity Agent** missions, allowing users to coordinate multiple agents on a single persistent, non-linear board.

## What problem it solves
It addresses the "Chat Fatigue" and context-switching overhead of complex, multi-stage projects. Instead of scrolling through long, linear chat histories, Canvas allows users to pin insights, visualize information hierarchies, and transform raw data into interactive widgets. It provides a visual "Working Memory" for both humans and AI agents.

## Where it fits in the stack
**AI Assistants & Knowledge / Workspace Orchestration**. It functions as the UI layer for the [Antigravity Agent](antigravity-agent.md) platform, sitting above the [Gemini](../ai_knowledge/gemini.md) model layer.

## Typical use cases
- **Multi-Source Research**: Aggregating information from [Google Search](google-search.md) into categorized blocks on a visual workspace.
- **Agentic Mission Control**: Coordinating multiple [Antigravity Agents](antigravity-agent.md) to complete complex research or engineering tasks.
- **Interactive Dashboard Creation**: Generating functional web-based widgets and data visualizations directly on the canvas.
- **Visual Brainstorming**: Converting text-heavy reports into flowcharts, infographics, and mind maps.
- **Educational Course Builder**: Organizing complex topics into interactive, visual learning paths.

## Strengths
- **Non-Linear Workspace**: Infinite board allows for spatial organization of information, improving human cognitive load.
- **Native Antigravity Integration**: (June 2026) Seamlessly deploy and monitor autonomous agents within the canvas environment.
- **Real-time Collaboration**: Multiple humans and agents can work on the same canvas simultaneously.
- **Component Generation**: Direct creation of HTML/JS/React widgets (e.g., "Build a project timeline component here").
- **Persistent Context**: The entire canvas acts as a 2M+ token context window for the underlying Gemini models.

## Limitations
- **Ecosystem Lock-in**: Deepest integration is limited to Google Workspace and Google Cloud services.
- **Mobile Experience**: The infinite-canvas paradigm is primarily optimized for desktop/tablet use and can be difficult to navigate on small screens.
- **Learning Curve**: Mastering the visual orchestration of multiple agents requires more effort than simple chat.

## When to use it
- For complex, long-running projects that involve multiple data sources and agentic tasks.
- When you need to visualize data or information hierarchies that are poorly served by linear text.
- When collaborating with a team (human or AI) on research, planning, or content creation.

## When not to use it
- For simple, one-off questions that can be answered in a standard chat interface.
- If you require a fully local, air-gapped solution (use [Open WebUI](../../services/open-webui.md) with local models).
- For text-only writing tasks where a standard document editor (like [Google Docs](google-docs.md)) is more appropriate.

## Getting started
1. **Access**: Open Gemini Canvas from the [Gemini Web Interface](https://gemini.google.com/canvas).
2. **Create Workspace**: Start a new "Mission" or "Project Board".
3. **Add Blocks**: Use the "Add" button or slash commands to insert text, images, or interactive components.
4. **Deploy Agents**: Use the Antigravity sidebar to spawn agents and assign them to specific blocks or tasks on the canvas.

## CLI examples
While primarily a GUI, Gemini Canvas can be interacted with via the Antigravity CLI (v2026.4.x):

```bash
# List active canvas workspaces
antigravity canvas list

# Export a specific canvas block to Markdown
antigravity canvas export --id block_123 --format markdown

# Trigger an agent mission on a specific canvas
antigravity mission start --canvas "Research Project A" --goal "Summarize block 456"
```

## API examples
### Python: Canvas Orchestration (Vertex AI)
```python
from google.cloud import aiplatform

# Initialize a Canvas mission programmatically
mission = aiplatform.CanvasMission(
    display_name="Market Analysis 2026",
    workspace_id="ws_789"
)

# Add a block with data
mission.add_block(
    content="Initial research findings on Blackwell GPUs...",
    block_type="text"
)

# Assign an agent to the mission
mission.assign_agent(agent_type="researcher", focus="competitive-landscape")
```

## Related tools / concepts
- [Gemini](../ai_knowledge/gemini.md)
- [Antigravity Agent](antigravity-agent.md)
- [Google Search](google-search.md)
- [NotebookLM](notebooklm.md)
- [Claude Artifacts](../ai_knowledge/claude.md)
- [ChatGPT Canvas](chatgpt.md)
- [Open WebUI](../../services/open-webui.md)
- [Learning Map](../../knowledge_base/learning-map.md)
- [Infinite Canvas Patterns](../../knowledge_base/patterns/infinite-canvas.md)

## Sources / References
- [Google Gemini Blog: Announcing Canvas](https://blog.google/technology/ai/google-gemini-canvas-update/)
- [Antigravity Agent Mission Guide](https://ai.google.dev/gemini-api/docs/antigravity)
- [Gemini 3.5 Capability Summary](https://ai.google.dev/gemini-api/docs/models/gemini)
- [Infinite Canvas Design Patterns](https://canvas.google.design/patterns)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
