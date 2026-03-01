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

## Limitations
- **Overhead**: Can be complex to set up and manage for simpler multi-agent tasks.
- **Cost**: Like most multi-agent frameworks, it can lead to high token consumption.

## When to use it
- When you need agents to interact via natural language "chat" to solve problems.
- When code execution is a central part of the agentic workflow.

## When not to use it
- For static pipelines that don't benefit from back-and-forth conversation.
- If you prefer a more rigid, non-conversational orchestration model.

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [CrewAI](crewai.md)
- [Semantic Kernel](semantic-kernel.md)
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md)

## Sources / References
- [GitHub](https://github.com/microsoft/autogen)
- [Official Website](https://microsoft.github.io/autogen/)

## Getting started

```bash
pip install pyautogen
```

```python
from autogen import AssistantAgent, UserProxyAgent

# Assistant agent for reasoning
assistant = AssistantAgent("assistant", llm_config={"model": "gpt-4"})

# User proxy agent for executing code
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})

# Start the conversation
user_proxy.initiate_chat(assistant, message="Show me the stock price of NVDA for the last 3 months.")
```

## Contribution Metadata

- Last reviewed: 2026-03-01
- Confidence: high
