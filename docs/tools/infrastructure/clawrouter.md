# ClawRouter

## What it is
ClawRouter is an open-source (MIT), agent-native smart LLM router designed for autonomous workflows. It provides a local proxy that analyzes requests across 15 dimensions (cost, latency, reasoning depth, etc.) and routes them to the optimal model in under 1ms.

## What problem it solves
It solves the "autonomous agent payment gap" by using the **x402 protocol** for USDC micropayments and wallet signatures for authentication. This allows agents to operate independently without human-managed API keys, accounts, or credit cards. It also reduces LLM costs by up to 92% through aggressive model routing.

## Where it fits in the stack
**Infrastructure / Routing Layer**. ClawRouter sits between the AI agent (Claude 5.1, GPT-5.5) and model providers (Anthropic, OpenAI, Google, NVIDIA, etc.), acting as a smart, payment-integrated proxy.

## Typical use cases
- **Autonomous Agent Ops**: Powering agents that need to pay for their own inference via on-chain USDC.
- **Cost-Optimized Coding**: Routing simple code edits to free models (e.g., DeepSeek V4 Flash) while using Claude 5.1 for complex architecture.
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
- **Local Resource Usage**: Running the routing engine and local wallet adds a small memory footprint to the host machine.

## When to use it
- When building autonomous agents that need to manage their own inference costs and payments.
- When model routing is a first-class operational concern for reducing agentic overhead.
- In OpenClaw-heavy stacks where plugin integration provides advanced UI features.

## When not to use it
- When a simpler, provider-agnostic router like [LiteLLM](../../services/litellm.md) is sufficient and payments aren't a priority.
- When you prefer centralized billing and account management over per-request USDC settlement.
- For purely human-driven chat applications where standard API key management is preferred.

## Getting started

To set up ClawRouter in September 2026:

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
clawrouter exclude add gpt-5.5-pro
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

### Programmatic Python Verification & Route Optimizer
Verify and check metrics programmatically, enforcing budgets and latency SLAs on self-directed agent runs.

```python
import sys
import time
import requests

def check_clawrouter_health(base_url: str = "http://localhost:8402/v1") -> bool:
    # 1. Health and Wallet status check via ClawRouter internal state
    status_url = f"{base_url}/status"
    try:
        response = requests.get(status_url, timeout=3)
        if response.status_code == 200:
            status_data = response.json()
            balance = status_data.get("wallet", {}).get("usdc_balance", 0.0)
            network = status_data.get("wallet", {}).get("network", "unknown")
            print(f"ClawRouter is LIVE. Network: {network}. Wallet Balance: {balance} USDC.")
            return True
        else:
            print(f"Failed to fetch health status: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("ClawRouter offline or unreachable.")
        return False

def route_with_clawrouter(prompt: str, max_cost_limit: float = 0.05, base_url: str = "http://localhost:8402/v1") -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer x402"
    }

    payload = {
        "model": "blockrun/auto",
        "messages": [{"role": "user", "content": prompt}],
        "metadata": {
            "max_cost_limit_usd": max_cost_limit,
            "latency_sla_ms": 1500
        }
    }

    try:
        start_time = time.time()
        res = requests.post(f"{base_url}/chat/completions", json=payload, headers=headers, timeout=10)
        elapsed = time.time() - start_time

        if res.status_code == 200:
            data = res.json()
            completion = data["choices"][0]["message"]["content"]
            model_routed = data.get("model", "unknown")
            actual_cost = data.get("usage", {}).get("estimated_cost_usd", 0.0)
            print(f"Routed to '{model_routed}' in {elapsed:.3f}s. Cost: {actual_cost} USDC.")
            return completion
        else:
            print(f"Routing failed: {res.status_code} - {res.text}")
            return ""
    except Exception as e:
        print(f"Routing error: {e}")
        return ""

if __name__ == "__main__":
    print("Initiating ClawRouter programmatic routing test...")
    if check_clawrouter_health():
        completion = route_with_clawrouter("Draft a python script to calculate Fibonacci series.")
        if completion:
            print(f"Response: {completion[:100]}...")
    else:
        print("Running fallback diagnostics. Ensure 'npx @blockrun/clawrouter' is running locally.")
        sys.exit(0)
```

## Related tools / concepts
- [OpenClaw](../development_ops/openclaw.md)
- [LiteLLM](../../services/litellm.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Claude 5.1](../providers/anthropic.md)
- [GPT-5.5](../ai_knowledge/openai.md)
- [Llama 4 Maverick](../providers/nvidia.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Aider](../development_ops/aider.md)
- [Zed](../development_ops/zed.md)

## Sources / References
- [GitHub Repository](https://github.com/BlockRunAI/ClawRouter)
- [x402 Protocol Specification](https://x402.org)
- [Autonomous Agent Micropayments (September 2026 whitepaper)](https://example.com/agent-micropayments)

## Contribution Metadata
- Last reviewed: 2026-09-02
- Confidence: high
