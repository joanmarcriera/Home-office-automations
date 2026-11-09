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
|  Gemini 4.0 Ultra)    |     |   inference endpoints)|     |   Local GPUs)         |
+-----------------------+     +-----------------------+     +-----------------------+
```

### Mathematical Foundations of 15-Dimension Routing Optimization

ClawRouter models the request dispatch decision as a multi-objective Pareto optimization problem across $D = 15$ normalized operational metrics. Let $\mathcal{M} = \{m_1, m_2, \dots, m_K\}$ represent the set of candidate LLM endpoints, and let $\mathbf{x} = [x_1, x_2, \dots, x_{15}]^T \in \mathbb{R}^{15}$ represent the feature embedding vector of the incoming prompt (e.g., semantic token entropy, task domain, prompt length, required output depth, tool-calling complexity).

The multi-objective routing score for candidate model $m_k$ under prompt context $\mathbf{x}$ is defined by:

$$
S(m_k, \mathbf{x}) = \sum_{i=1}^{15} w_i \cdot \phi_i(m_k, x_i) - \lambda_{\text{cost}} \cdot \mathcal{C}(m_k, \tau_{\text{in}}, \tau_{\text{out}}) - \lambda_{\text{lat}} \cdot \max(0, \mathcal{L}(m_k) - \mathcal{L}_{\text{SLA}})
$$

Where:
- $w_i \ge 0, \sum_{i=1}^{15} w_i = 1$ are user-configured or agent-tuned dimensional weighting coefficients.
- $\phi_i(m_k, x_i) \in [0, 1]$ represents the normalized capability compatibility score between metric dimension $i$ and model $m_k$.
- $\mathcal{C}(m_k, \tau_{\text{in}}, \tau_{\text{out}}) = \tau_{\text{in}} \cdot c_{\text{in}}^{(k)} + \tau_{\text{out}} \cdot c_{\text{out}}^{(k)}$ computes the anticipated financial transaction cost in USD (denominated in micro-USDC) based on token estimates $\tau_{\text{in}}$ and $\tau_{\text{out}}$.
- $\mathcal{L}(m_k)$ denotes the rolling exponentially weighted moving average (EWMA) latency of model $m_k$, bounded against SLA threshold $\mathcal{L}_{\text{SLA}}$.
- $\lambda_{\text{cost}}$ and $\lambda_{\text{lat}}$ are penalty multipliers ensuring strict adherence to budget constraints and response deadlines.

The optimal target endpoint $m^* \in \mathcal{M}$ satisfies:

$$
m^* = \arg\max_{m_k \in \mathcal{M}_{\text{viable}}} S(m_k, \mathbf{x})
$$

Where $\mathcal{M}_{\text{viable}} = \{m_k \in \mathcal{M} \mid \mathcal{C}(m_k) \le B_{\text{max}} \land P(\mathcal{L}(m_k) \le \mathcal{L}_{\text{SLA}}) \ge 1 - \epsilon\}$.

### Cryptographic x402 Micropayment Verification Protocol

ClawRouter interfaces with the decentralized x402 payment scheme. When a target model API requires payment, ClawRouter signs an EIP-712 or Solana ed25519 payload encapsulating:

$$
\sigma_{\text{agent}} = \text{Sign}_{SK_{\text{agent}}}\Big(\text{Keccak-256}\big(\text{ChainID} \parallel \text{RouterNonce} \parallel \text{Amount}_{\mu\text{USDC}} \parallel \text{ExpiryTimestamp}\big)\Big)
$$

The settlement gateway verifies the signature and debits the agent's non-custodial smart wallet without requiring interactive human 2FA or credit card pre-authorizations, achieving off-chain micropayment authorization in $< 45\text{ms}$.

## Where it fits in the stack
**Infrastructure / Routing Layer**. ClawRouter sits directly between autonomous AI agents (running via FastMCP 3.1, OpenClaw, or custom SDKs) and upstream LLM providers (Anthropic, OpenAI, Google, NVIDIA, vLLM), acting as a smart, payment-integrated proxy.

## Feature Comparison Matrix

| Capability / Metric | ClawRouter | LiteLLM Proxy | OpenRouter | Portkey Gateway | Martian Router |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Routing Latency Overhead** | **< 1.0 ms** | 8.5 – 15.0 ms | 45 – 120 ms | 12 – 25 ms | 20 – 40 ms |
| **Micropayment Protocol** | **Native x402 USDC** | None (API Keys) | Fiat / Web UI Stored | Fiat / Stripe | Fiat / Credit Cards |
| **Self-Hosted Deployment** | **Yes (MIT / Docker)**| Yes (Enterprise/OS) | No (SaaS only) | Hybrid / SaaS | No (SaaS only) |
| **Multi-Dimension Scoring** | **15 Dimensions** | Simple Fallbacks | Model Rank / Price | Rule-based Routing | Complexity Classifier |
| **Frontier Model Routing** | Claude 5.6 / GPT-5.6 | Claude / GPT / DeepSeek| 100+ Cloud APIs | 50+ Cloud APIs | Proprietary Matrix |
| **FastMCP 3.1 Server Bridge**| **Native Built-in** | Community plugin | No | No | No |
| **Local vLLM / TGI Fallback** | **Instant Zero-Cost** | Manual load balancer | Paid fallback only | Custom endpoints | Cloud endpoints only |
| **Non-Custodial Wallet Auth**| **Yes (Base / Solana)**| No | No | No | No |

## Typical use cases
- **Autonomous Agent Fleet Automation**: Empowering multi-agent coding swarms (e.g., Aider, Claude Code, OpenClaw) to operate 24/7 without developer credit cards by funding agents with dedicated micro-wallets.
- **Cost-Optimized Production Pipelines**: Automatically steering simple code formatting and metadata tagging prompts to free local vLLM or NVIDIA NIM instances while routing deep architectural reasoning to Claude 5.6 or GPT-5.6.
- **Strict SLA Latency Guardrails**: Enforcing sub-second response times on real-time conversational agents by automatically dropping down to quantized local SLMs whenever cloud upstream APIs experience latency spikes.
- **Zero-Trust Enterprise LLM Gateway**: Enforcing strict per-request cryptographic spending limits and model access policies across heterogeneous developer teams and automated CI/CD runners.

## Strengths
- **Sub-Millisecond Overhead**: Written in high-performance asynchronous TypeScript / Rust core engine, imposing negligible delay on inference roundtrips.
- **Autonomous Financial Agency**: Enables fully independent software agents through non-custodial crypto wallet integration on Base, Solana, and Arbitrum.
- **Massive Cost Savings**: Consistently yields 75% to 92% token spend reductions via intelligent multi-tiered classification and local inference caching.
- **Open Standards Native**: Drop-in replacement for any client expecting standard OpenAI-compatible `/v1/chat/completions` REST contracts.

## Limitations
- **Wallet Liquidity Management**: Agents require initial USDC funding on supported L2 chains; zero-balance states trigger HTTP 402 errors unless free-tier fallback routing is configured.
- **Dynamic Price Drift**: Cloud provider token price changes require periodic router catalog updates or automated pricing sync daemon activation.
- **Initial Classification Overhead**: Highly specialized edge models may require prompt tuning or custom routing rule overrides to match domain-specific coding standards.

## When to use it
- When building self-directed agentic workflows that must pay for their own computing resources autonomously.
- For high-volume multi-agent environments where routing simple tasks to local open-weights models saves thousands of dollars monthly.
- When an engineering team needs a single unified endpoint aggregating Anthropic, OpenAI, Google, DeepSeek, and local vLLM nodes.
- To enforce automated failover, latency circuit-breakers, and token consumption caps across distributed microservices.

## When not to use it
- In minimal single-script utilities where direct API calls to a single provider satisfy simplicity requirements.
- For legacy enterprise applications where corporate procurement mandates centralized monthly invoicing and net-30 terms.
- For offline air-gapped workstations where no external cloud model routing or cryptocurrency payment rails are permitted.

## Getting started

### Installation
Launch ClawRouter directly using Node/npx:
```bash
npx @blockrun/clawrouter
```

Alternatively, install globally via npm:
```bash
npm install -g @blockrun/clawrouter
```

### Initial Configuration (`clawrouter.config.json`)
```json
{
  "server": {
    "port": 8402,
    "host": "0.0.0.0",
    "timeout_ms": 30000
  },
  "payment": {
    "network": "base-mainnet",
    "wallet_key_path": "/etc/clawrouter/wallet.key",
    "max_micropayment_usd": 0.10,
    "allow_free_tier_fallback": true
  },
  "routing": {
    "default_model": "blockrun/auto",
    "sla_latency_target_ms": 1200,
    "cost_weight": 0.45,
    "latency_weight": 0.35,
    "quality_weight": 0.20
  },
  "providers": {
    "anthropic": {"api_key_env": "ANTHROPIC_API_KEY"},
    "openai": {"api_key_env": "OPENAI_API_KEY"},
    "local_vllm": {"endpoint": "http://127.0.0.1:8000/v1"}
  }
}
```

### Hello-World Example
Query the ClawRouter local proxy using the OpenAI Python client:
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8402/v1", api_key="x402")

response = client.chat.completions.create(
    model="blockrun/auto",
    messages=[{"role": "user", "content": "Hello ClawRouter! Analyze system status."}]
)
print(response.choices[0].message.content)
```

