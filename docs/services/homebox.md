# Homebox

## What it is

Homebox is an inventory and organization system built specifically for home users, focusing on simplicity, speed, and ease of use. Written in Go, it is extremely lightweight (typically using less than 50MB of RAM) and uses SQLite for portable data management.

## What problem it solves

Keeping track of physical belongings, their locations, warranties, and purchase details can be difficult. Homebox provides a centralized, self-hosted system to organize items across multiple locations (e.g., "Garage", "Attic", "Storage Unit") without the complexity of enterprise asset management tools.

## Where it fits in the stack

**Category**: Service / Inventory Management. It sits in the **personal/home organization** layer of the self-hosted stack.

## Typical use cases
- Organizing household belongings across multiple rooms and storage areas.
- Tracking warranties, purchase dates, and prices for insurance purposes.
- Managing small collections (e.g., tools, books, electronics).

## Strengths
- **Extremely lightweight**: Minimal resource footprint (Go + SQLite).
- **Simplicity**: Focused on home use rather than complex enterprise workflows.
- **Portable data**: Uses a single SQLite database file for easy backups.
- **Fast and responsive**: Modern, clean web interface.

## Limitations
- **Single-user focus**: Lacks complex multi-user permission models.
- **Minimal integrations**: Primarily a standalone system with a basic REST API.
- **Not for enterprise**: Not designed for massive concurrent users or complex supply chain needs.

## When to use it
- When you need a simple, fast inventory system to track household items.
- For organizing belongings across multiple locations (e.g., "Garage", "Attic", "Storage Unit").
- To keep track of warranties, purchase dates, and prices for insurance or maintenance purposes.
- When you want a self-hosted solution that is easy to backup and move.

## When not to use it
- When you need complex multi-user permission models or enterprise-grade asset management.
- When you require deep integration with e-commerce platforms or point-of-sale systems.
- If you need a system that supports a massive number of concurrent users (it is designed for home/small team use).

## Links
- [Official Website](https://homebox.software/)
- [GitHub Repository](https://github.com/sysadminsmedia/homebox)
- [Live Demo](https://demo.homebox.software/)

## Related tools / concepts
- [Grocy](grocy.md) — focused on groceries and meal planning
- [Mealie](mealie.md) — recipe manager with food inventory features
- [Snipe-IT](https://snipeitapp.com/) — Enterprise-grade IT asset management
- [Paperless-ngx](paperless-ngx.md) — for archiving physical receipts and warranties
- [Actual Budget](actual-budget.md) — for tracking the financial side of purchases

## Getting started

### Docker
The fastest way to run Homebox is using the official Docker image:

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
2. Create your initial admin account.
3. Navigate to **Locations** and create a new location called "Living Room".
4. Go to **Items**, click **Add Item**, and add "Smart TV" to the "Living Room" location.
5. You've started your inventory!

## CLI examples
While Homebox is primarily managed via its web interface, you can use `docker exec` for basic administrative tasks:

```bash
# View the help menu for the Homebox binary
docker exec homebox /app/homebox --help

# Check the version of the running Homebox instance
docker exec homebox /app/homebox version

# Export the internal database to a SQL file (manual backup)
docker exec homebox sqlite3 /data/homebox.db .dump > backup.sql
```

## API examples
Homebox provides a REST API for programmatic interaction.

### Health Check
```bash
curl -X GET "http://localhost:3100/api/v1/health"
```

### List Items (using a Bearer Token)
If authentication is enabled, you will need to provide an API token:

```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
     "http://localhost:3100/api/v1/items"
```

### Python Example
```python
import requests

url = "http://localhost:3100/api/v1/items"
headers = {"Authorization": "Bearer YOUR_API_TOKEN"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    items = response.json()
    for item in items:
        print(f"Item: {item['name']}, Location: {item['location']['name']}")
```

## Backlog
- Export data to CSV for insurance purposes.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-02

## Sources / References
- https://github.com/sysadminsmedia/homebox
- https://homebox.software/
- https://snipeitapp.com/
