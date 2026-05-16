# LangChain

## What it is
LangChain is a framework for developing applications powered by large language models. It provides a set of tools and abstractions for working with LLMs, including chain of thought, retrieval augmented generation, and agentic workflows.

## What problem it solves
Provides reusable building blocks and standardized abstractions for common LLM application patterns, so developers do not have to implement prompt chaining, RAG, or agent loops from scratch.

## Where it fits in the stack
AI & Knowledge — serves as a foundational framework that other tools in the stack (such as [Flowise](flowise.md)) build upon for LLM application development.

## Typical use cases
- Building retrieval-augmented generation (RAG) pipelines over private data.
- Creating multi-step agent workflows with tool use and memory.
- Exploring [LangGraph](https://langchain-ai.github.io/langgraph/) for complex, stateful multi-agent orchestration.
- Using Deep Agents for autonomous, long-running tasks requiring planning and subagents.
- Evaluating LLM applications using LangSmith for tracing and performance monitoring.

## Framework selection notes

LangChain now has a clearer split between its layers:

- **LangChain**: the quick-start framework for standardized agent and app patterns.
- **Deep Agents**: the opinionated harness for autonomous, long-running, non-deterministic tasks where planning, memory, and subagents matter.
- **LangGraph**: the lower-level stateful runtime when you want tighter control over workflow shape and execution semantics.

That distinction matters in practice. Many teams start with LangChain for fast prototyping, move to Deep Agents when the task needs more autonomy, and drop to LangGraph when they need explicit state-machine style control.

## Advanced Patterns

### LangGraph (Stateful Orchestration)
LangGraph allows you to build agents as state machines. This is essential for complex loops where an agent needs to reflect on its own work, retry failed steps, or coordinate with other agents in a multi-turn conversation.

### LangSmith (Observability & Evaluation)
LangSmith provides a unified platform for debugging, testing, and monitoring LangChain applications. It allows you to trace every step of a chain's execution, identify bottlenecks, and run automated evaluations against test datasets.

## Strengths
- Large and active open-source community with extensive documentation.
- Wide range of integrations with LLM providers, vector stores, and tools.
- Supports both Python and JavaScript/TypeScript.
- Robust ecosystem including LangSmith for observability and LangServe for deployment.

## Limitations
- Abstractions can add complexity and make debugging harder ("abstraction soup").
- Rapid pace of change can lead to breaking changes between versions.
- Can be overkill for simple LLM interactions where a direct SDK call suffices.

## When to use it
- When building complex LLM applications that require chaining, RAG, or agent patterns.
- When you need integrations with many different LLM providers and data sources.
- When you want to leverage a mature ecosystem for production-grade LLM ops (tracing, eval).

## When not to use it
- When the use case is a simple single-prompt LLM call.
- When you prefer a data-centric framework like [LlamaIndex](llamaindex.md) for pure RAG workloads.
- When you need a minimal, low-overhead framework for edge or resource-constrained environments.

## Related tools / concepts

- [LlamaIndex](llamaindex.md)
- [Haystack](../frameworks/haystack.md)
- [AI Templates](aitmpl.md)
- [Google Gemini](google-gemini.md)
- [Google Opal](google-opal.md)
- [Flowise](flowise.md)
- [Mastra](../frameworks/mastra.md)
- [AG2](../frameworks/ag2.md)

## Getting started

### Installation

Install the core LangChain package and the OpenAI integration:

```bash
pip install langchain langchain-openai
```

### Minimal Python Example

Minimal example to call an LLM:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke("Hello, how are you?")
print(response.content)
```

## API examples

### Simple Chain with Prompt Template, LLM, and Output Parser

This example demonstrates the recommended way to compose components using LangChain Expression Language (LCEL).

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Define the Prompt Template
prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")

# 2. Initialize the Model
model = ChatOpenAI(model="gpt-4o")

# 3. Initialize the Output Parser
output_parser = StrOutputParser()

# 4. Compose the Chain using LCEL
chain = prompt | model | output_parser

# 5. Invoke the Chain
response = chain.invoke({"topic": "bears"})
print(response)
```

### Agent with Tools
Creating an agent that can use a search tool and a calculator.

```python
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# 1. Load the prompt
prompt = hub.pull("hwchase17/openai-functions-agent")

# 2. Define tools
tools = [TavilySearchResults(max_results=1)]

# 3. Initialize LLM and Agent
llm = ChatOpenAI(model="gpt-4o")
agent = create_openai_functions_agent(llm, tools, prompt)

# 4. Create Agent Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Run the agent
agent_executor.invoke({"input": "What is the weather in Tokyo?"})
```

## Sources / references
- [Official Website](https://www.langchain.com/)
- [GitHub Repository](https://github.com/langchain-ai/langchain)
- [LangChain Deep Agents overview](https://www.langchain.com/deep-agents)
- [LangChain Expression Language (LCEL) Documentation](https://python.langchain.com/docs/concepts/lcel/)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high
