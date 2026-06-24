# ClawRouter

## What it is
ClawRouter is an open-source (MIT), agent-native smart LLM router designed for autonomous workflows. It provides a local proxy that analyzes requests across 15 dimensions (cost, latency, reasoning depth, etc.) and routes them to the optimal model in under 1ms.

## What problem it solves
It solves the "autonomous agent payment gap" by using the **x402 protocol** for USDC micropayments and wallet signatures for authentication. This allows agents to operate independently without human-managed API keys, accounts, or credit cards. It also reduces LLM costs by up to 92% through aggressive model routing.

## Where it fits in the stack
**Infrastructure / Routing Layer**. ClawRouter sits between the AI agent (Claude 4.8, GPT-5.5) and model providers (Anthropic, OpenAI, Google, NVIDIA, etc.), acting as a smart, payment-integrated proxy.

## Typical use cases
- **Autonomous Agent Ops**: Powering agents that need to pay for their own inference via on-chain USDC.
- **Cost-Optimized Coding**: Routing simple code edits to free models (e.g., DeepSeek V4 Flash) while using Claude Opus 4.8 for complex architecture.
- **Multi-Modal Orchestration**: Seamlessly switching between specialized models for text, vision, image generation, and voice calls.
- **Agentic Infrastructure**: Providing a local, <1ms routing layer for high-volume agent fleets.

## Strengths
- **Agent-First Auth**: Uses wallet signatures instead of API keys, making it truly native to autonomous entities.
- **Cost Efficiency**: Access to 6+ free models (NVIDIA-hosted) and smart routing that targets 90%+ savings.
- **Local & Fast**: Routing logic runs entirely locally with sub-1ms latency and no external routing dependencies.
- **Rich Ecosystem**: Supports 55+ models and integrates features like image generation, video generation, and AI-powered voice calls.
- **Non-Custodial Payments**: Agents pay per-request using USDC via x402 directly from their own local wallets.

## Limitations
- **Ecosystem Focus**: While standalone, its primary integrations are centered around OpenClaw and agent-native environments.
- **Payment Learning Curve**: Requires understanding of USDC micropayments and the x402 protocol for paid tiers.
- **Model Bias**: Routing logic is optimized for agentic workloads, which may differ from general chat requirements.

## When to use it
- When building autonomous agents that need to manage their own inference costs and payments.
- When model routing is a first-class operational concern for reducing agentic overhead.
- In OpenClaw-heavy stacks where plugin integration provides advanced UI features.

## When not to use it
- When a simpler, provider-agnostic router like [LiteLLM](../../services/litellm.md) is sufficient and payments aren't a priority.
- When you prefer centralized billing and account management over per-request USDC settlement.
- For purely human-driven chat applications where standard API key management is preferred.

## Getting started

To set up ClawRouter in June 2026:

1. **Installation**:
   ```bash
   npx @blockrun/clawrouter
   ```
2. **Wallet Setup**: On first run, a BIP-39 mnemonic and wallet (Base/Solana) are generated. Your address is printed to the console.
3. **Funding**: Optional. Skip for the free tier (6 models). For paid models, send USDC on the Base or Solana network to your address.
4. **Integration**: Point your client (Cursor, Continue, or OpenAI SDK) to `http://localhost:8402/v1/`.

## CLI examples

### Diagnostic Check
Run the "doctor" to verify system, wallet, and network status with AI-powered analysis:

```bash
npx @blockrun/clawrouter doctor
```

### Managing Models
Manually exclude or include models from the smart routing logic:

```bash
# Block expensive models
clawrouter exclude add gpt-5.4-pro
# Verify current exclusions
clawrouter exclude
```

### Phone & Voice Ops
Manage wallet-owned phone numbers for AI voice calls:

```bash
# Buy a US number for agentic calls
clawrouter phone numbers buy US --area-code 415
# List active numbers and expiry
clawrouter phone numbers list
```

## API examples

### Smart Routing Call
The default `blockrun/auto` model automatically selects the best model for each request:

```python
from openai import OpenAI

# ClawRouter local proxy
client = OpenAI(base_url="http://localhost:8402/v1", api_key="x402")

response = client.chat.completions.create(
    model="blockrun/auto",
    messages=[{"role": "user", "content": "Analyze this repo architecture."}]
)
```

### Image Generation (Asynchronous)
Generate high-fidelity images using specialized agent tools:

```bash
curl -X POST http://localhost:8402/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "flux",
    "prompt": "A futuristic city at sunset, cinematic lighting",
    "size": "1024x1024"
  }'
```

### AI-Powered Voice Call
Initiate a real outbound phone call with automated x402 settlement:

```bash
curl -X POST http://localhost:8402/v1/voice/call \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+14155552671",
    "task": "Confirm the 3pm Thursday meeting.",
    "max_duration": 5
  }'
```

## Example company use cases
- **High-volume agent ops**: route routine OpenClaw actions to cheaper models while reserving premium models for harder steps.
- **Multi-model specialization**: use one model for browsing, another for code generation, and another for summarization.
- **Cost-aware experimentation**: compare routing strategies before standardizing a production model mix.

## Selection comments
- Use **ClawRouter** when routing is part of the agent architecture itself.
- Use **LiteLLM** for broader, provider-agnostic routing across many application teams.
- Use **OpenRouter** when you want one billing and access layer, not a deeper routing control plane.

## Related tools / concepts
- [OpenClaw](../development_ops/openclaw.md)
- [LiteLLM](../../services/litellm.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Claude 4.8](../providers/anthropic.md)
- [GPT-5.5](../ai_knowledge/openai.md)
- [Llama 4 Maverick](../providers/nvidia.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Aider](../development_ops/aider.md)
- [Zed](../development_ops/zed.md)

## Sources / References
- [GitHub Repository](https://github.com/BlockRunAI/ClawRouter)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
