# AG2 (formerly AutoGen)

## What it is
AG2 is the next-generation evolution of the AutoGen framework. It is an open-source framework for building multi-agent AI applications that can converse with each other and interact with tools and environments. As of May 2026, it represents the rebranded and technically advanced successor to the original Microsoft AutoGen project.

## What problem it solves
It simplifies the development of complex AI systems where multiple agents need to collaborate, reason, and act to solve sophisticated problems. It addresses the overhead of managing agent state, conversation history, and tool-calling coordination in multi-agent environments.

## Where it fits in the stack
**Framework / Multi-Agent Orchestrator**.

## Typical use cases
- **Multi-agent Collaboration**: Building teams of agents to perform research, coding, and review in a coordinated loop.
- **Complex Problem Solving**: Breaking down difficult tasks into smaller parts handled by specialized agents with different roles.
- **Human-Agent Interaction**: Creating applications where humans can step in to provide feedback or approval within an agentic workflow.
- **Cross-Platform Agents**: Deploying agents that can operate across different environments (local, cloud, or edge).

## Strengths
- **Conversational Design**: Native support for complex natural language interactions and multi-party conversations.
- **Flexible Orchestration**: Supports various patterns such as group chats, round-robin, and custom state-based transitions.
- **Large Community**: Inherits a massive and active community from the AutoGen project, ensuring rapid bug fixes and updates.
- **Tool-Call Management**: Robust handling of complex tool-calling sequences across multiple agents.

## Limitations
- **Evolving API**: The transition from AutoGen to AG2 involves significant API refinements that may require migration efforts for older codebases.
- **Abstraction Depth**: The high level of abstraction can sometimes make it challenging to debug fine-grained agent behaviors without deep framework knowledge.

## When to use it
- When you want to build sophisticated multi-agent systems based on a proven and mature foundation.
- When you need a framework that natively supports complex, conversational AI workflows and human-in-the-loop patterns.
- When you want to leverage a wide range of pre-built agent types and coordination strategies.

## When not to use it
- For simple, single-agent tasks where a lighter SDK (like the OpenAI SDK directly) would suffice.
- If you prefer a more rigid, non-conversational orchestration model (e.g., simple DAG-based workflows).

## Getting started

### Installation
```bash
pip install ag2
```

### Basic Multi-Agent Example
```python
import autogen # The package name remains autogen for compatibility

config_list = [{"model": "gpt-4o", "api_key": "YOUR_API_KEY"}]

# Define specialized agents
researcher = autogen.AssistantAgent(
    "researcher",
    system_message="You are a researcher who finds relevant data.",
    llm_config={"config_list": config_list}
)

writer = autogen.AssistantAgent(
    "writer",
    system_message="You are a writer who summarizes data from the researcher.",
    llm_config={"config_list": config_list}
)

user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    code_execution_config={"work_dir": "workspace", "use_docker": False},
    human_input_mode="NEVER"
)

# Start a group chat
groupchat = autogen.GroupChat(agents=[user_proxy, researcher, writer], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

user_proxy.initiate_chat(
    manager,
    message="Research the latest features of AG2 and summarize them."
)
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0 License)
- **Cost**: Free (OSS)
- **Self-hostable**: Yes

## Related tools / concepts
- [AutoGen](autogen.md)
- [CrewAI](crewai.md)
- [Semantic Kernel](semantic-kernel.md)
- [LangGraph](langgraph.md)
- [Langflow](langflow.md)
- [Rivet](rivet.md)
- [Temporal](../orchestration/temporal.md)
- [PydanticAI](pydantic-ai.md)
- [Mastra](mastra.md)

## Sources / References
- [Official Website](https://ag2.ai/)
- [GitHub](https://github.com/ag2-ai/ag2)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-05-31)

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high