## CLI examples

### 1. Run Diagnostic Health Check
Verify routing engine health, wallet balances, and upstream model endpoints:
```bash
npx @blockrun/clawrouter doctor
```

### 2. Exclude High-Cost Models
Manage model routing rules by adding exclusions to the auto-router evaluation pool:
```bash
clawrouter exclude add gpt-5.5-pro
```

### 3. List Model Exclusions & Active Policies
View all active model exclusions currently configured in ClawRouter:
```bash
clawrouter exclude list
```

### 4. Query Real-Time Wallet Balance & Nonce
Inspect current agent wallet balances and micropayment nonce on Base L2:
```bash
clawrouter wallet status --network base-mainnet
```

### 5. Inspect Provider Latency EWMA
Display current 15-minute rolling average response latencies across backends:
```bash
clawrouter stats latency --format table
```

## Production Deployment & System Infrastructure

### Multi-Service Docker Compose Architecture
Deploy ClawRouter alongside an in-memory Redis state cache, local Prometheus metrics exporter, and fallback vLLM inference worker:

```yaml
version: '3.8'

services:
  clawrouter:
    image: blockrun/clawrouter:v3.2.0
    container_name: clawrouter-core
    restart: unless-stopped
    ports:
      - "8402:8402"
      - "9092:9092" # Prometheus metrics
    environment:
      CLAWRTOUTER_PORT: "8402"
      X402_NETWORK: "base-mainnet"
      AGENT_WALLET_KEY_PATH: "/etc/clawrouter/wallet.key"
      REDIS_URL: "redis://clawrouter-cache:6379/0"
      PROMETHEUS_METRICS_PORT: "9092"
      LOG_LEVEL: "info"
    volumes:
      - ./config/clawrouter.config.json:/etc/clawrouter/config.json:ro
      - clawrouter_wallet_data:/etc/clawrouter/
    depends_on:
      - clawrouter-cache
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8402/v1/health"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 5s

  clawrouter-cache:
    image: redis:7.2-alpine
    container_name: clawrouter-cache
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  vllm-fallback:
    image: vllm/vllm-openai:latest
    container_name: clawrouter-vllm-fallback
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      MODEL: "Qwen/Qwen2.5-7B-Instruct"
      MAX_MODEL_LEN: "8192"
    ports:
      - "8000:8000"

volumes:
  clawrouter_wallet_data:
  redis_data:
```

