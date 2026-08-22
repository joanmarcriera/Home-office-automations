# Mealie

Mealie is a self-hosted recipe manager and meal planner with a REST API backend and a modern, reactive frontend.

## What it is
Mealie is a comprehensive culinary management system that allows users to import recipes from the web, organize their collection, create meal plans, and generate shopping lists in a centralized, private environment. As of early January 2027, it features native integration with frontier models including **Claude 5.1 / 5.6**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro / Ultra**, **DeepSeek-V4**, **Llama 4**, **Gemma 3**, and **Qwen 3.8** for AI-powered recipe scaling, nutrition analysis, and autonomous grocery orchestration via **MCP 3.1 / FastMCP**.

## What problem it solves
Keeping track of digital recipes often involves scattered bookmarks, screenshots, or reliance on third-party SaaS platforms filled with ads and tracking. Mealie solves this by providing a unified, self-hosted vault where recipes are parsed into a clean, consistent format, making them easy to search, scale, and plan for the week.

## Where it fits in the stack
**Service / Home Automation**. It sits in the **personal lifestyle and planning** layer of the self-hosted stack, connecting culinary interests with inventory management and grocery logistics. It can be integrated with [Grocy](grocy.md) for deeper pantry management and [n8n](n8n.md) for automated grocery list syncing and [Agentic Workflows](../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- **Recipe Archival**: Importing and organizing thousands of recipes from various websites into a clean, ad-free format.
- **Weekly Meal Planning**: Planning breakfast, lunch, and dinner for the household using a visual calendar.
- **Automated Shopping Lists**: Generating consolidated shopping lists based on a weekly meal plan.
- **Recipe Scaling**: Automatically adjusting ingredient quantities for different serving sizes using [Gemma 3](../tools/ai_knowledge/local_llms.md).
- **AI Ingredient Extraction**: Using [Claude 5.1](../tools/providers/anthropic.md) or GPT-5.5/5.6 to extract ingredients from unstructured text or voice notes.

## Strengths
- **Superior Parsing**: Highly accurate recipe scraping from almost any URL using the `recipe-scrapers` library.
- **Mobile Friendly**: The web interface is fully responsive and behaves like a native app on mobile devices.
- **Extensive API**: Every feature is exposed via a REST API and [MCP 3.1](../tools/automation_orchestration/mcp.md) server, enabling deep integration with other home automation tools.
- **Multi-User**: Supports multiple users with shared or private recipe collections and meal plans.
- **AI Video Import**: Supports recipe imports from YouTube and TikTok via transcription and analysis.

## Limitations
- **Database Dependency**: Requires a PostgreSQL or SQLite database, which adds some complexity to the deployment compared to flat-file managers.
- **Inventory Depth**: While it has basic food inventory features, it is not as exhaustive as specialized tools like [Grocy](grocy.md).
- **VRAM for Local AI**: If using local [Whisper](whisper.md) models for video transcription, significant GPU resources are required.

## When to use it
- If you have a large collection of recipes you want to digitize and organize.
- If you want a self-hosted alternative to Paprika, Yummly, or AnyList.
- When you want to automate your meal planning and shopping list generation.
- To maintain privacy by keeping your family's dietary habits on your own hardware.

## When not to use it
- For simple shopping lists without recipe integration (consider [Vikunja](vikunja.md)).
- If you need a full enterprise-grade kitchen management system (though it’s great for home use).
- If you prefer physical cookbooks and do not need a digital archival system.

## Getting started

### Installation (Docker Compose)
Mealie v3.22.0 (early January 2027) supports both SQLite and PostgreSQL backends and features an integrated **MCP 3.1** server.

```yaml
services:
  mealie:
    image: ghcr.io/mealie-recipes/mealie:latest
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
      - TZ=Europe/London
      - MAX_WORKERS=1
      - WEB_CONCURRENCY=1
      - BASE_URL=http://localhost:9925
      - DEFAULT_EMAIL=admin@example.com
      - DEFAULT_PASSWORD=YourStrongPassword
      - DEFAULT_GROUP=Home
      - DEFAULT_HOUSEHOLD=Family
```

### Groups and Households
Mealie utilizes a two-tier user model for multi-tenant or multi-family deployments:
- **Groups**: Isolated tenants (no shared data between groups).
- **Households**: Subdivisions within a group. Members share recipes but have separate meal plans and shopping lists.

### AI Video Import (YouTube, TikTok)
Mealie supports AI-powered recipe imports from social media videos using the [Whisper](whisper.md) model or cloud APIs.
- **Workflow**: Paste a YouTube or TikTok URL into the import field.
- **Backend**: Transcribes video and structures ingredients/steps using GPT-5.5/5.6 or [Claude 5.1](../tools/providers/anthropic.md).
- **Setup**: Requires an API key configured in `Settings -> Integrations`.

## CLI examples
Mealie is primarily managed via the web UI or API, but you can interact with the container for maintenance.

```bash
# Check application logs
docker logs -f mealie

# Inspect the Mealie container environment
docker inspect mealie --format='{{range .Config.Env}}{{println .}}{{end}}'

# Perform a manual data backup (if using SQLite)
docker exec mealie tar -czf /app/data/mealie_backup.tar.gz /app/data/mealie.db
```

## API examples

### Fetch a specific recipe (Curl)
```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
     "http://localhost:9925/api/recipes/your-recipe-slug"
```

### Get all recipes and Pydantic Validation (Python)
Mealie provides a comprehensive API and **MCP 3.1** Task Protocol support. Here is a Python example utilizing **Pydantic v2** to parse and validate Mealie's recipe data models:

```python
import requests
from pydantic import BaseModel, Field
from typing import List, Optional

class MealieRecipeModel(BaseModel):
    """
    Pydantic v2 model representing a Mealie recipe structure parsed from URLs
    or created manually in the system.
    """
    name: str = Field(..., min_length=1, description="Name of the recipe")
    slug: str = Field(..., description="Unique URL slug generated by Mealie")
    description: Optional[str] = Field(None, description="Short summary or description")
    recipe_yield: str = Field(..., description="Yield or servings of the recipe (e.g., '4 servings')")
    ingredients: List[str] = Field(default_factory=list, description="List of raw ingredients")
    steps: List[str] = Field(default_factory=list, description="Sequential preparation steps")
    tags: List[str] = Field(default_factory=list, description="Organizational categories or tags")

# Ingestion validation
raw_recipe = {
    "name": "Spaghetti Carbonara",
    "slug": "spaghetti-carbonara",
    "description": "Classic Roman pasta dish with eggs, hard cheese, cured pork, and black pepper.",
    "recipe_yield": "4 servings",
    "ingredients": ["400g Spaghetti", "150g Guanciale", "4 large Eggs", "75g Pecorino Romano", "Black Pepper"],
    "steps": ["Boil pasta in salted water.", "Crisp guanciale in a pan.", "Whisk eggs and cheese together.", "Combine pasta, guanciale, and egg mixture off-heat.", "Serve with extra cheese and pepper."],
    "tags": ["Pasta", "Italian", "Quick Dinner"]
}

recipe = MealieRecipeModel.model_validate(raw_recipe)
print(f"Validated recipe: {recipe.name} ({recipe.recipe_yield}) with {len(recipe.ingredients)} ingredients.")
```

## Related tools / concepts
- [Grocy](grocy.md) — For more detailed food and pantry inventory management.
- [Home Assistant](home-assistant.md) — For displaying meal plans on home dashboards.
- [Vikunja](vikunja.md) — For managing complex grocery shopping tasks.
- [Linkwarden](linkwarden.md) — For bookmarking recipe ideas.
- [Actual Budget](actual-budget.md) — For tracking the financial cost of meal plans.
- [Whisper](whisper.md) — For local video-to-text transcription.
- [n8n](n8n.md) — For automating shopping list synchronization.
- [Paperless-ngx](paperless-ngx.md) — For archiving scanned physical recipe cards.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — For agentic culinary orchestration.

## Sources / references
- [Mealie Official Website](https://mealie.io/)
- [Mealie Documentation](https://docs.mealie.io/)
- [Mealie MCP Server GitHub](https://github.com/mealie-recipes/mcp-server-mealie)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
