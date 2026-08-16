# big-AGI

## What it is
big-AGI is a local-first, vendor-neutral, professional AI workspace and multi-model orchestrator. Designed for power users, researchers, and engineers, it provides a high-density, low-latency web interface to query and orchestrate multiple models simultaneously. By early January 2027, big-AGI features the **Beam 2** multi-model synthesis engine, stateful code-execution sandboxes, and native **FastMCP 3.1** protocol support.

## What problem it solves
It overcomes the limitations and interface friction of single-model web clients. Instead of manually copying prompts across separate browser tabs to compare outputs, big-AGI queries frontier models (Claude 5.1, GPT-5.5, Gemini 4.0 Pro) in parallel, merges their insights via customizable consensus pipelines, and executes generated code in persistent sandboxes.

## Where it fits in the stack
**AI Assistants & Knowledge / Professional AI Workspace**. It acts as a local-first control panel connecting the user's browser, remote API providers (OpenAI, Anthropic, OpenRouter), and self-hosted inference servers (Ollama, LM Studio, vLLM).

## Typical use cases
- **Multi-Model Synthesis (Beam 2)**: Querying multiple models simultaneously, applying automated reasoning synthesis, and merging the best components into a single response.
- **Stateful Sandbox Code Execution**: Running and debugging Python or Shell scripts within persistent, isolated containers.
- **FastMCP 3.1 Tool Integration**: Connecting browser sessions to local databases, file systems, and custom tools via FastMCP 3.1 endpoints.
- **Deep Technical Research**: Launching multi-step web searches with live citations, diagramming (Mermaid.js), and resumable session checkpoints.

## Strengths
- **Instant Response UI**: Highly optimized Next.js/React frontend handling markdown, LaTeX math, and live charts without UI lag.
- **Beam 2 Merge Engine**: Fully customizable, program-based multi-model reasoning and voting synthesis.
- **Persistent Code Sandboxing**: Built-in container support for safe, stateful execution of code scripts across chat turns.
- **Zero Lock-In Provider Support**: Direct connections to 20+ model providers and local endpoints with native reasoning effort controls.
- **Local-First Privacy**: API keys and session histories are stored locally in the browser or encrypted in transit.

## Limitations
- **High Information Density**: The feature-rich UI can have a learning curve for casual users seeking a basic chat client.
- **Browser-Bound Storage**: Relying on local browser storage requires periodic manual backup exports to prevent accidental cache loss.

## When to use it
- When verifying complex architectural decisions or debugging tricky code across multiple frontier models.
- When seeking a self-hostable workspace with persistent execution sandboxes and tool calling built into chat.
- When requiring granular control over sampling parameters, system prompts, and tool calling schemas.

## When not to use it
- For quick, lightweight conversational chats on mobile devices where simple apps suffice.
- In corporate environments that strictly forbid direct browser-to-API internet connections.

## Getting started

### 1. Web App Access
Access big-AGI directly in your web browser at [app.big-agi.com](https://app.big-agi.com/) and enter your API credentials.

### 2. Self-Hosted (Docker)
Deploy a persistent, self-hosted container instance on your local machine or server:

```bash
docker run -d \
  --name big-agi \
  -p 3000:3000 \
  -e NEXT_PUBLIC_SHOW_BENCHMARKS=false \
  ghcr.io/enricoros/big-agi
```

Open `http://localhost:3000` to access your self-hosted workspace.

## CLI examples

```bash
# Clone and run big-AGI locally in dev mode
git clone https://github.com/enricoros/big-AGI.git && cd big-AGI
npm install && npm run dev

# Update your Docker deployment to the latest build
docker pull ghcr.io/enricoros/big-agi && docker restart big-agi

# Deploy to a private Vercel project
npx vercel --prod
```

## API examples
### Python: Pydantic v2 Beam 2 Configuration Validator
```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field

class ModelWeight(BaseModel):
    model_id: str = Field(..., alias="modelId", description="Target model API identifier")
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Voting weight")

class Beam2Config(BaseModel):
    synthesis_mode: str = Field("cot-merge", alias="synthesisMode")
    candidate_models: List[ModelWeight] = Field(..., alias="candidateModels")
    max_tokens: int = Field(2048, alias="maxTokens")
    temperature: float = Field(0.3, ge=0.0, le=2.0)
    system_instruction: Optional[str] = Field(None, alias="systemInstruction")

async def test_beam_merge_validation():
    raw_payload = {
        "synthesisMode": "majority-consensus-cot",
        "candidateModels": [
            {"modelId": "anthropic/claude-5.1-sonnet", "weight": 1.0},
            {"modelId": "openai/gpt-5.5", "weight": 0.8},
            {"modelId": "google/gemini-4.0-pro", "weight": 0.7}
        ],
        "maxTokens": 4096,
        "temperature": 0.2,
        "systemInstruction": "Synthesize the response and verify race conditions."
    }

    validated_beam = Beam2Config.model_validate(raw_payload)
    print("Beam 2 Config Validated successfully.")
    print(f"Mode: {validated_beam.synthesis_mode}")
    print(f"Active Candidates: {len(validated_beam.candidate_models)}")

if __name__ == "__main__":
    asyncio.run(test_beam_merge_validation())
```

## Related tools / concepts
- [LobeHub](lobehub.md) — Visual multi-agent chat interface.
- [OpenRouter](openrouter.md) — Unified API aggregator for model routing.
- [FastMCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Open protocol for agent tools.
- [AnythingLLM](anythingllm.md) — RAG workspace for local documents.
- [Claude Code](../development_ops/claude-code.md) — CLI software engineering agent.

## Sources / references
- [big-AGI Official Site](https://big-agi.com/)
- [big-AGI GitHub Repository](https://github.com/enricoros/big-AGI)
- [big-AGI Release Documentation](https://big-agi.com/docs/changelog)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
