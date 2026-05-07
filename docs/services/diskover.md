# Diskover

Diskover is an open-source file indexer and data management tool that uses Elasticsearch to index and manage data across heterogeneous storage systems.

## What it is
Diskover is a high-performance file system crawler and disk space analyzer. It crawls your storage (local drives, NFS, SMB) and stores the metadata in Elasticsearch, providing a powerful web interface to search, filter, and visualize your data.

## What problem it solves
It solves the problem of "Data Sprawl" across large storage arrays. When you have terabytes of data across multiple servers, finding old versions of files, identifying duplicate data, or seeing which user is consuming the most space becomes difficult. Diskover makes your entire storage infrastructure searchable and quantifiable.

## Where it fits in the stack
In a homelab, Diskover acts as the **Storage Intelligence Layer**. It provides the metadata that allows automation scripts to identify which files should be archived, moved to cold storage (like Storj), or deleted to free up space.

## Typical use cases
- **Data Cleanup**: Finding and deleting files that haven't been accessed in over 2 years.
- **Duplicate Identification**: Using file hashes to find exact duplicates across different mounts.
- **Cost Analysis**: Calculating the cost of storage per department or user.
- **Dark Data Discovery**: Finding large log files or temp files that were forgotten.

## Strengths
- **Massive Scalability**: Leverages Elasticsearch to handle millions of file records with sub-second search times.
- **Extensible**: Supports custom plugins for metadata extraction.
- **Powerful Visualization**: Includes treemaps and charts for disk usage analysis.
- **Heterogeneous**: Can index anything that can be mounted as a file system.

## Limitations
- **Infrastructure Heavy**: Requires a running Elasticsearch instance, which is resource-intensive.
- **Scheduled, Not Real-time**: It provides a snapshot in time; changes to the file system aren't reflected until the next crawl.
- **Complex Setup**: Setting up the worker/web/ES stack can be daunting for beginners.

## When to use it
- When you need to gain visibility into large, heterogeneous storage environments.
- To identify "dark data," such as old, large, or duplicate files that are wasting space.
- When you want a searchable index of your files without having to scan the live file system every time.
- For data management tasks like cleanup, migration, or capacity planning.

## When not to use it
- If you only need a simple, real-time disk usage visualizer for a single local drive (consider `ncdu` or WizTree).
- If you don't have the resources to run Elasticsearch, which is a mandatory requirement for Diskover.
- For real-time file monitoring, as Diskover relies on scheduled indexing tasks.

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

Indexing and management tasks are performed using the `diskover.py` script.

```bash
# Index a specific directory into a new index
docker exec -it diskover python3 /app/diskover/diskover.py -i diskover-data /data

# Run an index task in the background (detached)
docker exec -d diskover python3 /app/diskover/diskover.py -i diskover-data /data

# List all indices in the Elasticsearch instance
curl -X GET "http://elasticsearch:9200/_cat/indices?v"

# Remove an index from Elasticsearch
curl -X DELETE "http://elasticsearch:9200/diskover-old-index"
```

## API examples

Diskover stores its data in Elasticsearch, allowing you to use the standard Elasticsearch REST API for advanced queries.

### Search for files larger than 1GB
```bash
curl -X GET "http://elasticsearch:9200/diskover-data/_search?q=filesize:>1073741824&pretty"
```

### Python example to query indices
```python
import requests

es_url = "http://elasticsearch:9200/_cat/indices?format=json"
response = requests.get(es_url)
indices = response.json()

for index in indices:
    if index['index'].startswith('diskover-'):
        print(f"Diskover Index: {index['index']}, Documents: {index['docs.count']}")
```

## Related tools / concepts
- [Storj](storj.md)
- [Syncthing](syncthing.md)
- [Rclone](https://rclone.org/)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [Paperless-ngx](paperless-ngx.md)

## Backlog
- Integrate with TrueNAS SCALE via NFS mount.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-15

## Sources / References
- [Diskover GitHub Repository](https://github.com/diskoverdata/diskover-community)
- [Diskover Official Site](https://diskoverdata.com/)
- [WizTree Official Site](https://diskanalyzer.com/)
- [ncdu Official Site](https://dev.yorhel.nl/ncdu)
- [LinuxServer.io Diskover Image](https://docs.linuxserver.io/images/docker-diskover/)
