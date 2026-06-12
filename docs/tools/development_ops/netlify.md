# Netlify

## What it is
Netlify is a cloud platform for deploying websites and frontend applications, with a strong focus on JAMstack workflows, previews, and simple frontend operations.

## What problem it solves
It makes it easy to publish and iterate on frontend sites without building a full deployment platform from scratch, offering atomic deploys and instant rollbacks.

## Where it fits in the stack
**Development & Ops / Frontend Hosting Platform**. It is a solid option for marketing sites, JAMstack projects, and frontend-first web experiences that do not require a heavy custom backend on day one. It is often used as a deployment target for `claude-4-8-opus-20260528` assisted projects.

## Typical use cases
- Marketing websites
- Small product sites and prototypes
- Static or mostly static frontend projects
- Form-driven lead capture pages
- Sites where deploy previews matter to the workflow

## Strengths
- Good developer experience for frontend teams
- Strong fit for static and JAMstack-style deployment
- Good preview workflow (Deploy Previews)
- Edge Functions (powered by Deno) for logic at the network edge

## Limitations
- Less of a default magnet than [Vercel](vercel.md) for AI app frontends
- Not as minimal as [GitHub Pages](github-pages.md) for docs-only sites
- Backend usually still lives elsewhere (e.g., Supabase, Firebase)

## When to use it
- When the site is mostly frontend and the team likes Netlify's workflow
- When deploy previews and frontend iteration are central
- When you want a credible free-tier launch option without treating hosting as a full project

## When not to use it
- When [Vercel](vercel.md) is the clearer default for a product or AI demo
- When [GitHub Pages](github-pages.md) is enough for repo-native static docs
- When the main challenge is backend services rather than frontend deployment

## Getting started

### CLI Installation
Install the Netlify CLI globally via npm:

```bash
npm install netlify-cli -g
```

### Authentication & Initialization
Authenticate your CLI session and initialize a new project:

```bash
# Login to your Netlify account
netlify login

# Initialize a project in the current directory
netlify init
```

### Hello World Deployment
To deploy a site manually from your terminal:

```bash
# Deploy to a draft URL for testing
netlify deploy

# Deploy to production
netlify deploy --prod
```

## CLI examples

### 1. Site Status
Check the status of the current site and linked Netlify project:
```bash
netlify status
```

### 2. Local Development Server
Spin up a local environment that emulates Netlify (including Functions and Edge Functions):
```bash
netlify dev
```

### 3. Build Environment
Run a build as it would run on Netlify's CI:
```bash
netlify build
```

## API examples

### Netlify Functions (Serverless)
Netlify Functions (AWS Lambda under the hood) allow you to run serverless backend code. Create a file at `netlify/functions/hello.ts`:

```typescript
import { Context } from "@netlify/functions"

export default async (req: Request, context: Context) => {
  return new Response("Hello from Netlify Functions!")
}
```

### Edge Functions
Example of an Edge Function that modifies the response based on the user's country:

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
- [Vercel OSS](vercel-oss.md)

## Sources / References
- [Official Website](https://www.netlify.com/)
- [Pricing](https://www.netlify.com/pricing/)
- [Documentation](https://docs.netlify.com/)
- [Netlify CLI Reference](https://cli.netlify.com/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
