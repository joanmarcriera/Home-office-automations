# Diskover

Diskover is an open-source file indexer and data management tool that uses Elasticsearch to index and manage data across heterogeneous storage systems.

## Description
It helps you identify disk space usage, find old or duplicate files, and gain insights into your storage infrastructure. It provides a web-based dashboard for visualizing and searching through your indexed file systems.

## When to use it
- When you need to gain visibility into large, heterogeneous storage environments.
- To identify "dark data," such as old, large, or duplicate files that are wasting space.
- When you want a searchable index of your files without having to scan the live file system every time.
- For data management tasks like cleanup, migration, or capacity planning.

## When not to use it
- If you only need a simple, real-time disk usage visualizer for a single local drive (consider `ncdu` or WizTree).
- If you don't have the resources to run Elasticsearch, which is a mandatory requirement for Diskover.
- For real-time file monitoring, as Diskover relies on scheduled indexing tasks.

## Links
- [GitHub Repository](https://github.com/diskoverdata/diskover-community)
- [Official Website](https://diskoverdata.com/)

## Alternatives
- [WizTree](https://diskanalyzer.com/) (Non-OSS, Windows)
- [ncdu](https://dev.yorhel.nl/ncdu) (CLI-based)
- [WinDirStat](https://windirstat.net/)

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
curl -X GET "http://localhost:9200/_cat/indices?v"

# Remove an index from Elasticsearch
curl -X DELETE "http://localhost:9200/diskover-old-index"
```

## API examples

Diskover stores its data in Elasticsearch, allowing you to use the standard Elasticsearch REST API for advanced queries.

### Search for files larger than 1GB
```bash
curl -X GET "http://localhost:9200/diskover-data/_search?q=filesize:>1073741824&pretty"
```

### Python example to query indices
```python
import requests

es_url = "http://localhost:9200/_cat/indices?format=json"
response = requests.get(es_url)
indices = response.json()

for index in indices:
    if index['index'].startswith('diskover-'):
        print(f"Diskover Index: {index['index']}, Documents: {index['docs.count']}")
```

## Backlog
- Integrate with TrueNAS SCALE via NFS mount.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-02

## Sources / References
- https://github.com/diskoverdata/diskover-community
- https://diskanalyzer.com/
- https://dev.yorhel.nl/ncdu
- https://docs.linuxserver.io/images/docker-diskover/
- https://github.com/diskoverdata/diskover-community/blob/master/INSTALL.md
