# AI Company Starter Stack

## What it is
The AI Company Starter Stack is an opinionated selection of tools and architectural patterns designed to turn a traditional business into an AI-native organization. It provides a curated list of "defaults" across various layers—from web surfaces and agent operating models to workflow control planes and local inference options—enabling teams to build operating leverage rather than just side experiments.

## What problem it solves
Most organizations struggle with "tool sprawl" when adopting AI, often implementing fragmented solutions that don't communicate or scale. This starter stack solves that by providing a unified operating system where [n8n](../services/n8n.md) coordinates workflows, [Claude Skills](../tools/agents/claude-skills-ecosystem.md) package procedures, and [mem0](../tools/agents/mem0.md) preserves context. It focuses on the "smallest stack" that provides maximum leverage across product, operations, and research, fully utilizing SOTA late December 2026 frontier models (Claude 5.1, GPT-5.5, Gemini 4.0 Pro/Flash, Llama 4, Gemma 3, and Qwen 3.6).

## Where it fits in the stack
**Category**: Knowledge Base / Architectural Pattern. It serves as the **operational blueprint** of the repository, integrating various tools from the `docs/services/` and `docs/tools/` directories into a cohesive business framework.

## Typical use cases
- **Bootstrapping an AI Agency**: Using the "Research and lead-intel pack" to automate client research and market synthesis.
- **Internal Operations Modernization**: Implementing the [Google Workspace CLI](../tools/automation_orchestration/google-workspace-cli.md) and n8n to automate administrative drudgery.
- **Privacy-Conscious R&D**: Setting up [LocalAI](../tools/infrastructure/localai.md) and [llmfit](../tools/development_ops/llmfit.md) for secure, internal-only AI development.
- **Rapid MVP Launch**: Following the "Website launch pack" to build and deploy a public-facing AI product shell.

## Strengths
- **High Cohesion**: Tools are selected based on how well they integrate with each other (e.g., n8n + Paperless + Vikunja).
- **Cost-Efficiency**: Prioritizes free or low-cost starter tiers and local inference options.
- **Scalable**: Provides a clear "Replace when" path for every layer, ensuring the stack grows with the company.
- **Outcome-Focused**: Categorized into "Expansion packs" targeted at specific business results.
- **State-of-the-Art Integration**: Fully supports Model Context Protocol FastMCP 3.1 specifications/schemas for distributed agent orchestration and long-running context.

## Limitations
- **Opinionated**: The "Default choice" may not fit companies with strict legacy infrastructure constraints (e.g., non-Google Workspace environments).
- **Maintenance Overhead**: Running a full self-hosted stack (n8n, Supabase, LocalAI) requires more technical expertise than using SaaS-only solutions.
- **Fast Obsolescence**: The "Frontier" models and tools change rapidly, requiring periodic review of the recommended defaults.

## When to use it
- When you are building a new company and want to be "AI-native" from day one.
- When your current AI efforts are fragmented and you need a unified operating model.
- When you want to reduce per-token costs by migrating some workloads to local/private inference.

## When not to use it
- If you already have a mature, high-scale AI infrastructure that requires specialized, non-standardized tools.
- If you are looking for a single-app solution rather than a comprehensive company-wide stack.

## Getting started
To implement the AI Company Starter Stack:

1. **Review the Default Stack**: Scan the table below to understand the core layers and recommended tools.
2. **Select an Expansion Pack**: Choose the pack (e.g., "Knowledge workspace pack") that matches your most urgent business bottleneck.
3. **Deploy the Core**: Start with [n8n](../services/n8n.md) and the [Google Workspace CLI](../tools/automation_orchestration/google-workspace-cli.md) to build your first automation.
4. **Iterate with Skills**: Package your repeatable procedures into the [Claude Skills Ecosystem](../tools/agents/claude-skills-ecosystem.md) to empower your team.

### The Default Stack Layers

| Layer | Default Choice | Role / Description |
| :--- | :--- | :--- |
| **Web Presence / Shell** | [FastHTML](../tools/frameworks/fasthtml.md) or [Vercel](../tools/cloudflare-pages.md) | Rapidly building and launching low-latency AI application shells. |
| **Workflow Engine** | [n8n](../services/n8n.md) | The central control plane coordinating tasks and scheduling cross-app APIs. |
| **Orchestration / Agents** | [Claude Skills](../tools/agents/claude-skills-ecosystem.md) / [FastMCP 3.1](../tools/automation_orchestration/mcp.md) | Standardized task execution, capability exposure, and tool calling protocols. |
| **Workspace Integration** | [Google Workspace CLI](../tools/automation_orchestration/google-workspace-cli.md) | Seamless programmatic control over office files, emails, and drive assets. |
| **Database / Context Store** | [mem0](../tools/agents/mem0.md) / Supabase | Cross-session memory persistence, user personalization, and vector stores. |
| **Internal Inference** | [LocalAI](../tools/infrastructure/localai.md) / [Ollama](../../services/ollama.md) | Running high-performance open-weight models locally to secure private data. |

