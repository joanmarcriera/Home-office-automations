# Netlify

## What it is
Netlify is a cloud platform for deploying websites and frontend applications, with a strong focus on modern JAMstack/Composable architecture workflows, automated deploy previews, and seamless serverless frontend operations.

## What problem it solves
It makes it easy to publish and iterate on modern frontend applications without building or managing complex cloud deployment pipelines from scratch. It provides atomic deploys, instant rollbacks, edge routing, and automated SSL, solving the complexity of manual web server and DNS management.

## Where it fits in the stack
**Development & Ops / Composable Frontend Hosting Platform**. It is a premier cloud platform for marketing sites, Hugo/Astro projects, and advanced frontend frameworks like **Next.js 15** and **Remix**. It is a common target for projects created or maintained by autonomous agents like **Claude 5.1** and **GPT-5.5**.

## Typical use cases
- High-performance marketing websites and landing pages.
- Composable frontend apps utilizing headless CMS backends.
- Deployment of documentation engines (such as MkDocs, Astro Starlight) where Deploy Previews streamline PR review processes.
- Form-driven user capture leveraging native Netlify Forms.
- Edge-personalized web applications using Edge Functions.

## Strengths
- **Developer-Centric UX**: Standard-setting integration with GitHub/GitLab with instant deployment on push.
- **Deploy Previews**: Automated generation of isolated, unique preview URLs for every pull request, simplifying visual validation.
- **Deno-Powered Edge Functions**: Serverless logic running at the nearest edge location using modern Deno 2.1 runtimes.
- **Unified Platform**: Integrated forms, identity management, and serverless background functions out of the box.

## Limitations
- **Backend Architecture**: Best suited for stateless or static applications; complex persistent database layers require third-party services (e.g., Supabase, Neon).
- **Bandwidth Limits**: Scale pricing can escalate quickly if high volumes of media or bandwidth are consumed on lower-tier plans.
- **Lock-In Risk**: Specific feature integrations (Netlify Forms, Identity) can introduce lock-in compared to pure containerized deployments.

## When to use it
- When building modern JAMstack sites (Next.js, Gatsby, Astro, Hugo) where rapid, atomic frontend iteration is vital.
- For collaborative teams that heavily leverage visual review and PR deploy previews.
- When you want a low-maintenance, fully managed environment for static docs and prototypes.

## When not to use it
- For monolithic server-rendered applications (e.g. Django, Ruby on Rails, Laravel) that require a persistent node/runtime process.
- When [GitHub Pages](github-pages.md) is already sufficient and natively integrated for simple static markdown repository documentation.
- When on-premise hosting or strict private cloud sandboxing is required (see [Grocy](../../services/grocy.md) or private Kubernetes).

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
Spin up a local environment that emulates Netlify's production environment (including serverless Functions and Edge Functions):
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

### Edge Functions (Deno 2.1+)
Example of an Edge Function that modifies the response based on the user's geographic location using modern Deno APIs:

```typescript
import { Context } from "@netlify/edge-functions";

export default async (request: Request, context: Context) => {
  const country = context.geo?.country?.name || "the world";
  return new Response(`Hello from ${country}!`, {
    headers: { "content-type": "text/html" },
  });
};
```

### Programmatic netlify.toml Validation using Pydantic v2
This Python script parses and validates Netlify deployment files (`netlify.toml`) against strict schema definitions using **Pydantic v2** to ensure deploy builds never fail in CI:

```python
import json
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict

class NetlifyBuildConfig(BaseModel):
    command: str = Field(..., description="Build command (e.g. npm run build)")
    publish: str = Field(..., description="Output directory to publish (e.g. dist, out)")
    functions: str = Field("netlify/functions", description="Folder containing serverless functions")

class NetlifyHeaderRule(BaseModel):
    for_path: str = Field(..., alias="for", description="URL path matcher")
    values: Dict[str, str] = Field(..., description="HTTP headers to inject")

class NetlifyConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    build: NetlifyBuildConfig = Field(..., description="Project build parameters")
    headers: List[NetlifyHeaderRule] = Field(default_factory=list, description="Custom HTTP header injection rules")
    edge_functions: List[Dict[str, str]] = Field(
        default_factory=list,
        validation_alias="edgeFunctions",
        description="Edge function mapping paths"
    )

def validate_netlify_config(raw_json: str) -> Optional[NetlifyConfig]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2
        config = NetlifyConfig.model_validate(data)
        return config
    except json.JSONDecodeError:
        print("Error: Input is not valid JSON.")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
    return None

# Example usage:
# if __name__ == "__main__":
#     sample_config = """
#     {
#         "build": {
#             "command": "npm run build",
#             "publish": "dist",
#             "functions": "netlify/functions"
#         },
#         "headers": [
#             {
#                 "for": "/*",
#                 "values": {
#                     "X-Frame-Options": "DENY",
#                     "X-Content-Type-Options": "nosniff"
#                 }
#             }
#         ]
#     }
#     """
#     validated = validate_netlify_config(sample_config)
#     if validated:
#         print("netlify.toml parsed and validated successfully!")
#         print(validated.model_dump_json(indent=2))
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
- Last reviewed: 2026-11-02
- Confidence: high
