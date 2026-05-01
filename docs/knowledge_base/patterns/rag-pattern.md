# RAG Pattern (Retrieval-Augmented Generation)

## What it is
Retrieval-Augmented Generation (RAG) is a design pattern that enhances the performance of Large Language Models (LLMs) by providing them with relevant information from external data sources before generating a response.

## What problem it solves
It addresses the limitations of LLMs, such as hallucinations (generating incorrect information) and a lack of access to up-to-date or private data, by grounding the model's output in verifiable facts retrieved from a reliable source.

## How it works
1. **User Query**: The user provides a prompt or question.
2. **Retrieval**: The system searches an external data source (e.g., a vector database) for information relevant to the query.
3. **Augmentation**: The retrieved information is combined with the original user query to create an augmented prompt.
4. **Generation**: The augmented prompt is sent to the LLM, which generates a response based on both its internal knowledge and the provided context.

## Typical use cases
- **Question Answering over Documents**: Providing answers based on a company's internal knowledge base or documentation.
- **Fact-Checking**: Verifying claims against a trusted data source.
- **Personalized Recommendations**: Generating suggestions based on user-specific data retrieved at query time.

## Strengths
- **Reduced Hallucinations**: Grounds the LLM's responses in external, verifiable data.
- **Access to Current Data**: Allows LLMs to use information that was not part of their training set.
- **Transparency**: Enables the system to provide citations or references for its answers.

## Limitations
- **Retrieval Quality**: The system's performance is heavily dependent on the quality and relevance of the retrieved information.
- **Latency**: Adding a retrieval step can increase the time it takes to generate a response.
- **Complexity**: Setting up and maintaining the retrieval infrastructure (e.g., embeddings, vector stores) adds complexity.

## When to use it
- When you need accurate, up-to-date information that is not present in the LLM's training data.
- When transparency and grounding of responses are critical.

## When not to use it
- For tasks where the LLM's internal knowledge is sufficient and no external context is required.
- If the latency introduced by retrieval is unacceptable for the use case.

## Related tools / concepts
- [Vector DB Comparison](../../knowledge_base/vector-db-comparison.md)
- [Agentic RAG](data-copilot-agentic-rag.md)
- [Docling](../../tools/process_understanding/docling.md)

## Sources / References
- [Wikipedia](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
- [Prompt Engineering Guide](https://www.promptingguide.ai/techniques/rag)

## Contribution Metadata
- Last reviewed: 2026-05-07
- Confidence: high
