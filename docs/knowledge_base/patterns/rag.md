# Retrieval-Augmented Generation (RAG)

## What it is

Retrieval-Augmented Generation (RAG) is an architectural pattern that optimizes the output of a Large Language Model (LLM) by referencing an authoritative knowledge base outside of its training data sources before generating a response. It combines the generative capabilities of LLMs with the precision of information retrieval systems.

## What problem it solves

*   **Hallucination Reduction:** By grounding the model in retrieved facts, it reduces the likelihood of the LLM making up information.
*   **Knowledge Freshness:** Allows the system to access real-time or recent data without the need for constant model retraining.
*   **Domain Specificity:** Enables LLMs to answer questions about private or niche datasets (e.g., internal company wikis, personal documents).
*   **Cost Reduction vs. Fine-tuning:** Updating a vector database is significantly cheaper and faster than fine-tuning a model on new data.

## Architecture

The standard RAG pipeline follows a linear process from data ingestion to response generation.

```text
INGESTION PHASE
[Documents] -> [Loading] -> [Chunking] -> [Embedding] -> [Vector Store]

RETRIEVAL & GENERATION PHASE
[User Query]
      |
      v
 [Embedding]
      |
      v
[Vector Store] -> (Retrieve top-k chunks) -> [Context]
                                               |
                                               v
[Prompt Template] <----------------------------+
(Context + Query)
      |
      v
    [LLM] -> [Generated Answer]
```

1.  **Document Loading:** Importing data from various formats (PDF, HTML, TXT, etc.).
2.  **Chunking:** Breaking documents into smaller, manageable pieces (chunks) to fit within the LLM's context window.
3.  **Embedding:** Converting text chunks into numerical vectors using an embedding model.
4.  **Vector Store:** Storing these vectors in a specialized database for fast similarity searching.
5.  **Retrieval:** Finding the most relevant chunks based on the user's query vector.
6.  **Generation:** Passing the retrieved context and the original query to the LLM to produce a grounded response.

## Variants

*   **Naive RAG:** The basic "retrieve-and-read" approach described above.
*   **Advanced RAG:** Introduces pre-retrieval (query rewriting, expansion) and post-retrieval (re-ranking, compression) optimizations.
*   **Modular RAG:** A highly flexible architecture involving specialized modules for routing, iterative retrieval, and self-correction (e.g., Self-RAG).
*   **GraphRAG:** Uses knowledge graphs to augment retrieval, capturing complex relationships between entities that vector embeddings might miss.
*   **Agentic RAG:** An agent-based approach where the LLM decides which tools to use, what to retrieve, and whether the retrieved information is sufficient to answer the query.

## Getting started

Below is a Python example using **LangChain** and **Ollama** for local execution, following modern LCEL practices.

```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Load a document
loader = TextLoader("your_data.txt")
documents = loader.load()

# 2. Chunking
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# 3. Embeddings & Vector Store
# Ensure Ollama is running locally with 'nomic-embed-text' pulled
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(texts, embeddings)

# 4. Define the Prompt
system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# 5. Query with Retrieval
# Ensure Ollama has 'llama3' or similar pulled
llm = Ollama(model="llama3")
retriever = vectorstore.as_retriever()

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

response = rag_chain.invoke({"input": "What is the main topic of the document?"})
print(response["answer"])
```

## Advanced Implementation: Re-ranking

Re-ranking is a common technique to improve precision by using a more expensive model to re-order the initial top-k results from the vector search.

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain_community.llms import Ollama

# 1. Setup base retriever (from 'Getting started' example)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# 2. Setup Re-ranker
# Flashrank is a lightweight, ultra-fast reranker that runs locally
compressor = FlashrankRerank()
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=base_retriever
)

# 3. Use in a chain
rag_chain = create_retrieval_chain(compression_retriever, question_answer_chain)

result = rag_chain.invoke({"input": "What specific architectural details are mentioned?"})
print(result["answer"])
```

## Key decisions

*   **Chunking Strategy:**
    *   *Fixed-size:* Simple, but can break semantic meaning.
    *   *Recursive:* Adjusts based on punctuation/structure.
    *   *Semantic:* Uses embeddings to find natural break points.
*   **Embedding Model Selection:**
    *   *Local:* (e.g., [Ollama](../../services/ollama.md) with `nomic-embed-text`, BGE, HuggingFace) for privacy and zero cost.
    *   *API-based:* (e.g., OpenAI, Cohere) for high performance with less local compute.
*   **Vector Store Selection:**
    *   Options include Chroma, Pinecone, Weaviate, or [pgvector](../../tools/infrastructure/index.md#sub-categories).
    *   See [Vector Databases in Infrastructure](../../tools/infrastructure/index.md#sub-categories).
*   **Retrieval Strategy:**
    *   *Similarity Search:* Standard vector distance (Cosine, Euclidean).
    *   *Maximal Marginal Relevance (MMR):* Balances relevance and diversity.
    *   *Hybrid Search:* Combines vector search with keyword-based (BM25) search.
*   **Re-ranking:** Using a second, more powerful model (e.g., Cohere Rerank) to re-order the top-k retrieved results for better precision.

## When to use it

*   When you need to ground LLM answers in facts.
*   When you have a large or frequently changing dataset.
*   When privacy prevents you from sending data to external model providers for fine-tuning.
*   When you need to cite sources for generated answers.

## When not to use it

*   When the answer is already well-covered by the LLM's base training data.
*   For purely creative writing tasks where factual grounding isn't required.
*   When the dataset is small enough to fit entirely within a large-context model's prompt (e.g., Gemini 1.5 Pro).
*   When ultra-low latency is required (RAG adds retrieval overhead).

## Related tools / concepts

*   **Orchestration Frameworks:** [LlamaIndex](../../tools/agents/index.md), [LangChain](../../tools/agents/index.md), Haystack
*   **RAG Platforms:** Dify, Flowise, RAGFlow
*   **Data Extraction:** Crawl4AI, Firecrawl, OCRmyPDF
*   **Infrastructure:** [Vector Databases](../../tools/infrastructure/index.md#sub-categories), [Embedding Models](../../tools/infrastructure/index.md#sub-categories)
*   **Evaluation:** RAGAS, DeepEval, TruLens

## Sources / references

*   [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al. 2020)](https://arxiv.org/abs/2005.11401)
*   [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511)
*   [RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval](https://arxiv.org/abs/2401.18059)
*   [From Local to Global: A GraphRAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130)

## Contribution Metadata

- Last reviewed: 2025-02-28
- Confidence: high
