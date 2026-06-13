# AutoGen

## What it is
AutoGen is an open-source framework from Microsoft Research that enables the development of LLM applications using multiple agents that can converse with each other to solve tasks. In June 2026, it is a leading framework for orchestrating complex multi-agent workflows involving `claude-4-8-opus-20260528` and GPT-5.5.

## What problem it solves
It enables complex workflows that require multiple turns of conversation, code generation and execution, and human-in-the-loop feedback. It automates the "chat" between agents to reach a goal, providing built-in support for conversational patterns and tool use.

## Where it fits in the stack
**Framework / Multi-Agent Orchestrator**. It sits between the foundation models and the application layer, managing agent interactions and execution environments.

## Typical use cases
- **Software Engineering**: An assistant agent writing code and a proxy agent executing it to fix bugs.
- **Group Chat**: Multiple specialized agents (e.g., Coder, Critic, Manager) discussing a problem.
- **Interactive Apps**: Agents that can ask humans for clarification or approval.
- **Dynamic Workflows**: Using finite state machines (FSM) to transition between agents based on task state.

## Strengths
- **Customizability**: Agents are highly configurable in terms of their behavior, system prompts, and tools.
- **Code Execution**: Built-in support for running generated code in Docker or local environments safely.
- **Conversational Patterns**: Supports diverse patterns like group chat, nested chat, and sequential chat.
- **Human Participation**: Native support for human-in-the-loop interactions via the `UserProxyAgent`.

## Limitations
- **Overhead**: Can be complex to set up and manage for simpler multi-agent tasks compared to lighter frameworks.
- **Cost**: Multi-agent loops can lead to high token consumption if not properly constrained.
- **State Management**: Managing complex state across many agents can become challenging in large-scale deployments.

## When to use it
- When you need agents to interact via natural language "chat" to solve problems.
- When code generation and execution are central parts of the agentic workflow.
- For complex, multi-step tasks requiring different specialized agent roles.

## When not to use it
- For static pipelines that don't benefit from back-and-forth conversation.
- If you prefer a more rigid, graph-based orchestration model (like [LangGraph](langgraph.md)).

## Getting started

### 1. Installation
Install AutoGen via pip:
```bash
pip install pyautogen
```

### 2. Configuration
Set up your LLM configuration for models like `claude-4-8-opus-20260528`.

### 3. Hello World Example
```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent("assistant", llm_config={"model": "gpt-4o"})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})

user_proxy.initiate_chat(assistant, message="Write a python script to fetch the current weather in London.")
```

## CLI examples

### 1. Run an AutoGen Studio instance
```bash
autogenstudio ui --port 8081
```

### 2. Install AutoGen with Docker support
```bash
pip install "pyautogen[docker]"
```

### 3. Execute a script with UserProxy CLI
```bash
python my_autogen_app.py --human_input_mode ALWAYS
```

## API examples

### Multi-Agent Group Chat
AutoGen allows for complex agent orchestration through its GroupChat and GroupChatManager classes.

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Define agents
coder = AssistantAgent("Coder", llm_config=llm_config)
user_proxy = UserProxyAgent("User", code_execution_config={"work_dir": "web"})
manager = GroupChatManager(
    groupchat=GroupChat(agents=[coder, user_proxy], messages=[]),
    llm_config=llm_config
)

# Start interaction
user_proxy.initiate_chat(manager, message="Build a simple dashboard.")
```

## Related tools / concepts
- [CrewAI](crewai.md)
- [LangGraph](langgraph.md)
- [Semantic Kernel](semantic-kernel.md)
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Plandex](../development_ops/plandex.md)
- [OpenSwarm](../development_ops/openswarm.md)
- [Smolagents](smolagents.md)
- [DSPy](dspy.md)

## Sources / References
- [GitHub Repository](https://github.com/microsoft/autogen)
- [Official Documentation](https://microsoft.github.io/autogen/)
- [AutoGen Blog: FSM for Agentic Workflows](https://microsoft.github.io/autogen/blog/2024/02/11/FSM-GroupChat/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
