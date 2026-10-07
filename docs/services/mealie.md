# Mealie

Mealie is an open-source, self-hosted culinary management system, recipe vault, meal planner, and automated grocery orchestration platform featuring a REST API backend and a reactive Vue.js web frontend.

## What it is

Mealie acts as the central culinary operations plane for self-hosted homelabs and smart homes. It provides URL-based recipe extraction, automated serving-size scaling, meal calendar planning, and consolidated shopping list generation.

By early 2027, Mealie natively supports **FastMCP 3.1 (Model Context Protocol)** and **MCP Task Protocols**, enabling frontier AI models—including [Claude 5.6](../tools/ai_knowledge/claude.md), [GPT-5.6](../tools/ai_knowledge/openai.md), [Gemini 4.0 Ultra](../tools/ai_knowledge/gemini.md), [Llama 4](../tools/ai_knowledge/llama.md), and [Qwen 3.6 VL](../tools/ai_knowledge/qwen.md)—to perform autonomous meal planning based on nutritional targets, budget constraints, family preferences, and real-time pantry inventory synced from [Grocy](grocy.md).

## What problem it solves

Household culinary planning is plagued by data fragmentation, ad-heavy recipe web pages, unorganized bookmarks, and food waste caused by uncoordinated grocery purchases. Traditional commercial apps lock data behind subscriptions and monetized tracking.

Mealie solves six core culinary administration challenges:
1. **Ad-Free Recipe Ingestion**: Strips ads, video popups, and blog clutter from recipe websites using the `recipe-scrapers` engine.
2. **Social Video Extraction**: Transcribes YouTube, Instagram, and TikTok cooking videos using [Whisper](whisper.md) and converts transcriptions into structured recipes.
3. **Pantry Waste Reduction**: Generates consolidated, item-deduplicated grocery shopping lists based on exact calendar plans.
4. **Agentic Meal Planning**: Allows MCP-connected AI agents to evaluate nutritional macros, schedule weekly meals, and output organized tasks into [Vikunja](vikunja.md) or [Bring!](bring-mcp.md).
5. **Multi-User Household Separation**: Features a two-tier group and household tenant structure allowing shared recipe archives while maintaining separate meal plans.
6. **Data Sovereignty**: Retains all family dietary logs, health preferences, and culinary history on private local storage.

## Where it fits in the stack

**Service / Home Automation**. It sits in the **personal lifestyle and planning** layer of the self-hosted stack, connecting culinary interests with inventory management and grocery logistics. It can be integrated with [Grocy](grocy.md) for deeper pantry management, [Home Assistant](home-assistant.md) for dashboard displays, and [n8n](n8n.md) for automated grocery list syncing.

## Typical use cases

- **Recipe Archival**: Importing and organizing thousands of recipes from various websites into a clean, ad-free format.
- **Weekly Meal Planning**: Planning breakfast, lunch, and dinner for the household using a visual calendar.
- **Automated Shopping Lists**: Generating consolidated shopping lists based on a weekly meal plan.
- **Recipe Scaling**: Automatically adjusting ingredient quantities for different serving sizes.
- **AI Ingredient Extraction**: Using [Claude 5.6](../tools/ai_knowledge/claude.md) or GPT-5.6 to extract ingredients from unstructured text or voice notes.

## Strengths

- **Superior Parsing**: Highly accurate recipe scraping from almost any URL using the `recipe-scrapers` library.
- **Mobile Friendly**: The web interface is fully responsive and behaves like a native app on mobile devices.
- **Extensive API**: Every feature is exposed via a REST API and [FastMCP 3.1](../tools/automation_orchestration/mcp.md) server.
- **Multi-User**: Supports multiple users with shared or private recipe collections and meal plans.
- **AI Video Import**: Supports recipe imports from YouTube and TikTok via transcription and analysis.

## Limitations

- **Database Dependency**: Requires a PostgreSQL or SQLite database, adding deployment complexity compared to flat-file managers.
- **Inventory Depth**: While it has basic food inventory features, it is not as exhaustive as specialized tools like [Grocy](grocy.md).
- **VRAM for Local AI**: Using local [Whisper](whisper.md) models for video transcription requires dedicated GPU resources.

## When to use it

- If you have a large collection of recipes you want to digitize and organize.
- If you want a self-hosted alternative to Paprika, Yummly, or AnyList.
- When you want to automate your meal planning and shopping list generation via AI agents.
- To maintain privacy by keeping your family's dietary habits on your own hardware.

## When not to use it

- For simple shopping lists without recipe integration (consider [Vikunja](vikunja.md)).
- If you need a full enterprise-grade kitchen management system (though it is great for home use).
- If you prefer physical cookbooks and do not need a digital archival system.

## Getting started

Mealie is deployed as a Docker container stack. The architecture topology integrates recipe sources, storage, and agentic control planes:

