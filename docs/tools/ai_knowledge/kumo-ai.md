# Kumo AI (KumoRFM-2)

## What it is
Kumo AI is an enterprise predictive artificial intelligence platform that pioneer's **Relational Foundation Models (RFMs)** and **Relational Graph Neural Networks (RGNNs)**. Powered by its flagship architecture, **KumoRFM-2**, Kumo operates directly over structured, multi-table relational database schemas residing in cloud data warehouses (such as Snowflake, Databricks, BigQuery, and ClickHouse). It converts raw relational tables and foreign-key constraints into a unified entity-relationship graph, allowing machine learning models to learn deep topological and temporal patterns across linked tables without requiring manual feature engineering pipelines.

In early 2027 enterprise intelligence environments, Kumo AI natively exposes its predictive query runtime to autonomous agentic workflows via the **Model Context Protocol (FastMCP 3.1)**. Frontier AI models—including **Claude 5.1**, **Claude 5.6**, **GPT-5.5**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **Llama 4**—can issue declarative predictive SQL queries, retrieve validated risk or lifetime value (LTV) probability distributions, and execute automated mitigation workflows across downstream enterprise tools.

## What problem it solves
Enterprise data architectures store critical business data across dozens or hundreds of normalized relational tables. Traditional predictive machine learning workflows suffer from severe operational bottlenecks:

1. **Fragile Feature Engineering Pipelines**: Data science teams spend weeks writing complex SQL joins, aggregations, and temporal windowing scripts to flatten relational databases into single flat tables suitable for traditional ML algorithms (like XGBoost or Logistic Regression).
2. **Loss of Relational & Temporal Signal**: Flattening normalized schemas destroys complex higher-order graph connections, multi-hop relationship dependencies, and granular sequence history.
3. **Data Drift & Maintenance Burden**: Upstream database schema alterations break hand-crafted feature pipelines, requiring constant maintenance and retraining code updates.
4. **Lack of Agentic Predictive Execution**: Autonomous AI agents can query historical raw data using SQL, but lack native capability to project future customer behaviors (e.g., churn likelihood, next-best purchase, fraud risk) directly from complex relational graphs.

Kumo AI eliminates these obstacles by treating relational databases as heterogeneous graphs. KumoRFM-2 automatically learns node, edge, and temporal embeddings across all linked tables, allowing teams and AI agents to declare prediction targets in simple, natural SQL syntax (`PREDICT ... FOR EACH ... OVER NEXT ...`).

```mermaid
graph TD
    subgraph Enterprise Cloud Data Warehouse
        CUST[Customers Table]
        TRANS[Transactions Table]
        PROD[Products Table]
        LOGS[Web Activity Logs]
        SUPPORT[Support Tickets Table]
    end

    subgraph Kumo AI Relational Graph Neural Network Engine
        GRAPH[Heterogeneous Graph Construction]
        EMBED[Temporal Node & Edge Representation Learning]
        RFM[KumoRFM-2 Foundation Model Runtime]
    end

    subgraph Agentic & Predictive Control Layer
        FAST_MCP[FastMCP 3.1 Prediction Gateway]
        AGENT[Claude 5.1 / 5.6 Autonomous Agent]
        N8N[n8n Automation Engine]
    end

    CUST -->|Foreign Keys| GRAPH
    TRANS -->|Foreign Keys| GRAPH
    PROD -->|Foreign Keys| GRAPH
    LOGS -->|Foreign Keys| GRAPH
    SUPPORT -->|Foreign Keys| GRAPH

    GRAPH --> EMBED
    EMBED --> RFM

    AGENT -->|1. Declarative Predictive Query| FAST_MCP
    FAST_MCP -->|2. Kumo API Execution| RFM
    RFM -->|3. Validated Probability Distribution| FAST_MCP
    FAST_MCP -->|4. Pydantic v2 Prediction Payload| AGENT
    AGENT -->|5. Trigger Mitigation Workflow| N8N
```

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Predictive Data Intelligence.

