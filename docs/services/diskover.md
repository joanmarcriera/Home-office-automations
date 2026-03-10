# Diskover

Diskover is an open-source file indexer and data management tool.

## Description
It helps you identify disk space usage, find old or duplicate files, and gain insights into your storage infrastructure.

## Links
- [GitHub Repository](https://github.com/diskoverdata/diskover-community)

## Alternatives
- [WizTree](https://diskanalyzer.com/) (Non-OSS)
- [ncdu](https://dev.yorhel.nl/ncdu)

## Getting started

### Docker installation
Diskover requires an Elasticsearch instance. Using Docker Compose is the recommended way to set up both:

```yaml
version: '2'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.10.1
    environment:
      - discovery.type=single-node
  diskover:
    image: lscr.io/linuxserver/diskover
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/London
      - ES_HOST=elasticsearch
    volumes:
      - /path/to/config:/config
      - /path/to/data:/data
    ports:
      - 80:80
    depends_on:
      - elasticsearch
```

## CLI examples

You can run indexing tasks manually using the `diskover.py` script inside the container.

```bash
# Run a manual index of the /data directory
docker exec -it diskover python3 /app/diskover/diskover.py -i my_index_name /data

# List all current indices in Elasticsearch
curl -X GET "http://localhost:9200/_cat/indices?v"

# Remove an old index
curl -X DELETE "http://localhost:9200/my_old_index"
```

## API examples

Diskover stores its data in Elasticsearch, so you can use the Elasticsearch REST API to query Diskover's data.

```bash
# Search for files larger than 1GB in the diskover index
curl -X GET "http://localhost:9200/diskover-test/_search?q=filesize:>1073741824&pretty"
```

## Backlog
- Integrate with TrueNAS SCALE via NFS mount.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/diskoverdata/diskover-community
- https://diskanalyzer.com/
- https://dev.yorhel.nl/ncdu
- https://docs.linuxserver.io/images/docker-diskover/
- https://github.com/diskoverdata/diskover-community/blob/master/INSTALL.md