### Hardened Systemd Service Unit (`clawrouter.service`)
For production bare-metal or cloud VM hosts requiring sandboxed execution, automatic crash restarts, and file descriptor limits:

```ini
[Unit]
Description=ClawRouter Agentic LLM Smart Proxy Daemon
Documentation=https://github.com/BlockRunAI/ClawRouter https://x402.org
After=network.target redis.service
Wants=network-online.target

[Service]
Type=simple
User=clawrouter
Group=clawrouter
WorkingDirectory=/opt/clawrouter
ExecStart=/usr/bin/clawrouter-daemon --config /etc/clawrouter/clawrouter.config.json
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=3s
Environment="NODE_ENV=production"
Environment="CLAWRTOUTER_HOME=/var/lib/clawrouter"
Environment="CLAWRTOUTER_PORT=8402"
Environment="X402_NETWORK=base-mainnet"
LimitNOFILE=65536
LimitNPROC=4096

# Security Hardening & Sandboxing
ProtectSystem=strict
ProtectHome=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
ReadWritePaths=/var/lib/clawrouter /var/log/clawrouter
PrivateTmp=true
NoNewPrivileges=true
MemoryDenyWriteExecute=true
CapabilityBoundingSet=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
```

## API examples

### FastMCP 3.1 Smart Routing Gateway Server
The following Python module implements a production-grade FastMCP 3.1 server exposing strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) to route multi-modal and reasoning prompts through ClawRouter:

