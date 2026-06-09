# Snowflake

## What it is
Snowflake is a cloud-based data warehousing platform that allows for the storage, processing, and analysis of vast amounts of data. As of June 2026, it has evolved into a comprehensive AI Data Cloud, providing a highly scalable and flexible architecture for modern data needs, including native LLM processing.

## What problem it solves
It eliminates the complexities of managing traditional on-premises data warehouses. Snowflake provides a unified platform for data engineering, data lakes, data science, and data sharing, enabling organizations to gain insights from their data more efficiently. It particularly excels at:
- **Centralizing AI Telemetry**: Consolidating traces from models like **Claude 4.7**, **GPT-5.5**, and **Llama 4 Maverick**.
- **Model Context Integration**: Using **MCP (Model Context Protocol)** to bridge enterprise data in Snowflake with agentic workflows.
- **In-place AI Processing**: Running inference directly on sensitive data without egressing to external providers via **Snowflake Cortex**.

## Where it fits in the stack
Snowflake sits in the **Data Storage and Analytics** layer. It serves as the enterprise-grade back-end for storing and querying logs, traces, and metrics, and increasingly as a compute provider for LLM-based data transformations.

## Typical use cases
- **AI Log Archiving**: Storing structured traces and JSON logs from AI providers (via [OpenRouter](../ai_knowledge/openrouter.md) Broadcast) for long-term audit and compliance.
- **Generative AI Workflows**: Using **Snowflake Cortex** functions (e.g., `AI_COMPLETE`, `AI_EXTRACT`) to process data directly where it resides.
- **Document Intelligence**: Extracting structured data from PDFs and images using `AI_PARSE_DOCUMENT`.
- **Business Intelligence**: Powering dashboards that correlate AI performance with business outcomes.
- **Data Engineering**: Using Snowpark to process and transform large volumes of AI-generated data using Python or SQL.
- **Secure Data Sharing**: Sharing AI telemetry data with partners or third-party auditors without moving the data.

## Strengths
- **Decoupled Compute and Storage**: Scale processing power independently of storage capacity, optimizing costs for variable AI workloads.
- **Multi-Cloud Support**: Available on AWS, Azure, and Google Cloud, preventing vendor lock-in.
- **Zero-Copy Cloning**: Create instant copies of production AI log tables for testing and development without additional storage costs.
- **Native JSON Support**: Efficiently handles the semi-structured JSON data produced by LLM providers.
- **Governance and Security**: Enterprise-grade access control and encryption for sensitive AI training and inference data.

## Limitations
- **Cloud-Only**: Cannot be run locally or in air-gapped environments.
- **Latency for Small Queries**: Optimized for massive analytical queries; may have higher latency for very small, transactional-style queries.
- **Cost Complexity**: Usage-based pricing can become expensive if large-scale AI processing (like frequent `AI_COMPLETE` calls) is not monitored.

## When to use it
- When you have massive volumes of AI log data that require enterprise-grade storage and complex analytical processing.
- If you need to perform "AI next to your data" using built-in LLM functions without moving sensitive information to external APIs.
- When you require multi-cloud flexibility or secure data sharing with third parties.
- For RAG systems where the knowledge base already resides in Snowflake.

## When not to use it
- For small-scale projects where a simpler database like [ClickHouse](clickhouse.md) or even SQLite would suffice.
- If you require an on-premises or fully local-first solution.
- For high-frequency, low-latency transactional writes that aren't primarily for analytical purposes.

## Getting started

### Installation (SnowSQL CLI)
```bash
# macOS (using Homebrew)
brew install --cask snowflake-snowsql
```

### Initial Configuration
Configure your connection in `~/.snowsql/config`:
```ini
[connections.my_conn]
accountname = <account_identifier>
username = <user>
password = <password>
```

### OpenRouter Log Ingestion Schema
Before connecting OpenRouter, create the following table in your Snowflake database:

```sql
CREATE TABLE OPENROUTER_TRACES (
    TIMESTAMP TIMESTAMP_NTZ,
    ID STRING,
    MODEL STRING,
    APP_ID STRING,
    USER_ID STRING,
    PROMPT_TOKENS NUMBER,
    COMPLETION_TOKENS NUMBER,
    TOTAL_TOKENS NUMBER,
    TOTAL_COST FLOAT,
    LATENCY FLOAT,
    STATUS STRING,
    REQUEST VARIANT,
    RESPONSE VARIANT
);
```

## CLI examples

### Connect via SnowSQL
```bash
snowsql -c my_conn
```

### Run an AI Query from CLI
Using Cortex functions to summarize a log entry:
```bash
snowsql -c my_conn -q "SELECT SNOWFLAKE.CORTEX.SUMMARIZE(RESPONSE:choices[0].message.content) FROM OPENROUTER_TRACES LIMIT 1"
```

### Upload a Local File to a Stage
```bash
snowsql -c my_conn -q "PUT file:///path/to/traces.jsonl @my_stage"
```

## API examples

### Python (snowflake-connector-python)
```python
import snowflake.connector

# Connect to Snowflake
ctx = snowflake.connector.connect(
    user='<user>',
    password='<password>',
    account='<account_identifier>',
    warehouse='COMPUTE_WH',
    database='AI_OBSERVABILITY',
    schema='PUBLIC'
)

# Execute a query to compare Claude 4.7 vs GPT-5.5 usage
try:
    cursor = ctx.cursor()
    cursor.execute("""
        SELECT MODEL, SUM(TOTAL_COST), AVG(LATENCY)
        FROM OPENROUTER_TRACES
        WHERE MODEL IN ('anthropic/claude-4.7', 'openai/gpt-5.5')
        GROUP BY MODEL
    """)
    for (model, cost, latency) in cursor:
        print(f"Model: {model} | Total Cost: ${cost:.2f} | Avg Latency: {latency:.2f}s")
finally:
    ctx.close()
```

### Snowpark (Python API)
Using Snowpark for more complex AI data processing:

```python
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, call_udf

session = Session.builder.configs(connection_parameters).create()
df = session.table("OPENROUTER_TRACES")

# Use Cortex AI functions via Snowpark
summary_df = df.select(
    col("MODEL"),
    call_udf("snowflake.cortex.summarize", col("REQUEST")).alias("REQUEST_SUMMARY")
)
summary_df.show()
```

## Related tools / concepts
- [ClickHouse](clickhouse.md) - High-performance analytical alternative.
- [OpenRouter](../ai_knowledge/openrouter.md) - Log streaming source.
- [S3 / S3-Compatible Storage](../intake_storage/s3-storage.md) - Staging and archiving.
- [Langfuse](langfuse.md) - OSS Observability that can export to Snowflake.
- [Braintrust](braintrust.md) - Enterprise eval stack.
- [Datadog](datadog.md) - Full-stack observability.
- [Arize AI](arize-ai.md) - ML Observability.
- [OpenAI](../ai_knowledge/openai.md) - Supported Cortex LLM provider.
- [Claude](../ai_knowledge/claude.md) - Supported Cortex LLM provider.
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md) - Protocol for connecting Snowflake data to agents.

## Sources / references
- [Official Website](https://www.snowflake.com/)
- [Snowflake Documentation](https://docs.snowflake.com/en/user-guide/intro-key-concepts)
- [OpenRouter Broadcast to Snowflake](https://openrouter.ai/docs/guides/features/broadcast/snowflake)
- [Snowflake Cortex AI](https://www.snowflake.com/en/product/features/cortex/)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
