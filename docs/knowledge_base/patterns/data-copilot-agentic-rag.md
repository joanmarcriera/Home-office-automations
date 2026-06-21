# Data Copilot: Agentic RAG & Hybrid Retrieval

Diagnostic analytics often requires more than just a SQL query. Answering "Why did revenue drop?" requires looking at data (SQL), standard operating procedures (SOPs), policy changes (Meeting Notes), and external factors. This pattern defines an agentic retrieval system that decides between structured (SQL) and unstructured (Docs) sources.

## What it is
The Agentic RAG (Retrieval-Augmented Generation) and Hybrid Retrieval pattern is a sophisticated data access strategy where an AI agent acts as a dynamic planner. It determines the most effective way to answer a complex query by coordinating between structured data sources (like SQL databases) and unstructured data sources (like Markdown documentation or PDFs).

## What problem it solves
Traditional RAG often fails at complex diagnostic questions (e.g., "Why did revenue drop?") because the answer is split across multiple systems. Structured data provides the "what" (the numbers), while unstructured documents provide the "why" (policy changes, meeting notes, project logs). This pattern bridges that gap, providing a unified, causal explanation.

## Where it fits in the stack
This pattern resides at the **Reasoning & Orchestration Layer** of the [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md). It serves as the intelligence layer above the raw [MCP Tooling](data-copilot-mcp-tooling.md) and database connectors.

## Typical use cases
- **Root Cause Analysis**: Diagnosing business metric fluctuations by correlating data spikes with project logs.
- **Compliance Auditing**: Checking if financial transactions (SQL) adhere to corporate travel policies (RAG).
- **Customer Support**: Troubleshooting technical issues by matching user account history (SQL) with technical manuals (RAG).
- **Personal Finance**: Explaining spending anomalies by linking bank statements to calendar events and receipts.

## Strengths
- **Comprehensive Context**: Combines quantitative proof with qualitative reasoning.
- **Autonomous Investigation**: Can perform "multi-hop" queries to track down missing information without human intervention.
- **Late Interaction (ColBERT)**: By 2026, agentic RAG has pivoted towards "late interaction" models like ColBERTv2 for significantly higher retrieval precision in deep research tasks.
- **Traceability**: Provides a clear audit trail from the final answer back to both database rows and document snippets.

## Limitations
- **Latency**: Coordination between multiple retrieval steps and synthesis can be slower than simple RAG.
- **Complexity**: Requires sophisticated prompt engineering for the "Planner" agent to make correct routing decisions.
- **Compute Cost**: Multi-step reasoning chains consume significantly more tokens than single-shot retrieval.

## Hybrid Retrieval Workflow

```mermaid
flowchart TD
    User([User Question]) --> Planner[1. Agentic Planner]
    Planner --> SourceCheck{Which Sources?}

    SourceCheck -- Structured --> SQLAgent[2. SQL Agent Layer]
    SourceCheck -- Unstructured --> RAGAgent[3. RAG Agent Layer]
    SourceCheck -- Both --> SQLAgent & RAGAgent

    SQLAgent --> RetrievalCheck{Sufficient?}
    RAGAgent --> RetrievalCheck

    RetrievalCheck -- No: Need more info --> Planner
    RetrievalCheck -- Yes --> Synthesis[4. Synthesis Agent]

    Synthesis --> Output[/Diagnostic Answer/]
```

## Layers

### 1. Agentic Planner
- **Role**: Analyzes the refined intent to determine if the answer lies in the database, the knowledge base, or a combination.
- **Decision Logic**:
  - If the question involves "How many", "Total", "Top X" -> **SQL**.
  - If the question involves "Why", "Policy", "Process", "Who is responsible" -> **RAG**.
  - If the question is a root-cause diagnosis (e.g., "Why did metric X change?") -> **Hybrid**.

### 2. SQL Agent Layer
- Follows the [Layered Text-to-SQL Architecture](../../architecture/data-copilot-text-to-sql.md).

### 3. RAG Agent Layer
- Uses semantic search over unstructured documents (SOPs, meeting notes, project logs).
- **Tool**: MCP server exposing local Markdown files.

### 4. Synthesis Agent
- Combines the structured data points from SQL with the qualitative context from RAG.
- **Output Requirements**: Must state assumptions and provide a confidence score.

