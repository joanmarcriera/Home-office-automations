# Frameworks

AI frameworks provide the abstractions needed to build, optimize, and deploy agentic and RAG-based applications. They handle the "glue" code of LLM interactions, tool execution, and prompt management.

## Framework Selection Guidance

| Goal | Recommended Frameworks | Why? |
| :--- | :--- | :--- |
| **General Purpose RAG** | [LlamaIndex](../ai_knowledge/llamaindex.md), [LangChain](../ai_knowledge/langchain.md) | Mature ecosystems with deep data and tool integrations. |
| **Multi-Agent Systems** | [AutoGen](autogen.md), [CrewAI](crewai.md), [AG2](ag2.md) | Specialized in agent coordination, delegation, and role-playing. |
| **Structured Output** | [Instructor](instructor.md), [PydanticAI](pydantic-ai.md) | Focus on typed, reliable data extraction using Pydantic. |
| **Optimization** | [DSPy](dspy.md) | Programmatic prompt optimization instead of manual trial-and-error. |
| **Local / Lightweight** | [Smolagents](smolagents.md), [Mastra](mastra.md) | Minimalist approach with focus on speed and developer experience. |

## Core Framework List

| Framework | Primary Language | Role |
| :--- | :--- | :--- |
| [AG2](ag2.md) | Python | Advanced multi-agent orchestration. |
| [AutoGen](autogen.md) | Python | Original multi-agent conversation framework. |
| [CrewAI](crewai.md) | Python | Role-based agent collaboration. |
| [DSPy](dspy.md) | Python | Prompt compiler and optimizer. |
| [Haystack](haystack.md) | Python | Modular pipeline framework for RAG. |
| [LangChain](../ai_knowledge/langchain.md) | Python / JS | Swiss-army knife for LLM apps. |
| [LlamaIndex](../ai_knowledge/llamaindex.md) | Python / JS | Context-augmented data framework. |
| [Mastra](mastra.md) | TypeScript | Integration-first agent engine. |
| [PydanticAI](pydantic-ai.md) | Python | Typed, functional agent framework. |
| [Semantic Kernel](semantic-kernel.md) | C# / Python | Microsoft-native agent SDK. |

## Related Tools / Concepts

- [Orchestration](../orchestration/index.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [Tool Calling & MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Agents](../agents/index.md)
- [Providers](../providers/index.md)
