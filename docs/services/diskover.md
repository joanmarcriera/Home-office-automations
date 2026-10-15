# Diskover

Diskover is an open-source file indexer and data management tool that uses Elasticsearch to index and manage data across heterogeneous storage systems, providing critical storage intelligence for agentic workflows in early January 2027.

## What it is
Diskover is a high-performance file system crawler and disk space analyzer. It crawls your storage (local drives, NFS, SMB) and stores the metadata in Elasticsearch, providing a powerful web interface and API to search, filter, and visualize your data. In the early January 2027 ecosystem, it serves as the ground truth for agents managing large-scale data archives, supporting the [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) (v3.1) and FastMCP specifications for automated storage queries.

## Architecture Flowchart

```
+-----------------------------------------------------------------------------------+
|                            Diskover Crawling & Indexing Pipeline                  |
+-----------------------------------------------------------------------------------+
                                          |
                                  [ Target Storage ]
                        (NFS / SMB / Local NVMe / TrueNAS Datasets)
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                              Diskover Crawler Workers                             |
|  - Directory Traversal & Stat Extraction                                         |
|  - File Hash Calculation (xxHash / MD5)                                           |
|  - MIME Type & File Metadata Parsing                                              |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                              Redis Task Queue / Cache                             |
|  - Distributed Batch Queueing                                                     |
|  - Worker Task State Synchronization                                             |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                              Elasticsearch 8.x Cluster                            |
|  - Dynamic Mapping for Storage Records                                            |
|  - Sub-second Full-text & Range Aggregations                                      |
+-----------------------------------------------------------------------------------+
                     /                                  \
                    /                                    \
                   v                                      v
+------------------------------------+  +-------------------------------------------+
|          Diskover Web UI           |  |       FastMCP 3.1 Server / API Gateway     |
| - Treemaps & Disk Usage Charts     |  | - Tool Calling: /search_files, /analyze   |
| - Visual Diff & Duplicate Scanners |  | - Structured Pydantic v2 Schema Output    |
+------------------------------------+  +-------------------------------------------+
```

## What problem it solves
It solves the problem of "Data Sprawl" across large storage arrays. When you have terabytes of data across multiple servers, finding old versions of files, identifying duplicate data, or seeing which user is consuming the most space becomes difficult. Diskover makes your entire storage infrastructure searchable and quantifiable, allowing tools like [Gemma 3](../tools/ai_knowledge/local_llms.md), [Llama 4](../tools/ai_knowledge/local_llms.md), [GPT-5.5](../tools/ai_knowledge/openai.md), and [Claude 5.1](../tools/providers/anthropic.md) to make informed decisions about data retention.

## Where it fits in the stack
In a homelab, Diskover acts as the **Storage Intelligence Layer**. It provides the metadata that allows automation scripts and autonomous agents to identify which files should be archived, moved to cold storage (like [Storj](storj.md)), or deleted to free up space. It integrates with [n8n](n8n.md) for automated lifecycle management.

## Typical use cases
- **Data Cleanup**: Finding and deleting files that haven't been accessed in over 2 years.
- **Duplicate Identification**: Using file hashes to find exact duplicates across different mounts.
- **Cost Analysis**: Calculating the cost of storage per department or user.
- **Dark Data Discovery**: Finding large log files or temp files that were forgotten.
- **Agentic Archival**: Providing a list of candidates for cold-storage migration to an [n8n](n8n.md) workflow.
- **Infrastructure Auditing**: Verifying that backup routines are actually capturing all intended data.

## Strengths
- **Massive Scalability**: Leverages Elasticsearch to handle millions of file records with sub-second search times.
- **Extensible**: Supports custom plugins for metadata extraction and classification.
- **Powerful Visualization**: Includes treemaps and charts for disk usage analysis.
- **Heterogeneous**: Can index anything that can be mounted as a file system.
- **API-First**: Easy to query via Elasticsearch's native REST API or specialized [MCP](../tools/automation_orchestration/mcp.md) tools.

## Limitations
- **Infrastructure Heavy**: Requires a running Elasticsearch instance, which is resource-intensive (baseline 4GB+ RAM).
- **Scheduled, Not Real-time**: It provides a snapshot in time; changes to the file system aren't reflected until the next crawl.
- **Complex Setup**: Setting up the worker/web/ES stack can be daunting for beginners.

## Storage Indexer Comparison Matrix

| Feature / Metric | Diskover | GrandPerspective | ncdu | WizTree / Everything | Czkawka |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Backend Storage** | Elasticsearch 8.x | In-Memory (Local) | In-Memory (Local) | MFT / Local Memory | SQLite / Local Memory |
| **Multi-Node / Heterogeneous** | Yes (NFS/SMB/S3) | Local Only | Local Only | Windows MFT / SMB | Local Only |
| **Agent / MCP 3.1 Integration** | Native via FastMCP | No | No | Windows API Only | CLI Only |
| **Scale Limit** | 100M+ Records | ~5M Files | ~10M Files | 10M+ Files (Local) | ~5M Files |
| **Search Speed** | < 50ms (Indexed) | Real-time scan | Real-time scan | Sub-second (MFT) | Minutes (Full Scan) |
| **Duplicate Detection** | xxHash / MD5 in ES | None | None | None | Per-hash comparison |
| **Resource Overhead** | High (ES + Redis) | Very Low | Minimal | Very Low | Low |

