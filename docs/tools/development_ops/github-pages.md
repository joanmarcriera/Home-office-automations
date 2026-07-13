# GitHub Pages

## What it is
GitHub Pages is a static site hosting service that takes HTML, CSS, and JavaScript files straight from a repository on GitHub and publishes a website. As of June 2026, it is the standard for hosting AI-generated documentation, project microsites, and [MkDocs](../../mkdocs.yml) knowledge bases directly from the source of truth.

## What problem it solves
It eliminates the friction between code development and documentation deployment. By integrating directly with GitHub repositories, it provides:
- **Automation**: Native integration with GitHub Actions for automated builds and deployments.
- **Security**: Automatic SSL/TLS encryption via Let's Encrypt and enforced HTTPS.
- **Cost Efficiency**: Free hosting for public repositories and GitHub Pro/Enterprise users.
- **Version Control**: Every site update is tracked via Git, enabling easy rollbacks and collaboration.

## Where it fits in the stack
**Development & Ops / Repo-Native Static Website Hosting**. It serves as the primary presentation layer for repository-resident information, often used in conjunction with [Claude Code](claude-code.md) or [Aider](aider.md) for automated documentation maintenance.

## Typical use cases
- Documentation sites for open-source projects (e.g., MkDocs, Docusaurus).
- Personal portfolios and technical blogs.
- Automated [Playwright](playwright.md) test reports and execution logs.
- Landing pages for [MCP](../automation_orchestration/mcp.md) servers and AI agent projects.
- Hosting [JSON](https://www.json.org/) schemas or static API specifications.

## Strengths
- **Native Ecosystem Integration**: No external hosting provider is needed if your code is already on GitHub.
- **Global Delivery**: Powered by GitHub's CDN for high availability and low latency.
- **Custom Domains**: Supports custom CNAME records with automatic HTTPS certificate provisioning.
- **Actions Integration**: Complete flexibility to use any static site generator via custom GitHub Actions workflows.

## Limitations
- **Static Content Only**: Does not support server-side languages like PHP, Ruby on Rails, or Python (backend).
- **Size and Bandwidth**: Sites are limited to 1GB in size and a soft bandwidth limit of 100GB per month.
- **Public/Private Visibility**: On free plans, GitHub Pages sites are always public if the repository is public.

## When to use it
- For hosting project documentation that lives alongside the source code.
- When you want zero-cost, zero-maintenance hosting for a static site.
- When your deployment pipeline is already built on GitHub Actions.
- For sharing AI-agent-generated reports or knowledge bases.

## When not to use it
- When your application requires a backend database or dynamic request processing.
- When using [Vercel](vercel.md) or [Netlify](netlify.md) for advanced edge functions or specialized frontend frameworks like Next.js.
- For high-traffic commercial sites that exceed the 100GB/month bandwidth recommendation.

## Getting started

### 1. Enable via Settings
1. Navigate to your repository's **Settings** tab.
2. Click **Pages** in the "Code and automation" section.
3. Choose your **Source**: either "Deploy from a branch" or "GitHub Actions".

### 2. Basic Setup (GitHub Actions)
If using "GitHub Actions", select the "Static HTML" template or use a custom workflow file in `.github/workflows/static.yml`.

## CLI examples

The GitHub CLI (`gh`) allows for managing and monitoring your Pages sites.

```bash
# Check the status of your GitHub Pages site
gh api repos/:owner/:repo/pages

# List recent Pages build runs
gh run list --workflow "pages-build-deployment"

# Trigger a manual build (if workflow_dispatch is configured)
gh workflow run deploy.yml
```

## API examples

### Get Pages configuration
Retrieve information about a GitHub Pages site.

```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <TOKEN>" \
  https://api.github.com/repos/OWNER/REPO/pages
```

### Request a Pages build
Trigger a new build and deployment for the site.

```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <TOKEN>" \
  https://api.github.com/repos/OWNER/REPO/pages/builds
```

## Related tools / concepts
- [MkDocs](../../mkdocs.yml) — Standard static site generator for technical documentation.
- [Claude Code](claude-code.md) — Terminal-based agent for managing GitHub-native projects.
- [Aider](aider.md) — AI pair programmer often used to author Pages content.
- [Netlify](netlify.md) — Advanced static hosting alternative with form handling.
- [Vercel](vercel.md) — Optimized hosting for React and Next.js applications.
- [Cloudflare Pages](cloudflare-pages.md) — High-performance edge hosting with advanced security.
- [MCP](../../tools/automation_orchestration/mcp.md) — Protocol often documented via GitHub Pages.
- [Playwright](playwright.md) — Testing framework that generates static reports for hosting.

## Sources / references
- [GitHub Pages Official Documentation](https://docs.github.com/en/pages)
- [Configuring a Custom Domain for your GitHub Pages Site](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [About GitHub Pages and Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll)
- [GitHub Actions: Deploy Pages Action](https://github.com/actions/deploy-pages)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
