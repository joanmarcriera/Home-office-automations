# Retrieval-Augmented Generation (RAG)

## What it is

Retrieval-Augmented Generation (RAG) is an architectural pattern that optimizes the output of a Large Language Model (LLM) by referencing an authoritative knowledge base outside of its training data sources before generating a response. It bridges the gap between the generative power of LLMs and the need for factual, up-to-date, and private information.

## What problem it solves

*   **Hallucination Reduction:** Grounding models in retrieved facts significantly reduces the likelihood of the LLM generating "plausible-sounding" but incorrect information.
*   **Knowledge Freshness:** Enables models to access the latest information without the prohibitive cost and time of retraining or fine-tuning.
*   **Domain Specificity:** Allows general-purpose models to answer questions about proprietary or niche datasets (e.g., internal company wikis, technical manuals).
*   **Cost Efficiency:** Updating a vector database is orders of magnitude cheaper and faster than fine-tuning a model on new data.
*   **Explainability:** RAG systems can provide citations for the sources used to generate a response, increasing user trust.

## Architecture

The standard RAG pipeline is divided into an Ingestion Phase and a Retrieval-Generation Phase.

```text
INGESTION PHASE (Data Preparation)
[Documents] -> [Load] -> [Chunk] -> [Embed] -> [Vector Store]
                                     |
                                     v
                           (Embedding Model)

RETRIEVAL & GENERATION PHASE (Query Time)
[User Query]
      |
      v
 [Embedding]
      |
      v
[Vector Store] --(Search)--> [Top-K Chunks]
                                   |
                                   v
[Prompt Template] <---- [Augmented Context]
(Context + Query)
      |
      v
    [LLM] --(Generate)--> [Answer + Citations]
```

### Core Components
1.  **Document Loading:** Importing data from sources like PDFs, Markdown, SQL databases, or APIs.
2.  **Chunking:** Splitting documents into smaller, semantically meaningful pieces (chunks) to respect LLM context limits.
3.  **Embedding:** Using a model (e.g., `nomic-embed-text`) to convert text chunks into numerical vectors.
4.  **Vector Store:** A specialized database (e.g., Chroma, Qdrant, pgvector) for storing and performing similarity searches on vectors.
5.  **Retrieval:** Fetching the most relevant chunks based on the vector similarity of the query.
6.  **Generation:** The LLM synthesizes the answer using the retrieved context and the user's query.

## Variants

*   **Naive RAG:** The basic "retrieve-and-read" flow. Highly effective for simple queries but struggles with complex reasoning or multi-hop questions.
*   **Advanced RAG:** Adds pre-retrieval (query expansion, rewriting) and post-retrieval (re-ranking, context compression) steps to improve precision and recall.
*   **Modular RAG:** A flexible architecture where components like routing, iterative retrieval, and self-reflection (e.g., [Self-RAG](https://arxiv.org/abs/2310.11511)) are added as needed.
*   **GraphRAG:** Augments vector retrieval with a Knowledge Graph to capture complex entity relationships that vector proximity alone might miss.
*   **Agentic RAG:** An agent-driven approach where the LLM uses tools to decide when to retrieve, what source to use, and whether the retrieved information is sufficient.

## Getting started

The following examples demonstrate a minimal local RAG setup using **Ollama** for both embeddings (`nomic-embed-text`) and generation (`llama3`).

=== "LangChain (LCEL)"

    ```python
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.chat_models import ChatOllama
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    # 1. Load and Chunk
    loader = TextLoader("docs/my_data.txt")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    # 2. Embed and Store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OllamaEmbeddings(model="nomic-embed-text")
    )
    retriever = vectorstore.as_retriever()

    # 3. Define LCEL Chain
    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the following context:
    {context}

    Question: {question}
    """)

    model = ChatOllama(model="llama3")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    # 4. Invoke
    print(rag_chain.invoke("What is the primary conclusion of the report?"))
    ```

=== "LlamaIndex"

    ```python
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.llms.ollama import Ollama

    # 1. Setup Local Models via Settings
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    Settings.llm = Ollama(model="llama3", request_timeout=360.0)

    # 2. Load Documents and Create Index
    # SimpleDirectoryReader reads all files in the specified directory
    documents = SimpleDirectoryReader("data/").load_data()
    index = VectorStoreIndex.from_documents(documents)

    # 3. Query the Index
    query_engine = index.as_query_engine()
    response = query_engine.query("What are the key findings?")
    print(response)
    ```

## Key decisions

*   **Chunking Strategy:**
    *   *Fixed-size:* Simple and fast, but may cut off context mid-sentence.
    *   *Recursive:* Splits on hierarchy (paragraphs, sentences) to preserve meaning.
    *   *Semantic:* Uses embeddings to find natural break points between topics.
*   **Embedding Model:**
    *   *Local:* Use [Ollama](../../services/ollama.md) with `nomic-embed-text` or BGE models for privacy and cost.
    *   *API:* OpenAI `text-embedding-3-small` or Cohere `embed-english-v3.0` for high performance.
*   **Vector Store:**
    *   Local: Chroma, Qdrant (local mode), [pgvector](../../tools/infrastructure/index.md#sub-categories).
    *   Cloud: Pinecone, Weaviate.
*   **Retrieval & Re-ranking:**
    *   *Similarity Search:* Basic cosine similarity.
    *   *Hybrid Search:* Combines vector search with keyword (BM25) search.
    *   *Re-ranking:* Use a cross-encoder model (e.g., Cohere Rerank) to refine the top results for significantly better accuracy.

## When to use it

*   When the model needs access to private or internal documentation.
*   When factual accuracy is more important than creative flair.
*   When knowledge needs to be updated frequently (daily or hourly).
*   When you need to verify the source of information via citations.

## When not to use it

*   When the entire dataset fits within a massive context window (e.g., Gemini 1.5 Pro's 2M tokens) and cost is not a primary concern.
*   For purely creative tasks (poetry, fiction) where external facts are unnecessary.
*   When latency requirements are extremely tight (sub-100ms), as RAG adds retrieval time.
*   When the LLM's base training data is already sufficient and up-to-date for the domain.

## Related tools / concepts

*   **Orchestration:** [LlamaIndex](../../tools/ai_knowledge/llamaindex.md), [LangChain](../../tools/ai_knowledge/langchain.md), [Haystack](../../tools/frameworks/haystack.md)
*   **Infrastructure:** [Vector Databases](../../tools/infrastructure/index.md#sub-categories), [Embedding Models](../../tools/infrastructure/index.md#sub-categories)
*   **Data Extraction:** [Crawl4AI](../../tools/process_understanding/crawl4ai.md), [Firecrawl](../../tools/process_understanding/firecrawl.md), [OCRmyPDF](../../tools/process_understanding/ocrmypdf.md)
*   **Evaluation:** RAGAS, DeepEval, TruLens
*   **Concepts:** [Tool Calling & MCP](tool-calling-and-mcp.md), [Agent Protocols](../agent_protocols.md)

## Sources / references

*   [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al. 2020)](https://arxiv.org/abs/2005.11401) - The foundational RAG paper.
*   [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511)
*   [RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval](https://arxiv.org/abs/2401.18059)
*   [From Local to Global: A GraphRAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130)

## Contribution Metadata

- Last reviewed: 2026-03-01
- Confidence: high
