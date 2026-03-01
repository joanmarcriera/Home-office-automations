# CrewAI

## What it is
CrewAI is an open-source framework for orchestrating role-playing, collaborative AI agents. It allows you to define agents with specific roles, goals, and backstories, then group them into a "crew" to perform complex tasks.

## What problem it solves
It simplifies the creation of multi-agent systems where agents need to collaborate and follow a specific process (sequential, hierarchical, etc.). It manages the communication and task hand-offs between agents automatically.

## Where it fits in the stack
Framework / Multi-Agent Orchestrator

## Typical use cases
- **Content Creation Pipelines**: A writer agent, a researcher agent, and an editor agent working together.
- **Market Analysis**: Agents researching competitors, analyzing trends, and summarizing findings.
- **Automated Support**: Triage agents handing off technical issues to specialist agents.

## Strengths
- **Role-Based Design**: Intuitive way to define agent personas.
- **Flexible Processes**: Supports different workflows (sequential, consensual, hierarchical).
- **Tool Integration**: Built-in support for LangChain tools and custom functions.

## Limitations
- **Token Usage**: Multi-agent loops can quickly consume many tokens.
- **Complexity**: Debugging "agent loop" behavior can be challenging when things go wrong.

## When to use it
- When a task is too complex for a single agent and requires specialized roles.
- When you want a high-level abstraction for agent collaboration.

## When not to use it
- For simple tasks where a single LLM call or a basic chain is enough.
- If you need extremely fine-grained control over the low-level agent communication protocol.

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

```bash
pip install crewai
```

```python
from crewai import Agent, Task, Crew

researcher = Agent(role='Researcher', goal='Find info about {topic}', backstory='Expert analyst')
writer = Agent(role='Writer', goal='Write a post about {topic}', backstory='Professional blogger')

task1 = Task(description='Research the latest trends in {topic}', agent=researcher, expected_output='A list of 5 trends')
task2 = Task(description='Write a 3-paragraph summary of the trends', agent=writer, expected_output='A blog post')

crew = Crew(agents=[researcher, writer], tasks=[task1, task2])
result = crew.kickoff(inputs={'topic': 'AI in 2024'})
print(result)
```

## Related tools / concepts
- [AutoGen](autogen.md)
- [LangChain](../ai_knowledge/langchain.md)
- [Multi-Agent Systems](../../architecture/multi_agent_knowledgeops.md)

## Sources / References
- [Official Website](https://www.crewai.com/)
- [GitHub](https://github.com/joaomdmoura/crewAI)
- [Documentation](https://docs.crewai.com/)

## Contribution Metadata

- Last reviewed: 2026-02-28
- Confidence: high
