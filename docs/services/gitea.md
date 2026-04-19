# Gitea

Gitea is a painless self-hosted Git service.

## Description
It is a community-managed lightweight code hosting solution written in Go. It provides features like issue tracking, code review, and CI/CD integration, with a focus on simplicity and performance.

## When to use it
- When you need a lightweight, low-resource Git hosting solution (runs comfortably on a Raspberry Pi).
- When you want a simple, GitHub-like experience for private or small-team projects.
- When you want to self-host your CI/CD pipelines via Gitea Actions.

## When not to use it
- When you require the deep enterprise features and complex permission models of GitLab.
- When you need a managed service with no maintenance overhead (consider GitHub or GitLab.com).

## Getting started

### Docker Compose
To run Gitea using Docker Compose:

```yaml
services:
  server:
    image: gitea/gitea:1.21
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
    restart: always
    volumes:
      - ./gitea:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"
      - "222:22"
```

Access the web interface at `http://localhost:3000`.

## AI & Automation
Gitea supports **Gitea Actions**, which is mostly compatible with GitHub Actions. This allows for integrating local AI into your development workflow.

### Automated Code Review Pattern
You can trigger a local LLM (via [Ollama](../services/ollama.md)) to review pull requests. Using `jq` ensures the code diff is safely encoded into the JSON payload:

```yaml
name: AI Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Send code to Local LLM
        run: |
          CODE_DIFF=$(git diff origin/main)
          # Safely encode payload using jq
          PAYLOAD=$(jq -n --arg diff "$CODE_DIFF" '{
            model: "codellama",
            prompt: ("Review this diff and suggest improvements:\n\n" + $diff),
            stream: false
          }')
          curl http://ollama-server:11434/api/generate -d "$PAYLOAD"
```

## CLI examples
The `gitea` binary inside the container can be used for administrative tasks:

```bash
# Create an admin user
docker exec -u 1000 -it gitea gitea admin user create --username admin --password secret --email admin@example.com --admin

# Dump database
docker exec -u 1000 -it gitea gitea dump
```

## API examples
Gitea features a comprehensive Swagger-documented API:

```bash
# Get repository information
curl -X GET "http://localhost:3000/api/v1/repos/owner/repo" \
  -H "Authorization: token <YOUR_TOKEN>"
```

## Links
- [Official Website](https://gitea.io/)
- [GitHub Repository](https://github.com/go-gitea/gitea)
- [Gitea Actions Overview](https://docs.gitea.com/usage/actions/overview)

## Alternatives
- [GitLab](https://about.gitlab.com/)
- [Forgejo](https://forgejo.org/)

## SSO & OIDC Integration
Gitea supports OIDC for Single Sign-On via [Authentik](authentik.md).

### Configuration Steps
1.  Navigate to **Site Administration > Authentication Sources**.
2.  Click **Add Authentication Source**.
3.  Set **Authentication Type** to `OpenID Connect`.
4.  Configure the following:
    -   **Authentication Name**: `authentik`
    -   **OAuth2 Provider**: `OpenID Connect`
    -   **Client ID (Key)**: `<Your Client ID>`
    -   **Client Secret**: `<Your Client Secret>`
    -   **OpenID Connect Auto Discovery URL**: `https://authentik.example.com/application/o/gitea/.well-known/openid-configuration`
    -   **Additional Scopes**: `email profile`

In Authentik, the Redirect URI should be: `https://gitea.example.com/user/oauth2/authentik/callback`

## Backlog
- Set up Gitea Actions for automated repository tasks.

## Sources / References
- https://gitea.io/
- https://github.com/go-gitea/gitea
- https://about.gitlab.com/
- [Gitea Documentation](https://docs.gitea.com/)
- [Gitea Actions Overview](https://docs.gitea.com/usage/actions/overview)
- [Forgejo](https://forgejo.org/)

## Contribution Metadata
- Last reviewed: 2026-04-08
- Confidence: high
