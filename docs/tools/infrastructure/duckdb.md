# DuckDB

DuckDB is an in-process SQL OLAP database management system designed for fast analytical queries on large datasets.

## What it is

DuckDB is an open-source, in-process SQL OLAP database management system. It is designed to provide high-performance analytical query execution while being extremely easy to install and use. Often described as "SQLite for Analytics," it runs within the host process, eliminating the need for a separate server process.

## What problem it solves

Traditional OLAP databases require complex setup and management of server processes. DuckDB solves this by providing a portable, zero-dependency database that can be integrated directly into applications. It addresses the need for fast, local analysis of large datasets (Parquet, CSV, JSON) without the overhead of data movement to a centralized data warehouse.

## Where it fits in the stack

**Infrastructure / Analytics Layer**. It serves as a local analytical engine that can be embedded in Python scripts, R sessions, or edge applications. It bridges the gap between raw data files and full-scale cloud data warehouses like Snowflake.

## Typical use cases

- **Local Data Analysis**: Querying large CSV or Parquet files directly on a laptop or local server.
- **Data Engineering Pipelines**: Using DuckDB as a fast intermediate processing engine for ETL/ELT tasks.
- **Embedded Analytics**: Providing analytical capabilities within a desktop or web application (via Wasm).
- **Agentic Data Tools**: Powering agents that need to perform complex SQL joins and aggregations over local files.

## Strengths

- **Zero Dependency**: Simple to install via `pip`, `npm`, or a single binary.
- **Columnar Execution**: Highly optimized for analytical queries (aggregations, joins).
- **File Format Support**: Native, high-speed support for Parquet, CSV, and JSON.
- **Great Integration**: Deep integration with Python (Pandas, Polars), R, and the Model Context Protocol (MCP).

## Limitations

- **Not for OLTP**: While it supports ACID transactions, it is not designed for high-concurrency transactional workloads (use PostgreSQL or SQLite for that).
- **Vertical Scaling Only**: As an in-process database, it scales with the host machine's resources rather than horizontally across a cluster.
- **Single Writer**: Limited support for concurrent writes across different processes.

## When to use it

- When you need to run analytical SQL queries on data that fits on a single machine's disk/memory.
- When you want to query Parquet or JSON files directly without importing them into a separate database.
- In CI/CD pipelines or short-lived environments where setting up a database server is too heavy.

## When not to use it

- When you need a highly concurrent, transactional database (OLTP).
- When your data requires a distributed, multi-node cluster for processing.
- When you need a persistent, multi-user database server with fine-grained access control.

## Getting started

DuckDB can be installed in seconds for most environments.

```bash
# Install the Python client
pip install duckdb

# Install the CLI on Linux/macOS
curl https://install.duckdb.org | sh

# Verify installation
duckdb --version
```

## CLI examples

Using the DuckDB CLI to query files directly:

```bash
# Query a CSV file directly from the shell
duckdb -c "SELECT * FROM 'data.csv' LIMIT 5;"

# Join a Parquet file and a JSON file
duckdb -c "SELECT p.id, j.name FROM 'users.parquet' p JOIN 'meta.json' j ON p.id = j.user_id;"

# Export a query result to a new Parquet file
duckdb -c "COPY (SELECT * FROM stations) TO 'output.parquet' (FORMAT PARQUET);"
```

## API examples

Interacting with DuckDB programmatically in Python:

```python
import duckdb

# Directly query a Parquet file and return a Pandas DataFrame
df = duckdb.query("SELECT * FROM 'large_data.parquet' WHERE value > 100").to_df()

# Perform an aggregation on a Pandas DataFrame
import pandas as pd
my_df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
result = duckdb.query("SELECT sum(a) FROM my_df").fetchone()

# Use DuckDB for persistent storage
con = duckdb.connect('my_database.db')
con.execute("CREATE TABLE users (id INTEGER, name VARCHAR)")
con.execute("INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob')")
```

## Related tools / concepts

- [SQLGlot](../development_ops/sqlglot.md) — SQL transpilation often used with DuckDB.
- [Pandas](../ai_knowledge/python.md) — Primary data manipulation library integrated with DuckDB.
- [SQLite](https://sqlite.org) — The transactional inspiration for DuckDB's "in-process" model.
- [MotherDuck](https://motherduck.com) — Managed cloud service for DuckDB.
- [Data Copilot](../../architecture/data-copilot-text-to-sql.md) — Architecture for text-to-SQL agents using DuckDB.
- [Agentic SQL Synthesis](../../architecture/data-copilot-text-to-sql.md) — Patterns for autonomous data analysis.
- [Gemma 3](../ai_knowledge/local_llms.md) — Local LLM capable of generating DuckDB-compatible SQL.
- [Infrastructure Index](index.md) — Overview of the local infrastructure stack.

## Sources / references

- [DuckDB Official Website](https://duckdb.org/)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [DuckDB GitHub Repository](https://github.com/duckdb/duckdb)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
