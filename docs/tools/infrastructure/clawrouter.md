# ClawRouter

## What it is
ClawRouter is an open-source (MIT), agent-native smart LLM router designed for autonomous workflows. It provides a local proxy that analyzes incoming inference requests across 15 dimensions (cost, latency, reasoning depth, token context size, privacy level, domain alignment, etc.) and routes them to the optimal backend model in under 1ms.

## What problem it solves
It solves the "autonomous agent payment gap" by leveraging the **x402 protocol** for USDC micropayments and local wallet cryptographic signatures for authentication. This allows autonomous AI agents to operate independently without human-managed API keys, corporate credit cards, or manual account provisioning. It also reduces aggregate LLM inference costs by up to 92% through dynamic model routing across frontier models (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**) and local open-weights inference servers (vLLM, TGI, Ollama).

## Architecture & System Flow

```
+-----------------------------------------------------------------------------------+
|                              Autonomous Agent Fleet                               |
|               (FastMCP 3.1 Tools / OpenClaw / Cursor / Auto-Agents)               |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v  HTTP / REST (OpenAI-compatible)
+-----------------------------------------+-----------------------------------------+
|                                    ClawRouter                                     |
|                                                                                   |
|  +-----------------------------------+   +-------------------------------------+  |
|  |     15-Dimension Routing Engine   |   |        x402 Micropayment Engine     |  |
|  |  - Cost & Token Budget Guardrails |   |  - On-chain USDC Settlement          |  |
|  |  - Latency SLA Thresholds (<1500ms)|   |  - Base / Solana Non-Custodial Wallet|  |
|  |  - Reasoning Depth Classifier     |   |  - Cryptographic Signature Verification|
|  +-----------------+-----------------+   +------------------+------------------+  |
|                    |                                        |                     |
|                    +--------------------+-------------------+                     |
|                                         |                                         |
+-----------------------------------------+-----------------------------------------+
                                          | <1ms Routing Overhead
            +-----------------------------+-----------------------------+
            |                             |                             |
            v                             v                             v
+-----------------------+     +-----------------------+     +-----------------------+
|  Frontier Cloud APIs  |     |   Free Hosted Models  |     | Open-Weights Clusters |
| (Claude 5.6, GPT-5.6, |     |  (NVIDIA-hosted free  |     |  (vLLM, TGI, Ollama,  |
|  Gemini 4.0 Ultra)    |     |   inference endpoints)|     |   Local Local GPUs)   |
+-----------------------+     +-----------------------+     +-----------------------+
```

## Where it fits in the stack
**Infrastructure / Routing Layer**. ClawRouter sits directly between autonomous AI agents (running via FastMCP 3.1, OpenClaw, or custom SDKs) and upstream LLM providers (Anthropic, OpenAI, Google, NVIDIA, vLLM), acting as a smart, payment-integrated proxy.

## Feature Comparison Matrix

| Feature / Dimension | ClawRouter | LiteLLM | OpenRouter | vLLM Proxy |
| :--- | :--- | :--- | :--- | :--- |
| **Authentication** | On-chain Wallet Signature (x402) | Static API Keys / OAuth | Static API Key / Pre-funded | Bearer Token / None |
| **Micropayments** | Native USDC (Base/Solana per request) | External Billing / Enterprise | Credit Card Pre-pay | Self-hosted Infrastructure |
| **Routing Latency** | <1ms Local Overhead | ~5–15ms Proxy Overhead | ~20–50ms Cloud Overhead | ~2–5ms Local Overhead |
| **Free Model Access** | 6+ Free Hosted Tier Endpoints | Requires Own Keys | Limited Free Tiers | Local GPU Resources |
| **Agent Native** | Built for Autonomous Workflows | Developer / Enterprise App Focus | Consumer / App Developer Focus | Inference Engine Operator Focus |
| **FastMCP 3.1 Support** | Native Protocol Integration | Custom Adapter Required | Custom Adapter Required | OpenAI Schema Wrapper |

## Typical use cases
- **Autonomous Agent Ops**: Powering agents that need to pay for their own inference via on-chain USDC without human intervention.
- **Cost-Optimized Coding**: Routing simple syntax checks to free open-weights models while escalating complex architectural queries to frontier models.
- **Multi-Modal Orchestration**: Seamlessly dispatching text, vision, image generation, and audio requests to specialized model backends.
- **Agentic Infrastructure**: Providing a local, sub-millisecond routing layer for high-volume agent fleets and FastMCP 3.1 tools.

