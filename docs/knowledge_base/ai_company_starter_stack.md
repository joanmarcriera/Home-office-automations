# AI Company Starter Stack

## What it is
The AI Company Starter Stack is an opinionated selection of tools and architectural patterns designed to turn a traditional business into an AI-native organization. It provides a curated list of "defaults" across various layers—from web surfaces and agent operating models to workflow control planes and local inference options—enabling teams to build operating leverage rather than just side experiments.

## What problem it solves
Most organizations struggle with "tool sprawl" when adopting AI, often implementing fragmented solutions that don't communicate or scale. This starter stack solves that by providing a unified operating system where [n8n](../services/n8n.md) coordinates workflows, [Claude Skills](../tools/agents/claude-skills-ecosystem.md) package procedures, and [mem0](../tools/agents/mem0.md) preserves context. It focuses on the "smallest stack" that provides maximum leverage across product, operations, and research, fully utilizing SOTA early-2027 frontier models (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, Qwen 3.6 VL).

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
- **State-of-the-Art Integration**: Fully supports Model Context Protocol (MCP 3.1) Task Protocol specifications for distributed agent orchestration and long-running context.

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

## CLI examples
```bash
# Initialize a new MCP 3.1-based project within the stack
mcp init my-agentic-workflow --version 3.1

# Deploy an MCP 3.1 server with native Task Protocol capabilities
mcp dev run my-agentic-workflow --port 8080

# Use Google Workspace CLI to list company documents for the agent
gw drive list --query "folder:'Company Strategy'"
```

## API examples
The following snippet demonstrates how to define a "Skill" and leverage the Model Context Protocol (MCP 3.1) Task Protocol with strict **Pydantic v2** validation within the starter stack:

```python
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from mcp import Client, TaskProtocol

# Define Pydantic v2 models for configuring company skills and task pipelines
class CompanyKnowledgeSearch(BaseModel):
    """Search for internal company knowledge across Docs and AnythingLLM."""
    query: str = Field(..., min_length=2, description="The search query for company knowledge.")
    depth: int = Field(default=3, ge=1, le=5, description="The depth of the search results hierarchy.")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Custom document category filters")

class StackTaskConfig(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the orchestration task")
    instruction: str = Field(..., description="Objective instructions for the execution engine")
    model_routing: str = Field(default="claude-5.1", description="Standard router model target")

# Standard MCP 3.1 Task Protocol registration
client = Client(endpoint="http://localhost:8080")
task_proto = TaskProtocol(client)

async def run_analysis():
    # Define and validate search parameters
    search_payload = {
        "query": "FastMCP 3.1 integration parameters",
        "depth": 4,
        "filters": {"category": "infrastructure"}
    }

    try:
        validated_search = CompanyKnowledgeSearch.model_validate(search_payload)

        # Build task configuration model and validate
        task_payload = {
            "name": "Knowledge Synthesis",
            "instruction": f"Synthesize internal knowledge base on {validated_search.query} utilizing Qwen 3.6 VL and Claude 5.6",
            "model_routing": "claude-5.6"
        }
        validated_task_cfg = StackTaskConfig.model_validate(task_payload)

        # Spawning a stateful research task using validated payload via MCP 3.1 Task Protocol
        task = await task_proto.create_task(
            name=validated_task_cfg.name,
            instruction=validated_task_cfg.instruction
        )
        print(f"Successfully initialized validated MCP 3.1 Task {task.id} with status: {task.status}")

    except ValidationError as e:
        print(f"Starter Stack Task configuration validation failed: {e}")
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
- Last reviewed: 2027-01-07
- Confidence: high
