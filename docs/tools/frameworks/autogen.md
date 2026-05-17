# AutoGen

## What it is
AutoGen is an open-source framework from Microsoft Research that enables the development of LLM applications using multiple agents that can converse with each other to solve tasks. It supports human participation and code execution.

## What problem it solves
It enables complex workflows that require multiple turns of conversation, code generation and execution, and human-in-the-loop feedback. It automates the "chat" between agents to reach a goal.

## Where it fits in the stack
Framework / Multi-Agent Orchestrator

## Typical use cases
- **Software Engineering**: An assistant agent writing code and a proxy agent executing it to fix bugs.
- **Group Chat**: Multiple specialized agents (e.g., Coder, Critic, Manager) discussing a problem.
- **Interactive Apps**: Agents that can ask humans for clarification or approval.

## Strengths
- **Customizability**: Agents are highly configurable in terms of their behavior and tools.
- **Code Execution**: Built-in support for running generated code in Docker or local environments.
- **Conversational Patterns**: Supports diverse conversation patterns like group chat, nested chat, and sequential chat.

## Technical Architecture: Conversational Patterns
AutoGen orchestrates agents through several established patterns:
- **Sequential Chat**: A linear chain where one agent's output becomes another's input.
- **Group Chat**: A multi-agent environment where a "GroupChatManager" decides which agent speaks next.
- **Nested Chat**: An agent can "nest" a whole conversation as a tool or a sub-task, effectively creating hierarchical reasoning.
- **StateFlow**: Using custom logic to transition between agents based on finite state machines (FSM).

## Limitations
- **Overhead**: Can be complex to set up and manage for simpler multi-agent tasks.
- **Cost**: Like most multi-agent frameworks, it can lead to high token consumption.

## When to use it
- When you need agents to interact via natural language "chat" to solve problems.
- When code execution is a central part of the agentic workflow.

## When not to use it
- For static pipelines that don't benefit from back-and-forth conversation.
- If you prefer a more rigid, non-conversational orchestration model.

## Getting started

### Installation
```bash
pip install pyautogen
```

### Minimal Python Example
```python
from autogen import AssistantAgent, UserProxyAgent

# Assistant agent for reasoning
assistant = AssistantAgent("assistant", llm_config={"model": "gpt-4"})

# User proxy agent for executing code
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})

# Start the conversation
user_proxy.initiate_chat(assistant, message="Show me the stock price of NVDA for the last 3 months.")
```

### Advanced Example: Critic Pattern
This pattern uses a "Critic" agent to review the work of a "Coder" before it is finalized.

```python
from autogen import ConversableAgent

coder = ConversableAgent(
    "coder",
    llm_config={"config_list": [{"model": "gpt-4"}]},
    system_message="You write Python code to solve math problems."
)

critic = ConversableAgent(
    "critic",
    llm_config={"config_list": [{"model": "gpt-4"}]},
    system_message="You review code for efficiency and correctness. Suggest improvements."
)

# Sequential chat with feedback loop
critic.initiate_chat(
    coder,
    message="Write a function for the Fibonacci sequence.",
    max_turns=2
)
```

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [CrewAI](crewai.md)
- [LangGraph](./langgraph.md)
- [Semantic Kernel](semantic-kernel.md)
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Claude Code Router](../development_ops/claude-code-router.md)
- [Model Context Protocol (MCP)](../../knowledge_base/agent_protocols.md)

## Sources / References
- [GitHub](https://github.com/microsoft/autogen)
- [Official Website](https://microsoft.github.io/autogen/)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high