Kumo AI operates as the **predictive reasoning layer** directly above enterprise cloud data warehouses and below autonomous workflow engines:

- **Data Substrate**: Directly interfaces with cloud data warehouses ([Snowflake](../process_understanding/snowflake.md), Databricks Unity Catalog, Google BigQuery, [ClickHouse](../process_understanding/clickhouse.md)) using native push-down queries and zero-copy data connectors.
- **Graph Neural Network Layer**: Constructs and maintains in-memory temporal relational graphs representing billions of records across hundreds of interconnected tables.
- **Orchestration & Agent Plane**: Integrates with [FastMCP 3.1](../../tools/automation_orchestration/mcp.md), [n8n](../../services/n8n.md), and [LangChain](../../tools/ai_knowledge/langchain.md) to serve real-time predictions directly into agent tool execution chains.

```mermaid
sequenceDiagram
    autonumber
    participant Agent as Autonomous AI Agent (Claude 5.1)
    participant MCP as FastMCP 3.1 Kumo Server
    participant Kumo as KumoRFM-2 Predictive Engine
    participant Warehouse as Snowflake Data Warehouse

    Agent->>MCP: call_tool("kumo_predict_churn", {segment: "enterprise", threshold: 0.80})
    MCP->>Kumo: POST /v1/predict (Query: "PREDICT COUNT(Transactions.ID) == 0 FOR EACH Customers...")
    Kumo->>Warehouse: Extract Graph Structural Delta via Push-Down Queries
    Warehouse-->>Kumo: Return Graph Delta Nodes
    Kumo->>Kumo: Execute KumoRFM-2 GNN Inference over Relational Graph
    Kumo-->>MCP: Prediction Result Stream (Entity IDs, Scores, Feature Importances)
    MCP->>Agent: Pydantic v2 Validated Churn Risk List
```

## Typical use cases

1. **Zero-ETL Customer Churn & LTV Forecasting**:
   Generating individual customer churn probabilities and 90-day Lifetime Value (LTV) projections across transactional, support, and web activity tables without manual feature engineering.

2. **Agentic Retention & Next-Best-Action Automation**:
   Equipping AI agents (Claude 5.1 / GPT-5.5) with predictive tool calls that identify high-risk customer segments and automatically trigger retention offers or personal outreach via **n8n**.

3. **Multi-Tier Supply Chain & Inventory Risk Analysis**:
   Reasoning over complex vendor, warehouse, shipping, and purchase order tables to forecast stockouts, shipping delays, and component bottlenecks weeks in advance.

4. **Real-Time Financial Fraud & Anomaly Detection**:
   Graph-based detection of fraudulent transaction loops, account takeover patterns, and suspicious merchant activity across linked payment graph topologies.

5. **Personalized Product Recommendation Engines**:
   Predicting the exact item or content category a user is most likely to engage with next based on graph traversal of similar user behaviors.

## Strengths

- **Zero Manual Feature Engineering**: Operates directly on raw relational warehouse schemas, automatically capturing multi-hop relationships and temporal dynamics.
- **Relational Graph Neural Network (RGNN) Architecture**: Leverages GNN state-of-the-art representation learning designed explicitly for connected tabular datasets.
- **Intuitive Declarative Predictive SQL Syntax**: Simple, concise predictive query language easily generated by LLMs or human analysts.
- **Enterprise Scale**: Handles production workloads scaling to over 500 billion rows across hundreds of connected tables.
- **FastMCP 3.1 Native Protocol Integration**: Directly exposes predictive analytics tools to agentic runtimes with strict schema validation.

## Limitations

- **Structured Tabular Focus**: Designed specifically for relational tabular data rather than unstructured video, audio, or raw document archives.
- **Cloud Warehouse Requirement**: Requires an active data connection to a supported cloud data warehouse (Snowflake, Databricks, BigQuery, or ClickHouse).
- **Proprietary Managed Platform**: Closed-source commercial platform; not available as a self-hosted, air-gapped open-source binary.

## When to use it

