# Homebox

## What it is

## What it is
A lightweight, self-hosted inventory management system written in Go. It uses a single SQLite database for all data, making it easy to host and backup.

## What problem it solves
It centralizes the tracking of household items, warranties, and insurance information, replacing disorganized spreadsheets or physical receipts with a searchable, location-aware digital catalog.

## Where it fits in the stack
It is a **Standalone Service** in the home automation stack, typically deployed via Docker and accessible via a web browser.

## Typical use cases
- Tracking high-value electronics for insurance purposes.
- Organizing storage units, attics, and garages.
- Managing specialized collections (e.g., tools, camping gear).

## Strengths
- **Lightweight**: Minimal CPU and RAM footprint.
- **Fast**: Responsive web interface.
- **Portable**: SQLite backend makes backups trivial.

## Limitations
- **Simplicity**: Lacks advanced supply chain or POS features found in enterprise ERPs.
- **Permissions**: Limited multi-user role-based access control.

## Description
It helps you keep track of your belongings, their locations, warranties, and purchase details. Written in Go, it is extremely lightweight (typically using less than 50MB of RAM) and uses SQLite for portable data management.

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
- [Grocy](grocy.md)
- [Inventory](inventory.md)
- [Paperless-ngx](paperless-ngx.md)
- [Immich](immich.md)
- [Nextcloud](nextcloud.md)

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

## Backup and insurance workflow

Homebox is most valuable when inventory data survives the loss of the server that hosts it:

1. Store the `/data` volume on backed-up storage, not inside an ephemeral container layer.
2. Schedule a database copy or SQL dump before major upgrades.
3. Export item lists and attachment metadata before insurance renewal periods.
4. Keep photos, receipts, and warranty PDFs in [Paperless-ngx](paperless-ngx.md) or another document store, then link the relevant record from Homebox notes.

For household automation, treat Homebox as the inventory index and the document system as the evidence archive. That avoids making one service responsible for both structured asset tracking and long-term document retention.

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
- Document a tested restore run from a copied `/data` volume.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-07

## Sources / References
- https://github.com/sysadminsmedia/homebox
- https://homebox.software/
- https://snipeitapp.com/
- https://docs.paperless-ngx.com/