## Multi-hop Investigation Flow
For complex root-cause "Why" questions, the agent performs a recursive 5-step investigation:

1.  **Step 1: Quantitative Baseline (Structured)**: Establish the exact delta via SQL.
2.  **Step 2: Event Correlation (Unstructured)**: Search RAG (Project Logs, GitHub PRs) for matching timestamps.
3.  **Step 3: Hypothesis Generation (Reasoning)**: Link the quantitative proof to the qualitative context.
4.  **Step 4: Targeted Validation (Structured/Hybrid)**: Run specific SQL/RAG queries to prove/disprove the hypothesis.
5.  **Step 5: Root Cause Synthesis**: Combine proof into a final report with citations.

## Getting started
Implementing Agentic RAG requires an orchestration framework and access to both structured and unstructured data sources.

### Prerequisites
- **Orchestration**: [n8n](../../services/n8n.md) or a Python-based framework like [LangGraph](https://www.langchain.com/langgraph).
- **Structured Data**: Postgres or SQLite with an [MCP SQL Server](../../tools/automation_orchestration/mcp.md).
- **Unstructured Data**: Markdown files indexed in a vector DB or served via an [MCP Filesystem Server](../../tools/automation_orchestration/mcp.md).

### Basic Configuration
1.  Initialize your **Planner Agent** with a prompt that defines the `SourceCheck` logic.
2.  Connect your **SQL Agent** to your database using the [SQL Validation Playbook](../../playbooks/data-copilot-sql-validation.md).
3.  Connect your **RAG Agent** to your document store.
4.  Implement the **Synthesis Agent** using the [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md).

## CLI examples
While Agentic RAG is typically an API-driven workflow, you can test retrieval steps using CLI tools.

```bash
# Test SQL retrieval via MCP CLI
mcp-cli call sqlite_server query "SELECT SUM(amount) FROM transactions WHERE date > '2026-06-01'"

# Test RAG retrieval via MCP CLI
mcp-cli call filesystem_server search_docs "revenue drop meeting notes"
```

## When to use it
- Use when the answer requires synthesizing data from disparate silos (e.g., Jira + Postgres).
- Use for complex "Why" questions that require multiple reasoning steps and causal linking.
- Use when high traceability and confidence scoring are required for business or financial decisions.

## When not to use it
- Don't use for simple fact retrieval (e.g., "What is the capital of France?") where a basic RAG setup is faster.
- Don't use for pure data aggregation tasks (e.g., "Total sales by region") where Text-to-SQL alone is sufficient.
- Avoid when ultra-low latency is the primary requirement and synthesis overhead is unacceptable.

## API examples
The following example shows a simplified "Planner" logic in Python.

```python
def planner_route(query: str) -> str:
    structured_keywords = ["total", "count", "average", "highest"]
    unstructured_keywords = ["why", "policy", "process", "reason"]

    if any(k in query.lower() for k in structured_keywords) and any(k in query.lower() for k in unstructured_keywords):
        return "hybrid"
    elif any(k in query.lower() for k in unstructured_keywords):
        return "rag"
    else:
        return "sql"

# Example usage
route = planner_route("Why did grocery spending spike last week?")
print(f"Routing to: {route}") # Output: hybrid
```

## Related tools / concepts
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md) — The foundation for structured data access.
- [Data Copilot MCP Tooling](data-copilot-mcp-tooling.md) — The tool layer for agentic retrieval.
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md) — For ensuring SQL accuracy.
- [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md) — Standard for the final output.
- [n8n Automation](../../services/n8n.md) — Preferred orchestration engine for low-code environments.
- [RAG Pattern](rag-pattern.md) — The baseline for unstructured retrieval.
- [Agentic Workflows](agentic-workflows.md) — The broader concept of LLMs-as-Planners.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Standard for tool-agent communication.
- [Self-Healing Agents](../self-healing-agent-research.md) — For autonomous remediation of retrieval failures.
- [Late Interaction (ColBERT)](rag-pattern.md) — Advanced retrieval mechanism.

## Sources / References
- [LangChain: Agentic RAG](https://python.langchain.com/docs/tutorials/rag/#agentic-rag)
- [Multi-hop RAG Strategies](https://github.com/langchain-ai/rag-from-scratch)
- [Agentic RAG Guide 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026)
- [ColBERTv2: Effective and Efficient Retrieval](https://arxiv.org/abs/2112.01488)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
