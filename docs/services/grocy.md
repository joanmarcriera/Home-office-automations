# Grocy

Grocy is a self-hosted groceries & household management solution for your home.

## Description
It tracks your stock, shopping list, recipes, and more.

## When to use it
- When you want to reduce food waste by tracking expiration dates.
- When you need a centralized system for household tasks, chores, and battery tracking.
- For meal planning based on current stock levels.

## When not to use it
- If you only need a simple, single-user grocery list (Grocy might be overkill).
- For enterprise-level inventory management or point-of-sale requirements.

## Getting started

### Docker Compose
The recommended way to run Grocy is using Docker Compose:

```yaml
services:
  grocy:
    image: lscr.io/linuxserver/grocy:latest
    container_name: grocy
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    volumes:
      - /path/to/grocy/config:/config
    ports:
      - 9283:80
    restart: unless-stopped
```

### Docker CLI
```bash
docker run -d \
  --name=grocy \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -p 9283:80 \
  -v /path/to/config:/config \
  --restart unless-stopped \
  lscr.io/linuxserver/grocy:latest
```

### Hello World
1. Start the container and access the web interface at `http://localhost:9283`.
2. Log in with the default credentials (**Username:** `admin`, **Password:** `admin`).
3. Go to **Master Data > Products** to add your first item.
4. Go to **Purchase** to add stock for that product.
5. Check the **Stock overview** to see your inventory and its expiration status.

## CLI examples
Use the Docker CLI for maintenance and troubleshooting:

```bash
# View real-time container logs
docker logs -f grocy

# Access the container shell for advanced maintenance
docker exec -it grocy /bin/bash

# Check the build version of the running image
docker inspect -f '{{ index .Config.Labels "build_version" }}' grocy
```

## API examples
Grocy features a RESTful API. Generate an API key in the web UI under **Manage API keys**.

### Python Example
```python
import requests

# Get current stock levels
url = "http://localhost:9283/api/stock"
headers = {"GROCY-API-KEY": "YOUR_API_KEY", "accept": "application/json"}

response = requests.get(url, headers=headers)
if response.ok:
    for item in response.json():
        print(f"Product: {item['product_id']}, Amount: {item['amount']}")
```

### Curl Example
```bash
# Get system information
curl -X GET "http://localhost:9283/api/system/info" \
     -H "GROCY-API-KEY: <your_api_key>"
```

## Links
- [Official Website](https://grocy.info/)
- [Demo](https://en.demo.grocy.info/)

## Alternatives
- [Homebox](homebox.md)
<!-- - [KitchenOwl](https://github.com/KitchenOwl/kitchenowl) (Link broken) -->

## Backlog
- Set up barcode scanning via mobile app.

## Sources / References

- [Official Website](https://grocy.info/)
- [LinuxServer.io Grocy Documentation](https://docs.linuxserver.io/images/docker-grocy/)

## Contribution Metadata

- Last reviewed: 2026-05-04
- Confidence: high
