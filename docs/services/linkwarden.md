# Linkwarden

## What it is

Linkwarden is an open-source collaborative bookmark manager designed to archive, organize, and collaborate on webpages. It goes beyond simple bookmarking by capturing a permanent snapshot (screenshot and PDF) of each bookmarked page, ensuring the information remains accessible even if the original website goes offline.

## What problem it solves

Web content is ephemeral; pages are often moved, deleted, or changed, leading to "link rot." Traditional bookmark managers only save a URL, which becomes useless if the target page disappears. Linkwarden solves this by creating a self-hosted archive of the content you save, providing both a visual screenshot and a searchable PDF for long-term reference and collaboration.

## Where it fits in the stack

**Category**: Service / Knowledge Management. It sits in the **information capture and archival** layer, acting as the primary intake point for interesting web content that needs to be preserved for future research or team projects.

## Typical use cases

- **Research Archival**: Saving technical articles, academic papers, or documentation with a guaranteed offline copy.
- **Team Collaboration**: Sharing collections of links and snapshots with colleagues in a private, organized environment.
- **Content Preservation**: Ensuring that "must-read" long-form articles are preserved before they are potentially moved behind a paywall or deleted.
- **Visual Bookmarking**: Using the screenshot preview to quickly identify saved resources at a glance.

## Strengths

- **Automatic Snapshots**: Automatically generates high-quality PNG screenshots and PDF versions of every link.
- **Collaborative**: Supports multiple users, collections, and team-based permissions.
- **Self-Hosted**: Full control over where your data and snapshots are stored, ensuring privacy and security.
- **Modern UI**: Features a clean, responsive interface with powerful search and tagging capabilities.

## Limitations

- **Resource Intensive**: Generating and storing thousands of screenshots and PDFs can consume significant CPU and disk space.
- **Complexity**: Requires a database (Postgres) and storage backend, making it slightly more complex to deploy than a single-file bookmark manager.
- **Browser Compatibility**: Snapshot accuracy can vary depending on the complexity of the target website's JavaScript and CSS.

## When to use it

- When you need more than just a link and want a permanent, offline copy of web content.
- For collaborative research projects where multiple people need to access and organize shared resources.
- When you want a self-hosted alternative to services like Pocket, Raindrop, or Instapaper.

## When not to use it

- If you only need a simple, single-user list of links and don't care about archival snapshots (consider [Shiori](https://github.com/go-shiori/shiori)).
- If you have very limited server resources and cannot afford the storage overhead of PDFs and images.

## Getting started

### Docker Compose
The recommended way to deploy Linkwarden is using Docker Compose. It requires a Postgres database.

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

### Hello World
1. Start the stack: `docker compose up -d`.
2. Open `http://localhost:3000` and create your initial admin account.
3. Create your first "Collection" (e.g., "Research").
4. Click **Add Link**, paste a URL (e.g., `https://example.com`), and save it.
5. Wait a few moments for Linkwarden to generate the screenshot and PDF.
6. Click on the link to view the archived snapshot.

### Browser Extension
The official Linkwarden browser extension allows you to quickly save links and snapshots while browsing.

