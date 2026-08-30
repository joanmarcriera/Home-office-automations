# Dolt

## What it is
Dolt is a fully SQL-compliant relational database that features Git-style version control capabilities (such as commit, branch, merge, pull, and push). Designed to be a drop-in replacement for MySQL, Dolt allows developers to version data alongside or instead of code. As of early 2027, Dolt has emerged as a crucial component in AI workflows for maintaining reproducible dataset versions, tracking model inputs/outputs, and managing training records over time.

## What problem it solves
Managing dataset lineage and schema drift in machine learning pipelines or multi-agent environments is notoriously difficult. Standard databases do not track revisions, making it hard to query "what did this database look like on Tuesday?" or run complex schema rollbacks. Dolt solves this by enabling branching and merging of the actual relational database state, providing perfect lineage, data audits, and instantaneous safe rollbacks.

## Where it fits in the stack
**Category**: Intake & Storage. Dolt functions as the relational storage layer. It is often combined with object storage like [MinIO](minio.md) or [S3 / S3-Compatible Storage](s3-storage.md). It fits as a state-tracking database inside [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md), storing the system state at every revision of an agent's execution.

## Typical use cases
- **Agent Memory Branching**: Branching database state for safe exploratory actions by autonomous droids before merging successful runs back to main.
- **Reproducible Dataset Tracking**: Versioning structured training datasets for model tuning.
- **Data Auditing**: Reviewing exactly which agent modified which table rows and when via git-like commit logs.
- **Federated Database Syncing**: Merging distributed database changes from edge nodes into a centralized data warehouse.

## Strengths
- **Pure SQL Compliance**: Drop-in replacement for MySQL, compatible with standard ORMs like SQLAlchemy and Sequelize.
- **Git-Style Versioning**: Native CLI tools for branch, merge, diff, commit, and log directly on SQL tables.
- **Instant Rollback**: Instantly revert the entire database state to any prior commit to recover from catastrophic agent errors.
- **High Collaboration**: DoltHub and DoltLab support sharing, pulling, and pushing database clones over remote networks.

## Limitations
- **Write Latency**: Due to versioning metadata overhead, write throughput can be 2x to 3x slower compared to raw un-versioned MySQL.
- **Storage Amplification**: Keeping historical table states and diff records increases disk space usage over time.
- **No Native pgvector**: Lacks native pgvector integration compared to Postgres-based engines like [Supabase](../infrastructure/supabase.md).

## When to use it
- When database rollback and absolute operational lineage are required.
- When multiple automated agents concurrently edit a shared database structure and require a merge-resolution conflict pipeline.
- When versioning structured evaluation benchmarks or prompts alongside training sets.

## When not to use it
- For ultra-high-throughput, sub-millisecond transactional write pipelines.
- When standard analytical vector search dominates your storage needs (prefer [DuckDB](../infrastructure/duckdb.md) or vector databases).

## Getting started

### Installation
Install the dolt binary via shell script or package manager:
```bash
sudo curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh | bash
```

### Initialize Database
```bash
# Create and navigate to database directory
mkdir my_dataset && cd my_dataset

# Initialize dolt repository
dolt init

# Create a test table
dolt sql -q "CREATE TABLE employees (id INT, name VARCHAR(255), PRIMARY KEY (id));"

# Commit the changes
dolt add .
dolt commit -m "Initialize employees table"
```

## CLI examples

### Creating a branch and inserting data
```bash
# Create and switch to a development branch
dolt checkout -b dev_branch

# View the active branches
dolt branch

# Insert data
dolt sql -q "INSERT INTO employees VALUES (1, 'Alice');"

# View the table diff
dolt diff
```

### Merging changes
```bash
# Commit dev branch changes
dolt add .
dolt commit -m "Added Alice"

# Switch back and merge
dolt checkout main
dolt merge dev_branch
```

## API examples

### Python: Connecting via SQLAlchemy
Since Dolt acts as a MySQL server, any MySQL driver can connect to it.

