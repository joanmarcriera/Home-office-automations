# Grocy

## What it is

Grocy is a self-hosted groceries & household management solution for your home. It provides a centralized web interface to track your food stock, shopping lists, recipes, chores, and household tasks. Since the **v4.8.0 (August 2026)** release, it requires PHP 8.5+ and features optimized quantity unit (QU) handling for faster product setup, along with structured sub-item barcode scans. By late December 2026, Grocy is frequently paired with SOTA agentic systems (e.g. Claude 5.1 and FastMCP 3.1) to automate stock tracking via image recognition and voice prompts.

## What problem it solves

Managing a household's inventory manually often leads to food waste (expired items), forgotten chores, and inefficient shopping trips. Grocy automates this by tracking expiration dates, managing recurring tasks, and allowing you to plan meals based on what you actually have in stock.

## Where it fits in the stack

**Category**: Service / Home Management. It sits in the **personal organization and inventory** layer of the self-hosted stack.

## Typical use cases

- **Stock Management**: Tracking everything you have in your pantry and fridge.
- **Meal Planning**: Planning meals and automatically generating shopping lists for missing ingredients.
- **Task Management**: Managing recurring household chores like "Clean the fridge" or "Change furnace filter".
- **Battery/Equipment Tracking**: Keeping track of battery charging cycles and maintenance for home appliances.
- **Agentic Grocery Reordering**: Connecting an agent running Claude 5.1 or GPT-5.5 to check low stock levels via Grocy API and automatically build a cart on home shopping apps.

## Strengths

- **Comprehensive**: Covers almost every aspect of household management in one tool.
- **Local Control**: All data stays on your own server, ensuring privacy.
- **Automation Ready**: Offers a robust REST API for integration with barcode scanners or smart home systems.
- **Lightweight**: Easy to run on low-power devices like a Raspberry Pi.
- **Quantity Unit Flexibility**: Advanced mapping (v4.8.0+) allows for automatic "1:1" unit conversions and tiered packaging setups during product creation.

## Limitations

- **Data Entry**: Requires discipline to keep the stock updated as you consume and buy items.
- **UI Complexity**: The interface can be overwhelming for some users due to the large number of features.
- **No Native Mobile App**: While third-party apps exist, the official experience is web-based.

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

### Python Example with Pydantic v2 Validation
This production-ready Python example fetches current stock levels from Grocy, parses the response, and uses strict **Pydantic v2** validation schemas to ensure type safety.

```python
from typing import List, Optional
import requests
from pydantic import BaseModel, Field, RootModel, ValidationError

# Define Pydantic v2 model for individual stock entries
class GrocyStockItem(BaseModel):
    product_id: int = Field(..., description="Unique ID of the product")
    amount: float = Field(..., ge=0.0, description="Current stock amount")
    amount_opened: float = Field(default=0.0, ge=0.0, description="Amount of stock currently opened")
    best_before_date: Optional[str] = Field(None, description="ISO format best before date")
    location_id: Optional[int] = Field(None, description="Physical location ID in the pantry/fridge")

# Use RootModel for validation of top-level lists in Pydantic v2
class GrocyStockResponse(RootModel[List[GrocyStockItem]]):
    pass

def fetch_and_validate_stock(api_url: str, api_key: str) -> Optional[List[GrocyStockItem]]:
    url = f"{api_url}/api/stock"
    headers = {
        "GROCY-API-KEY": api_key,
        "accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Validate response payload with RootModel
        validated_data = GrocyStockResponse.model_validate(response.json())
        return validated_data.root

    except requests.RequestException as e:
        print(f"API request failed: {e}")
    except ValidationError as e:
        print(f"Pydantic v2 validation error: {e.json()}")
    return None

if __name__ == "__main__":
    # Example execution (replace with your actual local details)
    stock = fetch_and_validate_stock("http://localhost:9283", "YOUR_API_KEY")
    if stock:
        for item in stock:
            print(f"Product ID: {item.product_id} | Amount: {item.amount}")
```

### Curl Example
```bash
# Get system information
curl -X GET "http://localhost:9283/api/system/info" \
     -H "GROCY-API-KEY: <your_api_key>"
```

### Barcode Scanning
To implement barcode scanning for faster data entry:
1. **Third-Party Apps**: Use "Grocy-Barcode" (Android/iOS) or "Grocy-Desktop" to connect to your instance via the API.
2. **Setup**:
   - In Grocy UI, go to **Manage API keys** and create a new key.
   - Enter your server URL and the API key into the app.
3. **Usage**: Scan a product's barcode to instantly add it to your shopping list or consume it from stock.

## Related tools / concepts

- [Homebox](homebox.md) — for non-food inventory and organization
- [Mealie](mealie.md) — for recipe management and meal planning
- [Paperless-ngx](paperless-ngx.md) — for archiving grocery receipts and warranties
- [Home Assistant](home-assistant.md) — for integrating Grocy data into smart home dashboards
- [Vikunja](vikunja.md) — for managing larger household projects and complex task lists
- [Linkwarden](linkwarden.md) — for saving online recipes and kitchen guides
- [Nextcloud](nextcloud.md) — For synchronizing meal planning documents and recipes.
- [Rclone Automation](rclone-automation.md) — For automated off-site backups of the Grocy database.
- [Authentik](authentik.md) — For securing the Grocy web interface with SSO.

## Backlog
- [ ] Perform quarterly technical freshness audit.
- [x] Set up barcode scanning via mobile app.

## Sources / References

- [Official Website](https://grocy.info/)
- [Grocy Demo](https://en.demo.grocy.info/)
- [LinuxServer.io Grocy Documentation](https://docs.linuxserver.io/images/docker-grocy/)

## Contribution Metadata

- Last reviewed: 2026-12-31
- Confidence: high
