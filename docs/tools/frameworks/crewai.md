# CrewAI

## What it is
CrewAI is an open-source framework for orchestrating role-playing, collaborative AI agents. It allows you to define agents with specific roles, goals, and backstories, then group them into a "crew" to perform complex tasks using structured processes. As of early 2027, **CrewAI Enterprise & Core v1.42+** has introduced deep native integration with **FastMCP 3.1** servers, multi-modal **Gemma 4** execution loops, and robust self-healing workflows driven by frontier models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4.

## What problem it solves
It simplifies the creation of multi-agent systems where agents need to collaborate and follow a specific workflow (sequential, hierarchical, consensual). It manages the communication, task hand-offs, and shared context between agents automatically. CrewAI eliminates the complex boilerplate of managing thread concurrency, task hand-offs, and short/long-term memory sync across multi-agent boundaries.

## Where it fits in the stack
**Framework / Multi-Agent Orchestrator**. It sits at the top of the agentic stack, coordinating multiple specialized models (like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Llama 4 Maverick) to achieve high-level objectives.

## Typical use cases
- **Content Creation Pipelines**: A writer agent, a researcher agent, and an editor agent working together.
- **Market Analysis**: Agents researching competitors, analyzing trends, and summarizing findings.
- **Automated Support**: Triage agents handing off technical issues to specialist agents.
- **Complex Software Development**: Coordinating architect, coder, and tester agents using software factory patterns.

## Strengths
- **Role-Based Design**: Intuitive way to define agent personas with backstories and goals.
- **Flexible Processes**: Supports different workflows including `Process.sequential`, `Process.hierarchical`, and `Process.consensual`.
- **Sophisticated Memory**: Integrated short-term, long-term, and entity memory systems.
- **Task Delegation**: Built-in mechanisms for agents to delegate sub-tasks to other crew members.
- **Self-Correction**: Agents can learn from past executions and improve their performance over time.
- **MCP 3.1 Support**: Native, fast-multiplexing integration with Model Context Protocol (MCP 3.1 / FastMCP 3.1) servers for rapid tool discovery and resource binding.

## Limitations
- **Token Usage**: Multi-agent loops and hierarchical reviews can quickly consume many tokens, requiring careful planning.
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
pip install crewai pydantic
```

### Minimal Python Example
```python
from crewai import Agent, Task, Crew
from pydantic import BaseModel, Field

# Define expected output schema using Pydantic v2
class ResearchReport(BaseModel):
    topic: str = Field(..., description="The main topic of research")
    key_findings: list[str] = Field(..., description="List of key findings or trends")
    summary: str = Field(..., description="A 3-paragraph executive summary")

# Define agents
researcher = Agent(
    role='Researcher',
    goal='Find info about {topic}',
    backstory='Expert analyst with access to the latest search databases'
)
writer = Agent(
    role='Writer',
    goal='Write a post about {topic}',
    backstory='Professional tech blogger'
)

# Define tasks with Pydantic v2 output validation
task1 = Task(
    description='Research the latest trends in {topic}',
    agent=researcher,
    expected_output='A list of 5 trends'
)
task2 = Task(
    description='Write a 3-paragraph summary of the trends',
    agent=writer,
    output_json=ResearchReport,  # Strict Pydantic v2 validation
    expected_output='A fully validated ResearchReport JSON'
)

# Kickoff the crew
crew = Crew(agents=[researcher, writer], tasks=[task1, task2])
result = crew.kickoff(inputs={'topic': 'AI in late 2026'})
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

### Hierarchical Process with Claude 5.1
```python
from crewai import Crew, Process
from langchain_anthropic import ChatAnthropic

# Configure a crew with a hierarchical process overseen by Claude 5.1
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.hierarchical,
    manager_llm=ChatAnthropic(model="claude-5-1-opus-202611"),
    memory=True,
    cache=True
)

result = crew.kickoff()
```

### Custom Tool Integration with Pydantic v2 Validation
```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, ValidationError

class ToolInputSchema(BaseModel):
    argument: str = Field(..., min_length=3, description="A non-empty string argument to process")

class MyCustomTool(BaseTool):
    name: str = "My Custom Validator Tool"
    description: str = "Processes raw input using strict Pydantic validation"
    args_schema: type[BaseModel] = ToolInputSchema

    def _run(self, argument: str) -> str:
        # Runtime validation and execution
        try:
            validated = ToolInputSchema(argument=argument)
            return f"Tool processed: {validated.argument}"
        except ValidationError as e:
            return f"Validation error occurred: {str(e)}"

# Assign to agent
agent = Agent(
    role='Specialist',
    goal='Process data',
    backstory='Data analyst',
    tools=[MyCustomTool()]
)
```

### MCP 3.1 / FastMCP 3.1 Server Integration
CrewAI native support for connecting to high-performance FastMCP servers.
```python
from crewai.tools import MCPTool

# Programmatic extraction of tools from an active FastMCP 3.1 server
mcp_tool = MCPTool(
    server_url="http://localhost:8000/mcp",
    tool_name="retrieve_knowledge_graph"
)

agent = Agent(
    role='MCP Integration Engineer',
    goal='Retrieve and synthesize graph databases',
    backstory='Expert in Model Context Protocol systems',
    tools=[mcp_tool]
)
```

## Related tools / concepts
- [AutoGen](autogen.md)
- [LangChain](../../tools/ai_knowledge/langchain.md)
- [LangGraph](./langgraph.md)
- [Multi-Agent Systems](../../architecture/multi_agent_knowledgeops.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Smolagents](smolagents.md)
- [PydanticAI](pydantic-ai.md)
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md)

## Sources / references
- [Official Website](https://www.crewai.com/)
- [GitHub](https://github.com/joaomdmoura/crewAI)
- [Documentation](https://docs.crewai.com/)
- [CrewAI late 2026 Enterprise Features](https://www.crewai.com/enterprise)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
