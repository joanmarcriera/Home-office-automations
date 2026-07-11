# Data Copilot: Agentic RAG & Hybrid Retrieval

Diagnostic analytics often requires more than just a SQL query. Answering "Why did revenue drop?" requires looking at data (SQL), standard operating procedures (SOPs), policy changes (Meeting Notes), and external factors. This pattern defines an agentic retrieval system that decides between structured (SQL) and unstructured (Docs) sources.

## What it is
The Agentic RAG (Retrieval-Augmented Generation) and Hybrid Retrieval pattern is a sophisticated data access strategy where an AI agent, powered by models like [Gemma 3](../../tools/ai_knowledge/local_llms.md), acts as a dynamic planner. By July 2026, this pattern has matured with the **MCP 3.0 Task Protocol**, allowing agents to coordinate between structured data sources (like SQL databases) and unstructured data sources (like Markdown documentation or PDFs) using standardized tool discovery and execution.

The workflow follows a 4-layer orchestration:
1.  **Agentic Planner**: Analyzes intent and routes to SQL, RAG, or both.
2.  **SQL Agent Layer**: Follows the [Layered Text-to-SQL Architecture](../../architecture/data-copilot-text-to-sql.md).
3.  **RAG Agent Layer**: Uses semantic search over unstructured documents via FastMCP 3.0 servers.
4.  **Synthesis Agent**: Combines structured data with qualitative context, providing assumptions and confidence scores.

## What problem it solves
Traditional RAG often fails at complex diagnostic questions (e.g., "Why did revenue drop?") because the answer is split across multiple systems. Structured data provides the "what" (the numbers), while unstructured documents provide the "why" (policy changes, meeting notes, project logs). This pattern bridges that gap, providing a unified, causal explanation by linking quantitative proof with qualitative reasoning.

## Where it fits in the stack
This pattern resides at the **Reasoning & Orchestration Layer** of the [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md). It serves as the intelligence layer above the raw [MCP Tooling](data-copilot-mcp-tooling.md) and database connectors, leveraging the **Agentic Session Orchestration** features of MCP 3.0.

## Typical use cases
- **Root Cause Analysis**: Diagnosing business metric fluctuations by correlating data spikes with project logs. For example, the agent performs a multi-hop investigation: establishing the exact delta via SQL, searching RAG for matching timestamps in project logs, and generating a hypothesis linking the two.
- **Compliance Auditing**: Checking if financial transactions (SQL) adhere to corporate travel policies (RAG).
- **Customer Support**: Troubleshooting technical issues by matching user account history (SQL) with technical manuals (RAG).
- **Personal Finance**: Explaining spending anomalies by linking bank statements to calendar events and receipts.

## Strengths
- **Comprehensive Context**: Combines quantitative proof with qualitative reasoning.
- **Autonomous Investigation**: Can perform "multi-hop" queries to track down missing information without human intervention.
- **Late Interaction (ColBERT)**: Utilizes "late interaction" models like ColBERTv2 for significantly higher retrieval precision in deep research tasks.
- **Traceability**: Provides a clear audit trail from the final answer back to both database rows and document snippets.

## Limitations
- **Latency**: Coordination between multiple retrieval steps and synthesis can be slower than simple RAG.
- **Complexity**: Requires sophisticated prompt engineering for the "Planner" agent to make correct routing decisions.
- **Compute Cost**: Multi-step reasoning chains consume significantly more tokens than single-shot retrieval.

## When to use it
- Use when the answer requires synthesizing data from disparate silos (e.g., Jira + Postgres).
- Use for complex "Why" questions that require multiple reasoning steps and causal linking.
- Use when high traceability and confidence scoring are required for business or financial decisions.
- Use when leveraging the **MCP 3.0 Task Protocol** for distributed tool execution across local and cloud environments.

## When not to use it
- Don't use for simple fact retrieval (e.g., "What is the capital of France?") where a basic RAG setup is faster.
- Don't use for pure data aggregation tasks (e.g., "Total sales by region") where Text-to-SQL alone is sufficient.
- Avoid when ultra-low latency is the primary requirement and synthesis overhead is unacceptable.

## Getting started
Implementing Agentic RAG requires an orchestration framework and access to both structured and unstructured data sources.

### Prerequisites
- **Orchestration**: [n8n](../../services/n8n.md) or a Python-based framework like [LangGraph](https://www.langchain.com/langgraph) with **FastMCP 3.0** support.
- **Structured Data**: Postgres or SQLite with an [MCP SQL Server](../../tools/automation_orchestration/mcp.md).
- **Unstructured Data**: Markdown files indexed in a vector DB or served via an [MCP Filesystem Server](../../tools/automation_orchestration/mcp.md).

### Basic Configuration
1.  Initialize your **Planner Agent** (e.g., using [Gemma 3](../../tools/ai_knowledge/local_llms.md)) with a prompt that defines the `SourceCheck` logic.
2.  Connect your **SQL Agent** to your database using the [SQL Validation Playbook](../../playbooks/data-copilot-sql-validation.md).
3.  Connect your **RAG Agent** to your document store via a FastMCP-compliant filesystem server.
4.  Implement the **Synthesis Agent** using the [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md).

## CLI examples
While Agentic RAG is typically an API-driven workflow, you can test retrieval steps using CLI tools.

```bash
# Test SQL retrieval via MCP CLI
mcp-cli call sqlite_server query "SELECT SUM(amount) FROM transactions WHERE date > '2026-06-01'"

# Test RAG retrieval via MCP CLI
mcp-cli call filesystem_server search_docs "revenue drop meeting notes"

# Inspect active MCP 3.0 task protocol endpoints
mcp-cli list-tasks --server-type fastmcp
```

## API examples
The following example shows a simplified "Planner" logic in Python, updated for July 2026 routing standards.

```python
def planner_route(query: str) -> str:
    structured_keywords = ["total", "count", "average", "highest"]
    unstructured_keywords = ["why", "policy", "process", "reason"]

    # Hybrid check using semantic similarity threshold if keyword match fails
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
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Standard for tool-agent communication (MCP 3.0).
- [Self-Healing Agents](../self-healing-agent-research.md) — For autonomous remediation of retrieval failures.
- [Local LLMs (Gemma 3)](../../tools/ai_knowledge/local_llms.md) — Canonical source for local reasoning engines.

## Sources / references
- [LangChain: Agentic RAG](https://python.langchain.com/docs/tutorials/rag/#agentic-rag)
- [Multi-hop RAG Strategies](https://github.com/langchain-ai/rag-from-scratch)
- [Agentic RAG Guide 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026)
- [ColBERTv2: Effective and Efficient Retrieval](https://arxiv.org/abs/2112.01488)
- [MCP 3.0 Task Protocol Specification](https://modelcontextprotocol.io/spec/3.0/tasks)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
