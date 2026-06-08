# AutoGen Studio

## What it is
AutoGen Studio is a low-code interface built on top of the AutoGen framework. It allows users to rapidly prototype, debug, and deploy multi-agent workflows through a web-based UI.

## What problem it solves
It lowers the barrier to entry for the AutoGen framework by providing a visual way to define agents, their skills, and their interaction patterns. It eliminates the need for complex Python orchestration scripts during the initial design phase of a multi-agent system.

## Where it fits in the stack
**Category**: Frameworks / Agent UI

## Typical use cases
- **Rapid Prototyping**: Quickly testing agent configurations and interaction patterns.
- **Workflow Debugging**: Visualizing agent conversations to identify bottlenecks or logic errors.
- **No-Code Agent Creation**: Allowing non-developers to create and test agent teams.
- **Skill Iteration**: Developing and testing Python functions (skills) that agents can use in real-time.

## Strengths
- **Visual Interface**: Intuitive UI for managing agents and sessions.
- **Skill Management**: Easy way to add and share Python skills among agents.
- **Session History**: Built-in persistence for agent conversations and results.
- **Exportable**: Workflows created in the UI can be exported as JSON for use in production Python scripts.

## Limitations
- **Feature Lag**: New features in the underlying AutoGen framework may take time to appear in the Studio.
- **Scalability**: Primarily designed for prototyping; production deployments usually migrate to pure code or custom APIs.
- **Resource Intensive**: Running the web UI and multiple agents locally can be heavy on system resources.

## When to use it
- For initial experimentation with multi-agent teams.
- When you need a visual way to explain or demonstrate agent behavior to stakeholders.
- For managing a library of reusable agent skills.

## When not to use it
- For production-scale applications requiring high customization and performance.
- In environments where a web-based UI is not permitted or accessible.

## Getting started

Install AutoGen Studio using pip:
```bash
pip install autogenstudio
```

Configure your LLM provider (e.g., OpenAI):
```bash
export OPENAI_API_KEY='your_api_key_here'
```

Launch the interface:
```bash
autogenstudio ui --port 8081
```

**Hello-world example**:
1. Open `http://localhost:8081` in your browser.
2. Navigate to the **Build** tab and create a new **Agent**.
3. Go to the **Playground**, create a new session, and send the message: "Plot a chart of NVDA and TSLA stock price change YTD."
4. Watch as the agents collaborate to write and execute Python code to generate the chart.

## CLI examples
AutoGen Studio provides a simple CLI for managing the web environment.

```bash
autogenstudio ui --port 8081    # Start the UI on a specific port
autogenstudio version           # Check the installed version
autogenstudio --help            # List all available CLI options
```

## API examples
While primarily a UI, you can programmatically run workflows exported from AutoGen Studio using the AutoGen framework.

```python
from autogenstudio import WorkflowManager

# Load a workflow exported as JSON from the Studio UI
workflow_manager = WorkflowManager(workflow="workflow.json")

# Run the workflow with a specific message
task_query = "What is the capital of France?"
workflow_manager.run(message=task_query)
```

## Licensing and cost
- **Open Source**: Yes (MIT).
- **Cost**: Free.
- **Self-hostable**: Yes.

## Related tools / concepts
- [AutoGen](autogen.md)
- [CrewAI](crewai.md)
- [Dify](../ai_knowledge/dify.md)
- [LangGraph](langgraph.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / References
- [Official GitHub](https://github.com/microsoft/autogen/tree/main/samples/apps/autogen-studio)
- [AutoGen Studio Documentation](https://microsoft.github.io/autogen/docs/autogen-studio/usage)

## Contribution Metadata
- Last reviewed: 2026-05-12
- Confidence: high