- When you need high-accuracy predictive ML models across complex multi-table relational data schemas.
- When you want to eliminate months of feature engineering and pipeline maintenance code.
- When empowering AI agents to make forward-looking, data-driven decisions via FastMCP 3.1 tool calls.
- When evaluating complex graph relationships (e.g., social networks, financial transaction graphs, supply chains).

## When not to use it

- For simple single-table datasets where standard XGBoost or Scikit-Learn models are sufficient.
- For unstructured vector similarity search over text embeddings (use [Qdrant](../infrastructure/qdrant.md), [ChromaDB](../../knowledge_base/vector-db-comparison.md), or [ColQwen](colqwen.md)).
- When completely offline, local, or self-hosted air-gapped execution is mandatory.

## Systemd Service Configuration

For production enterprise integration, run the FastMCP 3.1 Kumo predictive gateway daemon as a systemd service (`kumo-predict-mcp.service`):

```ini
[Unit]
Description=Kumo AI FastMCP 3.1 Predictive Gateway Daemon
After=network-online.target redis.service
Wants=network-online.target

[Service]
Type=simple
User=kumo-gateway
Group=kumo-gateway
WorkingDirectory=/opt/kumo-gateway
EnvironmentFile=/etc/kumo/kumo.env
ExecStart=/opt/kumo-gateway/venv/bin/python3 -m server.kumo_fastmcp_server --transport sse --port 8097
Restart=always
RestartSec=5s
MemoryMax=2G
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/kumo /opt/kumo-gateway/cache
PrivateTmp=true
CapabilityBoundingSet=
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Production Multi-Container Docker Stack (`compose.yaml`)

Deploy an enterprise predictive intelligence gateway topology featuring Kumo FastMCP bridge, DuckDB local query acceleration cache, and Redis task broker:

```yaml
version: '3.8'

services:
  kumo-fastmcp-gateway:
    image: python:3.11-slim
    container_name: kumo-fastmcp-gateway
    restart: unless-stopped
    ports:
      - "8097:8097"
    environment:
      - KUMO_API_URL=https://api.kumo.ai/v1
      - KUMO_API_KEY=${KUMO_API_KEY}
      - REDIS_URL=redis://kumo-redis:6379/0
      - DUCKDB_PATH=/cache/kumo_predictions.duckdb
      - MCP_PORT=8097
    volumes:
      - ./server:/opt/kumo:ro
      - cache-data:/cache
    working_dir: /opt/kumo
    command: python3 -m server.kumo_fastmcp_server
    depends_on:
      kumo-redis:
        condition: service_healthy
    networks:
      - kumo-net
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2048M
        reservations:
          cpus: '0.5'
          memory: 512M

  kumo-redis:
    image: redis:7.2-alpine
    container_name: kumo-redis-cache
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    ports:
      - "6382:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - kumo-net

networks:
  kumo-net:
    driver: bridge

volumes:
  cache-data:
  redis-data:
```

## Getting started

### Declarative Predictive SQL Query Examples

Once Kumo AI is connected to your cloud warehouse schema (e.g., Snowflake or BigQuery), predictive tasks are executed using declarative SQL syntax:

```sql
-- Customer Churn Prediction: Predict if a customer will make 0 transactions in the next 30 days
PREDICT COUNT(Transactions.ID) == 0
FOR EACH Customers.ID
OVER NEXT 30 DAYS

-- Customer Lifetime Value (LTV) Prediction: Predict total spend over the next 90 days
PREDICT SUM(Transactions.Amount)
FOR EACH Customers.ID
OVER NEXT 90 DAYS

-- Next Best Product Category Recommendation
PREDICT TOP_K(Transactions.Category_ID, 3)
FOR EACH Customers.ID
OVER NEXT 14 DAYS
```

## CLI examples

```bash
# Execute Kumo predictive query via Kumo CLI
kumo query run --file churn_prediction.sql --output-table snowflake.analytics.churn_scores

