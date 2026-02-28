# LangChain

## What it is
LangChain is a framework for developing applications powered by large language models. It provides a set of tools and abstractions for working with LLMs, including chain of thought, retrieval augmented generation, and agentic workflows.

## What problem it solves
Provides reusable building blocks and standardized abstractions for common LLM application patterns, so developers do not have to implement prompt chaining, RAG, or agent loops from scratch.

## Where it fits in the stack
AI & Knowledge — serves as a foundational framework that other tools in the stack (such as Flowise) build upon for LLM application development.

## Typical use cases
- Building retrieval-augmented generation pipelines over private data
- Creating multi-step agent workflows with tool use
- Exploring LangGraph for complex multi-agent orchestration

## Strengths
- Large and active open-source community with extensive documentation
- Wide range of integrations with LLM providers, vector stores, and tools
- Supports both Python and JavaScript/TypeScript

## Limitations
- Abstractions can add complexity and make debugging harder
- Rapid pace of change can lead to breaking changes between versions
- Can be overkill for simple LLM interactions

## When to use it
- When building complex LLM applications that require chaining, RAG, or agent patterns
- When you need integrations with many different LLM providers and data sources

## When not to use it
- When the use case is a simple single-prompt LLM call
- When you prefer a data-centric framework like LlamaIndex for pure RAG workloads

## Getting started

```bash
pip install langchain langchain-openai
```

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
chain = prompt | llm
```

## API examples

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_template("Explain {concept} in one sentence.")
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

response = chain.invoke({"concept": "quantum entanglement"})
print(response)
```

## Related tools / concepts
- [LlamaIndex](llamaindex.md)
- [Haystack](https://github.com/deepset-ai/haystack)

## Sources / references
- [Official Website](https://www.langchain.com/)
- [GitHub Repository](https://github.com/langchain-ai/langchain)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: medium
