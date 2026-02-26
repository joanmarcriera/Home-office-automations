# Dify

## What it is
Dify is an open-source LLM application development platform. It allows you to visually create and operate AI applications based on various LLMs, and includes tools for prompt engineering, RAG, and agent orchestration.

## What problem it solves
Lowers the barrier to building LLM-powered applications by providing a visual interface for designing prompts, RAG pipelines, and agent workflows without writing extensive code.

## Where it fits in the stack
AI & Knowledge — serves as a visual platform for building and deploying LLM applications, potentially connecting to the local Ollama instance.

## Typical use cases
- Building RAG applications with a visual drag-and-drop interface
- Rapid prototyping of prompt chains and agent workflows
- Setting up local RAG pipelines with Ollama and private data

## Strengths
- Open-source and self-hostable, aligning with the privacy-first approach
- Visual interface makes LLM app development accessible to non-developers
- Supports multiple LLM backends including local models via Ollama

## Limitations
- Requires running an additional service with its own dependencies
- Less flexible than code-first frameworks for highly custom workflows
- Smaller community and ecosystem compared to LangChain

## When to use it
- When you want to visually prototype and deploy LLM applications without writing code
- When building RAG or agent applications that connect to local LLM infrastructure

## When not to use it
- When you need fine-grained programmatic control over LLM pipelines
- When the overhead of running another service is not justified for simple tasks

## Related tools / concepts
- [Flowise](flowise.md)
- [LangFlow](https://github.com/langflow-ai/langflow)

## Sources / references
- [Official Website](https://dify.ai/)
- [GitHub Repository](https://github.com/langgenius/dify)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