## Strengths
- **Agent-First Auth**: Uses wallet cryptographic signatures instead of hardcoded API keys, ensuring non-custodial agent sovereignty.
- **Cost Efficiency**: Built-in access to free hosted endpoints and aggressive routing rules that target up to 90%+ cost reductions.
- **Local & Fast**: The decision matrix executes locally with sub-1ms routing overhead and zero network lookup delays.
- **Rich Ecosystem**: Supports over 55 backend models, image generation workflows, video processing, and AI voice calls.
- **Non-Custodial Settlement**: Agents pay per-request using USDC via x402 directly from local wallet keys.

## Limitations
- **Ecosystem Focus**: Primary integrations are tailored for OpenClaw, FastMCP 3.1, and agentic environments.
- **Payment Learning Curve**: Requires setting up USDC micropayments and configuring the x402 protocol for paid model tiers.
- **Model Bias**: Routing scoring heuristics are heavily optimized for autonomous, tool-calling agent workloads.
- **Local Resource Usage**: The local wallet daemon and routing engine require a lightweight, persistent background process.

## When to use it
- When building autonomous agents that need to manage their own inference budgets and per-request payments.
- When model routing latency and cost optimization are critical operational requirements for agentic fleets.
- In OpenClaw and FastMCP 3.1 stacks where native plugin and tool integration simplifies deployment.

## When not to use it
- When a simpler, centralized router like [LiteLLM](../../services/litellm.md) meets your needs and on-chain payment is unnecessary.
- When enterprise compliance requires traditional centralized invoicing and credit card billing.
- For purely human-driven interactive chat applications where standard API keys are already managed.

## Getting started

To set up ClawRouter in January 2027:

1. **Installation**:
   ```bash
   npx @blockrun/clawrouter
   ```
2. **Wallet Setup**: On first run, a BIP-39 mnemonic and wallet (Base/Solana) are generated automatically. Your address is printed to stdout.
3. **Funding**: Optional for free models (6 free models included). For paid frontier models, deposit USDC on Base or Solana.
4. **Integration**: Point your OpenAI SDK, Cursor, or FastMCP client to `http://localhost:8402/v1/`.

## CLI examples

### Diagnostic Check
Run the diagnostic suite to verify routing engine health, wallet balances, and upstream model availability:

```bash
npx @blockrun/clawrouter doctor
```

### Managing Model Routing Rules
Exclude expensive or latency-sensitive models from the auto-router evaluation pool:

```bash
# Exclude specific high-cost models
clawrouter exclude add gpt-5.5-pro

# List active exclusions
clawrouter exclude
```

### Phone & Voice Operations
Manage wallet-owned virtual phone numbers for automated AI outbound and inbound calls:

```bash
# Purchase a US phone number for agentic calls
clawrouter phone numbers buy US --area-code 415

# List active numbers and expiration dates
clawrouter phone numbers list
```

## API examples

### Smart Routing Call
The default `blockrun/auto` alias evaluates request parameters and dispatches to the optimal backend:

```python
from openai import OpenAI

# ClawRouter local proxy running at default port
client = OpenAI(base_url="http://localhost:8402/v1", api_key="x402")

response = client.chat.completions.create(
    model="blockrun/auto",
    messages=[{"role": "user", "content": "Analyze repo architecture and outline refactoring targets."}]
)
print(response.choices[0].message.content)
```

### FastMCP 3.1 Integration Pattern
Register ClawRouter as an MCP tool server for agentic frameworks:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
import requests

mcp = FastMCP("clawrouter-mcp-server")

class RouteInferenceInput(BaseModel):
    prompt: str = Field(description="The user prompt or query to route")
    max_cost_usd: float = Field(default=0.02, description="Maximum USD budget for this single request")
    required_latency_ms: int = Field(default=2000, description="Latency SLA threshold in milliseconds")

class RouteInferenceOutput(BaseModel):
    selected_model: str
    response_text: str
    cost_usd: float
    latency_ms: float

