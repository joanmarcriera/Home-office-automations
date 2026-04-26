# Mealie

Mealie is a self-hosted recipe manager and meal planner with a RestAPI backend and a reactive frontend.

## Description
Mealie allows you to easily import recipes from websites, manage your food inventory, and plan your weekly meals.

## Where it fits in the stack
**Category**: Service / Home Automation

## Typical use cases
- Organizing a personal recipe collection.
- Meal planning and grocery list generation.
- Importing recipes from URLs with high accuracy.

## Strengths
- Excellent recipe parsing from external websites.
- Mobile-friendly responsive UI.
- Comprehensive REST API.

## Limitations
- Requires a database (PostgreSQL recommended for production).
- Still under active development with occasional breaking changes.

## When to use it
- If you have a large collection of recipes you want to digitize and organize.
- If you want a self-hosted alternative to Paprika or Yummly.

## When not to use it
- For simple shopping lists without recipe integration.

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
Mealie is primarily managed via the web UI or API, but you can interact with the container.

### Check logs
```bash
docker logs -f mealie
```

## API examples

### Get all recipes (Python)
```python
import requests

MEALIE_URL = "http://localhost:9925/api"
API_TOKEN = "your-api-token"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

response = requests.get(f"{MEALIE_URL}/recipes", headers=headers)
print(response.json())
```

## Related tools / concepts
- [Grocy](grocy.md) (for detailed inventory management)
- [Nextcloud Cookbook](https://github.com/nextcloud/cookbook)

## Sources / References
- [Official Website](https://mealie.io/)
- [Mealie Documentation](https://docs.mealie.io/)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
