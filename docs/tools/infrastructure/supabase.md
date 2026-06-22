# Supabase

## What it is
Supabase is an open-source backend platform built around PostgreSQL with managed database, authentication, storage, realtime, and edge-function services. It provides a suite of tools that mimic the Firebase experience but with the power and flexibility of a relational database, fully integrated with the June 2026 agentic ecosystem.

## What problem it solves
It reduces the amount of backend infrastructure teams need to assemble before shipping apps that need persistence, authentication, file storage, and simple server-side logic. By offering a "Backend-as-a-Service" (BaaS) model on top of PostgreSQL, it ensures that projects remain scalable and compatible with standard SQL tools and AI-driven data analysis.

## Where it fits in the stack
**Infrastructure / Backend Platform**. It is the default persistence layer for AI tools, agent dashboards, and workflow state management. It bridges the gap between static hosting and complex custom backends, supporting native vector search and agentic hooks.

## Typical use cases
- **Agent Memory**: Storing long-term semantic memory and state for AI agents using `pgvector`.
- **Identity Management**: Native authentication for internal AI dashboards and customer-facing agent portals.
- **Realtime Coordination**: Synchronizing multi-agent workflows via database change listeners.
- **Edge Inference Hooks**: Running lightweight AI logic or API orchestration via Supabase Edge Functions.
- **RAG Infrastructure**: Serving as the unified store for document embeddings and metadata.

## Strengths
- **PostgreSQL-First Architecture**: Leverages the full power of SQL, including advanced extensions like `pg_graphql` and `pgvector`.
- **Open-Source Core**: Avoids vendor lock-in with strong community adoption and robust self-hosting options.
- **MCP 3.0 Support**: Native integration with the Model Context Protocol for secure, agentic data access.
- **Edge Computing**: Deno-based Edge Functions provide global, low-latency execution for AI logic.

## Limitations
- **Schema Discipline**: Requires understanding of relational database design and Row Level Security (RLS) policies.
- **Deno Ecosystem**: Edge Functions use Deno, which may differ from standard Node.js environments for some legacy packages.
- **Scale Considerations**: While highly scalable, complex real-time filters on very high-volume tables require careful optimization.

## When to use it
- When you need a production-grade backend for an AI application with minimal setup.
- When your project requires both relational data and vector embeddings in a single store.
- When building multi-agent systems that need a shared, real-time state layer.
- When prioritizing open-source components and the ability to self-host.

## When not to use it
- For simple, local-only projects where a local SQLite file or `rclone` is sufficient.
- If the application requires deep kernel-level customization of the database engine.
- For purely static sites where no persistence or authentication is required.

## Getting started

### Installation
```bash
# Install the Supabase CLI
npm install supabase --save-dev

# Initialize a new Supabase project
npx supabase init
```

### Minimal Implementation (TypeScript)
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://your-project.supabase.co'
const supabaseKey = process.env.SUPABASE_KEY
const supabase = createClient(supabaseUrl, supabaseKey)

// Fetch data from a table
const { data, error } = await supabase
  .from('agents')
  .select('*')
```

## CLI examples

### Local Development
```bash
# Start the full Supabase stack locally using Docker
supabase start

# Check the status of local services
supabase status
```

### Database Management
```bash
# Generate a new migration file
supabase migration new add_vector_support

# Push local changes to a remote project
supabase db push
```

### Edge Functions
```bash
# Create a new function
supabase functions new agent-hook

# Deploy the function to the cloud
supabase functions deploy agent-hook
```

## API examples

### Python SDK with Vector Search
```python
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Perform a similarity search via a PostgreSQL function
result = supabase.rpc(
    "match_documents",
    {
        "query_embedding": [0.1, 0.2, 0.3], # Vector from embedding model
        "match_threshold": 0.8,
        "match_count": 5
    }
).execute()
```

### Realtime Subscription
```javascript
const channel = supabase
  .channel('agent-status')
  .on(
    'postgres_changes',
    { event: 'UPDATE', schema: 'public', table: 'tasks' },
    (payload) => {
      console.log('Task updated:', payload.new.status)
    }
  )
  .subscribe()
```

## Related tools / concepts
- [Vercel](../development_ops/vercel.md) — Recommended frontend hosting partner.
- [Cloudflare Pages](../development_ops/cloudflare-pages.md) — Edge-native static and function hosting.
- [n8n](../../services/n8n.md) — Workflow automation that often uses Supabase for long-term state.
- [Dify](../ai_knowledge/dify.md) — Agentic development platform with native Supabase support.
- [Open WebUI](../../services/open-webui.md) — Self-hosted LLM interface compatible with Supabase backends.
- [LiteLLM](../../services/litellm.md) — AI proxy often used alongside Supabase for cost tracking.
- [MCP 3.0](../../knowledge_base/self-healing-agent-research.md) — Protocol for agentic data interaction.
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md) — Strategic guide for BaaS-backed sites.

## Sources / references
- [Supabase Official Website](https://supabase.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Supabase GitHub Repository](https://github.com/supabase/supabase)
- [Supabase AI & Vector Guide](https://supabase.com/docs/guides/ai)
- [PostgREST Documentation](https://postgrest.org/)
- [Dify.ai](https://dify.ai/)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
