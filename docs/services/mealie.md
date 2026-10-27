# Mealie

Mealie is a self-hosted, recipe manager and meal planning platform featuring a FastAPI REST backend and a modern reactive Web frontend.

## What it is

Mealie provides an all-in-one culinary data management system designed to import, organize, scale, and schedule recipes while generating unified grocery shopping lists across multi-user households.

By early 2027, Mealie natively supports integration with leading foundation models—including [Claude 5.6](../tools/ai_knowledge/claude.md), [GPT-5.6](../tools/ai_knowledge/openai.md), [Gemini 4.0 Ultra](../tools/ai_knowledge/gemini.md), [DeepSeek-V4](../tools/ai_knowledge/claude.md), and local [Qwen 3.6 VL](../tools/ai_knowledge/qwen.md)—via [MCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md) and [FastMCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md) servers. This allows autonomous agents to perform meal optimization, dietary constraint tracking, pantry deficit checks via [Grocy](grocy.md), and dynamic shopping list generation.

```
+-------------------------------------------------------------------------------------------------------------------+
|                                          MEALIE ARCHITECTURE & FLUID INTEGRATION                                  |
+-------------------------------------------------------------------------------------------------------------------+
|                                                                                                                   |
|  +------------------------+     +-------------------------+     +-------------------------+                       |
|  | Web Recipe Scraper     |     | Social Video Import     |     | OCR Scanned Recipe PDF  |                       |
|  | (recipe-scrapers)      |     | (YouTube / TikTok AI)   |     | (Paperless-ngx)         |                       |
|  +-----------+------------+     +-----------+-------------+     +-----------+-------------+                       |
|              |                              |                               |                                     |
|              +------------------------------+-------------------------------+                                     |
|                                             |                                                                     |
|                                             v                                                                     |
|                             +-------------------------------+                                                     |
|                             |   Mealie Core (FastAPI App)   |                                                     |
|                             |   PostgreSQL / SQLite Storage |                                                     |
|                             +---------------+---------------+                                                     |
|                                             | REST / OpenAPI & FastMCP 3.1                                        |
|                                             v                                                                     |
|     +---------------------------------------+---------------------------------------+                             |
|     |                                       |                                       |                             |
|     v                                       v                                       v                             |
| +-------------------------+       +--------------------------+        +--------------------------+                |
| | FastMCP 3.1 Agent Server|       | Home Assistant           |        | Grocy / Task Sync        |                |
| | (Claude / GPT / Qwen)   |       | Dashboard & Meal Sensor  |        | (n8n / Vikunja)          |                |
| +-------------------------+       +--------------------------+        +--------------------------+                |
|                                                                                                                   |
+-------------------------------------------------------------------------------------------------------------------+
```

## What problem it solves

Digital recipe collection is historically fragmented across browser bookmarks, physical cookbooks, mobile screenshots, and ad-saturated blogs. Furthermore, translating a collection of selected recipes into a normalized, non-redundant grocery list requires manual ingredient parsing and unit conversion.

Mealie solves this by serving as a central, ad-free culinary data repository. Its scraping engine converts raw Web URLs into schema-compliant recipes, automatically standardizing ingredient units and serving quantities. Integrated with AI models, it converts social media video tutorials (e.g., YouTube Shorts, TikTok) and hand-written recipe cards into structured, scaled meal plans.

## Where it fits in the stack

**Category**: Service / Household Planning & Operations.

Mealie sits in the **application & inventory management layer**:
1. **Upstream Data Ingestion**: Web scrapers, YouTube/TikTok transcription via [Whisper](whisper.md), and [Paperless-ngx](paperless-ngx.md) OCR.
2. **Core Operations**: Mealie FastAPI container + PostgreSQL database.
3. **Downstream Integration**: [Home Assistant](home-assistant.md) wall-mounted displays, [Grocy](grocy.md) inventory reconciliation, and [Vikunja](vikunja.md) task management.
4. **Agent Layer**: FastMCP 3.1 tool servers providing recipe access to autonomous household agents.

