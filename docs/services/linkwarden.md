# Linkwarden

## What it is
Linkwarden is an open-source collaborative bookmark manager designed to archive, organize, and collaborate on webpages. It captures a permanent snapshot (screenshot and PDF) of each bookmarked page, ensuring the information remains accessible even if the original website goes offline or changes.

## What problem it solves
Web content is ephemeral; pages are often moved, deleted, or put behind paywalls, leading to "link rot." Traditional bookmark managers only save a URL, which is useless if the target page disappears. Linkwarden solves this by creating a self-hosted archive of the content, providing both a visual screenshot and a searchable PDF for long-term reference.

## Where it fits in the stack
**Category**: Service / Knowledge Management. It sits in the **information capture and archival** layer, acting as a primary intake point for web research that needs to be preserved for future use by humans or AI agents.

## Typical use cases
- **Research Archival**: Saving technical documentation or academic papers with guaranteed offline copies.
- **Team Collaboration**: Sharing curated collections of links and snapshots with colleagues in a private environment.
- **Content Preservation**: Ensuring long-form articles are preserved before they are potentially deleted or moved.
- **Agentic Knowledge Intake**: Using AI agents (Claude 4.8 Opus, GPT-5.5) to scrape and summarize archived PDFs for RAG workflows.

## Strengths
- **Automatic Snapshots**: Automatically generates high-quality PNG screenshots and PDF versions of every link.
- **Collaborative**: Supports multiple users, shared collections, and granular permissions.
- **Self-Hosted**: Full control over data and archival storage, ensuring privacy and security.
- **v2.14+ Performance**: Next.js 15 foundations with optimistic rendering for a fast, responsive interface.

## Limitations
- **Resource Intensive**: Generating and storing thousands of screenshots and PDFs can consume significant CPU and disk space.
- **Complexity**: Requires a database (PostgreSQL) and a storage backend, making it more complex than single-file managers.
- **Snapshot Accuracy**: Accuracy can vary depending on the target website's complex JavaScript or CSS layouts.

## When to use it
- When you need a permanent, offline copy of web content for long-term reference or research.
- For collaborative projects where shared resources need to be organized and preserved.
- When you want a self-hosted, privacy-first alternative to services like Pocket, Raindrop, or Instapaper.

## When not to use it
- If you only need a simple, single-user list of links and do not require archival snapshots.
- If you have very limited server resources and cannot afford the storage and processing overhead.
- For managing code snippets (use [Gitea](gitea.md) or [Trilium](trilium.md) instead).

## Getting started

### Installation (Docker Compose)
The recommended deployment method using PostgreSQL for data persistence.

```yaml
services:
  linkwarden:
    image: ghcr.io/linkwarden/linkwarden:latest
    container_name: linkwarden
    restart: always
    ports:
      - 3000:3000
    environment:
      - DATABASE_URL=postgresql://linkwarden:password@postgres:5432/linkwarden
      - NEXTAUTH_SECRET=change-this-to-a-random-string
      - NEXTAUTH_URL=http://localhost:3000
      - STORAGE_FOLDER=/data/data
    volumes:
      - ./data:/data/data
    depends_on:
      - postgres

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_USER=linkwarden
      - POSTGRES_DB=linkwarden
    volumes:
      - ./pgdata:/var/lib/postgresql/data
```

### Browser Extension
The official extension allows for quick saving while browsing.
1. Install for [Chrome/Edge](https://chrome.google.com/webstore/detail/linkwarden/afmionibalcnkdpgolnfnidniikfhnnh) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/linkwarden/).
2. Configure your instance URL and API key in the extension settings.

## CLI examples

### Maintenance & Backups
Using `docker exec` for database and log management.

```bash
# Backup the PostgreSQL database
docker exec -t postgres pg_dumpall -c -U linkwarden > linkwarden_backup.sql

# View real-time application logs for troubleshooting
docker logs -f linkwarden
```

### File System Audit
Checking the storage folder for archived assets.

```bash
# List archived PDF and PNG files in the storage volume
docker exec linkwarden ls -lh /data/data
```

## API examples

### Fetching Links (Python)
Integrating Linkwarden into automated research or newsletter workflows.

```python
import requests

API_URL = "http://linkwarden.local:3000/api/v1"
API_KEY = "YOUR_API_KEY"
headers = {"Authorization": f"Bearer {API_KEY}"}

def get_recent_links():
    response = requests.get(f"{API_URL}/links", headers=headers)
    if response.status_code == 200:
        links = response.json()['response']
        for link in links[:5]:
            print(f"Title: {link['title']}, URL: {link['url']}")

if __name__ == "__main__":
    get_recent_links()
```

### Bulk Adding Links (Curl)
Programmatically saving a list of URLs from a script.

```bash
curl -X POST "http://linkwarden.local:3000/api/v1/links" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com", "collectionId": 1}'
```

## Related tools / concepts
- [Changedetection.io](changedetection.md) — For monitoring archived pages for changes.
- [Paperless-ngx](paperless-ngx.md) — For complementary document management and OCR.
- [Nextcloud](nextcloud.md) — For general file storage and document collaboration.
- [SearXNG](searXNG.md) — Private search engine to discover new content to archive.
- [Authentik](authentik.md) — For managing SSO access to the Linkwarden UI.
- [Tailscale](tailscale.md) — Secure remote access to your bookmark collections.
- [Gitea](gitea.md) — For versioning research notes derived from links.
- [Home Assistant](home-assistant.md) — For automating notifications about new archives.

## Sources / References
- [Official Website](https://linkwarden.app/)
- [GitHub Repository](https://github.com/linkwarden/linkwarden)
- [v2.14 Release Notes](https://linkwarden.app/blog/releases/2.14)
- [Next.js Documentation](https://nextjs.org/docs)

## Contribution Metadata
- Last reviewed: 2026-06-17
- Confidence: high
