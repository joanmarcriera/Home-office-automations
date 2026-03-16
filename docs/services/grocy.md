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

### Docker
The recommended way to install Grocy is via the LinuxServer.io Docker image:

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
1. Access the web interface at `http://localhost:9283`.
2. Log in with the default credentials:
   - **Username:** `admin`
   - **Password:** `admin`
3. Navigate to **Stock overview** to see your current inventory or add your first product.

## CLI examples
Grocy does not have an official CLI. However, you can manage the Docker container and perform maintenance tasks:

```bash
# View container logs
docker logs grocy

# Access the container shell
docker exec -it grocy /bin/bash

# Check the build version of the running container
docker inspect -f '{{ index .Config.Labels "build_version" }}' grocy
```

## API examples
Grocy provides a RESTful API. Authenticate using an API key (generated in the web UI under "Manage API keys").

### Python Example
```python
import requests

url = "http://localhost:9283/api/stock"
headers = {
    "GROCY-API-KEY": "YOUR_API_KEY",
    "accept": "application/json"
}

response = requests.get(url, headers=headers)
print(response.json())
```

### Curl Example
```bash
# Get current stock
curl -X GET "http://localhost:9283/api/stock" \
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

- Last reviewed: 2026-03-02
- Confidence: high
