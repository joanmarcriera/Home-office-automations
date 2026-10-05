# Dolt

## What it is
Dolt is a fully SQL-compliant relational database that features Git-style version control capabilities (such as commit, branch, merge, pull, and push). Designed to be a drop-in replacement for MySQL, Dolt allows developers and autonomous AI agent systems to version relational data alongside code. As of early 2027, Dolt has emerged as an indispensable state-tracking and dataset lineage storage engine across multi-agent orchestration architectures, Model Context Protocol (FastMCP 3.1) tool pipelines, and autonomous data science environments.

Unlike traditional relational databases that only maintain the latest state (or rely on binary transaction logs for point-in-time recovery), Dolt tracks versioned table history directly in a prolly tree data structure. This structural design enables instantaneous branching, row-level structural merging, conflict resolution via SQL queries, and zero-copy database cloning across localized nodes and cloud platforms like DoltHub and DoltLab.

```
+-----------------------------------------------------------------------------------+
|                               DOLT DATABASE ENGINE                                |
|                                                                                   |
|  +------------------------+   +-----------------------+   +--------------------+  |
|  |   SQL Execution Layer  |   | Prolly Tree Storage   |   | Git Versioning Engine|  |
|  | (MySQL 8.0 Protocol)   |   | (Content-Addressed)   |   | (Branch, Merge, Diff)|  |
|  +-----------+------------+   +-----------+-----------+   +---------+----------+  |
|              |                            |                         |             |
|              +----------------------------+-------------------------+             |
|                                           |                                       |
|                                           v                                       |
|  +-----------------------------------------------------------------------------+  |
|  |                             System Tables Layer                             |  |
|  |  dolt_log  |  dolt_branches  |  dolt_status  |  dolt_diff  |  dolt_conflicts  |  |
|  +-----------------------------------------------------------------------------+  |
+------------------------------------+----------------------------------------------+
                                     |
                                     v
+------------------------------------+----------------------------------------------+
|                         FASTMCP 3.1 & AGENT RUNTIME INTERFACE                     |
|                                                                                   |
|  +-----------------------+     +------------------------+     +-----------------+ |
|  | Multi-Agent Branching |     | Lineage Audit Tracking |     | Safe Reversion  | |
|  | (Exploratory Isolation)     | (Pydantic v2 Schema)   |     | (Auto-Rollback) | |
|  +-----------------------+     +------------------------+     +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Managing dataset lineage, transactional safety, and schema evolution across distributed AI workflows or autonomous agent ensembles presents severe challenges:

1. **Agent Corruption and Hallucinated Edits**: Autonomous droids or LLM execution loops can perform destructive SQL operations (`UPDATE`, `DELETE`, `DROP TABLE`). Traditional SQL databases require expensive and slow snapshot restores to recover. Dolt enables instant rollback via `dolt_rollback` or `CALL DOLT_REVERT()`.
2. **Parallel Agent Memory Divergence**: When multiple agents execute complex tasks in parallel (e.g., automated web scrapers, data cleaning droids, and feature engineering pipelines), running concurrent writes against a single database main branch introduces race conditions and lock contention. Dolt allows each agent to work in an isolated git branch (`agent/scrape-01`, `agent/clean-02`) and merge results back into `main` using structural merge protocols.
3. **Dataset Lineage and Auditing**: Compliance standards require tracking exactly which LLM call, prompt context, or agent task modified specific row values in training datasets or feature stores. Dolt system tables (`dolt_log`, `dolt_diff_<table>`) provide row-level attribution metadata for every commit.
4. **Reproducible Model Training**: ML teams need to train models on exact snapshots of relational data. Dolt commit hashes serve as immutable version tags for training datasets.

## Where it fits in the stack
**Category**: Intake & Storage. Dolt operates as the version-controlled relational state engine. It integrates seamlessly into broader modern AI stacks:

- **State Storage Layer**: Serves as the primary operational database storing structured facts, agent execution logs, task queues, and dynamic knowledge graphs.
- **MCP Integration Layer**: Interfaced via FastMCP 3.1 servers, enabling agents running frontier models (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, **Qwen 3.6 VL**) to branch database state prior to risky tool execution.
- **Storage Ecosystem**: Operates alongside blob storage platforms like [MinIO](minio.md) or [S3 / S3-Compatible Storage](s3-storage.md), while relying on vector databases like [Weaviate](../infrastructure/weaviate.md) or [Qdrant](../infrastructure/qdrant.md) for semantic embeddings.
- **Orchestration**: Frequently embedded inside [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) orchestrated by frameworks such as [Ag2](../frameworks/ag2.md), [Smolagents](../frameworks/smolagents.md), or [Temporal](../automation_orchestration/temporal.md).

## Typical use cases
- **Agent Sandbox Branching**: An autonomous software engineer agent creates a branch `fix/issue-402`, populates local test database tables, runs unit tests, and merges the modified relational data back into `main` only if all tests pass.
- **Autonomous Feature Engineering**: Feature extraction agents populate tables with newly computed mathematical metrics. Diff tracking via `dolt_diff` allows data scientists to inspect the precise impact of new feature algorithms before approving deployment.
- **Collaborative Human-in-the-Loop (HITL) Annotation**: Human reviewers and automated annotation droids concurrently label raw documents. Dolt's conflict resolution table (`dolt_conflicts`) highlights overlapping annotation discrepancies for human arbitration.
- **Versioned Prompt & Evaluation Storage**: Storing prompt templates, LLM benchmark evaluations, and ground-truth validation datasets with full version history and rollback capabilities.

## Strengths
- **Native MySQL 8.0 Compatibility**: Connects seamlessly with standard MySQL clients, Python ORMs (`SQLAlchemy`, `SQLModel`, `Peewee`), and node drivers (`mysql2`).
- **Git-like Version Control Operations**: Supports `dolt commit`, `dolt branch`, `dolt merge`, `dolt push`, `dolt pull`, and `dolt diff` directly through SQL procedure calls (`CALL DOLT_COMMIT(...)`) or CLI utilities.
- **Prolly Tree Storage Engine**: Content-addressed B-tree variant allows structural sharing across branches, enabling efficient storage of large datasets with millions of rows.
- **SQL-Based Version Auditing**: Allows querying historical table states using temporal SQL syntax (`SELECT * FROM employees AS OF '2027-01-01'`) or inspecting commit logs via `dolt_log`.
- **Remote Synchronization**: Built-in pushing and fetching to DoltHub (cloud SaaS) or DoltLab (self-hosted enterprise server) for federated data synchronization.

## Limitations
- **Write Performance Overhead**: Structural hashing and content-addressed storage overhead make raw SQL write throughput 2x–3x slower than unversioned MySQL 8.0.
- **Disk Amplification**: Storing complete commit histories and index prolly trees increases storage footprint over prolonged execution without regular garbage collection (`dolt gc`).
- **Lacks Native Vector Search**: Does not include native vector distance operators (unlike PostgreSQL with `pgvector`), necessitating pairing with dedicated vector indices or [DuckDB](../infrastructure/duckdb.md) for hybrid search.

## When to use it
- When autonomous AI agents require safe, isolated database sandboxes for multi-step task execution.
- When strict regulatory compliance or auditability mandates tracking row-level provenance and commit timestamps for every dataset edit.
- When multiple automated agents or human annotators need to concurrently modify a shared relational database without lock contention.
- When dataset snapshotting and zero-copy branching are required for ML experiment reproducibility.

## When not to use it
- For high-frequency, sub-millisecond transactional write workloads (e.g., high-frequency financial trading tick stores).
- When the application primary requirement is purely un-structured vector similarity search (prefer dedicated vector databases like [Qdrant](../infrastructure/qdrant.md) or [Weaviate](../infrastructure/weaviate.md)).
- When simple static file versioning (like Git LFS) is sufficient for non-relational binary assets.

## Getting started

### Installation
Install the dolt binary via official shell script or package managers:
```bash
# Direct binary installation script
sudo curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh | bash

