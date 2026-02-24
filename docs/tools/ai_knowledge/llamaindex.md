# LlamaIndex

## What it is
LlamaIndex (formerly GPT Index) is a data framework for LLM applications. It focuses on connecting custom data sources to LLMs for retrieval-augmented generation (RAG).

## What problem it solves
It simplifies the process of data ingestion, indexing, and retrieval, providing the tools needed to build "knowledge-aware" agents that can accurately answer questions based on private data.

## Where it fits in the pipeline
**Store / Understand / Reason**

## Typical use cases (in this homelab / family automation context)
- **Personal Knowledge Management**: Indexing all your PDFs, notes, and emails to make them searchable by an LLM.
- **Homelab Log Analysis**: Using the data framework to help an AI understand and troubleshoot server logs.
- **Contextual Search**: Building a search engine that understands the context of your family's history and documents.

## Integration points
- **Data Connectors**: Over 100 connectors for various data sources (Slack, Discord, Google Drive, local files).
- **LLMs**: Supports all major LLM providers.
- **Storage**: Integrates with multiple vector databases and file storage systems.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Free tier**: N/A (Self-hosted)
- **Self-hostable**: Yes

## Strengths
- Unmatched focus on data handling and retrieval performance.
- Easy to build complex RAG systems with high accuracy.
- Strong support for structured data (e.g., SQL integration).

## Limitations
- Less focused on general agent "actions" compared to LangChain.
- Can be complex to tune for optimal retrieval performance.

## Alternatives / Related tools
- **LangChain**
- **Haystack**

## Links
- [Official Website](https://www.llamaindex.ai/)
- [GitHub](https://github.com/run-llama/llama_index)
