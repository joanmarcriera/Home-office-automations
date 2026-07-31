# big-AGI

## What it is
big-AGI is a local-first, vendor-neutral, professional AI workspace and multi-model orchestrator. Built for researchers, engineers, and power users, it provides a high-density, zero-latency frontend to interact with multiple models simultaneously. As of late October / November 2026, it fully integrates specialized multi-model merge pipelines ("Beam 2"), persistent code-execution sandboxes ("Anthropic Containers"), and Model Context Protocol (MCP 3.1) servers.

## What problem it solves
It resolves the "single-model bubble" and "interface friction" inherent in proprietary LLM interfaces. Rather than switching tabs or copying prompts back and forth to compare outputs, big-AGI allows users to query multiple frontier models (Claude 5.1, GPT-5.5, Gemini 4.0) at once, merge their insights, and execute code within a persistent, stateful environment without vendor lock-in.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Professional AI Workspace. It serves as a high-performance, local-first "control bridge" between the user's browser, remote API providers (like Anthropic, OpenAI, or OpenRouter), and local inference runtimes (like Ollama or vLLM).

## Typical use cases
- **Multi-Model Synthesis (Beam 2)**: Querying multiple frontier and local models in parallel, running automated synthesis loops, and merging the absolute best parts of each response.
- **Stateful Sandbox Execution**: Writing, testing, and debugging code inside persistent bash containers ("Anthropic Containers") that maintain local files across chat turns.
- **Unified Tool Handshakes**: Linking browser sessions with external databases, filesystem contexts, and custom APIs via native MCP 3.1 integrations.
- **Deep Technical Research**: Launching deeply detailed, multi-step web searches with accurate cite attribution and automatic, fully resumable checkpoint sessions.

## Strengths
- **Instant Response UI**: Highly optimized browser interface utilizing Next.js and React that handles markdown, LaTeX, and live Mermaid diagrams without lag.
- **Beam 2 Merge Engine**: Fully customizable, program-based multi-model reasoning that allows users to adjust candidate models and voting weights dynamically.
- **Stateful Sandboxing**: Out-of-the-box persistent browser sandboxes for safe execution of Python and Shell scripts.
- **Zero Lock-In Provider Support**: Direct connections to 20+ vendors and local inference servers, with auto-detection of features like native reasoning effort control.
- **Local-First & Secure**: User credentials and API keys are stored locally in the browser’s localStorage or encrypted via custom transit protocols.

## Limitations
- **High Cognitive Load**: The high-density, feature-packed UI can be overwhelming for casual users who only need a simple, conversational chat interface.
- **Browser-Bound Storage**: Relying entirely on browser local storage means configurations can be lost if browser caches are wiped without manual exports.

## When to use it
- When your technical workflow requires verifying critical decisions or complex code solutions across multiple distinct model providers.
- If you need a zero-friction, self-hostable workspace with persistent bash and file capabilities built right into the chat.
- When you want complete, granular control over sampling parameters, temperature, system prompts, and tool calling at the model level.

## When not to use it
- For quick, casual conversations where a simple mobile app or a lightweight desktop client like Jan.ai would suffice.
- In enterprise environments that forbid browser-direct connections to external API gateways without central administrative proxies.

## Getting started

### 1. Instant Web Access
You can run big-AGI instantly in your browser by visiting the official, local-first web app at [app.big-agi.com](https://app.big-agi.com/) and configuring your API keys.

### 2. Self-Hosted (Docker)
To deploy a persistent, self-hosted container instance of big-AGI on your local network:

```bash
docker run -d \
  --name big-agi \
  -p 3000:3000 \
  -e NEXT_PUBLIC_SHOW_BENCHMARKS=false \
  ghcr.io/enricoros/big-agi
```

After deployment, navigate to `http://localhost:3000` to access your workspace.

## CLI examples
While big-AGI is fundamentally a graphical web application, its workspace templates and deployments are managed via command-line utilities.

```bash
# Clone the repository and run big-AGI locally in development mode
git clone https://github.com/enricoros/big-AGI.git && cd big-AGI
npm install && npm run dev

# Update your running Docker container to the latest late-2026 build
docker pull ghcr.io/enricoros/big-agi && docker restart big-agi

# Deploy the workspace to a private Vercel project
npx vercel --prod
```

## API examples
Below is a complete Python program utilizing `pydantic` (v2) to define and validate a "Beam 2" model combination request configuration for big-AGI's backend orchestrators.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field

class ModelWeight(BaseModel):
    model_id: str = Field(..., alias="modelId", description="The exact API name of the target model")
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="The combination weight for synthesis")

class Beam2Config(BaseModel):
    synthesis_mode: str = Field("cot-merge", alias="synthesisMode")
    candidate_models: List[ModelWeight] = Field(..., alias="candidateModels")
    max_tokens: int = Field(2048, alias="maxTokens")
    temperature: float = Field(0.3, ge=0.0, le=2.0)
    system_instruction: Optional[str] = Field(None, alias="systemInstruction")

async def test_beam_merge_validation():
    # Simulated payload matching big-AGI's internal state structures
    raw_payload = {
        "synthesisMode": "majority-consensus-cot",
        "candidateModels": [
            {"modelId": "anthropic/claude-5.1-sonnet", "weight": 1.0},
            {"modelId": "openai/gpt-5.5-preview", "weight": 0.8},
            {"modelId": "google/gemini-4.0-pro", "weight": 0.6}
        ],
        "maxTokens": 4096,
        "temperature": 0.2,
        "systemInstruction": "Synthesize the code and ensure all race conditions are handled."
    }

    # Validate utilizing Pydantic v2 features
    validated_beam = Beam2Config.model_validate(raw_payload)
    print("Beam 2 Configuration successfully validated.")
    print(f"Active Synthesis Mode: {validated_beam.synthesis_mode}")
    print(f"Valid Candidates Count: {len(validated_beam.candidate_models)}")
    for candidate in validated_beam.candidate_models:
        print(f"  - {candidate.model_id} (Weight: {candidate.weight})")

if __name__ == "__main__":
    asyncio.run(test_beam_merge_validation())
```

## Related tools / concepts
- [LobeHub](lobehub.md) — High-quality multi-agent visual dashboard.
- [OpenRouter](openrouter.md) — Recommended API aggregator and router for big-AGI deployments.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard standard enabling local tools in browser-chats.
- [LiteLLM](../../services/litellm.md) — Local server interface for model load balancing and cost monitoring.
- [AnythingLLM](../ai_knowledge/anythingllm.md) — Alternative workspace focused on local document RAG.
- [Claude Code](../development_ops/claude-code.md) — Command-line agent that compliments visual research workspaces.

## Sources / references
- [big-AGI Official Website](https://big-agi.com/)
- [big-AGI GitHub Repository](https://github.com/enricoros/big-AGI)
- [big-AGI 2026 Core Release & Beam 2 Changelog](https://big-agi.com/docs/changelog)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