1. **Install**: Download the extension for [Chrome/Edge](https://chrome.google.com/webstore/detail/linkwarden/afmionibalcnkdpgolnfnidniikfhnnh) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/linkwarden/).
2. **Configure**: Click the extension icon and enter your self-hosted instance URL (`http://localhost:3000`) and your API key.
3. **Save**: Click the "Save to Linkwarden" button on any webpage to automatically capture it into your preferred collection.

## CLI examples
While primarily managed via the web, you can use Docker for maintenance:

```bash
# View application logs
docker logs -f linkwarden

# Access the Linkwarden container shell
docker exec -it linkwarden /bin/sh

# Backup the Postgres database
docker exec -t postgres pg_dumpall -c -U linkwarden > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
```

## API examples
Linkwarden provides a REST API for programmatic interaction. You can generate an API key in your user settings.

### List all links (Python)
```python
import requests

API_URL = "http://localhost:3000/api/v1"
API_KEY = "YOUR_API_KEY"

headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(f"{API_URL}/links", headers=headers)
if response.status_code == 200:
    links = response.json()
    for link in links['response']:
        print(f"Title: {link['title']}, URL: {link['url']}")
```

### Add a new link (Curl)
```bash
curl -X POST "http://localhost:3000/api/v1/links" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.wikipedia.org", "collectionId": 1}'
```

### Advanced: Automated Tagging via LLM (Python)
This pattern fetches untagged links and uses a local LLM (via [Ollama](ollama.md)) to suggest and apply tags.

```python
import requests
import json

BASE_URL = "http://localhost:3000/api/v1"
API_KEY = "YOUR_LINKWARDEN_API_KEY"
OLLAMA_URL = "http://localhost:11434/api/generate"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def get_untagged_links():
    res = requests.get(f"{BASE_URL}/links", headers=headers)
    return [l for l in res.json()['response'] if not l.get('tags')]

def suggest_tags(title, description):
    prompt = f"Suggest 3 short tags for a bookmark titled '{title}' with description '{description}'. Return as JSON list of strings."
    res = requests.post(OLLAMA_URL, json={"model": "llama3", "prompt": prompt, "stream": False, "format": "json"})
    return json.loads(res.json()['response'])

for link in get_untagged_links():
    tags = suggest_tags(link['title'], link.get('description', ''))
    requests.patch(f"{BASE_URL}/links/{link['id']}",
                  headers=headers,
                  json={"tags": [{"name": t} for t in tags]})
    print(f"Tagged '{link['title']}' with {tags}")
```

### Advanced: Bulk PDF Export Management
Linkwarden stores archives as IDs. This script identifies links with PDF archives and downloads them for external backup.

```python
import requests

API_KEY = "YOUR_API_KEY"
headers = {"Authorization": f"Bearer {API_KEY}"}

def download_pdf(link_id, filename):
    # Endpoint to get preservation details
    res = requests.get(f"http://localhost:3000/api/v1/links/{link_id}", headers=headers)
    link_data = res.json()['response']

    # Check for PDF archive ID
    pdf_archive = next((a for a in link_data.get('archives', []) if a['format'] == 'pdf'), None)
    if pdf_archive:
        # Download the actual file
        file_res = requests.get(f"http://localhost:3000/api/v1/archives/{pdf_archive['id']}", headers=headers)
        with open(f"./backups/{filename}.pdf", "wb") as f:
            f.write(file_res.content)

# Example usage
download_pdf(123, "my_preserved_page")
```

## Related tools / concepts

- [Changedetection.io](changedetection.md) — for monitoring websites for changes after bookmarking them.
- [Nextcloud](nextcloud.md) — can be used to sync and store Linkwarden's PDF exports.
- [Tailscale](tailscale.md) — for secure remote access to your bookmark collections.
- [Paperless-ngx](paperless-ngx.md) — For complementary document management and OCR.
- [Authentik](authentik.md) — For managing SSO access to your bookmarking service.
- [Gitea](gitea.md) — For versioning the research notes derived from bookmarked links.
- [SearXNG](searXNG.md) — For private search to find new content to bookmark.
- [Home Assistant](home-assistant.md) — For automating notifications about newly archived links.
- [IT-Tools](it-tools.md) — For processing snippets found in bookmarked pages.
- [Omni Tools](omni-tools.md) — A similar collection of web-based utilities.

## Sources / References

- [Official Website](https://linkwarden.app/)
- [GitHub Repository](https://github.com/linkwarden/linkwarden)
- [Wallabag Official Site](https://wallabag.org/)

## Backlog
- [ ] Perform quarterly technical freshness audit.

## Contribution Metadata

- Last reviewed: 2026-05-08
- Confidence: high