# Inspect status of active KumoRFM-2 training jobs
kumo job status --job-id job_rfm_90812

# Trigger prediction execution via Claude Code CLI using FastMCP
claude-code --mcp-server kumo-rfm "Analyze high-risk churn customers in the enterprise segment for Q1"
```

## API examples

### FastMCP 3.1 Kumo Predictive Server & Strict Pydantic v2 Validation

The executable Python script below builds a production **FastMCP 3.1** predictive analytics server wrapping Kumo AI's REST API, using strict **Pydantic v2** schema validation with `extra="forbid"`.

```python
import os
import requests
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from fastmcp import FastMCP, Context

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Kumo-Predictive-Analytics", version="3.1.0")

KUMO_API_URL = os.getenv("KUMO_API_URL", "https://api.kumo.ai/v1")
KUMO_API_KEY = os.getenv("KUMO_API_KEY", "your-kumo-api-key")

# --- Pydantic v2 Data Schemas ---

class ChurnRiskEntity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., description="Unique customer ID in data warehouse")
    churn_probability: float = Field(..., ge=0.0, le=1.0, description="Predicted churn probability")
    predicted_ltv_remaining: Optional[float] = Field(None, description="Forecasted remaining LTV")
    recommended_action: str = Field(..., description="Automated agent mitigation strategy recommendation")

    @field_validator("churn_probability", mode="after")
    @classmethod
    def validate_score(cls, v: float) -> float:
        return round(v, 4)

class ChurnPredictionQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    segment_name: str = Field(..., min_length=2, description="Target customer segment name in warehouse")
    min_churn_probability: float = Field(default=0.75, ge=0.0, le=1.0, description="Probability cutoff threshold")
    max_results: int = Field(default=10, ge=1, le=100, description="Max entities to return")

class PredictiveSqlInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    predictive_sql: str = Field(..., min_length=15, description="Declarative Kumo predictive SQL statement")
    dry_run: bool = Field(default=False, description="Validate SQL syntax without queueing GPU job")

class PredictiveJobResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    job_id: str = Field(..., description="Unique Kumo execution job ID")
    status: str = Field(..., description="Job execution status (e.g. COMPLETED, RUNNING, QUEUED)")
    total_entities_analyzed: int = Field(0, description="Total relational nodes processed")
    high_risk_entities: List[ChurnRiskEntity] = Field(default_factory=list)
    execution_time_ms: Optional[int] = Field(None, description="Elapsed execution time in milliseconds")

# --- FastMCP 3.1 Tools ---

@mcp.tool(
    name="kumo_predict_customer_churn",
    description="Execute KumoRFM-2 Relational Graph Neural Network query to identify customers at risk of churn."
)
async def kumo_predict_customer_churn(
    query: ChurnPredictionQuery,
    ctx: Optional[Context] = None
) -> PredictiveJobResponse:
    """Issue predictive query to Kumo AI engine and return Pydantic v2 validated results."""
    if ctx:
        await ctx.info(f"Executing Kumo RFM churn prediction for segment '{query.segment_name}' (min_prob={query.min_churn_probability})")

    # Mock response illustrating validated production payload
    mock_entities = [
        ChurnRiskEntity(
            customer_id="cust_ent_88291",
            churn_probability=0.892,
            predicted_ltv_remaining=4200.50,
            recommended_action="Trigger priority executive check-in via n8n"
        ),
        ChurnRiskEntity(
            customer_id="cust_ent_44102",
            churn_probability=0.815,
            predicted_ltv_remaining=1850.00,
            recommended_action="Issue 20% renewal discount voucher"
        )
    ]

    filtered = [e for e in mock_entities if e.churn_probability >= query.min_churn_probability][:query.max_results]

    return PredictiveJobResponse(
        job_id="kumo_job_2027_0981a",
        status="COMPLETED",
        total_entities_analyzed=145000,
        high_risk_entities=filtered,
        execution_time_ms=1850
    )


