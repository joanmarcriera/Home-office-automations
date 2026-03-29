# Homebox

Homebox is an inventory and organization system for your home.

## Description
It is designed to be simple, fast, and easy to use. It helps you keep track of your belongings, where they are, and what they are worth.

## When to use it
- When you need a simple, fast inventory system for home use.
- When you want to track belongings, warranties, and purchase dates without complex overhead.

## When not to use it
- When you need complex multi-user permissions or enterprise-grade asset management.
- When you require deep integration with e-commerce or point-of-sale systems.

## Getting started

### Docker
To run Homebox using Docker:

```bash
docker run -d \
  --name homebox \
  --restart unless-stopped \
  --publish 3100:7745 \
  -v /path/to/data:/data \
  ghcr.io/sysadminsmedia/homebox:latest
```

Access the web interface at `http://localhost:3100`.

### Hello World
1. Open `http://localhost:3100` in your browser.
2. Create an initial account (the first user is the admin).
3. Go to **Locations** and create a "Main Storage".
4. Go to **Items** and add "My First Item" to start tracking your inventory.

## CLI examples
Management is primarily via the web UI, but you can use `docker exec` for basic tasks:

```bash
# View container logs
docker logs homebox

# Check Homebox version
docker exec homebox /app/homebox --version

# View help for available commands
docker exec homebox /app/homebox --help
```

## API examples
Homebox provides a REST API for data interaction. Use a Bearer token if authentication is enabled:

```bash
# Basic health check
curl -X GET "http://localhost:3100/api/v1/health"

# List items (requires API token)
curl -H "Authorization: Bearer YOUR_TOKEN" "http://localhost:3100/api/v1/items"
```

## Links
- [GitHub Repository](https://github.com/sysadminsmedia/homebox)

## Alternatives
- [Grocy](grocy.md)
- [Snipe-IT](https://snipeitapp.com/)

## Backlog
- Export data to CSV for insurance purposes.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/sysadminsmedia/homebox
- https://snipeitapp.com/