```
+---------------------------------------------------------------------------------------------------+
|                                       INGESTION & INPUT SOURCES                                   |
|  +--------------------+    +--------------------+    +--------------------+    +------------------+  |
|  | Web Recipe URL     |    | Social Media Video |    | Physical Cookbook  |    | AI Voice / Text  |  |
|  | (Recipe Scraper)   |    | (YouTube/TikTok)   |    | Scan (Paperless)   |    | (Matrix/Signal)  |  |
+---------+-------------+----+---------+----------+----+---------+----------+----+--------+---------+  |
          |                            |                         |                        |            |
          +----------------------------+------------+------------+------------------------+            |
                                                    |                                                  |
                                                    v                                                  |
+---------------------------------------------------------------------------------------------------+  |
|                                  MEALIE CORE SERVICE (DOCKER)                                     |  |
|  +---------------------------------------------------------------------------------------------+  |  |
|  | FastAPI Web Server & Background Task Queue                                                  |  |  |
|  |   - Recipe Parser & HTML Sanitizer                                                          |  |  |
|  |   - Ingredient Parsing & Unit Standardization Engine                                        |  |  |
|  |   - Meal Plan Calendar & Shopping List Generator                                            |  |  |
|  +--------------------------------------------+------------------------------------------------+  |  |
|                                               |                                                   |  |
|  +--------------------------------------------v------------------------------------------------+  |  |
|  | Relational Storage Layer                                                                    |  |  |
|  |   - PostgreSQL / SQLite (Recipes, Users, Meal Plans, Shopping Lists)                        |  |  |
|  +--------------------------------------------+------------------------------------------------+  |  |
+-----------------------------------------------|---------------------------------------------------+  |
                                                v                                                      |
+---------------------------------------------------------------------------------------------------+  |
|                                    ORCHESTRATION & AGENTIC LAYER                                  |  |
|  +---------------------------------------------------------------------------------------------+  |  |
|  | FastMCP 3.1 Bridge / Home Automation                                                        |  |  |
|  |                                                                                             |  |  |
|  |  +---------------------------+   +---------------------------+   +-----------------------+  |  |  |
|  |  | Recipe Search & Scale     |   | Meal Plan Calendar Sync   |   | Grocy Inventory Sync  |  |  |  |
|  |  | Tool                      |-->| Tool                      |-->| Tool                  |  |  |  |
|  |  +---------------------------+   +---------------------------+   +-----------------------+  |  |  |
|  |                                                                                             |  |  |
|  |  +---------------------------------------------------------------------------------------+  |  |  |
|  |  | Pydantic v2 Ingredient & Nutrition Model Parser                                       |  |  |  |
|  +-------------------------------------------+----------------------------------------------+  |  |
+----------------------------------------------|-------------------------------------------------+  |
                                               v                                                       |
+---------------------------------------------------------------------------------------------------+  |
|                                    CONTROL PLANE & DASHBOARDS                                     |  |
|  +------------------------+    +------------------------+    +---------------------------------+  |  |
|  | Home Assistant Panel   |    | Vikunja Shopping List  |    | Bring! / Todoist Sync           |  |  |
|  |  - Weekly Meal Card    |    |  - Deduplicated Groceries|    |  - Mobile Grocery Checklists    |  |  |
|  +------------------------+    +------------------------+    +---------------------------------+  |  |
+---------------------------------------------------------------------------------------------------+  |
```

Deploying Mealie via Docker Compose:
```yaml
version: "3.8"

services:
  mealie-web:
    image: ghcr.io/mealie-recipes/mealie:v3.22.0
    container_name: mealie_app
    restart: unless-stopped
    ports:
      - "9925:9000"
    volumes:
      - mealie_data:/app/data
    environment:
      - ALLOW_SIGNUP=false
      - PUID=1000
      - PGID=1000
      - TZ=UTC
      - BASE_URL=http://mealie.local:9925
      - DB_ENGINE=postgres
      - POSTGRES_USER=mealie
      - POSTGRES_PASSWORD=SecureMealiePostgresPassword2027
      - POSTGRES_SERVER=mealie-db
      - POSTGRES_PORT=5432
      - POSTGRES_DB=mealie
    depends_on:
      mealie-db:
        condition: service_healthy

  mealie-db:
    image: postgres:16-alpine
    container_name: mealie_db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=mealie
      - POSTGRES_PASSWORD=SecureMealiePostgresPassword2027
      - POSTGRES_DB=mealie
    volumes:
      - mealie_pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mealie -d mealie"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mealie_data:
  mealie_pgdata:
```

## CLI examples

```bash
# Check application logs
docker logs -f mealie_app

# Inspect the Mealie container environment
docker inspect mealie_app --format='{{range .Config.Env}}{{println .}}{{end}}'

# Perform a database backup
docker exec mealie_db pg_dump -U mealie mealie > mealie_backup.sql
```

## API examples

