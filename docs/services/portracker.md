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
The recommended way to deploy Portracker is via Docker Compose. It requires host PID access and specific capabilities to monitor system ports.

```yaml
services:
  portracker:
    image: mostafawahied/portracker:latest
    container_name: portracker
    restart: unless-stopped
    pid: "host"  # Required for port detection
    cap_add:
      - SYS_PTRACE     # Allows reading other PIDs' /proc entries
      - SYS_ADMIN      # Allows namespace access for host ports
    security_opt:
      - apparmor:unconfined # Required on some systems for port access
    ports:
      - "4999:4999"
    volumes:
      - ./data:/data
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

Access the dashboard at `http://localhost:4999`.

### Hello World
1. Start Portracker: `docker compose up -d`.
2. Open `http://localhost:4999` in your browser.
3. Observe how Portracker automatically discovers other running Docker containers and their ports on your system.
4. Run a new container (e.g., `docker run -d -p 8888:80 nginx`) and see it appear in real-time.

## CLI examples
Management and inspection can be done via Docker commands:

```bash
# View real-time logs of discovered services
docker logs -f portracker

# Check the version of Portracker
docker exec portracker ./portracker --version

# Force a re-scan by clearing the cache
docker exec portracker rm -rf /app/data/cache
```

## API examples
Portracker provides a simple health check and status API:

```bash
# Check service health
curl http://localhost:4999/api/v1/health

# Check the scan status (if supported)
curl http://localhost:4999/api/v1/status
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
- Last reviewed: 2026-03-02

## Sources / References
- https://github.com/mostafa-wahied/portracker
- https://nmap.org/
- https://www.netdata.cloud/