# Verify installation
dolt version
```

### Initialize and Configure Database
```bash
# Create project workspace
mkdir -p /opt/dolt_data/agent_memory && cd /opt/dolt_data/agent_memory

# Initialize Dolt repository
dolt init --name "Agent Runtime System" --email "agent@agentic-insights.internal"

# Start Dolt SQL Server on default MySQL port 3306
dolt sql-server --host=0.0.0.0 --port=3306 --user=root --password=secret_pass &
```

## CLI examples

### Creating Branches, Tables, and Structural Commits
```bash
# Connect locally and create base schema
dolt sql -q "
CREATE TABLE task_state (
    task_id VARCHAR(64) PRIMARY KEY,
    agent_id VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL,
    payload JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"

# Commit initial schema to main branch
dolt add .
dolt commit -m "Initialize task_state relational schema"

# Create a new isolated agent execution branch
dolt checkout -b agent/task-101

# Insert experimental records on branch
dolt sql -q "INSERT INTO task_state (task_id, agent_id, status, payload) VALUES ('task-101', 'droid-alpha', 'IN_PROGRESS', '{\"step\": \"extraction\"}');"

# View diff between current branch and main
dolt diff main

# Commit changes on agent branch
dolt commit -am "Record task-101 extraction state"

# Switch back to main and perform structural merge
dolt checkout main
dolt merge agent/task-101
```

### Querying History and Reverting Edits
```bash
# Query the commit log system table
dolt sql -q "SELECT commit_hash, committer, message, date FROM dolt_log LIMIT 5;"

# Query table state as of a historical commit
dolt sql -q "SELECT * FROM task_state AS OF 'v1.0.0';"

# Revert a bad commit
dolt sql -q "CALL DOLT_REVERT('2b30c4d009e8b7c6d5e4f3a2b1c0e9d8c7b6a5fa');"
```

## API examples

### Python FastMCP 3.1 Server with Dolt Versioning & Pydantic v2
The following complete FastMCP 3.1 server exposes version-controlled Dolt database operations to autonomous frontier agents, including branch creation, transaction execution, commit generation, and audit logging with strict Pydantic v2 schema enforcement.

```python
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError
from fastmcp import FastMCP
import pymysql

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dolt_mcp_server")

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    "Dolt-Versioned-Storage-Engine",
    version="3.1.0",
    description="FastMCP 3.1 server for Dolt relational database version control & agent memory management"
)

