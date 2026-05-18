# GitHub Pages

## What it is
GitHub Pages is GitHub's static site hosting service for project sites, documentation, blogs, and other repo-backed web content. It integrates directly with GitHub repositories to automate the deployment of static files.

## What problem it solves
It gives teams the simplest path from a Git repository to a publicly hosted static website, especially when the website is documentation or content rather than an application. It removes the need for managing separate hosting infrastructure for static content.

## Where it fits in the stack
**Development & Ops / Repo-Native Static Website Hosting**. It is the best fit when the site should stay tightly coupled to a repository and remain mostly static.

## Typical use cases
- Project documentation sites (e.g., MkDocs, Docusaurus)
- Public blogs (e.g., Jekyll, Hugo)
- Portfolio sites
- Tool directories generated from repo data
- Landing pages with minimal dynamic behavior
- Storybook or documentation for UI components

## Example website types
- A docs site for an open-source project
- A personal or company portfolio site
- A static knowledge base
- A project microsite that is maintained directly from Markdown or a static-site generator

## Deployment Strategies
GitHub Pages supports two primary deployment methods:
1.  **Branch-based**: Deploying from a specific branch (usually `main`, `gh-pages`, or a `/docs` folder on `main`).
2.  **GitHub Actions**: Using a custom workflow to build and deploy your site. This is now the recommended approach for modern static-site generators.

## GitHub Actions Integration
Modern workflows use GitHub Actions to build the site in a CI/CD environment and then upload the artifacts to GitHub Pages.

### Example Workflow: Static HTML/JS
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## Custom Domains & SSL
GitHub Pages supports custom domains (e.g., `www.example.com`).
- **Enforced HTTPS**: GitHub provides automatic SSL certificates via Let's Encrypt for all GitHub Pages sites.
- **DNS Configuration**: Requires CNAME, ALIAS, or A records depending on whether you use a subdomain or an apex domain.

## Security & Access Control
- **Visibility**: On GitHub Free, GitHub Pages sites are always public if the repository is public. On GitHub Pro/Enterprise, you can host private GitHub Pages sites accessible only to organization members.
- **Subdomain Isolation**: Each site is hosted on a unique subdomain of `github.io` (or a custom domain), providing some level of security isolation between projects.

## Jekyll Integration
Jekyll is the "native" static site generator for GitHub Pages. GitHub runs Jekyll builds automatically if it detects a `_config.yml` file and you are using the branch-based deployment method. For custom Jekyll plugins, you must use GitHub Actions.

## Comparison with Alternatives
- **[Vercel](vercel.md)**: Better for dynamic apps, Next.js, and advanced edge functions.
- **[Netlify](netlify.md)**: Better for form handling, identity services, and complex build plugins.
- **[Cloudflare Pages](cloudflare-pages.md)**: Better for global edge performance and deep integration with Cloudflare DNS/WAF.

## Strengths
- Very simple mental model
- Excellent for static content tied to a repo
- Strong fit for docs-first workflows
- Good default when you want low overhead and no application platform complexity
- Zero cost for public repositories

## Limitations
- Not intended for dynamic app behavior (no server-side logic)
- Minimal backend story compared with [Vercel](vercel.md) plus [Supabase](../infrastructure/supabase.md)
- Less suitable for AI demos or authenticated product MVPs (on free tier)
- 1GB limit for repository size and 100GB monthly bandwidth soft limit

## When to use it
- When the website is mostly docs, content, or a static project site
- When the repo is the source of truth for the site
- When low maintenance matters more than app flexibility
- When you are already using GitHub for version control

## When not to use it
- When the site needs auth, database-backed interactions, or an app-like frontend
- When [Vercel](vercel.md) or [Cloudflare Pages](cloudflare-pages.md) better matches the product shape
- When your launch depends on dynamic product workflows rather than static publishing
- When you need complex server-side redirects or headers not supported by `.htaccess` or similar

## Troubleshooting Common Issues
- **404 Errors**: Often caused by incorrect path routing in SPAs (Single Page Applications). Requires a `404.html` workaround.
- **Build Failures**: Check GitHub Actions logs for dependency issues or configuration errors.
- **DNS Mismatch**: Ensure CNAME records in the repo match the DNS provider settings.

## Free-tier comments
- Excellent free-tier fit for docs, blogs, portfolios, and repo-centric static sites
- Pair with third-party services only when you need specific dynamic features
- Migrate away when the site stops being "mostly static"

## Common combinations
- **[GitHub Pages](github-pages.md) + Markdown docs**: best default for repo-native documentation.
- **[GitHub Pages](github-pages.md) + [Playwright](playwright.md)**: automated E2E testing of the static site before deployment.
- **[GitHub Pages](github-pages.md) + [Aider](aider.md)**: using AI to generate and iterate on the static content.
- **[GitHub Pages](github-pages.md) + [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md)**: use this path when deciding whether static simplicity is enough.

## Related tools / concepts
- [Cloudflare Pages](cloudflare-pages.md)
- [Vercel](vercel.md)
- [Netlify](netlify.md)
- [GitHub Actions](github-pages.md) (Implicitly used)
- [Docker](../infrastructure/docker.md) (for local build environments)
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md)

## Sources / References
- [Official Overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Configuring a Custom Domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [About GitHub Pages and Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
