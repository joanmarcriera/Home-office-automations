# Portracker

## What it is

Portracker is a self-hosted, real-time network port monitoring and service discovery tool. It scans your network to identify active ports and maps them to the services they represent, providing a centralized dashboard for network visibility.

## What problem it solves

In complex homelab or home-office environments, keeping track of which service is using which port can be difficult, often leading to port conflicts or forgotten "ghost" services. Portracker provides a real-time, visual map of your network's port usage, integrating directly with Docker and TrueNAS to provide context for each open port.

## Where it fits in the stack

**Category**: Service / Infrastructure Monitoring. It sits in the **network observability** layer, providing a higher-level view than raw packet sniffers but more focus on port mapping than general-purpose metrics dashboards.

## Typical use cases
- Monitoring active ports on a local network or server.
- Discovering "shadow IT" or unexpected services running in containers.
- Planning port assignments for new services to avoid conflicts.
- Auditing network exposure for security purposes.

## Strengths
- **Real-time Discovery**: Automatically detects new services as they come online.
- **Docker Integration**: Maps ports directly to container names and status.
- **Lightweight**: Low resource consumption, making it suitable for always-on monitoring.
- **Clean Dashboard**: Easy-to-read interface for quick network audits.

## Limitations
- **Not a Firewall**: It monitors ports but does not provide active blocking or security enforcement.
- **Local Scope**: Primarily designed for local network segments; large-scale enterprise scanning is better handled by tools like Nmap.

## When to use it
- When you want to monitor open ports on your network in real-time.
- To discover new services running in Docker containers or on TrueNAS.
- To avoid port conflicts by having a clear map of assigned ports.

## When not to use it
- For deep packet inspection or security auditing (use specialized tools like Suricata or Snort).
- If you only need a one-time port scan (use `nmap`).

## Getting started

### Docker Compose
The recommended way to deploy Portracker is via Docker Compose. Enable `ENABLE_AUTH` for secure access.

```yaml
services:
  portracker:
    image: mostafawahied/portracker:latest
    container_name: portracker
    restart: unless-stopped
    pid: "host"
    cap_add:
      - SYS_PTRACE
      - SYS_ADMIN
    security_opt:
      - apparmor:unconfined
    ports:
      - "4999:4999"
    environment:
      - ENABLE_AUTH=true
      - SESSION_SECRET=change-this-to-a-random-string
    volumes:
      - ./portracker-data:/data
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

### Hello World
1. Start Portracker: `docker compose up -d`.
2. Open `http://localhost:4999` in your browser.
3. If authentication is enabled, follow the setup wizard to create your admin account.
4. Observe how Portracker automatically discovers running Docker containers and their mapped ports.
5. Launch a new container (e.g., `docker run -d -p 8080:80 nginx`) and watch it appear in the dashboard within seconds.

## CLI examples
Manage the Portracker container and its environment:

```bash
# View real-time application logs
docker logs -f portracker

# Inspect the container environment variables
docker inspect portracker --format='{{range .Config.Env}}{{println .}}{{end}}'

# Reset the internal SQLite database (DANGER: deletes all data)
docker exec -it portracker rm /data/portracker.db
```

## API examples
Portracker provides internal API endpoints for health and status monitoring.

### Health Check
```bash
curl -X GET "http://localhost:4999/api/v1/health"
```

### Peer-to-Peer Status
In multi-node setups, you can query the status of a specific peer:

```bash
curl -X GET "http://localhost:4999/api/v1/status" \
     -H "x-api-key: YOUR_PEER_API_KEY"
```

## Related tools / concepts
- [Home Assistant](home-assistant.md) — for monitoring smart device availability
- [Netdata](https://www.netdata.cloud/) — for deep real-time system and network metrics
- [Uptime Kuma](https://github.com/louislam/uptime-kuma) — for service availability monitoring
- [SearXNG](searXNG.md) — for privacy-respecting network-wide search
- [Nmap](https://nmap.org/) — for one-time, deep security port scans

## Backlog
- Set up alerts for unexpected port changes.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-04

## External links
- [GitHub Repository](https://github.com/mostafa-wahied/portracker)

## Sources / References
- https://github.com/mostafa-wahied/portracker
- https://nmap.org/
- https://www.netdata.cloud/