# Configuration models
class DoltConfig(BaseModel):
    host: str = Field(default="127.0.0.1", description="Dolt SQL server hostname")
    port: int = Field(default=3306, description="Dolt SQL server port")
    user: str = Field(default="root", description="Database user")
    password: str = Field(default="secret_pass", description="Database password")
    database: str = Field(default="agent_memory", description="Active database name")

# Schema models for strict agent validation
class TaskRecordSchema(BaseModel):
    task_id: str = Field(..., alias="taskId", min_length=4, max_length=64, description="Unique task identifier")
    agent_id: str = Field(..., alias="agentId", min_length=2, max_length=64, description="Executing agent ID")
    status: str = Field(..., description="Task status (PENDING, RUNNING, COMPLETED, FAILED)")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary task context metadata")

class DoltCommitLogSchema(BaseModel):
    commit_hash: str = Field(..., alias="commitHash", description="Dolt SHA-1 commit hash")
    committer: str = Field(..., description="Entity or agent committing the data")
    commit_date: datetime = Field(..., alias="commitDate", description="UTC timestamp of the commit")
    message: str = Field(..., max_length=5000, description="Audit log commit message")

def get_connection(config: DoltConfig):
    return pymysql.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.database,
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )

@mcp.tool()
def create_agent_branch(branch_name: str, config: Optional[DoltConfig] = None) -> str:
    """
    Creates an isolated Dolt branch for safe exploratory agent execution.
    """
    cfg = config or DoltConfig()
    conn = get_connection(cfg)
    try:
        with conn.cursor() as cursor:
            # Execute Dolt SQL procedure to checkout a new branch
            cursor.execute(f"CALL DOLT_CHECKOUT('-b', '{branch_name}');")
            return f"Successfully created and checked out branch '{branch_name}'."
    except Exception as e:
        logger.error(f"Failed to create branch: {e}")
        return f"Error creating branch: {str(e)}"
    finally:
        conn.close()

