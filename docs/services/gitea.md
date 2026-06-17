# Gitea

## What it is
Gitea is a community-managed lightweight code hosting solution written in Go. It provides a complete Git service including repository management, issue tracking, code review, and CI/CD integration, with a focus on simplicity and high performance. It is a painless self-hosted Git service that serves as the backbone for private DevOps ecosystems in the June 2026 era.

## What problem it solves
It allows developers and home lab enthusiasts to host their own private Git repositories without the resource overhead of GitLab or the privacy concerns of public cloud providers like GitHub. In 2026, it specifically addresses the need for local, air-gapped code storage for proprietary AI training datasets and sensitive automation scripts that utilize Claude 4.8 Opus and GPT-5.5. It provides a central hub for code collaboration and automation that can run on low-power hardware.

## Where it fits in the stack
Gitea sits in the **Development & DevOps** layer. It serves as the primary source of truth for code, configuration files, and automation workflows. It is the central registry for local GitOps, often triggering pipelines that deploy services across the entire homelab stack.

## Typical use cases
- **Private Code Hosting**: Maintaining internal tools and projects away from public eyes.
- **GitOps**: Storing infrastructure-as-code (Ansible, Terraform, K3s manifests) and triggering deployments.
- **AI Dataset Management**: Hosting versioned datasets for fine-tuning local models.
- **Local CI/CD**: Running Gitea Actions for automated testing and deployment.
- **Documentation**: Hosting project documentation via Gitea's built-in wiki or Markdown support.
- **Mirrors**: Maintaining local mirrors of critical public repositories for offline access.
- **SSO Integration**: Using OIDC for centralized authentication via Authentik.

## Strengths
- **Performance**: Extremely lightweight and fast; runs comfortably on a Raspberry Pi 5 or low-power NAS.
- **GitHub-Like UX**: Familiar interface that requires minimal learning for existing Git users.
- **Built-in CI/CD**: Gitea Actions provides high compatibility with GitHub Actions workflows, including concurrency support and reusable workflows from private repositories.
- **v1.26+ Features**: Keyboard shortcuts (e.g., `s` for search), subpath archives, Vite-based front-end toolchain, Terraform registry/state backend support, and automatic release notes generation.
- **Self-Contained**: Can be run as a single binary or a small Docker container with minimal dependencies.
- **Enterprise Ready**: Supports OIDC, LDAP, and advanced repository mirroring.

## Limitations
- **Ecosystem**: Smaller plugin and integration ecosystem compared to GitHub or GitLab.
- **Scaling**: Lacks the massive horizontal scaling capabilities (like GitLab Geo) for multi-region global teams.
- **Native AI Features**: Lacks deeply integrated, first-party AI coding assistants found in GitHub (Copilot), though it is easily extended via custom Actions and local LLMs (e.g., Ollama).

## When to use it
- When you want a lightweight, self-hosted alternative to GitHub or GitLab.
- For managing GitOps workflows on home lab infrastructure with low resource overhead.
- To maintain private copies of code and configuration without cloud dependencies.
- When running Git services on edge devices or low-resource hardware like a NAS.

## When not to use it
- If you require advanced enterprise features like geo-replication or deep compliance auditing found in GitLab.
- When you need the massive social ecosystem and public visibility of GitHub.
- If your team relies heavily on proprietary third-party integrations that only support GitHub/GitLab APIs specifically.

## Getting started

### Docker Compose
To run Gitea using Docker Compose:

```yaml
services:
  server:
    image: gitea/gitea:1.26.2
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

### SSO & OIDC Integration (Authentik)
1. Navigate to **Site Administration > Authentication Sources > Add Authentication Source**.
2. Set **Authentication Type** to `OpenID Connect`.
3. Configure the following:
    - **Authentication Name**: `authentik`
    - **OAuth2 Provider**: `OpenID Connect`
    - **Client ID (Key)**: `<Your Client ID>`
    - **Client Secret**: `<Your Client Secret>`
    - **OpenID Connect Auto Discovery URL**: `https://authentik.example.com/application/o/gitea/.well-known/openid-configuration`
    - **Additional Scopes**: `email profile`

### Enabling Gitea Actions
1. In your `app.ini`, ensure Actions are enabled:
```ini
[actions]
ENABLED = true
```
2. **Set up a Runner**: Gitea Actions requires a separate "Gitea Runner" (formerly `act_runner`).
3. **Registration**: Registration tokens are managed via the administrative UI or CLI.

## CLI examples
The `gitea` binary inside the container can be used for administrative tasks:

```bash
# Create an admin user
docker exec -u 1000 -it gitea gitea admin user create --username admin --password secret --email admin@example.com --admin

# Dump database and configuration for backup
docker exec -u 1000 -it gitea gitea dump

# List all repositories on the instance
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
  -d '{"title": "Bug Report", "body": "Observed in June 2026 build."}'

# Automated Code Review Pattern (Ollama Integration)
# Trigger a local LLM to review a pull request
CODE_DIFF=$(git diff origin/main)
PAYLOAD=$(jq -n --arg diff "$CODE_DIFF" '{
  model: "codellama",
  prompt: ("Review this diff and suggest improvements:\n\n" + $diff),
  stream: false
}')
curl http://ollama-server:11434/api/generate -d "$PAYLOAD"
```

## Related tools / concepts
- [Ollama](ollama.md) — For running local AI code reviews via Gitea Actions.
- [Authentik](authentik.md) — For centralized SSO and user management.
- [Ansible](../tools/orchestration/ansible.md) — For automating the deployment of Gitea itself.
- [Nextcloud](nextcloud.md) — For syncing documentation and larger binary artifacts.
- [n8n](n8n.md) — For orchestrating workflows triggered by Gitea webhooks.
- [Vikunja](vikunja.md) — For project management integrated with Gitea issues.
- [Paperless-ngx](paperless-ngx.md) — For archiving documentation generated from Git repositories.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Standard for integrating Gitea into AI agent workflows.
- [Forgejo](https://forgejo.org/) — A community-driven fork of Gitea focusing on software freedom.
- [Argocd](https://argoproj.github.io/cd/) — For Kubernetes-native GitOps using Gitea as a source.

## Sources / references
- [Official Website](https://gitea.io/)
- [GitHub Repository](https://github.com/go-gitea/gitea)
- [Gitea Documentation](https://docs.gitea.com/)
- [Gitea 1.26.0 Release Blog](https://blog.gitea.com/release-of-1.26.0/)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