```python
"""FastMCP 3.1 Smart Routing Gateway Server for ClawRouter.

Provides automated inference dispatch, cost budget validation, and x402 wallet
settlement status queries with strict Pydantic v2 data models.
"""

from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clawrouter-mcp-gateway")

# Initialize FastMCP 3.1 server
mcp = FastMCP(
    "ClawRouter Smart Gateway",
    instructions="Intelligent multi-tier LLM inference router with x402 micropayments."
)

# -----------------------------------------------------------------------------
# Strict Pydantic v2 Schemas
# -----------------------------------------------------------------------------

class ChatMessageInput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    role: Literal["system", "user", "assistant", "tool"] = Field(
        ..., description="Message author role"
    )
    content: str = Field(..., min_length=1, description="Message text content")

class RouteInferenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    messages: List[ChatMessageInput] = Field(
        ..., min_length=1, description="Sequential dialogue context messages"
    )
    preferred_tier: Literal["auto", "economy", "balanced", "frontier", "local-free"] = Field(
        default="auto", description="Target inference performance tier"
    )
    max_cost_usd: float = Field(
        default=0.05, ge=0.0, le=2.0, description="Upper bound USD budget per request"
    )
    latency_sla_ms: int = Field(
        default=2000, ge=100, le=60000, description="Maximum acceptable latency in ms"
    )
    temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="Sampling randomness parameter"
    )

class ModelUsageStats(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)

class RouteInferenceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    dispatched_model: str = Field(..., description="The concrete model chosen by the router")
    completion_text: str = Field(..., description="Generated model response text")
    latency_ms: float = Field(..., ge=0.0, description="Observed roundtrip execution latency")
    usage: ModelUsageStats = Field(..., description="Detailed token consumption and cost")
    micropayment_tx_hash: Optional[str] = Field(
        None, description="x402 Base/Solana settlement transaction hash if paid"
    )

class WalletStatusQuery(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    network: Literal["base-mainnet", "solana-mainnet", "arbitrum-one"] = Field(
        default="base-mainnet", description="Blockchain network to query"
    )

class WalletStatusResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    network: str
    usdc_balance: float
    is_operational: bool
    current_nonce: int

# -----------------------------------------------------------------------------
# FastMCP 3.1 Server Tools
# -----------------------------------------------------------------------------

@mcp.tool(name="route_inference_request")
def route_inference_request(req: RouteInferenceRequest) -> RouteInferenceResponse:
    """Dispatches dialogue requests through ClawRouter with SLA and cost budget protection."""
    url = "http://localhost:8402/v1/chat/completions"
    headers = {
        "Authorization": "Bearer x402",
        "Content-Type": "application/json"
    }

    payload = {
        "model": f"blockrun/{req.preferred_tier}",
        "messages": [m.model_dump() for m in req.messages],
        "temperature": req.temperature,
        "metadata": {
            "max_cost_limit_usd": req.max_cost_usd,
            "latency_sla_ms": req.latency_sla_ms
        }
    }

    t0 = time.time()
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=req.latency_sla_ms / 1000 + 5.0)
        res.raise_for_status()
        data = res.json()
        latency = (time.time() - t0) * 1000

        usage_raw = data.get("usage", {})
        usage_obj = ModelUsageStats(
            prompt_tokens=usage_raw.get("prompt_tokens", 0),
            completion_tokens=usage_raw.get("completion_tokens", 0),
            total_tokens=usage_raw.get("total_tokens", 0),
            estimated_cost_usd=usage_raw.get("estimated_cost_usd", 0.0)
        )

        return RouteInferenceResponse(
            dispatched_model=data.get("model", "unknown-fallback"),
            completion_text=data["choices"][0]["message"]["content"],
            latency_ms=round(latency, 2),
            usage=usage_obj,
            micropayment_tx_hash=data.get("x402_tx_hash")
        )
    except Exception as exc:
        logger.error(f"ClawRouter routing failure: {exc}")
        # Return graceful zero-cost fallback message
        return RouteInferenceResponse(
            dispatched_model="error-circuit-breaker",
            completion_text=f"Routing error encountered: {str(exc)}",
            latency_ms=round((time.time() - t0) * 1000, 2),
            usage=ModelUsageStats(),
            micropayment_tx_hash=None
        )

@mcp.tool(name="get_wallet_micropayment_status")
def get_wallet_micropayment_status(query: WalletStatusQuery) -> WalletStatusResponse:
    """Retrieves the autonomous agent's current on-chain USDC balance and execution readiness."""
    url = f"http://localhost:8402/v1/wallet/status?network={query.network}"
    try:
        res = requests.get(url, timeout=3.0)
        res.raise_for_status()
        data = res.json()
        balance = float(data.get("usdc_balance", 0.0))
        return WalletStatusResponse(
            network=query.network,
            usdc_balance=balance,
            is_operational=balance > 0.005,
            current_nonce=int(data.get("nonce", 0))
        )
    except Exception as exc:
        logger.warning(f"Failed to query wallet status: {exc}")
        return WalletStatusResponse(
            network=query.network,
            usdc_balance=0.0,
            is_operational=False,
            current_nonce=0
        )

if __name__ == "__main__":
    mcp.run()
```

