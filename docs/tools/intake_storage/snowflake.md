# Snowflake

## What it is
Snowflake is a fully managed, cloud-native data platform that unifies data warehousing, data lakes, data engineering, data science, and AI/ML workloads into a single system. It is designed to run on top of major public cloud providers (AWS, Azure, and GCP).

## What problem it solves
Snowflake addresses the complexities and limitations of traditional on-premises and early cloud data warehouses. It decouples storage and compute, allowing them to scale independently and infinitely. This eliminates resource contention and provides a seamless way to share data across organizations without moving it.

## Where it fits in the stack
**Category**: Intake & Storage / Cloud Data Warehouse

## Typical use cases
- **Enterprise Data Warehousing**: Consolidating data from disparate sources for a "single source of truth."
- **Data Lakes**: Storing and analyzing massive volumes of structured, semi-structured (JSON, Avro, XML), and unstructured data.
- **Data Sharing and Collaboration**: Securely sharing live data with partners and customers via the Snowflake Marketplace.
- **AI and ML Development**: Building and deploying AI applications using Snowflake Cortex and Snowpark.

## Strengths
- **Decoupled Architecture**: Storage and compute scale independently, optimizing costs and performance.
- **Zero Management**: No hardware to manage, and software updates are handled automatically by Snowflake.
- **Multi-Cloud and Cross-Region**: Consistent experience across AWS, Azure, and GCP via the "Snowgrid."
- **Natively Supports Semi-Structured Data**: Efficiently handles JSON and other formats without complex ingestion pipelines.
- **Robust Security**: Built-in encryption, multi-factor authentication, and comprehensive access control.

## Limitations
- **Cloud-Only**: Cannot be run on-premises or in private cloud environments.
- **Cost Complexity**: Usage-based pricing (credits) can be difficult to predict without careful monitoring.
- **Proprietary**: While it supports open standards like Apache Iceberg, the core platform is proprietary.

## When to use it
- When you need a scalable, maintenance-free data platform for enterprise analytics.
- When you need to share data securely across different business units or organizations.
- When your workload has highly variable compute demands.

## When not to use it
- For simple applications that only require a small, low-cost relational database.
- If you have a strict requirement for on-premises data storage.
- If you prefer a fully open-source stack.

## Licensing and cost
- **SaaS**: Yes.
- **Cost**: Usage-based pricing. Customers purchase credits for compute and pay for storage by the terabyte.
- **Free Tier**: Trial accounts with limited credits are usually available.

## Getting started

### Installation
Snowflake is a SaaS platform; there is no server to install. You interact with it via the Snowsight web UI or various clients.

### Basic usage
Using the Snowflake SQL client or web worksheet:

```sql
-- Create a database and schema
CREATE DATABASE my_db;
CREATE SCHEMA my_schema;

-- Create a table with a VARIANT column for JSON
CREATE TABLE raw_data (
  id INT,
  payload VARIANT
);

-- Insert JSON data
INSERT INTO raw_data (id, payload)
SELECT 1, PARSE_JSON('{"name": "test", "value": 100}');
```

## CLI examples
The Snowflake CLI (`snow`) can be used for automation:

```bash
# Connect to Snowflake
snow connection test

# Run a SQL command
snow sql -q "SELECT count(*) FROM my_db.my_schema.raw_data"

# Upload a file to a stage
snow stage copy ./data.csv @my_stage
```

## API examples
Snowflake provides native APIs for Python, Java, and other languages.

**Python (using snowflake-connector-python):**
```python
import snowflake.connector

# Connect to Snowflake
ctx = snowflake.connector.connect(
    user='<user>',
    password='<password>',
    account='<account_identifier>'
)

# Create a cursor and execute a query
cs = ctx.cursor()
try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchone()
    print(one_row[0])
finally:
    cs.close()
ctx.close()
```

## Related tools / concepts
- [ClickHouse](clickhouse.md)
- [Apache Tika](../../services/tika.md)
- [Unstructured.io](unstructured.md)
- [Datadog](../process_understanding/datadog.md)

## Sources / references
- [Snowflake Documentation](https://docs.snowflake.com/)
- [Snowflake Key Concepts](https://docs.snowflake.com/en/user-guide/intro-key-concepts)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