@mcp.tool()
def insert_task_state(record: Dict[str, Any], config: Optional[DoltConfig] = None) -> str:
    """
    Inserts or updates a task state record into the Dolt database with strict Pydantic v2 validation.
    """
    cfg = config or DoltConfig()
    try:
        validated_record = TaskRecordSchema.model_validate(record)
    except ValidationError as ve:
        return f"Validation Error: {ve.errors()}"

    conn = get_connection(cfg)
    try:
        with conn.cursor() as cursor:
            query = """
            INSERT INTO task_state (task_id, agent_id, status, payload)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE status=%s, payload=%s;
            """
            payload_json = json.dumps(validated_record.payload)
            cursor.execute(query, (
                validated_record.task_id,
                validated_record.agent_id,
                validated_record.status,
                payload_json,
                validated_record.status,
                payload_json
            ))
            return f"Successfully recorded state for task '{validated_record.task_id}'."
    except Exception as e:
        logger.error(f"Database insertion failed: {e}")
        return f"Database Error: {str(e)}"
    finally:
        conn.close()

@mcp.tool()
def commit_branch_changes(branch_name: str, commit_message: str, author: str, config: Optional[DoltConfig] = None) -> str:
    """
    Commits all pending table changes on the active branch with audit tracking.
    """
    cfg = config or DoltConfig()
    conn = get_connection(cfg)
    try:
        with conn.cursor() as cursor:
            # Add all tables
            cursor.execute("CALL DOLT_ADD('.');")
            # Commit with author attribution
            cursor.execute(f"CALL DOLT_COMMIT('-m', %s, '--author', %s);", (commit_message, f"{author} <{author}@agentic-insights.internal>"))

            # Fetch latest commit hash
            cursor.execute("SELECT @@dolt_repo_head as head_hash;")
            res = cursor.fetchone()
            head_hash = res["head_hash"] if res else "UNKNOWN"
            return f"Successfully committed changes to branch '{branch_name}'. Commit Hash: {head_hash}"
    except Exception as e:
        logger.error(f"Commit operation failed: {e}")
        return f"Commit Error: {str(e)}"
    finally:
        conn.close()

@mcp.tool()
def audit_commit_log(limit: int = 10, config: Optional[DoltConfig] = None) -> List[Dict[str, Any]]:
    """
    Queries Dolt system tables to return strictly validated audit commit history.
    """
    cfg = config or DoltConfig()
    conn = get_connection(cfg)
    validated_logs = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT commit_hash as commitHash, committer, date as commitDate, message FROM dolt_log ORDER BY date DESC LIMIT %s;", (limit,))
            rows = cursor.fetchall()
            for row in rows:
                try:
                    log_obj = DoltCommitLogSchema.model_validate(row)
                    validated_logs.append(log_obj.model_dump(by_alias=True, mode="json"))
                except ValidationError as ve:
                    logger.warning(f"Skipping malformed commit record: {ve}")
            return validated_logs
    except Exception as e:
        logger.error(f"Audit log query failed: {e}")
        return []
    finally:
        conn.close()

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Python: Multi-Agent Parallel Execution & Merge Workflow
The following pattern demonstrates how Python workflows can orchestrate parallel agents using Dolt branching and automated merge conflict detection.