## Typical use cases

- **Single-Click Recipe Extraction**: Ingesting recipe URLs, automatically stripping away narrative text, and organizing ingredients into structured categories.
- **Visual Drag-and-Drop Meal Planning**: Building weekly breakfast, lunch, and dinner plans on an interactive family calendar.
- **Consolidated Shopping List Aggregation**: Automatically combining overlapping ingredients (e.g., "3 cloves garlic" + "2 cloves garlic" -> "5 cloves garlic") across selected weekly meals.
- **AI-Powered Social Video Parsing**: Extracting steps and ingredient lists from culinary videos using vision-language models ([Qwen 3.6 VL](../tools/ai_knowledge/qwen.md)) or audio transcription ([Whisper](whisper.md)).
- **Macro & Nutritional Analysis**: Evaluating weekly meal plan nutritional data via FastMCP tool calls connected to LLM knowledge bases.

## Strengths

- **High-Precision Parsing**: Powered by the open-source `recipe-scrapers` library, supporting thousands of domain formats.
- **Multi-Tenant Authorization**: Full support for Groups (tenant boundary) and Households (shared recipe pool with separate meal calendars).
- **FastMCP 3.1 Protocol Native**: Exposes clean tool protocols for direct connection to Claude, GPT-5, and open-weights agents.
- **Full OpenAPI Compliance**: Every application function is available via documented REST endpoints.

## Limitations

- **Complex Inventory Reconciliation**: Does not include barcode scanning or real-time shelf-life tracking (requires pairing with [Grocy](grocy.md)).
- **Database Scalability**: Requires PostgreSQL for large multi-family deployments; SQLite is restricted to smaller single-family setups.

## When to use it

- When replacing commercial meal-planning services (Paprika, AnyList, Whisk) with a self-hosted alternative.
- When creating automated, agentic meal-planning systems that sync with local smart home dashboards.
- When organizing family recipes in a clean, multi-user environment.

## When not to use it

- For complex commercial restaurant kitchen management or inventory auditing (consider [Grocy](grocy.md)).
- When seeking a simple text-based task list without recipe parsing or nutritional awareness (use [Vikunja](vikunja.md)).

## Getting started

### Installation via Docker Compose

```yaml
version: "3.8"
services:
  mealie:
    image: ghcr.io/mealie-recipes/mealie:v3.22.0
    container_name: mealie
    restart: unless-stopped
    ports:
      - "9925:9000"
    volumes:
      - ./mealie-data:/app/data
    environment:
      - ALLOW_SIGNUP=false
      - PUID=1000
      - PGID=1000
      - TZ=UTC
      - MAX_WORKERS=2
      - WEB_CONCURRENCY=2
      - BASE_URL=http://mealie.local:9925
      - DEFAULT_EMAIL=admin@home.arpa
      - DEFAULT_PASSWORD=ChangeThisStrongPassword123
      - DEFAULT_GROUP=Home
      - DEFAULT_HOUSEHOLD=Family
      - DB_ENGINE=postgres
      - POSTGRES_USER=mealieuser
      - POSTGRES_PASSWORD=mealiepass
      - POSTGRES_SERVER=postgres-db
      - POSTGRES_PORT=5432
      - POSTGRES_DB=mealiedb
    depends_on:
      - postgres-db

  postgres-db:
    image: postgres:16-alpine
    container_name: mealie-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: mealieuser
      POSTGRES_PASSWORD: mealiepass
      POSTGRES_DB: mealiedb
    volumes:
      - mealie_pg_data:/var/lib/postgresql/data

volumes:
  mealie_pg_data:
```

