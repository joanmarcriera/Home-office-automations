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

### Installation (Docker Compose)
Mealie v3.17.0 (May 2026) supports both SQLite and PostgreSQL backends.

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
      - TZ=Europe/Istanbul
      - MAX_WORKERS=1
      - WEB_CONCURRENCY=1
      - BASE_URL=http://localhost:9925
      - DEFAULT_EMAIL=admin@example.com
      - DEFAULT_PASSWORD=YourStrongPassword
      - DEFAULT_GROUP=Home
      - DEFAULT_HOUSEHOLD=Family
```

## AI Video Import (YouTube, TikTok)
Mealie v3.13.0+ supports AI-powered recipe imports from social media videos.
- **Workflow**: Paste a YouTube or TikTok URL into the import field.
- **Backend**: Transcribes video using OpenAI Whisper and structures ingredients/steps.
- **Setup**: Requires an OpenAI API key configured in `Settings -> Integrations -> OpenAI`.

## Groups and Households
Mealie v3.17.0 utilizes a two-tier user model for multi-tenant or multi-family deployments:
- **Groups**: Isolated tenants (no shared data between groups).
- **Households**: Subdivisions within a group. Members share recipes but have separate meal plans and shopping lists.

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

## External Sync & Automations
Mealie's API allows for seamless integration with external task managers and automation platforms like [n8n](n8n.md).

### Syncing Shopping Lists to Vikunja (n8n)
To synchronize Mealie shopping lists with [Vikunja](vikunja.md), you can use an n8n workflow:

1.  **Trigger**: Schedule (e.g., every 6 hours) or Mealie Webhook (on list update).
2.  **Fetch Mealie List**: Use the HTTP Request node to call `GET /api/shopping-lists/default`.
3.  **Format Data**: Map Mealie ingredients to Vikunja task objects.
4.  **Update Vikunja**: Use the Vikunja node to create or update tasks in a "Grocery" project.

### API Example: Exporting Ingredients
```python
import requests

url = "http://localhost:9925/api/shopping-lists/default"
headers = {"Authorization": "Bearer YOUR_API_TOKEN"}

response = requests.get(url, headers=headers)
items = response.json().get('items', [])
for item in items:
    print(f"Buy: {item['note']} ({item['food']['name']})")
```

## Backlog
- [x] Perform quarterly technical freshness audit (May 2026).

## Sources / References

- [Official Website](https://mealie.io/)
- [Mealie Documentation](https://docs.mealie.io/)
- [Recipe Scrapers Library](https://github.com/hweav/recipe-scrapers)
- [Mealie v3.17.0 Release Guide (Localtonet)](https://localtonet.com/blog/self-host-your-recipe-manager-mealie-and-tandoor-setup-guide)

## Contribution Metadata

- Last reviewed: 2026-05-26
- Confidence: high