```python
import pymysql
import json
from datetime import datetime

def execute_parallel_agent_workflow():
    db_config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "secret_pass",
        "database": "agent_memory"
    }

    # Step 1: Initialize main connection
    conn = pymysql.connect(**db_config, autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    try:
        print("--- Step 1: Creating Main Base Table ---")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feature_store (
            feature_id VARCHAR(64) PRIMARY KEY,
            value FLOAT NOT NULL,
            computed_by VARCHAR(64) NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("CALL DOLT_ADD('.');")
        cursor.execute("CALL DOLT_COMMIT('-m', 'Initialize feature_store schema');")

        print("--- Step 2: Agent Alpha Branches and Computes ---")
        cursor.execute("CALL DOLT_CHECKOUT('-b', 'agent/alpha-features');")
        cursor.execute("INSERT INTO feature_store (feature_id, value, computed_by) VALUES ('feat_01', 0.942, 'Agent_Alpha');")
        cursor.execute("CALL DOLT_COMMIT('-a', '-m', 'Agent Alpha computed feat_01');")

        print("--- Step 3: Agent Beta Branches from Main and Computes ---")
        cursor.execute("CALL DOLT_CHECKOUT('main');")
        cursor.execute("CALL DOLT_CHECKOUT('-b', 'agent/beta-features');")
        cursor.execute("INSERT INTO feature_store (feature_id, value, computed_by) VALUES ('feat_02', 128.45, 'Agent_Beta');")
        cursor.execute("CALL DOLT_COMMIT('-a', '-m', 'Agent Beta computed feat_02');")

        print("--- Step 4: Merging Agent Alpha into Main ---")
        cursor.execute("CALL DOLT_CHECKOUT('main');")
        cursor.execute("CALL DOLT_MERGE('agent/alpha-features');")

        print("--- Step 5: Merging Agent Beta into Main ---")
        cursor.execute("CALL DOLT_MERGE('agent/beta-features');")

        print("--- Step 6: Verifying Merged Results on Main ---")
        cursor.execute("SELECT * FROM feature_store;")
        features = cursor.fetchall()
        for f in features:
            print(f"Feature: {f['feature_id']} | Value: {f['value']} | Computed By: {f['computed_by']}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    execute_parallel_agent_workflow()
```

## Production Deployment & Systemd Service Guide
To run Dolt as a persistent background database service in Linux production environments:

### Systemd Service Configuration
Create `/etc/systemd/system/dolt.service`:
```ini
[Unit]
Description=Dolt SQL Server Database Service
After=network.target

[Service]
Type=simple
User=dolt
Group=dolt
WorkingDirectory=/var/lib/dolt/agent_memory
ExecStart=/usr/local/bin/dolt sql-server --host=0.0.0.0 --port=3306 --user=root --password=secret_pass --max-connections=500
Restart=always
RestartSec=5s
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now dolt.service
sudo systemctl status dolt.service
```

## Related tools / concepts
- [MinIO](minio.md) — Local S3-compatible blob storage companion for database dumps and model artifacts.
- [S3 / S3-Compatible Storage](s3-storage.md) — Enterprise object storage standard for historical Dolt backups.
- [DuckDB](../infrastructure/duckdb.md) — Fast in-process analytical SQL engine for embedded vector/parquet analytics.
- [Supabase](../infrastructure/supabase.md) — Hosted enterprise PostgreSQL platform with real-time subscriptions and vector search.
- [Weaviate](../infrastructure/weaviate.md) — Native vector database for semantic search companion integration.
- [Gitea](../../services/gitea.md) — Self-hosted Git server for code repositories operating alongside Dolt data stores.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Design patterns for version-controlled, multi-agent systems.
- [Model Context Protocol](../automation_orchestration/mcp.md) (FastMCP 3.1) — Standardized tool protocols interfacing agents with version-controlled databases.

## Sources / references
- [Dolt Official Website](https://www.dolthub.com/)
- [Dolt Documentation & SQL System Tables Reference](https://docs.dolthub.com/)
- [Dolt GitHub Repository](https://github.com/dolthub/dolt)
- [InfoQ: Version Control for Relational Databases with Dolt](https://www.infoq.com/news/2026/07/dolt-version-control/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
