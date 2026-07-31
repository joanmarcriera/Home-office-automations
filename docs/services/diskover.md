# Diskover

Diskover is an open-source file indexer and data management tool that uses Elasticsearch to index and manage data across heterogeneous storage systems, providing critical storage intelligence for agentic workflows in late October / November 2026.

## What it is
Diskover is a high-performance file system crawler and disk space analyzer. It crawls your storage (local drives, NFS, SMB) and stores the metadata in Elasticsearch, providing a powerful web interface and API to search, filter, and visualize your data. In the late October / November 2026 ecosystem, it serves as the ground truth for agents managing large-scale data archives, supporting the [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) (v3.1) and FastMCP specifications for automated storage queries.

## What problem it solves
It solves the problem of "Data Sprawl" across large storage arrays. When you have terabytes of data across multiple servers, finding old versions of files, identifying duplicate data, or seeing which user is consuming the most space becomes difficult. Diskover makes your entire storage infrastructure searchable and quantifiable, allowing tools like [Gemma 3](../tools/ai_knowledge/local_llms.md), [Llama 4](../tools/ai_knowledge/local_llms.md), and [Claude 5.1](../tools/providers/anthropic.md) to make informed decisions about data retention.

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

## When to use it
- When you need to gain visibility into large, heterogeneous storage environments.
- To identify "dark data," such as old, large, or duplicate files that are wasting space.
- When you want a searchable index of your files without having to scan the live file system every time.
- To provide storage-context to AI agents like [Gemma 3](../tools/ai_knowledge/local_llms.md) or [Claude 5.1](../tools/providers/anthropic.md).

## When not to use it
- If you only need a simple, real-time disk usage visualizer for a single local drive (consider `ncdu` or WizTree).
- If you don't have the resources to run Elasticsearch, which is a mandatory requirement for Diskover.
- For real-time file monitoring or real-time file system events (use `inotify` or specialized watchers).

## Getting started

### Docker installation
The recommended way to run Diskover is using Docker Compose, as it handles both the Diskover application and the required Elasticsearch instance.

```yaml
version: '2'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.22
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - esdata:/usr/share/elasticsearch/data
  diskover:
    image: lscr.io/linuxserver/diskover
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

### Python example to query indices with Pydantic v2 Validation
In late October / November 2026, integrating Storage Intelligence into AI pipelines relies on structured schemas. Below is an asynchronous Python snippet retrieving and validating indices and storage statistics from Diskover's backend Elasticsearch engine using **Pydantic v2**:

```python
import asyncio
import httpx
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class ElasticsearchIndexModel(BaseModel):
    health: str = Field(..., description="The status of the Elasticsearch index (green, yellow, red)")
    status: str = Field(..., description="The open/close status of the index")
    index: str = Field(..., description="Name of the index")
    docs_count: Optional[int] = Field(None, alias="docs.count", description="Number of indexed file objects")
    store_size: Optional[str] = Field(None, alias="store.size", description="Raw text representing total size on disk")

    @field_validator("docs_count", mode="before")
    @classmethod
    def parse_docs_count(cls, value):
        if value is None or value == "null" or value == "":
            return 0
        try:
            return int(value)
        except ValueError:
            return 0

async def query_diskover_indices(es_host: str) -> List[ElasticsearchIndexModel]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{es_host}/_cat/indices?format=json")
        response.raise_for_status()
        raw_list = response.json()

        # Validates and parses the Elasticsearch metadata payload using Pydantic v2
        return [ElasticsearchIndexModel.model_validate(item) for item in raw_list]

async def main():
    try:
        indices = await query_diskover_indices("http://localhost:9200")
        diskover_indices = [idx for idx in indices if idx.index.startswith("diskover-")]
        print(f"Discovered {len(diskover_indices)} Diskover index/indices:")
        for idx in diskover_indices:
            print(f"- Index: {idx.index} | Health: {idx.health} | Files Indexed: {idx.docs_count} | Storage: {idx.store_size}")
    except Exception as e:
        print(f"Validation failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

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
- Last reviewed: 2026-11-05
- Confidence: high
