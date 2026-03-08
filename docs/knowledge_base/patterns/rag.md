# Retrieval-Augmented Generation (RAG)

## What it is

Retrieval-Augmented Generation (RAG) is an architectural pattern that optimizes the output of a Large Language Model (LLM) by referencing an authoritative knowledge base outside of its training data sources before generating a response. It bridges the gap between the generative power of LLMs and the need for factual, up-to-date, and private information.

## What problem it solves

*   **Hallucination Reduction:** Grounding models in retrieved facts significantly reduces the likelihood of the LLM generating "plausible-sounding" but incorrect information.
*   **Knowledge Freshness:** Enables models to access the latest information without the prohibitive cost and time of retraining or fine-tuning.
*   **Domain Specificity:** Allows general-purpose models to answer questions about proprietary or niche datasets (e.g., internal company wikis, technical manuals).
*   **Cost Efficiency:** Updating a vector database is orders of magnitude cheaper and faster than fine-tuning a model on new data.
*   **Explainability:** RAG systems can provide citations for the sources used to generate a response, increasing user trust.

## Where it fits in the stack

RAG is a core **Reasoning Engine** pattern (Layer 3 in the [AI Tooling Landscape](../ai_tooling_landscape.md)). It sits between the raw **Infrastructure/Models** (Layer 0-2) and the **Orchestration/Frameworks** (Layer 5-6) that implement the retrieval logic.

## Architecture

The RAG architecture consists of a disconnected ingestion pipeline and a real-time retrieval-generation loop.

```text
                                     +-----------------------+
                                     |  Ingestion Pipeline   |
                                     +----------+------------+
                                                |
          +----------+      +-----------+       v       +------------+       +--------------+
          | Documents| ---> | Load/Parse| ---> [Chunk] ---> [Embed]  | ---> | Vector Store |
          +----------+      +-----------+               +-----+------+       +--------------+
                                                              ^
                                                              |
                                                     +--------+---------+
                                                     | Embedding Model  |
                                                     +------------------+

                                     +-----------------------+
                                     |  Retrieval Pipeline   |
                                     +----------+------------+
                                                |
          +----------+      +-----------+       v       +------------+
          |User Query| ---> |  Rewrite  | ---> [Embed] | Vector DB  |
          +----------+      +-----------+       |       +-----+------+
                                                |             |
                                                |      (Similarity Search)
                                                |             |
                                                v             v
          +----------+      +-----------+    +--------+    +----------+       +--------------+
          | Response | <--- | Generative| <--- [Augment] <--- [Re-rank] <--- | Top-K Chunks |
          +----------+      |    LLM    |    +--------+    +----------+       +--------------+
                            +-----------+
```

### Core Pipeline
1.  **Document Loading:** Importing data from sources like PDFs, Markdown, SQL databases, or APIs.
2.  **Chunking:** Splitting documents into smaller, semantically meaningful pieces (chunks) to respect LLM context limits.
3.  **Embedding:** Using a model (e.g., `nomic-embed-text`) to convert text chunks into numerical vectors.
4.  **Vector Store:** A specialized database (e.g., Chroma, Qdrant, pgvector) for storing and performing similarity searches on vectors.
5.  **Retrieval:** Fetching the most relevant chunks based on the vector similarity of the query.
6.  **Generation:** The LLM synthesizes the answer using the retrieved context and the user's query.

## Variants

*   **Naive RAG:** The traditional "retrieve-and-read" flow. Highly effective for simple queries but struggles with complex reasoning or multi-hop questions across multiple documents.
*   **Advanced RAG:** Improves on Naive RAG by adding sophisticated pre- and post-retrieval steps:
    *   **Pre-retrieval:** Query expansion (generating multiple versions of the query) and Query Transformation (rewriting for better search compatibility).
    *   **Post-retrieval:** Re-ranking (scoring chunks with a precise cross-encoder) and Context Compression (removing irrelevant noise from chunks).
*   **Modular RAG:** A flexible architecture where components are added as needed:
    *   **Routing:** Directing queries to the most relevant data silo (e.g., SQL vs Vector DB).
    *   **Iterative Retrieval:** Retrieving, generating a partial answer, then retrieving again based on the partial answer.
    *   **Self-RAG:** The model critiques its own retrieved chunks and generated response for relevance, support, and utility.
*   **GraphRAG:** Augments vector retrieval with a Knowledge Graph. It extracts entities and relationships to provide both global context (summarizing entire datasets) and local context (finding specific facts), solving the "blindness" of vector search to broad themes.
*   **Agentic RAG:** An agent-driven approach where the LLM is equipped with retrieval tools. The agent plans its search strategy, chooses between multiple data sources, and performs multi-step reasoning before delivering the final answer.

