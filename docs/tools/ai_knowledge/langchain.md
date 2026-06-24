# LangChain

## What it is
LangChain is a comprehensive framework for developing applications powered by large language models. It provides a modular set of tools and abstractions for working with LLMs, including prompt templates, memory, retrieval-augmented generation (RAG) pipelines, and agentic workflows.

## What problem it solves
It provides reusable building blocks and standardized abstractions for common LLM application patterns. Developers can focus on high-level logic rather than implementing prompt chaining, document chunking, or agent loops from scratch, significantly reducing time-to-market for complex AI products.

## Where it fits in the stack
**AI Assistants & Knowledge / Frameworks**. It serves as a foundational layer that other tools in the stack (such as [Flowise](flowise.md)) build upon for LLM application development and orchestration.

## Typical use cases
- **RAG Pipelines**: Building retrieval systems over private data sources (PDFs, SQL, Notion).
- **Agent Orchestration**: Creating multi-step agent workflows with tool use and memory.
- **Complex Logic Chaining**: Using LangChain Expression Language (LCEL) to compose granular model steps.
- **Observability**: Evaluating and tracing LLM applications using [LangSmith](../benchmarking/langsmith.md).

## Framework selection notes
LangChain now has a clearer split between its architectural layers:
- **LangChain**: The quick-start framework for standardized agent and app patterns.
- **Deep Agents**: The opinionated harness for autonomous, long-running, non-deterministic tasks requiring planning and subagents.
- **LangGraph**: The lower-level stateful runtime when you want tighter control over workflow shape and execution semantics.

## Strengths
- **Massive Ecosystem**: Large and active open-source community with extensive documentation and third-party integrations.
- **Provider Agnostic**: Supports a wide range of LLM providers (Anthropic, OpenAI, Google) and vector stores.
- **Multi-Language**: Robust support for both Python and JavaScript/TypeScript.
- **Production Ready**: Integrated ecosystem including LangSmith for observability and LangServe for deployment.

## Limitations
- **Abstraction Density**: The high level of abstraction can add complexity and make debugging harder ("abstraction soup").
- **Volatility**: The rapid pace of change can occasionally lead to breaking changes between minor versions.
- **Overhead**: Can be overkill for simple LLM interactions where a direct SDK call suffices.

## When to use it
- When building complex LLM applications that require chaining, RAG, or agent patterns.
- When you need integrations with many different LLM providers and data sources.
- When you want to leverage a mature ecosystem for production-grade LLM ops (tracing, evaluation).

## When not to use it
- When the use case is a simple single-prompt LLM call.
- When you prefer a data-centric framework like [LlamaIndex](llamaindex.md) for pure RAG workloads.
- When you need a minimal, low-overhead framework for edge or resource-constrained environments.

## Getting started

### Installation
Install the core LangChain package and the OpenAI integration:

```bash
pip install langchain langchain-openai
```

### Minimal Python Example
Minimal example to call an LLM using the standardized interface:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke("Hello, how are you?")
print(response.content)
```

## CLI examples

### LangGraph CLI
Manage and deploy stateful agents using the [LangGraph](../frameworks/langgraph.md) CLI:
```bash
# Install the CLI
pip install langgraph-cli

# Check the version
langgraph --version
```

### LangSmith Login
Authenticate your local environment for tracing:
```bash
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="your-api-key"
```

## API examples

### LCEL Chain Composition
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

## Related tools / concepts
- [LlamaIndex](llamaindex.md) — Data-centric RAG framework.
- [Haystack](../frameworks/haystack.md) — Alternative orchestration library.
- [Google Gemini](google-gemini.md) — Supported model provider.
- [Google Opal](google-opal.md) — No-code builder in the same ecosystem.
- [Flowise](flowise.md) — Visual UI for LangChain.
- [Mastra](../frameworks/mastra.md) — High-performance agent framework.
- [AG2](../frameworks/ag2.md) — Multi-agent conversation framework.
- [LangSmith](../benchmarking/langsmith.md) — Tracing and evaluation platform.
- [LangGraph](../frameworks/langgraph.md) — Stateful agent runtime.

## Sources / references
- [Official Website](https://www.langchain.com/)
- [GitHub Repository](https://github.com/langchain-ai/langchain)
- [LangChain Deep Agents overview](https://www.langchain.com/deep-agents)
- [LangChain Expression Language (LCEL) Documentation](https://python.langchain.com/docs/concepts/lcel/)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
