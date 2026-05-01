# ClickHouse

## What it is
ClickHouse is a high-performance, column-oriented SQL database management system (DBMS) designed for online analytical processing (OLAP). It allows for real-time analytical queries on massive datasets containing billions of rows.

## What problem it solves
It solves the problem of slow analytical queries on large volumes of data. Unlike traditional row-oriented databases (like PostgreSQL or MySQL), ClickHouse stores data in columns, which significantly accelerates aggregations and complex calculations required for big data analytics.

## Where it fits in the stack
**Category**: Intake & Storage / Analytics Database

## Typical use cases
- **Web and App Analytics**: Real-time tracking of user behavior and clicks.
- **Observability and Monitoring**: Storing and querying logs, events, and metrics at scale.
- **Business Intelligence**: Powering interactive dashboards that require sub-second response times on large datasets.
- **Ad Tech**: Processing and analyzing massive streams of advertising data.

## Strengths
- **Superior Query Performance**: Consistently one of the fastest OLAP databases in industry benchmarks.
- **Efficient Data Compression**: Columnar storage and specialized codecs reduce disk space usage and I/O.
- **Standard SQL Support**: Supports a declarative SQL dialect including JOINs, subqueries, and window functions.
- **Scalability**: Designed to scale linearly from a single server to thousands of nodes.
- **Reliability**: Features like asynchronous multi-master replication ensure data availability.

## Limitations
- **Not for OLTP**: Not designed for transactional workloads with frequent single-row updates or deletes.
- **Complexity for Small Data**: The overhead of management may not be justified for small datasets where a simple relational database would suffice.
- **Higher Resource Usage**: Optimized for speed, it can be resource-intensive during heavy ingestion or complex queries.

## When to use it
- When you need to perform real-time analytics on millions or billions of rows.
- When query latency must be sub-second for interactive user experiences.
- When storage efficiency for analytical data is a priority.

## When not to use it
- As a primary transactional database (OLTP) for a web application.
- If your dataset is small and easily handled by PostgreSQL or SQLite.
- If you require strong ACID guarantees across many small, frequent transactions.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0).
- **Cloud**: ClickHouse Cloud (SaaS) offers usage-based pricing on AWS, GCP, and Azure.
- **Self-hostable**: Yes.

## Getting started

### Installation
On Linux or macOS, you can install the ClickHouse client and server via a single script:

```bash
curl https://clickhouse.com/ | sh
./clickhouse server
```

### Basic usage
Connect to the server using the client:

```bash
./clickhouse client
```

Create a table and insert data:

```sql
CREATE TABLE hits (
    EventDate Date,
    UserID UInt32,
    URL String
) ENGINE = MergeTree()
ORDER BY (EventDate, UserID);

INSERT INTO hits VALUES ('2026-05-08', 123, 'https://example.com');
```

## CLI examples
```bash
# Run a query directly from the shell
clickhouse-client --query "SELECT count() FROM hits"

# Import data from a CSV file
clickhouse-client --query "INSERT INTO hits FORMAT CSV" < data.csv

# Export results to Parquet format
clickhouse-client --query "SELECT * FROM hits" --format Parquet > results.parquet
```

## API examples
ClickHouse provides a REST HTTP API, as well as native drivers for various languages.

**Python (using clickhouse-connect):**
```python
import clickhouse_connect

client = clickhouse_connect.get_client(host='localhost', username='default', password='')

result = client.query('SELECT count(*) FROM hits')
print(result.result_rows)

client.insert('hits', [[date(2026, 5, 8), 456, 'https://clickhouse.com']], column_names=['EventDate', 'UserID', 'URL'])
```

## Related tools / concepts
- [Snowflake](snowflake.md)
- [Apache Tika](../../services/tika.md)
- [PostHog](../process_understanding/posthog.md)
- [Datadog](../process_understanding/datadog.md)

## Sources / references
- [Official ClickHouse Documentation](https://clickhouse.com/docs/en/intro)
- [ClickHouse GitHub Repository](https://github.com/ClickHouse/ClickHouse)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