### Execution Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User / Agent
    participant WebUI as Mealie Web UI / FastMCP
    participant Core as Mealie FastAPI Core
    participant Scraper as recipe-scrapers / LLM
    participant DB as PostgreSQL Database
    participant HA as Home Assistant REST

    User / Agent->>WebUI: Submit Recipe URL / Ingest Command
    WebUI->>Core: POST /api/recipes/create-from-url
    Core->>Scraper: Fetch & Parse HTML / Video Schema
    Scraper-->>Core: Return Extracted JSON Schema
    Core->>DB: Store Recipe & Ingredient Records
    Core-->>WebUI: Return Created Recipe Object
    Core->>HA: Push Notification ("New Recipe Added")
```

## Production Deployment & Orchestration

### Systemd Service Daemon (`/etc/systemd/system/mealie.service`)
To manage Mealie directly via systemd in non-Docker or bare-metal LXC setups:

```ini
[Unit]
Description=Mealie Household Recipe & Meal Planning Backend Service
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=mealie
Group=mealie
WorkingDirectory=/opt/mealie
ExecStart=/opt/mealie/venv/bin/uvicorn mealie.app:app --host 0.0.0.0 --port 9925 --workers 4
Restart=always
RestartSec=5
Environment="PRODUCTION=true"
Environment="DB_ENGINE=postgres"
Environment="POSTGRES_SERVER=127.0.0.1"
Environment="POSTGRES_USER=mealieuser"
Environment="POSTGRES_PASSWORD=mealiepass"
Environment="POSTGRES_DB=mealiedb"
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

## CLI examples

### 1. Ingesting a Web Recipe via REST
```bash
curl -X POST "http://localhost:9925/api/recipes/create-from-url" \
     -H "Authorization: Bearer YOUR_MEALIE_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.seriouseats.com/recipes/2011/12/ultra-crispy-roast-potatoes-recipe.html"}'
```

### 2. Exporting Database Backup from Container
```bash
docker exec -it mealie tar -czf /app/data/mealie_db_backup.tar.gz /app/data/mealie.db
```

## API examples

Below is a complete Python script demonstrating API interaction with Mealie using strict Pydantic v2 validation models:

```python
"""
Mealie REST API Client with Pydantic v2 Schema Validation
"""

from typing import List, Optional, Dict, Any
import requests
from pydantic import BaseModel, Field, HttpUrl, ValidationError

class IngredientItem(BaseModel):
    title: str = Field(..., description="Raw ingredient string or formatted name")
    note: Optional[str] = Field(None, description="Additional preparation notes")
    unit: Optional[str] = Field(None, description="Parsed measurement unit (e.g., grams, tbsp)")
    quantity: Optional[float] = Field(None, description="Numeric quantity")

class MealieRecipe(BaseModel):
    id: str = Field(..., description="Unique UUID identifier")
    name: str = Field(..., description="Recipe title")
    slug: str = Field(..., description="URL slug")
    description: Optional[str] = Field(None, description="Recipe summary")
    recipe_yield: str = Field(..., alias="recipeYield", description="Serving yield string")
    recipe_ingredient: List[IngredientItem] = Field(default_factory=list, alias="recipeIngredient")
    recipe_instructions: List[Dict[str, Any]] = Field(default_factory=list, alias="recipeInstructions")
    tools: List[str] = Field(default_factory=list)

class MealieAPIClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def get_recipe_by_slug(self, slug: str) -> Optional[MealieRecipe]:
        endpoint = f"{self.base_url}/api/recipes/{slug}"
        response = requests.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            try:
                return MealieRecipe.model_validate(response.json())
            except ValidationError as ve:
                print(f"Schema validation error: {ve}")
                return None
        else:
            print(f"API Request failed with status code: {response.status_code}")
            return None

# Usage example
if __name__ == "__main__":
    client = MealieAPIClient("http://localhost:9925", "YOUR_MEALIE_API_TOKEN")
    # recipe = client.get_recipe_by_slug("spaghetti-carbonara")
```

### FastMCP 3.1 Agent Tool Server

Exposing Mealie to autonomous agents for meal querying and automated shopping list item creation:

