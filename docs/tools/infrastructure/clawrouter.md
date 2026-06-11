# ClawRouter

## What it is
ClawRouter is an MIT-licensed, agent-native LLM router developed by BlockRunAI, specifically designed for [OpenClaw](../development_ops/openclaw.md) and other agentic workflows. It provides a high-performance routing layer that optimizes model calls based on cost, latency, and reasoning requirements in real-time.

## What problem it solves
It addresses the complexity of managing multi-model agent workloads. By providing sub-1ms routing decisions, ClawRouter ensures that agents like **Claude 4.8** are used for high-stakes reasoning while simpler tasks are routed to cost-effective models like **GPT-5.5-mini** or **Llama 4 Maverick (8B)**, all while supporting the x402 protocol for automated USDC micropayments.

## Where it fits in the stack
**Infrastructure / Routing Layer**. It sits between the agent orchestration layer ([OpenClaw](../development_ops/openclaw.md)) and the model providers, serving as a smart gateway for all LLM traffic.

## Typical use cases
- **Cost-Optimized Agent Ops**: Automatically routing routine tool calls to cheaper models.
- **Low-Latency Interactions**: Selecting the fastest available provider for real-time chat.
- **Model Specialization**: Routing coding tasks to **Claude 4.8** and web search tasks to **GPT-5.5**.
- **Automated Micropayments**: Using the x402 protocol to handle per-request billing in USDC.

## Strengths
- **Sub-1ms Overhead**: Minimal latency impact on the inference pipeline.
- **Agent-Native Design**: Built with autonomous agent patterns in mind, unlike generic API proxies.
- **Micropayment Support**: Native integration with the x402 protocol for decentralized billing.
- **Protocol Compatibility**: Full support for the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).

## Limitations
- **Ecosystem Focus**: Best optimized for OpenClaw; may require extra configuration for other frameworks.
- **Complexity**: Requires careful rule definitions to avoid suboptimal model selection.
- **Niche Protocol**: x402 support is powerful but requires specific wallet/payment setup.

## When to use it
- When building large-scale agent fleets that require fine-grained cost and performance control.
- When using **OpenClaw** as your primary agent runtime.
- If you need to implement automated, decentralized payments for AI inference.

## When not to use it
- For simple, single-model applications where a direct API call or [LiteLLM](../../services/litellm.md) is sufficient.
- If you do not require specialized routing or micropayment features.

## Getting started

### Installation (Binary)
Download the latest release from the BlockRunAI repository:

```bash
curl -L https://github.com/BlockRunAI/ClawRouter/releases/latest/download/clawrouter -o /usr/local/bin/clawrouter
chmod +x /usr/local/bin/clawrouter
```

### Basic Configuration
Create a `clawrouter.yml` file to define your routing rules:

```yaml
# clawrouter.yml
routing_rules:
  - condition: "intent == 'coding'"
    target: "anthropic/claude-4-8-opus"
  - condition: "intent == 'triage'"
    target: "openai/gpt-5-5-mini"
  - default: "meta/llama-4-maverick-70b"

payment:
  protocol: "x402"
  wallet_address: "0x..."
```

## CLI examples

### 1. Starting the Router
Start the ClawRouter service with a specific configuration:
```bash
clawrouter start --config ./clawrouter.yml --port 8989
```

### 2. Validating Rules
Test your routing logic without sending actual requests:
```bash
clawrouter validate --rule "intent == 'coding'"
```

### 3. Monitoring Traffic
View real-time routing statistics and costs:
```bash
clawrouter stats --live
```

## API examples

### Simple Routing Request
Send a request to the ClawRouter endpoint, which will then forward it to the optimal model:

```bash
curl -X POST http://localhost:8989/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "messages": [{"role": "user", "content": "Write a Python script to sort a list."}],
       "metadata": {"intent": "coding"}
     }'
```

### Programmatic Rule Update
Update routing weights dynamically via the management API:

```python
import requests

config_update = {
    "weights": {
        "anthropic": 0.7,
        "openai": 0.3
    }
}

requests.post("http://localhost:8989/admin/config", json=config_update)
```

## Related tools / concepts
- [OpenClaw](../development_ops/openclaw.md) — The primary agent runtime for ClawRouter.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Supported protocol for tool-calling.
- [LiteLLM](../../services/litellm.md) — General-purpose LLM router.
- [OpenRouter](../ai_knowledge/openrouter.md) — Unified API for model access.
- [Claude 4.8](../ai_knowledge/index.md) — High-end reasoning target.
- [Llama 4 Maverick](../ai_knowledge/index.md) — Cost-effective inference target.
- [Aider](../development_ops/aider.md) — Coding agent that can use ClawRouter.

## Sources / references
- [GitHub Repository](https://github.com/BlockRunAI/ClawRouter)
- [BlockRunAI Official Documentation](https://blockrun.ai/docs/clawrouter)
- [x402 Protocol Specification](https://x402.org/spec)

## Contribution Metadata
- Last reviewed: 2026-06-11
- Confidence: high
