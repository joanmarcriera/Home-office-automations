# Snowflake

## What it is
Snowflake is a cloud-based data warehousing platform that allows for the storage, processing, and analysis of vast amounts of data. It is built for the cloud and provides a highly scalable and flexible architecture for modern data needs.

## What problem it solves
It eliminates the complexities of managing traditional on-premises data warehouses. Snowflake provides a unified platform for data engineering, data lakes, data science, and data sharing, enabling organizations to gain insights from their data more efficiently.

## Where it fits in the stack
**Category**: Process & Understanding / Data Warehouse

## Typical use cases
- **AI Log Archiving**: Storing structured traces and JSON logs from AI providers (via OpenRouter Broadcast) for long-term audit and compliance.
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

## Limitations
- **Cloud-Only**: Cannot be run locally or in air-gapped environments.
- **Latency for Small Queries**: Optimized for massive analytical queries; may have higher latency for very small, transactional-style queries.
- **Cost Complexity**: Usage-based pricing can become expensive if large-scale AI processing (like frequent `AI_COMPLETE` calls) is not monitored.

## When to use it
- When you have massive volumes of AI log data that require enterprise-grade storage and complex analytical processing.
- If you need to perform "AI next to your data" using built-in LLM functions without moving sensitive information to external APIs.
- When you require multi-cloud flexibility or secure data sharing with third parties.

## When not to use it
- For small-scale projects where a simpler database like [ClickHouse](clickhouse.md) or even SQLite would suffice.
- If you require an on-premises or fully local-first solution.
- For high-frequency, low-latency transactional writes that aren't primarily for analytical purposes.

## Getting started

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

### Analytical Query Example
```sql
SELECT
    DATE_TRUNC('day', TIMESTAMP) as usage_day,
    MODEL,
    SUM(TOTAL_COST) as daily_cost,
    AVG(LATENCY) as avg_latency
FROM OPENROUTER_TRACES
GROUP BY 1, 2
ORDER BY usage_day DESC, daily_cost DESC;
```

### Python Integration (Snowpark)
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

## CLI examples

### Connect via SnowSQL
```bash
snowsql -c my_conn
```

### Run a Query from CLI
```bash
snowsql -c my_conn -q "SELECT current_version()"
```

### Upload a Local File to a Stage
```bash
snowsql -c my_conn -q "PUT file:///path/to/data.csv @my_stage"
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

# Execute a query
try:
    cursor = ctx.cursor()
    cursor.execute("SELECT MODEL, SUM(TOTAL_COST) FROM OPENROUTER_TRACES GROUP BY MODEL")
    for (model, cost) in cursor:
        print(f"Model: {model}, Total Cost: ${cost:.2f}")
finally:
    ctx.close()
```

## Related tools / concepts
- [ClickHouse](clickhouse.md) (Analytical alternative)
- [OpenRouter](../ai_knowledge/openrouter.md) (Log streaming source)
- [S3 / S3-Compatible Storage](../intake_storage/s3-storage.md) (Staging and archiving)
- [MinIO](../intake_storage/minio.md) (On-premise object storage)
- [Langfuse](langfuse.md) (OSS Observability)
- [Braintrust](braintrust.md) (Enterprise eval stack)
- [Datadog](datadog.md) (Full-stack observability)
- [Arize AI](arize-ai.md) (ML Observability)
- [OpenAI](../ai_knowledge/openai.md) (Supported Cortex LLM provider)
- [Claude](../ai_knowledge/claude.md) (Supported Cortex LLM provider)
- [KnowledgeOps Standards](../../standards.md) (Data governance)

## Sources / references
- [Official Website](https://www.snowflake.com/)
- [Snowflake Documentation](https://docs.snowflake.com/en/user-guide/intro-key-concepts)
- [OpenRouter Broadcast to Snowflake](https://openrouter.ai/docs/guides/features/broadcast/snowflake)
- [Snowflake Cortex AI](https://www.snowflake.com/en/product/features/cortex/)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