### Automated Daemon Health Probe Script
Production probe script for CI/CD runners and Kubernetes liveness checks:

```python
#!/usr/bin/env python3
"""Automated Health Verification Probe for ClawRouter Daemon."""

import sys
import time
import requests

PROBE_URL = "http://127.0.0.1:8402/v1/health"

def run_probe(retries: int = 3, timeout_sec: float = 2.0) -> bool:
    for attempt in range(1, retries + 1):
        try:
            start_time = time.monotonic()
            resp = requests.get(PROBE_URL, timeout=timeout_sec)
            elapsed_ms = (time.monotonic() - start_time) * 1000
            if resp.status_code == 200:
                payload = resp.json()
                active_backends = payload.get("active_backends", 0)
                wallet_ok = payload.get("wallet_ready", False)
                print(f"[OK] ClawRouter healthy (latency: {elapsed_ms:.1f}ms, backends: {active_backends}, wallet_ready: {wallet_ok})")
                return True
            else:
                print(f"[WARN] Attempt {attempt}: Received HTTP {resp.status_code}")
        except requests.RequestException as e:
            print(f"[WARN] Attempt {attempt}: Connection failed ({e})")
        time.sleep(1.0)
    print("[ERROR] ClawRouter health check failed after maximum retries.")
    return False

if __name__ == "__main__":
    if not run_probe():
        sys.exit(1)
```

## Diagnostic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| `x402 Authorization Failed (402 Payment Required)` | Agent local wallet has insufficient USDC balance for on-chain micropayment. | Fund the agent's Base or Solana wallet with USDC or add free-tier model overrides (`blockrun/free-auto`) in config. |
| `ECONNREFUSED 127.0.0.1:8402` | ClawRouter proxy daemon is not running locally. | Launch the daemon using `npx @blockrun/clawrouter` or start `clawrouter.service` via `systemctl start clawrouter`. |
| `SLA Exceeded Timeout (504)` | Target LLM provider latency exceeded specified `latency_sla_ms`. | Adjust SLA metadata thresholds in request payload or exclude high-latency backends using `clawrouter exclude add <model>`. |
| `Invalid Wallet Signature Error` | Wallet secret key corrupted or mismatch between network environments. | Re-generate keypair using `clawrouter wallet reset` and verify `X402_NETWORK` matches target chain ID (e.g. `base-mainnet`). |
| `FastMCP Tool Handshake Failure` | MCP client and ClawRouter daemon version protocol mismatch. | Upgrade `@blockrun/clawrouter` and `mcp` SDK packages to latest FastMCP 3.1 supported versions. |
| `High Memory Consumption in Router Daemon` | Large prompt context caching memory leak in Node.js runtime. | Restart `clawrouter.service`, configure max context window limits in `clawrouter.config.json`, or upgrade to latest v3.2 release. |
| `Non-Deterministic Model Selection Flip-Flop` | Model score weights are too evenly balanced for near-identical latency backends. | Increase `quality_weight` or `cost_weight` dampening factors in `clawrouter.config.json` routing stanza. |
| `Redis Cache Connection Timeout` | Redis service crashed or firewall blocking port 6379 on `clawrouter-cache`. | Verify Redis container health via `docker ps` and check socket permissions on `/var/run/redis/redis.sock`. |

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
