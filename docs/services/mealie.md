# Mealie

## What it is

Mealie is a self-hosted recipe manager and meal planner with a REST API backend and a modern, reactive frontend. It allows users to import recipes from the web, organize their collection, create meal plans, and generate shopping lists in a centralized, private environment.

## What problem it solves

Keeping track of digital recipes often involves scattered bookmarks, screenshots, or reliance on third-party SaaS platforms filled with ads and tracking. Mealie solves this by providing a unified, self-hosted vault where recipes are parsed into a clean, consistent format, making them easy to search, scale, and plan for the week.

## Where it fits in the stack

**Category**: Service / Home Automation. It sits in the **personal lifestyle and planning** layer of the self-hosted stack, connecting culinary interests with inventory management and grocery logistics.

## Typical use cases

- **Recipe Archival**: Importing and organizing thousands of recipes from various websites into a clean, ad-free format.
- **Weekly Meal Planning**: Planning breakfast, lunch, and dinner for the household using a visual calendar.
- **Automated Shopping Lists**: Generating consolidated shopping lists based on a weekly meal plan.
- **Recipe Scaling**: Automatically adjusting ingredient quantities for different serving sizes.

## Strengths

- **Superior Parsing**: Highly accurate recipe scraping from almost any URL using the `recipe-scrapers` library.
- **Mobile Friendly**: The web interface is fully responsive and behaves like a native app on mobile devices.
- **Extensive API**: Every feature is exposed via a REST API, enabling deep integration with other home automation tools.
- **Multi-User**: Supports multiple users with shared or private recipe collections and meal plans.

## Limitations

- **Database Dependency**: Requires a PostgreSQL or SQLite database, which adds some complexity to the deployment compared to flat-file managers.
- **Evolving Project**: Under active development, which means occasional breaking changes in the API or schema.
- **Inventory Depth**: While it has basic food inventory features, it is not as exhaustive as specialized tools like Grocy.

## When to use it

- If you have a large collection of recipes you want to digitize and organize.
- If you want a self-hosted alternative to Paprika, Yummly, or AnyList.
- When you want to automate your meal planning and shopping list generation.

## When not to use it

- For simple shopping lists without recipe integration.
- If you need a full enterprise-grade kitchen management system (though it’s great for home use).

## Getting started

The easiest way to install Mealie is via Docker Compose.

### Installation (Docker)
```bash
docker run -d \
  --name mealie \
  -p 9925:9000 \
  -v mealie-data:/app/data/ \
  ghcr.io/mealie-recipes/mealie:latest
```

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

### Get all recipes (Python)
Mealie provides a comprehensive API. You will need to obtain a Bearer token from your user profile.

```python
import requests

MEALIE_URL = "http://localhost:9925/api"
API_TOKEN = "your-api-token"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

response = requests.get(f"{MEALIE_URL}/recipes", headers=headers)
if response.status_code == 200:
    for recipe in response.json()['data']:
        print(f"Recipe: {recipe['name']}, Rating: {recipe['rating']}")
```

### Fetch a specific recipe (Curl)
```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
     "http://localhost:9925/api/recipes/your-recipe-slug"
```

## Related tools / concepts

- [Grocy](grocy.md) — for more detailed food and pantry inventory management
- [Home Assistant](home-assistant.md) — for displaying meal plans or shopping lists on home dashboards
- [Nextcloud Cookbook](https://github.com/nextcloud/cookbook) — a lighter alternative integrated into Nextcloud
- [Vikunja](vikunja.md) — for managing complex grocery shopping tasks beyond simple lists
- [Linkwarden](linkwarden.md) — for bookmarking recipe ideas before importing them into Mealie
- [Actual Budget](actual-budget.md) — for tracking the financial cost of your weekly meal plans

## Backlog
- Sync shopping lists with external task managers.

## Sources / References

- [Official Website](https://mealie.io/)
- [Mealie Documentation](https://docs.mealie.io/)
- [Recipe Scrapers Library](https://github.com/hweav/recipe-scrapers)

## Contribution Metadata

- Last reviewed: 2026-06-25
- Confidence: high
