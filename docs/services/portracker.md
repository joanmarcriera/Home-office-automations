# Portracker

Portracker is a self-hosted, real-time port monitoring and discovery tool.

## Description
It provides a dashboard to monitor active ports on your network and discover new services. It integrates well with TrueNAS and Docker to display native apps, virtual machines, and containers.

## When to use it
- When you want to monitor open ports on your network in real-time.
- To discover new services running in Docker containers or on TrueNAS.
- To avoid port conflicts by having a clear map of assigned ports.

## When not to use it
- For deep packet inspection or security auditing (use specialized tools like Suricata or Snort).
- If you only need a one-time port scan (use `nmap`).

## Getting started

### Docker Compose
The easiest way to deploy Portracker is via Docker Compose:

```yaml
services:
  portracker:
    image: mostafawahied/portracker:latest
    container_name: portracker
    ports:
      - "3050:3050"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./data:/app/data
    restart: always
```

Access the dashboard at `http://localhost:3050`.

### Hello World
1. Start Portracker: `docker compose up -d`.
2. Open `http://localhost:3050` in your browser.
3. Observe how Portracker automatically discovers other running Docker containers and their ports on your system.
4. Run a new container (e.g., `docker run -d -p 8888:80 nginx`) and see it appear in real-time.

## CLI examples
You can interact with the Portracker container using Docker commands:

```bash
# View real-time logs of discovered services
docker logs -f portracker

# Check the version of Portracker
docker exec portracker ./portracker --version

# Clear the scan cache
docker exec portracker rm -rf /app/data/cache
```

## API examples
Portracker provides a simple health check and status API:

```bash
# Check service health
curl http://localhost:3050/health
```

## Links
- [GitHub Repository](https://github.com/mostafa-wahied/portracker)

## Alternatives
- [Nmap](https://nmap.org/)
- [Netdata](https://www.netdata.cloud/)

## Backlog
- Set up alerts for unexpected port changes.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/mostafa-wahied/portracker
- https://nmap.org/
- https://www.netdata.cloud/
