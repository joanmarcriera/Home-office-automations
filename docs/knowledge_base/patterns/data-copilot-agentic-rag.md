# Data Copilot: Agentic RAG & Hybrid Retrieval

Diagnostic analytics often requires more than just a SQL query. Answering "Why did revenue drop?" requires looking at data (SQL), standard operating procedures (SOPs), policy changes (Meeting Notes), and external factors. This pattern defines an agentic retrieval system that decides between structured (SQL) and unstructured (Docs) sources.

## What it is
The Agentic RAG (Retrieval-Augmented Generation) and Hybrid Retrieval pattern is a sophisticated data access strategy where an AI agent acts as a dynamic planner. In late October / November 2026, this pattern has matured with [Gemma 3](../../tools/ai_knowledge/local_llms.md) and [Llama 4](../../tools/ai_knowledge/local_llms.md) providing high-efficiency local planning and the **MCP 3.1 Task Protocol** standardizing how agents hand off sub-tasks between specialized retrieval tools. It determines the most effective way to answer a complex query by coordinating between structured data sources (like SQL databases) and unstructured data sources (like Markdown documentation or PDFs).

### Hybrid Retrieval Workflow

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

## What problem it solves
Traditional RAG often fails at complex diagnostic questions (e.g., "Why did revenue drop?") because the answer is split across multiple systems. Structured data provides the "what" (the numbers), while unstructured documents provide the "why" (policy changes, meeting notes, project logs). This pattern bridges that gap, providing a unified, causal explanation.

## Where it fits in the stack
This pattern resides at the **Reasoning & Orchestration Layer** of the [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md). It serves as the intelligence layer above the raw [MCP Tooling](data-copilot-mcp-tooling.md) and database connectors, leveraging **FastMCP 3.1** for low-latency tool discovery and execution.

## Typical use cases
- **Root Cause Analysis**: Diagnosing business metric fluctuations by correlating data spikes with project logs.
- **Compliance Auditing**: Checking if financial transactions (SQL) adhere to corporate travel policies (RAG).
- **Customer Support**: Troubleshooting technical issues by matching user account history (SQL) with technical manuals (RAG).
- **Personal Finance**: Explaining spending anomalies by linking bank statements to calendar events and receipts.
- **Planner Logic Validation**: Programmatically routing queries using schema validation models in Python.

## Strengths
- **Comprehensive Context**: Combines quantitative proof with qualitative reasoning.
- **Autonomous Investigation**: Can perform "multi-hop" queries to track down missing information without human intervention.
- **Late Interaction (ColBERT)**: By late 2026, agentic RAG has pivoted towards "late interaction" models like ColBERTv2 for significantly higher retrieval precision in deep research tasks.
- **Traceability**: Provides a clear audit trail from the final answer back to both database rows and document snippets.

## Limitations
- **Latency**: Coordination between multiple retrieval steps and synthesis can be slower than simple RAG.
- **Complexity**: Requires sophisticated prompt engineering for the "Planner" agent to make correct routing decisions.
- **Compute Cost**: Multi-step reasoning chains consume significantly more tokens than single-shot retrieval.

## When to use it
- Use when the answer requires synthesizing data from disparate silos (e.g., Jira + Postgres).
- Use for complex "Why" questions that require multiple reasoning steps and causal linking.
- Use when high traceability and confidence scoring are required for business or financial decisions.

## When not to use it
- Don't use for simple fact retrieval (e.g., "What is the capital of France?") where a basic RAG setup is faster.
- Don't use for pure data aggregation tasks (e.g., "Total sales by region") where Text-to-SQL alone is sufficient.
- Avoid when ultra-low latency is the primary requirement and synthesis overhead is unacceptable.

## Getting started
Implementing Agentic RAG requires an orchestration framework and access to both structured and unstructured data sources.

### Layers

#### 1. Agentic Planner
- **Role**: Analyzes the refined intent to determine if the answer lies in the database, the knowledge base, or a combination.
- **Decision Logic**:
  - If the question involves "How many", "Total", "Top X" -> **SQL**.
  - If the question involves "Why", "Policy", "Process", "Who is responsible" -> **RAG**.
  - If the question is a root-cause diagnosis (e.g., "Why did metric X change?") -> **Hybrid**.