## Typical use cases

*   **Technical Support:** Answering questions based on product manuals and documentation.
*   **Internal Knowledge Base:** Querying company wikis, HR policies, or project notes.
*   **Legal/Compliance:** Searching through large volumes of contracts or regulations.
*   **Personal Finance:** Reasoning over bank statements and expense logs (e.g., in [Actual Budget](../../services/actual-budget.md)).

## Getting started

The following examples demonstrate a minimal local RAG setup using **Ollama** for both embeddings (`nomic-embed-text`) and generation (`llama3`).

=== "LangChain"

    ```python
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.chat_models import ChatOllama
    from langchain_core.prompts import ChatPromptTemplate
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain

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

    # 3. Create Retrieval Chain
    model = ChatOllama(model="llama3")

    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the following context:
    {context}

    Question: {input}
    """)

    combine_docs_chain = create_stuff_documents_chain(model, prompt)
    rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

    # 4. Invoke
    response = rag_chain.invoke({"input": "What is the primary conclusion of the report?"})
    print(response["answer"])
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
*   **Embedding Model Selection:**
    *   *Local:* Use [Ollama](../../services/ollama.md) with `nomic-embed-text` or BGE models for privacy and cost.
    *   *API:* OpenAI `text-embedding-3-small` or Cohere `embed-english-v3.0` for high performance.
*   **Vector Store Selection:**
    *   Local: Chroma, Qdrant (local mode), [pgvector](../../tools/infrastructure/index.md#sub-categories).
    *   Cloud: Pinecone, Weaviate, Milvus.
*   **Retrieval Strategy:**
    *   *Similarity Search:* Basic cosine similarity for fast, direct matching.
    *   *Maximum Marginal Relevance (MMR):* Balances relevance with diversity to avoid redundant information in the context window.
    *   *Hybrid Search:* Combines vector search with keyword (BM25) search to capture both semantic meaning and specific terminology.
*   **Re-ranking:**
    *   *Cross-Encoders:* Use a model (e.g., Cohere Rerank) to score the relationship between query and chunk directly, significantly improving precision over vector similarity alone.

## Strengths

*   **Factual Accuracy:** Grounding in real data reduces hallucinations.
*   **Transparency:** Citations provide a way to verify the model's output.
*   **Efficiency:** Much faster and cheaper than fine-tuning for knowledge updates.
*   **Privacy:** Can be run entirely locally with tools like Ollama and local vector DBs.

## Limitations

*   **Retrieval Quality:** The answer is only as good as the retrieved context (Garbage In, Garbage Out).
*   **Context Window:** Even with RAG, LLMs have limits on how much context they can process effectively.
*   **Complexity:** Managing chunking strategies and vector database indexes adds architectural overhead.
*   **Latency:** The retrieval and potential re-ranking steps add time to the overall response generation.

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

*   **RAG Platforms:** [Dify](../../tools/ai_knowledge/dify.md), [Flowise](../../tools/ai_knowledge/flowise.md), [RAGFlow](../../tools/process_understanding/ragflow.md)
*   **Orchestration:** [LlamaIndex](../../tools/ai_knowledge/llamaindex.md), [LangChain](../../tools/ai_knowledge/langchain.md), [Haystack](../../tools/frameworks/haystack.md)
*   **Infrastructure:** [Vector Databases](../../tools/infrastructure/index.md), [Embedding Models](../../tools/infrastructure/index.md)
*   **Data Extraction:** [Crawl4AI](../../tools/process_understanding/crawl4ai.md), [Firecrawl](../../tools/process_understanding/firecrawl.md), [OCRmyPDF](../../tools/process_understanding/ocrmypdf.md)
*   **Local Solutions:** [Paperless-AI](../../services/paperless-ai.md), [PageIndex](../../tools/process_understanding/pageindex.md)
*   **Evaluation:** RAGAS, DeepEval, TruLens
*   **Concepts:** [Tool Calling & MCP](tool-calling-and-mcp.md), [Agent Protocols](../agent_protocols.md)

## Sources / references

*   [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al. 2020)](https://arxiv.org/abs/2005.11401) - The foundational RAG paper.
*   [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection (Akari et al. 2023)](https://arxiv.org/abs/2310.11511)
*   [RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval (Sarthi et al. 2024)](https://arxiv.org/abs/2401.18059)
*   [From Local to Global: A GraphRAG Approach to Query-Focused Summarization (Edge et al. 2024)](https://arxiv.org/abs/2404.16130)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high
