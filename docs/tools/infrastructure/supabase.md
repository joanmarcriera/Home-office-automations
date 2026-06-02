# Supabase

## What it is
Supabase is an open-source backend platform built around Postgres with managed database, auth, storage, realtime, and edge-function services. It provides a suite of tools that mimic the Firebase experience but with the power and flexibility of a relational database.

## What problem it solves
It reduces the amount of backend infrastructure teams need to assemble before shipping apps that need persistence, authentication, file storage, and simple server-side logic. By offering a "Backend-as-a-Service" (BaaS) model on top of Postgres, it ensures that projects remain scalable and compatible with standard SQL tools.

## Where it fits in the stack
**Infrastructure / Backend Platform**. It is often the default persistence layer for AI tools, agent dashboards, workflow state, and app prototypes. It bridges the gap between static hosting and complex custom backends.

## Typical use cases
- Storing workflow state and user data for AI agents.
- Authentication for internal AI tools and dashboards.
- Realtime dashboards and lightweight app backends.
- Waitlist and lead-capture backends for public sites.
- Persistence, auth, and storage for AI product MVPs.
- Backend layer for internal operations dashboards.

## Strengths
- **Postgres-first architecture**: Leverages the full power of SQL and specialized extensions like `pgvector`.
- **Broad feature set**: Auth, Database, Storage, and Edge Functions in one unified platform.
- **Open-source core**: Avoids vendor lock-in with strong community adoption and self-hosting options.
- **Realtime capabilities**: Built-in support for listening to database changes via WebSockets.

## Limitations
- **Backend Discipline**: Still requires schema design, security policy (RLS), and lifecycle discipline.
- **Runtime Constraints**: Edge Functions use Deno, which may have different package support than standard Node.js.
- **Migration Overhead**: Transitioning from a purely NoSQL mindset requires learning relational patterns.

## When to use it
- When you want a fast path from prototype to production-grade backend.
- When AI or automation projects need a durable state layer quickly.
- When a website needs forms, auth, storage, or app state without building a full backend from scratch.
- When building AI applications that require vector search via `pgvector`.

## When not to use it
- When a local-only SQLite or file-based store is enough.
- When you need deep control over every backend component (e.g., custom kernel modules).
- When the site is purely static and a backend would be unnecessary complexity.

## Getting started

### Installation
```bash
# Install the Supabase CLI
npm install supabase --save-dev

# Initialize a new Supabase project
npx supabase init
```

### Minimal Example
```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://your-project.supabase.co'
const supabaseKey = process.env.SUPABASE_KEY
const supabase = createClient(supabaseUrl, supabaseKey)

const { data, error } = await supabase
  .from('profiles')
  .select('*')
```

## CLI examples
```bash
# Login to the CLI
supabase login

# Start local development stack (Docker required)
supabase start

# Link a local project to a remote Supabase project
supabase link --project-ref your-project-ref

# Deploy Edge Functions
supabase functions deploy my-ai-endpoint
```

## API examples
```python
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Insert data into a table
response = supabase.table("todos").insert({"task": "Learn Supabase", "status": "pending"}).execute()

# Query data with filters
data = supabase.table("todos").select("*").eq("status", "pending").execute()
```

## Architecture

Supabase is not a single monolith but a suite of integrated open-source tools centered around a **PostgreSQL** database.

- **PostgreSQL (Database)**: The core storage engine, providing relational capabilities and `pgvector` for AI tasks.
- **GoTrue (Auth)**: A JWT-based API for managing users and issuing access tokens.
- **PostgREST (REST API)**: Automatically turns your database schema into a RESTful API.
- **Realtime (Elixir)**: Listens to PostgreSQL replication streams and broadcasts changes over WebSockets.
- **Storage**: A S3-compatible interface for managing large files, backed by PostgreSQL for metadata.
- **Edge Functions (Deno)**: Serverless functions that run TypeScript logic globally with low latency.

## Security and Row Level Security (RLS)

Security in Supabase is handled primarily through **Row Level Security (RLS)** in PostgreSQL. This allows you to define granular access policies directly on your tables.

- **JWT Integration**: When a user logs in, Supabase issues a JWT. The PostgreSQL `auth.uid()` function can then be used in RLS policies to restrict data access.
- **Service Role Key**: A "super admin" key that bypasses RLS, intended for backend-to-backend communication (never expose in the frontend).
- **Anon Key**: A public key intended for use in the frontend, subject to RLS policies.

Example RLS Policy:
```sql
-- Only allow users to see their own profiles
create policy "Users can view their own profiles"
  on profiles for select
  using ( auth.uid() = id );
```

## Vector Database & AI
Supabase provides native vector support via the `pgvector` extension, making it a powerful choice for RAG (Retrieval-Augmented Generation) workflows.

```sql
-- Enable the pgvector extension
create extension vector;

-- Create a table with a vector column
create table documents (
  id bigserial primary key,
  content text,
  embedding vector(1536) -- Match OpenAI embedding dimensions
);

-- Use a function to perform similarity search
create or replace function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
returns table (
  id bigint,
  content text,
  similarity float
)
language sql stable
as $$
  select
    documents.id,
    documents.content,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where 1 - (documents.embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
$$;
```

## Advanced Implementation

### Edge Functions with AI SDK
Supabase Edge Functions can run AI logic close to the user. Below is a Deno example using the Vercel AI SDK.

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { OpenAIStream, StreamingTextResponse } from "https://esm.sh/ai"
import OpenAI from "https://esm.sh/openai"

const openai = new OpenAI({ apiKey: Deno.env.get('OPENAI_API_KEY') })

serve(async (req) => {
  const { messages } = await req.json()
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    stream: true,
    messages,
  })
  const stream = OpenAIStream(response)
  return new StreamingTextResponse(stream)
})
```

### Realtime Filters
Subscribe to specific database changes to drive agentic UI updates.

```javascript
const channel = supabase
  .channel('agent-tasks')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'tasks',
      filter: 'status=eq.pending'
    },
    (payload) => console.log('New pending task for agent:', payload)
  )
  .subscribe()
```

## Example website pairings
- [Vercel](../development_ops/vercel.md) + Supabase for an AI SaaS MVP.
- [Cloudflare Pages](../development_ops/cloudflare-pages.md) + Supabase for an internal ops tool.
- [Netlify](../development_ops/netlify.md) + Supabase for a forms-driven marketing site.

## Related tools / concepts
- [Vercel](../development_ops/vercel.md) — Frontend hosting and serverless logic.
- [Cloudflare Pages](../development_ops/cloudflare-pages.md) — Edge-native static and function hosting.
- [Netlify](../development_ops/netlify.md) — Atomic deploys and edge functions.
- [GitHub Pages](../development_ops/github-pages.md) — Simple repo-native static hosting.
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md) — Strategy for low-cost AI deployments.
- [n8n](../../services/n8n.md) — Workflow automation that often uses Supabase for state.
- [Tavily](../providers/tavily.md) — AI-native search that can feed data into Supabase.
- [Open WebUI](../../services/open-webui.md) — Self-hosted UI for LLMs that can be backed by Postgres.
- [Dify](../automation_orchestration/dify.md) — LLM application development platform.

## Sources / References
- [Official Website](https://supabase.com/)
- [Documentation](https://supabase.com/docs)
- [GitHub Repository](https://github.com/supabase/supabase)
- [pgvector on Supabase](https://supabase.com/docs/guides/ai)
- [Dify Integration](../ai_knowledge/dify.md)

## Contribution Metadata
- Last reviewed: 2026-06-02
- Confidence: high
