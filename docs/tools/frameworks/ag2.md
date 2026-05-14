# AG2 (formerly AutoGen)

## What it is
AG2 is the next-generation evolution of the AutoGen framework. It is an open-source framework for building multi-agent AI applications that can converse with each other and interact with tools and environments.

## What problem it solves
It simplifies the development of complex AI systems where multiple agents need to collaborate, reason, and act to solve sophisticated problems.

## Where it fits in the stack
**Framework / Multi-Agent Orchestrator**.

## Typical use cases
- **Multi-agent Collaboration**: Building teams of agents to perform research, coding, and review.
- **Complex Problem Solving**: Breaking down difficult tasks into smaller parts handled by specialized agents.
- **Human-Agent Interaction**: Creating applications where humans and AI agents work together seamlessly.

## Strengths
- **Conversational Design**: Excellent support for natural language interactions between agents.
- **Flexible Orchestration**: Supports various patterns of agent communication and coordination.
- **Large Community**: Inherits a large and active community from the AutoGen project.

## Limitations
- **Evolving API**: As a newer project (though based on AutoGen), the API may undergo changes.
- **Abstraction Depth**: Like most frameworks, it introduces abstractions that may hide underlying complexity.

## When to use it
- When you want to build sophisticated multi-agent systems based on a proven foundation.
- When you need a framework that supports complex, conversational AI workflows.

## When not to use it
- For simple, single-agent tasks.
- If you prefer a more rigid or non-conversational orchestration model.

## Getting started

### Installation
```bash
pip install "ag2[openai]"
```

### Basic Example
```python
import autogen

config_list = [{"model": "gpt-4", "api_key": "YOUR_API_KEY"}]

assistant = autogen.AssistantAgent(
    "assistant",
    llm_config={"config_list": config_list}
)

user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

user_proxy.initiate_chat(
    assistant,
    message="Tell me a joke about autonomous agents."
)
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0 License)
- **Cost**: Free
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

## Sources / References
- [Official Website](https://ag2.ai/)
- [GitHub](https://github.com/ag2-ai/ag2)

## Contribution Metadata
- Last reviewed: 2026-05-07
- Confidence: high