@mcp.tool()
def route_agent_request(input_data: RouteInferenceInput) -> RouteInferenceOutput:
    """Routes an agent prompt through ClawRouter using x402 micropayments and custom budget SLA."""
    url = "http://localhost:8402/v1/chat/completions"
    headers = {"Authorization": "Bearer x402", "Content-Type": "application/json"}
    payload = {
        "model": "blockrun/auto",
        "messages": [{"role": "user", "content": input_data.prompt}],
        "metadata": {
            "max_cost_limit_usd": input_data.max_cost_usd,
            "latency_sla_ms": input_data.required_latency_ms
        }
    }
    res = requests.post(url, json=payload, headers=headers, timeout=15)
    res.raise_for_status()
    data = res.json()

    return RouteInferenceOutput(
        selected_model=data.get("model", "unknown"),
        response_text=data["choices"][0]["message"]["content"],
        cost_usd=data.get("usage", {}).get("estimated_cost_usd", 0.0),
        latency_ms=res.elapsed.total_seconds() * 1000
    )

if __name__ == "__main__":
    mcp.run()
```

### Programmatic Python Routing & Health Verification (Pydantic v2)
Enforce budget controls and latency SLAs on self-directed agent workflows:

```python
import sys
import time
import requests
from pydantic import BaseModel, Field
from typing import Optional

class RoutingMetadata(BaseModel):
    max_cost_limit_usd: float = Field(default=0.05, ge=0.0, description="Max USD budget per request")
    latency_sla_ms: int = Field(default=1500, ge=100, description="Target max latency in milliseconds")

class ChatMessage(BaseModel):
    role: str
    content: str

class ClawRouterRequest(BaseModel):
    model: str = Field(default="blockrun/auto")
    messages: list[ChatMessage]
    metadata: RoutingMetadata = Field(default_factory=RoutingMetadata)

class UsageInfo(BaseModel):
    estimated_cost_usd: float = Field(default=0.0)

class ChoiceMessage(BaseModel):
    content: str

class Choice(BaseModel):
    message: ChoiceMessage

class ClawRouterResponse(BaseModel):
    model: str
    choices: list[Choice]
    usage: Optional[UsageInfo] = None

def check_clawrouter_health(base_url: str = "http://localhost:8402/v1") -> bool:
    try:
        response = requests.get(f"{base_url}/status", timeout=3)
        if response.status_code == 200:
            status_data = response.json()
            balance = status_data.get("wallet", {}).get("usdc_balance", 0.0)
            network = status_data.get("wallet", {}).get("network", "unknown")
            print(f"ClawRouter is LIVE. Network: {network}. Wallet Balance: {balance} USDC.")
            return True
        return False
    except requests.exceptions.RequestException:
        print("ClawRouter offline or unreachable.")
        return False

def route_with_clawrouter(prompt: str, base_url: str = "http://localhost:8402/v1") -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer x402"
    }

    req = ClawRouterRequest(
        messages=[ChatMessage(role="user", content=prompt)],
        metadata=RoutingMetadata(max_cost_limit_usd=0.05, latency_sla_ms=1500)
    )

    try:
        start_time = time.time()
        res = requests.post(f"{base_url}/chat/completions", json=req.model_dump(), headers=headers, timeout=10)
        elapsed = time.time() - start_time

        if res.status_code == 200:
            data = ClawRouterResponse.model_validate(res.json())
            completion = data.choices[0].message.content
            cost = data.usage.estimated_cost_usd if data.usage else 0.0
            print(f"Routed to '{data.model}' in {elapsed:.3f}s. Cost: {cost} USDC.")
            return completion
        else:
            print(f"Routing failed: {res.status_code} - {res.text}")
            return ""
    except Exception as e:
        print(f"Routing error: {e}")
        return ""

if __name__ == "__main__":
    if check_clawrouter_health():
        completion = route_with_clawrouter("Draft a python script to calculate Fibonacci series.")
        if completion:
            print(f"Response: {completion[:100]}...")
    else:
        print("Running fallback diagnostics. Ensure 'npx @blockrun/clawrouter' is running locally.")
```

## Related tools / concepts
- [OpenClaw](../development_ops/openclaw.md)
- [LiteLLM](../../services/litellm.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Claude 5.6](../providers/anthropic.md)
- [GPT-5.6](../ai_knowledge/openai.md)
- [Llama 4 Maverick](../providers/nvidia.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Aider](../development_ops/aider.md)
- [Zed](../development_ops/zed.md)

## Sources / References
- [GitHub Repository](https://github.com/BlockRunAI/ClawRouter)
- [x402 Protocol Specification](https://x402.org)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
