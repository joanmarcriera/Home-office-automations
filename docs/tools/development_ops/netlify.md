# Netlify

## What it is
Netlify is a cloud platform for deploying websites and frontend applications, with a strong focus on JAMstack workflows, deploy previews, and simple frontend operations.

## What problem it solves
It makes it easy to publish and iterate on frontend sites without building a full deployment platform from scratch. It provides atomic deploys, instant rollbacks, and automated SSL, solving the complexity of manual web server management.

## Where it fits in the stack
**Development & Ops / Frontend Hosting Platform**. It is a solid option for marketing sites, JAMstack projects, and frontend-first web experiences. It is often used as a deployment target for projects assisted by **Claude 4.8 Opus** and **GPT-5.5**.

## Typical use cases
- Marketing websites and landing pages.
- Small product sites and prototypes built with **React** or **Next.js**.
- Static or mostly static frontend projects (e.g., Hugo, Gatsby).
- Form-driven lead capture pages using Netlify Forms.
- Documentation sites where deploy previews matter for collaborative review.

## Strengths
- **Developer Experience**: Exceptionally smooth onboarding and integration with GitHub/GitLab.
- **JAMstack Native**: Optimized for modern static site generators and frontend frameworks.
- **Deploy Previews**: Automatically generates a unique URL for every pull request, simplifying review.
- **Edge Functions**: Powered by Deno, allowing low-latency logic at the network edge.

## Limitations
- **Backend Constraints**: Backend usually requires external services (e.g., Supabase, Firebase) as Netlify is primarily frontend-focused.
- **Pricing Tiers**: Costs can escalate quickly for enterprise features or high-bandwidth sites.
- **Less AI-Default**: [Vercel](vercel.md) is often the more common default choice for many AI-native frontend templates.

## When to use it
- When the site is primarily frontend and the team values a streamlined deployment workflow.
- When deploy previews and atomic frontend iteration are central to your development cycle.
- When you want a credible, generous free-tier option for launching prototypes.

## When not to use it
- When [Vercel](vercel.md) is the clearer default for a specific product or AI demo framework.
- When [GitHub Pages](github-pages.md) is sufficient for simple, repo-native static documentation.
- When the primary challenge involves complex server-side state or heavy custom backend infrastructure.

## Getting started

### 1. CLI Installation
Install the Netlify CLI globally via npm to manage your sites from the terminal:

```bash
npm install netlify-cli -g
```

### 2. Authentication & Initialization
Authenticate your CLI session and link your local directory to a Netlify project:

```bash
# Login to your Netlify account
netlify login

# Initialize a project in the current directory
netlify init
```

### 3. Hello World Deployment
To deploy a site manually or to production from your terminal:

```bash
# Deploy to a draft URL for testing
netlify deploy

# Deploy to production
netlify deploy --prod
```

## CLI examples

### 1. Site Status
Check the status of the current site and its linked Netlify project details:
```bash
netlify status
```

### 2. Local Development Server
Spin up a local environment that emulates Netlify's production environment (including Functions and Edge Functions):
```bash
netlify dev
```

### 3. Build Environment
Run a build locally exactly as it would run on Netlify's CI/CD pipeline:
```bash
netlify build
```

## API examples

### Netlify Functions (Serverless)
Netlify Functions allow you to run serverless backend code (AWS Lambda under the hood). Create a file at `netlify/functions/hello.ts`:

```typescript
import { Context } from "@netlify/functions"

export default async (req: Request, context: Context) => {
  return new Response("Hello from Netlify Functions!")
}
```

### Edge Functions (Deno)
Example of an Edge Function that modifies the response based on the user's geographic location:

```typescript
import { Context } from "@netlify/edge-functions";

export default async (request: Request, context: Context) => {
  const country = context.geo?.country?.name || "the world";
  return new Response(`Hello from ${country}!`, {
    headers: { "content-type": "text/html" },
  });
};
```

## Related tools / concepts
- [Vercel](vercel.md)
- [Cloudflare Pages](cloudflare-pages.md)
- [GitHub Pages](github-pages.md)
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md)
- [Supabase](../infrastructure/supabase.md)
- [Cursor](cursor.md)
- [GitHub Copilot](github_copilot.md)
- [Vercel AI Gateway](../providers/vercel-ai-gateway.md)

## Sources / References
- [Official Netlify Website](https://www.netlify.com/)
- [Netlify Pricing](https://www.netlify.com/pricing/)
- [Netlify Documentation](https://docs.netlify.com/)
- [Netlify CLI Reference](https://cli.netlify.com/)

## Contribution Metadata
- Last reviewed: 2026-06-30
- Confidence: high
