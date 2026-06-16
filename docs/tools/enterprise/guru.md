# Guru

## What it is
Guru is an enterprise knowledge management platform that uses AI to capture, verify, and deliver trusted information directly into team workflows. It emphasizes "verified knowledge" to ensure that the information users find is accurate and up-to-date.

## What problem it solves
It solves the problem of "knowledge decay" and "shoulder-tapping." By institutionalizing a verification workflow, Guru ensures that internal wikis don't become stale. It also reduces repetitive questions by making verified info available via a browser extension and Slack.

## Where it fits in the stack
**Category**: Enterprise AI / Knowledge Management
Guru serves as the "source of truth" for verified company information, often integrated with AI agents like Claude 4.8 Opus to provide high-fidelity answers to employee queries.

## Typical use cases
- **Sales and Support Enablement**: Providing agents with verified product specifications, talk tracks, and troubleshooting steps.
- **Internal Wiki & Handbook**: Managing company policies and procedures with automated reminders for periodic review.
- **AI-Powered Search & Assistant**: Using Guru's "Answers" feature to get direct responses to natural language questions based on verified cards.

## Strengths
- **Verification Workflow**: Built-in system for subject matter experts (SMEs) to periodically verify that content is still accurate.
- **Contextual Delivery**: Browser extension and integrations (Slack, MS Teams) bring knowledge to where users are already working.
- **AI Answers**: Leverages generative AI to synthesize answers from across verified knowledge cards, with clear citations.
- **Template Library**: Extensive set of templates for common knowledge management needs.

## Limitations
- **Maintenance Overhead**: Requires active participation from experts to keep the verification engine running effectively.
- **Content Fragmentation**: If not managed strictly, knowledge can become scattered across too many small cards.
- **SaaS Only**: No option for a fully self-hosted or offline-first deployment.

## When to use it
- When your organization struggles with outdated documentation and "stale wiki" syndrome.
- If you need a solution that pushes information to users within their existing tools (like Zendesk or Salesforce).
- For teams that prioritize "verified truth" over raw data volume.

## When not to use it
- For personal note-taking or loosely organized research (consider Obsidian or Logseq).
- If your team is small enough that informal knowledge sharing is still highly effective.
- For managing high-concurrency technical documentation that belongs in a Git-backed system (consider MkDocs or Docusaurus).

## Getting started
Guru is typically deployed as a web application and browser extension. Organizations create "Collections" and "Cards" to store information. Developers can use the Guru API to automate card creation, search, and the verification process.

## CLI examples
While there is no official CLI, the Guru API is easily accessible via the command line using `curl`.

```bash
# Search for a knowledge card related to 'vacation policy'
curl -X GET "https://api.getguru.com/api/v1/search/cards?q=vacation+policy" \
  -u "$GURU_USER_EMAIL:$GURU_API_TOKEN" \
  -H "Accept: application/json"
```

## API examples
The Guru API allows for advanced knowledge operations, such as programmatically syncing documentation from an external source and marking it as verified.

```python
import requests
import os

# Guru uses Basic Auth
USER = os.getenv("GURU_USER_EMAIL")
TOKEN = os.getenv("GURU_API_TOKEN")
AUTH = (USER, TOKEN)

def create_verified_card(title, content, collection_id):
    """
    Creates a new knowledge card in Guru and assigns a verification interval.
    """
    url = "https://api.getguru.com/api/v1/cards"
    payload = {
        "title": title,
        "content": content,
        "collectionId": collection_id,
        "shareStatus": "TEAM",
        "verificationInterval": 90 # Days until verification is required
    }

    response = requests.post(url, auth=AUTH, json=payload)
    response.raise_for_status()
    return response.json()

# Example: Ingesting a new policy updated by Claude 4.8 Opus
new_card = create_verified_card(
    "June 2026 AI Ethics Guidelines",
    "<p>Updated guidelines for the use of GPT-5.5 and Claude 4.8...</p>",
    "COLLECTION_ID_123"
)
print(f"Created Card ID: {new_card['id']}")
```

## Related tools / concepts
- [Dashworks](dashworks.md) — AI-powered unified search across internal apps.
- [Glean](glean.md) — enterprise-scale search and knowledge platform.
- [Notion AI](../ai_knowledge/notion-ai.md) — AI-powered workspace for docs and collaboration.
- [Obsidian](../ai_knowledge/obsidian.md) — local-first personal knowledge management.
- [Logseq](../ai_knowledge/logseq.md) — privacy-focused local knowledge base.
- [AnyType](../intake_storage/anytype.md) — decentralized, local-first knowledge base.
- [SilverBullet](../intake_storage/silverbullet.md) — extensible open-source wiki alternative.

## Sources / references
- [Guru Official Website](https://www.getguru.com/)
- [Guru Developer API Documentation](https://developer.getguru.com/reference/guru-api-overview)
- [Knowledge Management Patterns](../../knowledge_base/README.md)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