#### 2. SQL Agent Layer
- Follows the [Layered Text-to-SQL Architecture](../../architecture/data-copilot-text-to-sql.md).

#### 3. RAG Agent Layer
- Uses semantic search over unstructured documents (SOPs, meeting notes, project logs).
- **Tool**: MCP server exposing local Markdown files.

#### 4. Synthesis Agent
- Combines the structured data points from SQL with the qualitative context from RAG.
- **Output Requirements**: Must state assumptions and provide a confidence score.

### Multi-hop Investigation Flow
For complex root-cause "Why" questions, the agent performs a recursive 5-step investigation:

1.  **Step 1: Quantitative Baseline (Structured)**: Establish the exact delta via SQL.
2.  **Step 2: Event Correlation (Unstructured)**: Search RAG (Project Logs, GitHub PRs) for matching timestamps.
3.  **Step 3: Hypothesis Generation (Reasoning)**: Link the quantitative proof to the qualitative context.
4.  **Step 4: Targeted Validation (Structured/Hybrid)**: Run specific SQL/RAG queries to prove/disprove the hypothesis.
5.  **Step 5: Root Cause Synthesis**: Combine proof into a final report with citations.

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

## API examples

### Agentic Planner Route Schema (Python & Pydantic v2)
The following Python script defines how a Planner Agent routes incoming requests, validating and scoring the classification using modern Pydantic v2 models.

```python
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class RouteDestination(str, Enum):
    """The target retrieval system for the query."""
    SQL = "sql"
    RAG = "rag"
    HYBRID = "hybrid"

class QueryAnalysis(BaseModel):
    """Pydantic v2 schema for capturing planner-analyzed query parameters and routing."""
    original_query: str = Field(..., description="The unmodified user request query string")
    route: RouteDestination = Field(..., description="Calculated routing destination based on keywords and heuristics")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="The planner's classification confidence")
    extracted_keywords: List[str] = Field(default_factory=list, description="Extracted semantic entities or keywords")

    @field_validator("route", mode="before")
    @classmethod
    def apply_keyword_heuristics(cls, v: str, info) -> str:
        """Heuristically override route based on presence of key terms if classification is ambiguous."""
        query = info.data.get("original_query", "").lower()
        structured_keywords = ["total", "count", "average", "highest", "percent"]
        unstructured_keywords = ["why", "policy", "process", "reason", "explain"]

        has_struct = any(k in query for k in structured_keywords)
        has_unstruct = any(k in query for k in unstructured_keywords)

        if has_struct and has_unstruct:
            return RouteDestination.HYBRID
        elif has_unstruct:
            return RouteDestination.RAG
        elif has_struct:
            return RouteDestination.SQL
        return v

# Example Verification Usage
if __name__ == "__main__":
    test_payload = {
        "original_query": "Why did grocery spending spike in June?",
        "route": "sql", # Will be heuristically overridden to hybrid
        "confidence_score": 0.95,
        "extracted_keywords": ["grocery", "spending", "spike", "june"]
    }

    try:
        analyzed_query = QueryAnalysis.model_validate(test_payload)
        print(f"Analysis Succeeded! Route: {analyzed_query.route.value}")
        print(f"Confidence: {analyzed_query.confidence_score}")
    except ValidationError as e:
        print(f"Validation failed: {e.json(indent=2)}")
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
- [Local LLMs (Gemma 3)](../../tools/ai_knowledge/local_llms.md) — High-efficiency local planners for agentic loops.
- [FastMCP](../../tools/automation_orchestration/mcp.md) — High-performance tool discovery and communication.

## Sources / References
- [LangChain: Agentic RAG](https://python.langchain.com/docs/tutorials/rag/#agentic-rag)
- [Multi-hop RAG Strategies](https://github.com/langchain-ai/rag-from-scratch)
- [Agentic RAG Guide 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026)
- [ColBERTv2: Effective and Efficient Retrieval](https://arxiv.org/abs/2112.01488)

## Contribution Metadata
- Last reviewed: 2026-11-20
- Confidence: high
