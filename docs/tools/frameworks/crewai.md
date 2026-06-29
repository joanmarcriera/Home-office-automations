# CrewAI

## What it is
CrewAI is an open-source framework for orchestrating role-playing, collaborative AI agents. It allows you to define agents with specific roles, goals, and backstories, then group them into a "crew" to perform complex tasks using structured processes.

## What problem it solves
It simplifies the creation of multi-agent systems where agents need to collaborate and follow a specific workflow (sequential, hierarchical, consensual). It manages the communication, task hand-offs, and shared context between agents automatically.

## Where it fits in the stack
**Framework / Multi-Agent Orchestrator**. It sits at the top of the agentic stack, coordinating multiple specialized models (like Claude 4.8 and GPT-5.5) to achieve high-level objectives.

## Typical use cases
- **Content Creation Pipelines**: A writer agent, a researcher agent, and an editor agent working together.
- **Market Analysis**: Agents researching competitors, analyzing trends, and summarizing findings.
- **Automated Support**: Triage agents handing off technical issues to specialist agents.
- **Complex Software Development**: Coordinating architect, coder, and tester agents.

## Strengths
- **Role-Based Design**: Intuitive way to define agent personas with backstories and goals.
- **Flexible Processes**: Supports different workflows including `Process.sequential`, `Process.hierarchical`, and `Process.consensual`.
- **Sophisticated Memory**: Integrated short-term, long-term, and entity memory systems.
- **Task Delegation**: Built-in mechanisms for agents to delegate sub-tasks to other crew members.
- **Self-Correction**: Agents can learn from past executions and improve their performance over time.
- **MCP 3.0 Support**: Native integration with the Model Context Protocol for tool discovery and cross-agent resource sharing.

## Limitations
- **Token Usage**: Multi-agent loops and hierarchical reviews can quickly consume many tokens.
- **Complexity**: Debugging "agent loop" behavior or emergent collaboration failures can be challenging.
- **Latency**: Multiple agents working in sequence or hierarchy increases the total time to result.

## When to use it
- When a task is too complex for a single agent and requires specialized roles.
- When you want a high-level abstraction for agent collaboration without writing the low-level communication logic.
- For building systems that require persistent "corporate memory" across multiple runs.

## When not to use it
- For simple tasks where a single LLM call or a basic chain is enough.
- If you need extremely fine-grained control over the raw communication protocol.
- When latency is the most critical factor and serial agent steps are prohibitive.

## Getting started

### Installation
```bash
pip install crewai
```

### Minimal Python Example
```python
from crewai import Agent, Task, Crew

# Define agents
researcher = Agent(role='Researcher', goal='Find info about {topic}', backstory='Expert analyst')
writer = Agent(role='Writer', goal='Write a post about {topic}', backstory='Professional blogger')

# Define tasks
task1 = Task(description='Research the latest trends in {topic}', agent=researcher, expected_output='A list of 5 trends')
task2 = Task(description='Write a 3-paragraph summary of the trends', agent=writer, expected_output='A blog post')

# Kickoff the crew
crew = Crew(agents=[researcher, writer], tasks=[task1, task2])
result = crew.kickoff(inputs={'topic': 'AI in 2026'})
print(result)
```

## CLI examples

```bash
# Creating a new crewAI project template
crewai create crew my_new_crew

# Running a crewAI project from the CLI
crewai run

# Training the crew with specific feedback
crewai train -n 5
```

## API examples

### Hierarchical Process with Claude 4.8
```python
from crewai import Crew, Process
from langchain_anthropic import ChatAnthropic

# Configure a crew with a hierarchical process overseen by Claude 4.8
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.hierarchical,
    manager_llm=ChatAnthropic(model="claude-4-8-opus-20260528"),
    memory=True,
    cache=True
)

result = crew.kickoff()
```

### Custom Tool Integration
```python
from crewai_tools import BaseTool

class MyCustomTool(BaseTool):
    name: str = "My Tool"
    description: str = "Clear description of what this tool does"

    def _run(self, argument: str) -> str:
        # Implementation of the tool logic
        return f"Tool processed: {argument}"

# Assign to agent
agent = Agent(
    role='Specialist',
    goal='Process data',
    backstory='Data analyst',
    tools=[MyCustomTool()]
)
```

## Related tools / concepts
- [AutoGen](autogen.md)
- [LangChain](../../tools/ai_knowledge/langchain.md)
- [LangGraph](./langgraph.md)
- [Multi-Agent Systems](../../architecture/multi_agent_knowledgeops.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Claude Code Router](../development_ops/claude-code-router.md)
- [Smolagents](smolagents.md)
- [Plandex](../development_ops/plandex.md)
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md)

## Sources / references
- [Official Website](https://www.crewai.com/)
- [GitHub](https://github.com/joaomdmoura/crewAI)
- [Documentation](https://docs.crewai.com/)
- [CrewAI 2026 Enterprise Features](https://www.crewai.com/enterprise)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