### Starter Expansion Packs

#### 1. Research and Lead-Intel Pack
- **Default Stack Integration**: Automated scraping and market synthesis.
- **Recommended Tools**: [Tavily](../tools/providers/tavily.md) and [Browser Use](../tools/automation_orchestration/browser-use.md).

#### 2. Knowledge Workspace Pack
- **Default Stack Integration**: Local corporate indexing and tasks.
- **Recommended Tools**: [AnythingLLM](../tools/ai_knowledge/anythingllm.md), [Paperless](../reference-implementations/paperless/README.md), and [Vikunja](../tools/automation_orchestration/vikunja-mcp.md).

#### 3. Local / Secure R&D Pack
- **Default Stack Integration**: Air-gapped pipeline and fine-tuning.
- **Recommended Tools**: [LocalAI](../tools/infrastructure/localai.md) and [llmfit](../tools/development_ops/llmfit.md).

## CLI examples
```bash
# Initialize a new FastMCP 3.1-based project within the stack
mcp init my-agentic-workflow --version 3.1

# Deploy an FastMCP 3.1 server with native Task Protocol capabilities
mcp dev run my-agentic-workflow --port 8080

# Use Google Workspace CLI to list company documents for the agent
gw drive list --query "folder:'Company Strategy'"
```

## API examples
The following snippet demonstrates how to define a "Skill" and leverage the Model Context Protocol (FastMCP 3.1) Task Protocol within the starter stack:

```python
from pydantic import BaseModel, Field
from mcp import Client, TaskProtocol

class CompanyKnowledgeSearch(BaseModel):
    """Search for internal company knowledge across Docs and AnythingLLM."""
    query: str = Field(..., description="The search query for company knowledge.")
    depth: int = Field(default=3, description="The depth of the search results.")

# Standard FastMCP 3.1 Task Protocol registration
client = Client(endpoint="http://localhost:8080")
task_proto = TaskProtocol(client)

async def run_analysis():
    # Spawning a stateful research task using FastMCP 3.1 Task Protocol
    task = await task_proto.create_task(
        name="Knowledge Synthesis",
        instruction="Synthesize internal knowledge base utilizing Qwen 3.6 and Claude 5.1"
    )
    print(f"Initialized FastMCP 3.1 Task {task.id} with status: {task.status}")
```

### Programmatic Workspace Config Validation
Ensure secure routing of API calls and local keys when deploying the starter stack, validating configuration data using **Pydantic v2**:
```python
from pydantic import BaseModel, Field, SecretStr
from typing import Literal

class StarterStackConfig(BaseModel):
    environment: Literal["development", "production"] = "development"
    n8n_api_url: str = Field(..., description="API endpoint for workflow orchestration")
    mcp_port: int = Field(default=8080, ge=1024, le=65535)
    anthropic_api_key: SecretStr = Field(..., description="Claude 5.1 credentials")

# Validate the operational configuration programmatically
raw_config = {
    "environment": "production",
    "n8n_api_url": "https://n8n.mycompany.local/api/v1",
    "mcp_port": 8080,
    "anthropic_api_key": "sk-ant-prod-12345"
}

config = StarterStackConfig.model_validate(raw_config)
print(f"Validated Starter Stack in {config.environment} mode on port {config.mcp_port}")
```

## Related tools / concepts
- [AI Tooling Landscape](ai_tooling_landscape.md)
- [AI Builder Index](ai_builder_index.md)
- [Agent Framework Learning Map](agent_framework_learning_map.md)
- [Agent Protocols](agent_protocols.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [Model Routing Guide](model_routing_guide.md)
- [API Pricing & Free Tiers](api_pricing_free_tiers.md)
- [Starred AI Agent Repos](starred_ai_agent_repos.md)
- [Multi-Agent KnowledgeOps](../architecture/multi_agent_knowledgeops.md)
- [Infrastructure](../architecture/infrastructure.md)

## Sources / references
- [Free AI Website Playbook](free_ai_website_playbook.md)
- [Starred AI / Agent Repositories Over 10K Stars](starred_ai_agent_repos.md)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Superpowers](https://github.com/obra/superpowers)
- [Context7](https://github.com/upstash/context7)
- [Browser Use](https://github.com/browser-use/browser-use)
- [Google Workspace CLI](https://github.com/googleworkspace/cli)
- [mem0](https://github.com/mem0ai/mem0)
- [DeerFlow](https://github.com/bytedance/deer-flow)
- [Claude Cookbooks](https://github.com/anthropics/claude-cookbooks)
- [LocalAI](https://github.com/mudler/LocalAI)
- [llmfit](https://github.com/AlexsJones/llmfit)
- [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm)
- [OpenBB](https://github.com/OpenBB-finance/OpenBB)
- [ClawRouter](https://github.com/BlockRunAI/ClawRouter)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