```python
"""
FastMCP 3.1 Server: Mealie Household Agent Integration
"""

from typing import Dict, Any, List, Optional
import requests
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MealieAgentTool")

class RecipeSearchInput(BaseModel):
    query: str = Field(..., description="Dish or ingredient keyword search string.")
    limit: int = Field(default=5, ge=1, le=20, description="Maximum number of matches.")

class ShoppingListItemInput(BaseModel):
    shopping_list_id: str = Field(..., description="Target shopping list UUID string.")
    note: str = Field(..., description="Item name or description with quantity (e.g., '2 kg Organic Carrots').")
    display_category: Optional[str] = Field("Produce", description="Grocery store section grouping.")

@mcp.tool()
def search_mealie_recipes(input_data: RecipeSearchInput) -> Dict[str, Any]:
    """
    Searches the household Mealie recipe repository for matching culinary options.
    """
    url = "http://localhost:9925/api/recipes"
    params = {"q": input_data.query, "perPage": input_data.limit}
    headers = {"Authorization": "Bearer YOUR_MEALIE_API_TOKEN"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            summary = [{"name": item.get("name"), "slug": item.get("slug")} for item in items]
            return {"success": True, "matches_found": len(summary), "recipes": summary}
        return {"success": False, "error": f"HTTP status {response.status_code}"}
    except Exception as err:
        return {"success": False, "error": str(err)}

@mcp.tool()
def add_item_to_mealie_shopping_list(input_data: ShoppingListItemInput) -> Dict[str, Any]:
    """
    Adds a missing ingredient or household item directly to a specified Mealie shopping list.
    """
    url = f"http://localhost:9925/api/groups/shopping-lists/{input_data.shopping_list_id}/items"
    headers = {
        "Authorization": "Bearer YOUR_MEALIE_API_TOKEN",
        "Content-Type": "application/json"
    }
    payload = {
        "note": input_data.note,
        "checked": False
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5.0)
        if response.status_code in (200, 201):
            return {"success": True, "added_item": input_data.note}
        return {"success": False, "error": f"HTTP status {response.status_code}"}
    except Exception as err:
        return {"success": False, "error": str(err)}

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Guide

| Issue / Symptom | Root Cause | Recommended Resolution |
| :--- | :--- | :--- |
| **Recipe Scraping Fails (403/500)** | Target site blocked scraper user-agent or altered HTML structure | Update Mealie container to the latest release to pull updated `recipe-scrapers` package (`docker compose pull`). |
| **Database Migration Timeout** | SQLite locked during multi-threaded worker access | Convert storage engine from SQLite to PostgreSQL via `DB_ENGINE=postgres` in Docker environment. |
| **FastMCP Token Authorization Error** | Mealie API bearer token expired or lacking write scope | Generate an explicit API key under Mealie Profile -> Manage API Tokens with `Household` write access. |
| **Home Assistant Sync Stalled** | Webhook endpoint unreachable or port mismatch | Verify Mealie API port (default 9000/9925) and check CORS settings under `ALLOW_CORS=true`. |

## Related tools / concepts

- [Grocy](grocy.md): Advanced food, pantries, and consumable expiration tracking.
- [Home Assistant](home-assistant.md): Dashboard display and automated voice ordering integration.
- [Vikunja](vikunja.md): Household collaborative task management.
- [Whisper](whisper.md): Audio transcription model for video recipe imports.
- [Paperless-ngx](paperless-ngx.md): Scanned document archive for physical recipe cards.
- [FastMCP 3.1 Pattern](../knowledge_base/patterns/tool-calling-and-mcp.md): Protocol for agent tool execution.

## Sources / references

- [Mealie Documentation](https://docs.mealie.io/)
- [Mealie GitHub Repository](https://github.com/mealie-recipes/mealie)
- [Mealie MCP Server Ecosystem](https://github.com/mealie-recipes/mcp-server-mealie)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