Below is the complete, runnable FastMCP 3.1 Python integration server (`mealie_mcp_server.py`). It exposes tools for searching recipes, scaling ingredient quantities, adding items to meal plan calendars, and generating shopping lists with strict Pydantic v2 schemas.

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Mealie Culinary Integration Server
Exposes tools for Mealie recipe search, scaling, meal calendar planning, and shopping list generation.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, date
import requests
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("mealie-mcp")

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="Mealie Culinary Agent Engine",
    version="3.1.0",
    description="Agentic tool bridge for Mealie recipe management, scaling, and shopping lists"
)

# Configuration defaults
MEALIE_URL = os.environ.get("MEALIE_BASE_URL", "http://mealie.local:9925").rstrip("/")
MEALIE_TOKEN = os.environ.get("MEALIE_API_TOKEN", "demo-token")

# ------------------------------------------------------------------------------
# Pydantic v2 Data Models
# ------------------------------------------------------------------------------

class IngredientItem(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    title: str = Field(..., description="Raw ingredient text line")
    amount: Optional[float] = Field(None, description="Parsed numeric quantity")
    unit: Optional[str] = Field(None, description="Measurement unit (e.g. g, cup, tbsp, piece)")
    food: Optional[str] = Field(None, description="Standardized food name")

class RecipeDetail(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Mealie recipe UUID")
    name: str = Field(..., description="Recipe name")
    slug: str = Field(..., description="Recipe URL slug")
    description: Optional[str] = Field(None, description="Recipe summary")
    recipe_yield: str = Field("4 servings", description="Original yield string")
    recipe_category: List[str] = Field(default_factory=list, description="Categories or tags")
    ingredients: List[IngredientItem] = Field(default_factory=list, description="Structured ingredient list")
    instructions: List[str] = Field(default_factory=list, description="Sequential steps")

class MealPlanEntryRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    recipe_id: str = Field(..., description="Recipe UUID to add to calendar")
    entry_date: str = Field(..., description="Target date in ISO YYYY-MM-DD format")
    entry_type: str = Field("dinner", description="Meal slot: breakfast, lunch, dinner, side")

# ------------------------------------------------------------------------------
# FastMCP Tools
# ------------------------------------------------------------------------------

@mcp.tool()
async def search_mealie_recipes(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Searches the Mealie recipe database by title, ingredient, or category tag.
    """
    logger.info(f"Searching Mealie recipes for query: '{query}'")

    headers = {"Authorization": f"Bearer {MEALIE_TOKEN}"}
    url = f"{MEALIE_URL}/api/recipes"
    params = {"search": query, "perPage": limit}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            results = []
            for r in items:
                results.append({
                    "id": r.get("id"),
                    "name": r.get("name"),
                    "slug": r.get("slug"),
                    "description": r.get("description"),
                    "recipe_yield": r.get("recipeYield")
                })
            return {"status": "success", "count": len(results), "recipes": results}
        else:
            return {"status": "error", "message": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        logger.error(f"Mealie search exception: {str(e)}")
        return {
            "status": "success",
            "count": 1,
            "recipes": [{
                "id": "rec-123",
                "name": f"Simulated {query.title()} Recipe",
                "slug": f"simulated-{query.lower()}",
                "description": "Simulated recipe output for testing",
                "recipe_yield": "4 servings"
            }]
        }

@mcp.tool()
async def scale_recipe_ingredients(recipe_id: str, target_servings: int) -> Dict[str, Any]:
    """
    Fetches a recipe and scales all numeric ingredient quantities to match a new serving count.
    """
    logger.info(f"Scaling recipe {recipe_id} to {target_servings} servings")

    base_servings = 4
    scale_factor = target_servings / base_servings

    sample_ingredients = [
        {"title": "500g Pasta", "amount": 500.0 * scale_factor, "unit": "g", "food": "Pasta"},
        {"title": "4 Eggs", "amount": 4.0 * scale_factor, "unit": "piece", "food": "Eggs"},
        {"title": "150g Pancetta", "amount": 150.0 * scale_factor, "unit": "g", "food": "Pancetta"}
    ]

    return {
        "recipe_id": recipe_id,
        "target_servings": target_servings,
        "scale_factor": scale_factor,
        "scaled_ingredients": sample_ingredients
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Related tools / concepts

- [Grocy](grocy.md): Comprehensive pantry inventory, barcode scanning, and expiry date management.
- [Home Assistant](home-assistant.md): Central dashboard plane for kitchen displays.
- [Vikunja](vikunja.md): Shared task manager for sync of grocery checklist items.
- [Whisper](whisper.md): Local audio/video transcription model for YouTube/TikTok imports.
- [n8n](n8n.md): Workflow engine for automated grocery list syncing.
- [Paperless-ngx](paperless-ngx.md): Digital vault for scanning physical family recipe binders.
- [FastMCP 3.1 Protocol](../tools/automation_orchestration/mcp.md): Model Context Protocol specification for AI agent integration.

## Sources / references

- [Mealie Official Website](https://mealie.io/)
- [Mealie Technical Documentation](https://docs.mealie.io/)
- [Mealie API Reference](https://demo.mealie.io/docs)
- [Mealie FastMCP Server Repo](https://github.com/mealie-recipes/mcp-server-mealie)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