```python
from sqlalchemy import create_engine, text

# Dolt local SQL server runs on port 3306 by default
engine = create_engine("mysql+pymysql://root@127.0.0.1:3306/my_dataset")

with engine.connect() as connection:
    # Query database commits using Dolt's system tables
    result = connection.execute(text("SELECT * FROM dolt_log;"))
    for row in result:
        print(f"Commit: {row.commit_hash} - Author: {row.committer} - Msg: {row.message}")
```

### Python: Executing Branch Checkout over SQL
```python
with engine.connect() as connection:
    # Switch active session branch to dev_branch using dolt procedures
    connection.execute(text("CALL DOLT_CHECKOUT('dev_branch');"))

    # Query data on dev branch
    rows = connection.execute(text("SELECT * FROM employees;"))
    for r in rows:
        print(r)
```

### Python: FastMCP 3.1 Task Protocol & Strict Commit Log Validation (Pydantic v2)
When managing dataset lineage under autonomous coordination by early 2027 SOTA models (e.g., **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, or **Qwen 3.6 VL**), commit logs should be strictly parsed and validated using Pydantic v2 to ensure no unauthorized database modifications occurred.

```python
import json
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError

class DoltCommitLogSchema(BaseModel):
    commit_hash: str = Field(..., alias="commitHash", min_length=32, max_length=40, description="Dolt SHA-1 commit hash")
    committer: str = Field(..., min_length=1, description="Entity or agent committing the data")
    commit_date: datetime = Field(..., alias="commitDate", description="UTC timestamp of the commit")
    task_id: Optional[str] = Field(None, alias="taskId", description="FastMCP 3.1 task protocol ID")
    message: str = Field(..., max_length=5000, description="Audit log commit description")

def validate_dolt_commit(row_data: dict) -> DoltCommitLogSchema:
    """
    Validates a SQL row mapping from `dolt_log` using strict Pydantic v2 validation.
    """
    try:
        # Strict validation with alias mapping
        return DoltCommitLogSchema.model_validate(row_data)
    except ValidationError as e:
        print(f"Commit lineage audit failed verification: {e.errors()}")
        raise

if __name__ == "__main__":
    test_row = {
        "commitHash": "2b30c4d009e8b7c6d5e4f3a2b1c0e9d8c7b6a5fa",
        "committer": "Agent_Claude_5.6",
        "commitDate": "2027-01-07T01:30:00Z",
        "taskId": "task-fastmcp-2027-0107",
        "message": "Update prompt embeddings for Gemma 4 dataset under FastMCP 3.1 task context"
    }
    try:
        validated_commit = validate_dolt_commit(test_row)
        print(f"Verification successful. Hash: {validated_commit.commit_hash[:8]} - Message: {validated_commit.message}")
    except ValidationError:
        pass
```

## Related tools / concepts
- [AnyType](anytype.md) — Local-first personal knowledge storage.
- [Caldav](caldav.md) — Standard database protocol for calendars.
- [Khoj](khoj.md) — Offline search database and interface.
- [LlamaParse](llamaparse.md) — Document parsing dataset pipeline source.
- [MinIO](minio.md) — Local S3 storage companion for backups.
- [S3 / S3-Compatible Storage](s3-storage.md) — Global file storage.
- [DuckDB](../infrastructure/duckdb.md) — In-process analytical database.
- [Supabase](../infrastructure/supabase.md) — Enterprise-grade PostgreSQL platform.
- [Gitea](../../services/gitea.md) — Local Git server for hosting code repositories.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Designing version-controlled agent environments.
- [Model Context Protocol](../automation_orchestration/mcp.md) (FastMCP 3.1) — Agent-to-database communication interfaces.

## Sources / references
- [Dolt Website](https://www.dolthub.com/)
- [Dolt Documentation](https://docs.dolthub.com/)
- [InfoQ: Dolt SQL Version Control Announcement](https://www.infoq.com/news/2026/07/dolt-version-control/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
