# Data Copilot: Agentic RAG & Hybrid Retrieval

Diagnostic analytics often requires more than just a SQL query. Answering "Why did revenue drop?" requires looking at data (SQL), standard operating procedures (SOPs), policy changes (Meeting Notes), and external factors. This pattern defines an agentic retrieval system that decides between structured (SQL) and unstructured (Docs) sources.

## Goal
Enable the Data Copilot to answer complex diagnostic questions by deciding when to query SQL, documents, or both, and synthesizing the results with confidence scoring.

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

1.  **Step 1: Quantitative Baseline (Structured)**:
    - **Action**: Query SQL to establish the exact delta.
    - **Example**: "Net revenue for 'Smart Home' category fell by £12k (15%) week-over-week starting Tuesday."
2.  **Step 2: Event Correlation (Unstructured)**:
    - **Action**: Search RAG (Project Logs, GitHub PRs, Change logs) for events matching the "Tuesday" timestamp.
    - **Example**: Found PR #442: "Update pricing logic for Smart Home sensors."
3.  **Step 3: Hypothesis Generation (Reasoning)**:
    - **Action**: Use an LLM to link the revenue drop to the pricing change.
    - **Hypothesis**: "The new pricing logic might have increased the price beyond a psychological threshold ($99 -> $105)."
4.  **Step 4: Targeted Validation (Structured/Hybrid)**:
    - **Action**: Perform a specific SQL query to check the conversion rate vs. price change.
    - **Example**: "Compare conversion rate for sensors priced >$100 vs <$100."
5.  **Step 5: Root Cause Synthesis**:
    - **Action**: Combine SQL proof with document context into a final report.
    - **Result**: "Revenue dropped because the Tuesday deployment (PR #442) moved 5 top-selling sensors above the $100 price point, where conversion fell by 40%."

## Retrieval Sufficiency & Confidence Scoring

### Retrieval Sufficiency Matrix
Before synthesis, the agent must evaluate the retrieved data against this matrix:

| Component | Sufficient | Partially Sufficient | Insufficient |
| :--- | :--- | :--- | :--- |
| **Quantification** | Exact delta found in SQL. | General trend found, no exact numbers. | No data found in SQL. |
| **Causality** | Event found in RAG matching timestamp. | Event found, but timestamp is off. | No related logs found. |
| **Traceability** | Every claim has a source ID. | Some claims rely on model "general knowledge". | No citations available. |

**Action**: If "Insufficient" is reached in any category, the agent must trigger a "Knowledge Gap" alert instead of synthesizing an answer.

### Sufficiency Check
Before synthesis, the planner must ask: "Do I have enough information to answer the user's specific diagnostic question without guessing?"

**Criteria for Sufficiency**:
- **Source grounding**: Every claim in the synthesis must be traceable to a specific SQL row or document snippet.
- **Dimensional alignment**: If the SQL identifies a drop in a specific category (e.g., "Kitchen"), the RAG retrieval must have explicitly searched for that category.
- **Temporal alignment**: The quantitative change and the qualitative event must occur within a logical timeframe (e.g., event precedes or coincides with the change).

- **Low Sufficiency**: "I found the metric drop, but no corresponding notes in the logs."
- **Action**: Report findings but state the missing link.

### Confidence Scoring
The final score is calculated using these penalty weights:
- **Baseline**: 1.0
- **No direct causal link**: -0.3
- **Ambiguous SQL results**: -0.2
- **Old document context (>90 days)**: -0.15
- **Single source only**: -0.1

- **High (0.8 - 1.0)**: Direct match in SQL + explicit reason found in RAG.
- **Medium (0.5 - 0.7)**: Metric drop found, but reason is inferred from general policy.
- **Low (0.0 - 0.4)**: Correlating data found but no causal links.

## Example Q&A: Diagnostic

### Example 1: Home Finance
**Question**: "Why did my grocery spending spike last week?"

**Agent Logic**:
1.  **SQL Query**: Finds top categories for last week. (Result: 'Dining Out' is 3x higher than average).
2.  **RAG Query**: Search for "Dining", "Restaurants", or "Guests" in family logs/calendar. (Result: Found "Anniversary Dinner" on April 20).
3.  **Synthesis**: "Your spending spiked by £150 last week primarily due to 'Dining Out'. This is explained by the 'Anniversary Dinner' event found in your calendar for April 20."
4.  **Confidence**: 0.95 (Direct causal link found).

### Example 2: Business Metric
**Question**: "Why did conversion rate (Metric X) drop for the 'Outdoor' category?"

**Agent Logic**:
1.  **Step 1 (SQL)**: Compares conversion rate per category. (Result: 'Outdoor' category conversion fell from 3.2% to 1.8% starting Tuesday).
2.  **Step 2 (RAG)**: Searches project logs for "Outdoor category". (Result: Found entry in `dev_log.md`: "Deployed new image gallery component for Outdoor category on Tuesday morning").
3.  **Step 3 (Refined SQL)**: Queries for error rates in the Outdoor category. (Result: 404 errors on image assets spiked on Tuesday).
4.  **Synthesis**: "Conversion rate (Metric X) for the 'Outdoor' category dropped from 3.2% to 1.8% due to a buggy deployment of the new image gallery component on Tuesday, which caused image asset failures."
5.  **Confidence**: 0.90 (Strong correlation between deployment event and error spike).

## Sources / References
- [LangChain: Agentic RAG](https://python.langchain.com/docs/tutorials/rag/#agentic-rag)
- [Multi-hop RAG Strategies](https://github.com/langchain-ai/rag-from-scratch)

## Related tools / concepts
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Data Copilot MCP Tooling](data-copilot-mcp-tooling.md)
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md)
- [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md)
- [n8n Automation](../../services/n8n.md)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
- Related Issues: #188
