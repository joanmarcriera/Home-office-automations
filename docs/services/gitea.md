# Gitea

Gitea is a painless self-hosted Git service.

## What it is
Gitea is a community-managed lightweight code hosting solution written in Go. It provides a complete Git service including repository management, issue tracking, code review, and CI/CD integration, with a focus on simplicity and high performance.

## What problem it solves
It allows developers and home lab enthusiasts to host their own private Git repositories without the resource overhead of GitLab or the privacy concerns of GitHub. It provides a central hub for code collaboration and automation that can run on low-power hardware.

## Where it fits in the stack
Gitea sits in the **Development & DevOps** layer. It serves as the primary source of truth for code, configuration files, and automation workflows. It is often the trigger for CI/CD pipelines that deploy other services in the stack.

## Typical use cases
- **Private Code Hosting**: Maintaining internal tools and projects away from public eyes.
- **GitOps**: Storing infrastructure-as-code (Ansible, Terraform, K3s manifests) and triggering deployments.
- **Documentation**: Hosting project documentation via Gitea's built-in wiki or Markdown support.
- **Mirrors**: Maintaining local mirrors of critical public repositories for offline access.

## Strengths
- **Performance**: Extremely lightweight and fast; runs comfortably on a Raspberry Pi.
- **GitHub-Like UX**: Familiar interface that requires minimal learning for existing Git users.
- **Self-Contained**: Can be run as a single binary or a small Docker container with minimal dependencies.
- **Built-in CI/CD**: Gitea Actions provides GitHub Actions compatibility out of the box.

## Limitations
- **Ecosystem**: Smaller plugin and integration ecosystem compared to GitHub or GitLab.
- **Enterprise Features**: Lacks some of the advanced high-availability and compliance features of GitLab Enterprise.

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

# List all repositories
docker exec -u 1000 -it gitea gitea admin repo list
```

## API examples
Gitea features a comprehensive Swagger-documented API:

```bash
# Get repository information
curl -X GET "http://localhost:3000/api/v1/repos/owner/repo" \
  -H "Authorization: token <YOUR_TOKEN>"

# Create a new issue via API
curl -X POST "http://localhost:3000/api/v1/repos/owner/repo/issues" \
  -H "Authorization: token <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Bug Report", "body": "Something is broken."}'
```

## Related tools / concepts
- [Ollama](ollama.md) — For running local AI code reviews via Gitea Actions.
- [Authentik](authentik.md) — For SSO and user management.
- [Drone](https://www.drone.io/) — A popular third-party CI/CD engine that integrates deeply with Gitea.
- [Forgejo](https://forgejo.org/) — A community-driven fork of Gitea focusing on software freedom.
- [Ansible](../tools/orchestration/ansible.md) — For automating the deployment of Gitea itself.

## Links
- [Official Website](https://gitea.io/)
- [GitHub Repository](https://github.com/go-gitea/gitea)
- [Gitea Actions Overview](https://docs.gitea.com/usage/actions/overview)

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

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-20

## Sources / References
- https://gitea.io/
- https://github.com/go-gitea/gitea
- https://docs.gitea.com/
- https://forgejo.org/
