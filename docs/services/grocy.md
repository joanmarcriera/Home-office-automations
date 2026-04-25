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
The recommended way to install Grocy is via Docker Compose:

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
      - /path/to/config:/config
    ports:
      - 9283:80
    restart: unless-stopped
```

### Docker Run
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
While primarily web-based, you can use the Docker CLI for maintenance:

```bash
# View container logs to troubleshoot startup
docker logs -f grocy

# Execute a database migration manually (if needed)
docker exec -it grocy php /app/www/public/index.php /migrate

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
if response.status_code == 200:
    for item in response.json():
        print(f"Product ID: {item['product_id']}, Amount: {item['amount']}")
```

### Curl Example
```bash
# Get current stock
curl -X GET "http://localhost:9283/api/stock" \
     -H "GROCY-API-KEY: <your_api_key>"

# Add a specific amount to stock (Product ID 1)
curl -X POST "http://localhost:9283/api/stock/products/1/add" \
     -H "GROCY-API-KEY: <your_api_key>" \
     -H "Content-Type: application/json" \
     -d '{"amount": 5, "transaction_type": "purchase"}'
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
- [Grocy API Documentation (Swagger)](https://demo.grocy.info/api)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high