## When to use it
- When you need to gain visibility into large, heterogeneous storage environments.
- To identify "dark data," such as old, large, or duplicate files that are wasting space.
- When you want a searchable index of your files without having to scan the live file system every time.
- To provide storage-context to AI agents like [Gemma 3](../tools/ai_knowledge/local_llms.md), [GPT-5.5](../tools/ai_knowledge/openai.md), or [Claude 5.1](../tools/providers/anthropic.md).

## When not to use it
- If you only need a simple, real-time disk usage visualizer for a single local drive (consider `ncdu` or WizTree).
- If you don't have the resources to run Elasticsearch, which is a mandatory requirement for Diskover.
- For real-time file monitoring or real-time file system events (use `inotify` or specialized watchers).

## Getting started

### Docker installation
The recommended way to run Diskover is using Docker Compose, as it handles both the Diskover application and the required Elasticsearch instance.

```yaml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.17.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
    volumes:
      - esdata:/usr/share/elasticsearch/data
  diskover:
    image: lscr.io/linuxserver/diskover:latest
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
      - ES_HOST=elasticsearch
    volumes:
      - /path/to/config:/config
      - /path/to/data:/data
    ports:
      - 80:80
    depends_on:
      - elasticsearch
volumes:
  esdata:
```

### Hello World
1. Start the containers: `docker-compose up -d`.
2. Access the web UI at `http://localhost`. The default credentials are `diskover` / `darkdata`.
3. Run your first index: `docker exec -it diskover python3 /app/diskover/diskover.py -i my_first_index /data`.
4. Refresh the web UI and select the `my_first_index` index in Settings to view your data.

## CLI examples

Indexing and management tasks are performed using the `diskover.py` script inside the container.

```bash
# Index a specific directory into a new index
docker exec -it diskover python3 /app/diskover/diskover.py -i diskover-data /data

# Run an index task in the background (detached)
docker exec -d diskover python3 /app/diskover/diskover.py -i diskover-data /data

# List all indices in the Elasticsearch instance
curl -X GET "http://elasticsearch:9200/_cat/indices?v"

# Remove an index from Elasticsearch
curl -X DELETE "http://elasticsearch:9200/diskover-old-index"

# Compare two indices to find differences (Visual Diff helper)
docker exec -it diskover python3 /app/diskover/diskover.py --diff index_a index_b
```

## API examples

Diskover stores its data in Elasticsearch, allowing you to use the standard Elasticsearch REST API for advanced queries.

### Search for files larger than 1GB
```bash
curl -X GET "http://elasticsearch:9200/diskover-data/_search?q=filesize:>1073741824&pretty"
```

### FastMCP 3.1 FastMCP Server Implementation with Pydantic v2
In early January 2027, integrating Storage Intelligence into AI agent pipelines relies on FastMCP 3.1 server tools. Below is an asynchronous FastMCP tool exposing file metadata queries and duplicate identification with strict **Pydantic v2** validation:

```python
import asyncio
import httpx
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from fastmcp import FastMCP

# Initialize FastMCP Server for Diskover Storage Intelligence
mcp = FastMCP("Diskover Storage Intelligence", version="3.1.0")

class FileSearchQuery(BaseModel):
    index_name: str = Field(default="diskover-*", description="Elasticsearch index pattern")
    min_size_bytes: int = Field(default=104857600, ge=0, description="Minimum file size in bytes (default 100MB)")
    extension: Optional[str] = Field(None, description="File extension filter (e.g., 'iso', 'mp4', 'gguf')")
    limit: int = Field(default=50, ge=1, le=500, description="Maximum number of file records returned")

class FileMetadataRecord(BaseModel):
    filename: str = Field(..., description="Base filename")
    filepath: str = Field(..., description="Absolute file path")
    filesize: int = Field(..., description="File size in bytes")
    extension: str = Field(default="", description="File extension")
    last_modified: str = Field(..., description="ISO timestamp of last modification")
    owner: str = Field(default="unknown", description="POSIX file owner")

    @field_validator("filename", mode="before")
    @classmethod
    def sanitize_filename(cls, value: str) -> str:
        return value.strip() if value else "unnamed_file"

class StorageSummaryResponse(BaseModel):
    total_files_found: int = Field(..., description="Total files matching query criteria")
    total_bytes: int = Field(..., description="Aggregated size in bytes")
    records: List[FileMetadataRecord] = Field(..., description="Validated list of file objects")

@mcp.tool()
async def search_storage_files(query: FileSearchQuery, es_host: str = "http://localhost:9200") -> StorageSummaryResponse:
    """Search for indexed files across Diskover Elasticsearch clusters with size and extension filters."""
    must_clauses = [{"range": {"filesize": {"gte": query.min_size_bytes}}}]
    if query.extension:
        must_clauses.append({"term": {"extension.keyword": query.extension.lower()}})

    search_payload = {
        "size": query.limit,
        "query": {"bool": {"must": must_clauses}},
        "sort": [{"filesize": {"order": "desc"}}]
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{es_host}/{query.index_name}/_search", json=search_payload)
        resp.raise_for_status()
        data = resp.json()

        hits = data.get("hits", {}).get("hits", [])
        total_count = data.get("hits", {}).get("total", {}).get("value", len(hits))
        records = []
        sum_bytes = 0

        for hit in hits:
            source = hit.get("_source", {})
            fsize = source.get("filesize", 0)
            sum_bytes += fsize
            records.append(FileMetadataRecord(
                filename=source.get("name", "unknown"),
                filepath=source.get("parent_path", "") + "/" + source.get("name", ""),
                filesize=fsize,
                extension=source.get("extension", ""),
                last_modified=source.get("mtime", ""),
                owner=source.get("owner", "unknown")
            ))

        return StorageSummaryResponse(
            total_files_found=total_count,
            total_bytes=sum_bytes,
            records=records
        )

if __name__ == "__main__":
    mcp.run()
```