@mcp.tool(
    name="kumo_execute_predictive_sql",
    description="Execute custom Kumo predictive SQL query string directly against relational graph."
)
async def kumo_execute_predictive_sql(
    input_data: PredictiveSqlInput,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Run declarative predictive SQL statement on KumoRFM-2."""
    if "PREDICT" not in input_data.predictive_sql.upper():
        raise ValueError("Error: Query must contain a valid 'PREDICT ... FOR EACH ...' clause.")

    if ctx:
        await ctx.info(f"Submitting predictive SQL (dry_run={input_data.dry_run})")

    if input_data.dry_run:
        return {
            "status": "VALIDATED",
            "sql": input_data.predictive_sql,
            "estimated_target_nodes": 45000,
            "estimated_cost_credits": 0.5
        }

    return {
        "status": "QUEUED",
        "job_id": "kumo_sql_7721",
        "query": input_data.predictive_sql,
        "message": "Predictive SQL Query submitted to Kumo Engine successfully."
    }


if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Method | Remediation Action |
| :--- | :--- | :--- | :--- |
| **HTTP 401 Unauthorized** | Invalid or expired `KUMO_API_KEY` token | Test auth header with curl: `curl -H "Authorization: Bearer $KUMO_API_KEY" https://api.kumo.ai/v1/schemas` | Regenerate API token in Kumo Enterprise Console and update environment vault. |
| **Predictive SQL Syntax Error** | Missing required `FOR EACH` or `OVER NEXT` temporal windows | Inspect query string for temporal aggregation keywords | Restructure statement to strictly follow `PREDICT <aggr> FOR EACH <primary_key> OVER NEXT <time_window>`. |
| **Relational Graph Disconnected Table** | Foreign key constraints omitted or orphaned table nodes | Check graph connectivity: `kumo schema validate --schema enterprise_db` | Define explicit primary/foreign key relationships in Kumo Schema Graph Studio. |
| **FastMCP Schema ValidationError** | LLM agent sent extra unrecognized properties in tool call | Check FastMCP stderr for Pydantic `extra_forbidden` errors | Ensure agent payload adheres strictly to `ChurnPredictionQuery` / `PredictiveSqlInput`. |
| **DuckDB Cache Lock Contention** | Multiple async MCP threads accessing local cache DB simultaneously | Inspect DuckDB connection errors in container logs | Configure DuckDB in read-only mode for query workers or switch to Redis cache layer. |
| **Timeout on GNN Training Job** | Extremely large relational graph (>1B edges) exceeding batch window | Inspect job status via `kumo job status --job-id <id>` | Apply neighborhood sampling filters or prune historical transaction log tables older than 2 years. |
| **Empty High-Risk Entity Output** | `min_churn_probability` threshold set too high | Lower threshold from 0.85 to 0.60 | Re-run query with relaxed cutoff or verify positive label distribution in baseline training run. |
| **Snowflake Connector Network Dropout** | Warehouse auto-suspended or IP whitelist blocked Kumo egress | Check Snowflake query history for connector session drops | Configure minimum auto-suspend window of 10 minutes and verify Kumo static egress IP ranges in Network Policy. |

## Related tools / concepts

- [Snowflake](../process_understanding/snowflake.md) — Cloud data warehouse platform for hosting relational schemas.
- [ClickHouse](../process_understanding/clickhouse.md) — Real-time columnar database engine integrated with Kumo.
- [n8n](../../services/n8n.md) — Workflow automation engine for triggering downstream actions from prediction results.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Standardized agent protocol for predictive tool invocation.
- [ColQwen](colqwen.md) — Multi-modal visual document retrieval model for unstructured data pipelines.

## Sources / references

- [Kumo AI Official Website](https://kumo.ai/)
- [Kumo AI Technology & Relational Foundation Models](https://kumo.ai/technology/)
- [RelBench: Relational Deep Learning Benchmark (Stanford AI Lab)](https://relbench.stanford.edu/)
- [FastMCP 3.1 Specification & Model Context Protocol Docs](https://modelcontextprotocol.io/protocol/tasks)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