## Troubleshooting & Error Remediation

| Issue / Error | Root Cause | Resolution Strategy |
| :--- | :--- | :--- |
| `Elasticsearch heap out of memory` | ES heap exceeded default 1GB allocation during deep crawls | Set `ES_JAVA_OPTS=-Xms4g -Xmx4g` in Docker Compose environment settings. |
| `Crawler worker lockup on NFS` | NFS stale file handle or server timeout during deep directory traversal | Mount NFS with `timeo=600,retrans=2,hard,noresvport` and enable `--threads 4` in diskover.py. |
| `Web UI login failure (401)` | Default admin database uninitialized or secret key mismatch | Exec into container and run `python3 /app/diskover/diskover_web_init.py --reset-admin`. |
| `Index mapping conflict error` | Upgraded ES schema without reindexing legacy diskover indexes | Run index alias alias migration: `curl -X POST "http://localhost:9200/_reindex"`. |
| `FastMCP query timeout (>30s)` | ES query searching multi-terabyte index without proper field mappings | Add explicit field mappings for `filesize` and `extension.keyword` before crawling. |

## Production Guardrails & Security

1. **Read-Only Storage Mounting**: Mount target storage datasets into Diskover worker containers using the `:ro` (read-only) flag to guarantee zero accidental modification or file deletion during indexing.
2. **Elasticsearch Network Isolation**: Bind Elasticsearch ports (`9200`, `9300`) to internal Docker network aliases or `127.0.0.1` unless authentication (X-Pack or reverse proxy) is strictly enabled.
3. **Scheduled Off-Peak Crawls**: Configure cron jobs to trigger `diskover.py` during low-usage hours (e.g., 02:00 AM) to minimize IOPS contention on active production NAS pools.

## Related tools / concepts
- [Storj](storj.md) — Targeted off-site storage for large, cold datasets identified by Diskover.
- [n8n](n8n.md) — Orchestrate cleanup workflows based on Elasticsearch query results.
- [Syncthing](syncthing.md) — Track synchronization state and identify orphaned replicas.
- [Paperless-ngx](paperless-ngx.md) — Complementary metadata management for OCR'd documents.
- [Authentik](authentik.md) — Secure access to the Diskover web interface via SSO.
- [Gitea](gitea.md) — Version control for storage management scripts.
- [Nextcloud](nextcloud.md) — User-facing storage that can be indexed by Diskover.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Standard for agentic storage intelligence.

## TrueNAS SCALE & NFS Integration
To index data residing on a [TrueNAS SCALE](../architecture/infrastructure.md) server, you must mount the datasets to the Diskover host via NFS. This allows the crawler to access the file metadata directly.

### Host Configuration (Linux)
Install the NFS client and mount the TrueNAS dataset:

```bash
sudo apt update && sudo apt install nfs-common -y
sudo mkdir -p /mnt/truenas_data
sudo mount -t nfs <TRUENAS_IP>:/mnt/tank/data /mnt/truenas_data
```

### Docker Volume Mapping
Add the mount point to your `docker-compose.yaml` to make it accessible to the Diskover container:

```yaml
services:
  diskover:
    # ... other config ...
    volumes:
      - /mnt/truenas_data:/data/truenas:ro
```

### Crawling the NFS Mount
Once mounted, you can trigger a crawl of the TrueNAS data from within the container:

```bash
docker exec -it diskover python3 /app/diskover/diskover.py -i truenas-index /data/truenas
```

## Sources / references
- [Diskover GitHub Repository](https://github.com/diskoverdata/diskover-community)
- [Diskover Official Site](https://diskoverdata.com/)
- [LinuxServer.io Diskover Image](https://docs.linuxserver.io/images/docker-diskover/)
- [Elasticsearch Documentation](https://www.elastic.co/guide/index.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
