# Helicone

## What it is
Helicone is an open-source, high-performance AI Gateway and LLM observability platform. It functions as an intelligent proxy between application code and multiple upstream AI providers (such as Anthropic, OpenAI, Google Gemini, and Groq). As of late October 2026, Helicone is fully integrated with **Model Context Protocol (MCP 3.1)** and the **Asynchronous Control Protocol (ACP)**, allowing autonomous agents to query, parse, and act on their own tracing data in real time.

## What problem it solves
Managing and debugging production LLM applications is extremely challenging due to non-deterministic model outputs, erratic prompt routing, and lack of systemic tracking. Helicone addresses these core pain points by offering:
- **Zero-Latency Telemetry**: Full tracing of prompt strings, inputs, completions, and output metadata.
- **Accurate Financial Auditing**: Granular billing tracking, token counts, and cost modeling across 100+ different frontier and local models.
- **Resilience and Reliability**: Out-of-the-box routing configurations, automated retries, and high-availability fallbacks when upstream providers suffer outages.
- **Prompt Management**: Centralized prompt templates, strict version-control, and A/B testing playplaygrounds entirely decoupled from application source code.
- **Agent Execution Analysis**: Tracing multi-step reasoning chains in advanced models like **Claude 5.1** and **GPT-5.5** to uncover loop failures and infinite logic recursions.

## Where it fits in the stack
Helicone operates at the **AI Gateway and Observability** layer. Positioned exactly between the client SDK and upstream endpoints, it intercepts requests to append custom tags, cache completions, handle rate-limiting, and stream telemetry.

## Typical use cases
- **Enterprise-Grade Observability**: Monitoring real-time cost, token throughput, and success rates of API-driven user tasks.
- **Advanced Agent Swarm Tracing**: Tracking complex, multi-turn tool handoffs and subagent executions to optimize runtime.
- **Slick Prompt Iteration**: Decoupling, versioning, and deploying new system prompts directly via the Helicone Dashboard without redeploying code.
- **Dataset Exporting & Fine-Tuning**: Tagging and piping production request/response pairs directly into fine-tuning ecosystems like OpenPipe or Unsloth.
- **Intelligent Response Caching**: Serving repeated semantic queries from a low-latency proxy cache to eliminate duplicate upstream LLM fees.

## Strengths
- **Instant Integration**: Requires only a change to the client's `base_url` and the addition of a header—no bulky external SDK packages.
- **Open-Source & Secure**: Fully self-hostable via Docker, enabling strict compliance with data sovereignty regulations.
- **Broad Model Support**: Acts as a unified portal for over 100 commercial and open-weights models.
- **Advanced Metadata Tagging**: Enables custom keys (e.g., user groups, cohort IDs, feature flags) for multi-dimensional filtering.
- **Minimal Performance Overhead**: Adds less than 10ms of network latency under normal operation.

## Limitations
- **Single Point of Failure**: If the proxy gateway experiences a failure, upstream LLM features may be blocked (prevented by self-hosting or implementing local client failover routines).
- **Latency Overlap**: A tiny network hop is introduced, which is negligible for streaming but should be accounted for in ultra-low latency real-time voice loops.
- **Lagging Provider APIs**: Newly released provider parameters may take a short time to propagate through the proxy, though raw body forwarding minimizes this.

## When to use it
- When you require a centralized, secure portal to track, monitor, and route LLM queries across a diverse, multi-provider stack.
- When you need instant, zero-boilerplate telemetry for libraries that support standard OpenAI/Anthropic base URL overrides.
- When compliance mandates that all user and model interactions must be audited, self-hosted, and stored on internal infrastructure.

## When not to use it
- In basic, single-user applications or local exploratory notebooks where extra proxy configuration outweighs the monitoring benefits.
- If you are utilizing a specialized multi-agent framework like [AgentOps](agentops.md) that is already instrumented for complex multi-turn session tracking.

## Getting started

### Installation
Because Helicone relies on gateway proxy interception, you can use the standard provider SDKs without installing specialized third-party dependencies:

```bash
pip install openai anthropic pydantic
```

### Basic Proxy Integration (Python)
To route requests through the Helicone API gateway, update the client configuration to point to the secure gateway URL and pass your Helicone authentication token:

```python
import os
from openai import OpenAI

# Initialize the OpenAI client redirected to Helicone
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://gateway.helicone.ai/v1",
    default_headers={
        "Helicone-Auth": f"Bearer {os.environ.get('HELICONE_API_KEY')}"
    }
)
```

## CLI examples

### Running the Docker Stack Locally
To run a complete, self-hosted instance of Helicone with logging, caching, and a database:
```bash
git clone https://github.com/Helicone/helicone.git
cd helicone/docker
./helicone-compose.sh helicone up -d
```

### Direct Gateway Querying via curl
You can execute requests directly through the gateway using CLI curls:
```bash
curl https://gateway.helicone.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Helicone-Auth: Bearer $HELICONE_API_KEY" \
  -H "Helicone-Property-Environment: production" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Ping gateway!"}]
  }'
```

## API examples

### Completion with Structured Metadata Logging
Attach specialized custom property tags to your payload to enable deep performance segmentation in your Helicone dashboard.

```python
import os
import sys
from openai import OpenAI, APIError

def execute_tracked_completion(prompt_text: str, user_tier: str):
    """Executes a completion tracked by Helicone with custom properties and model target."""
    api_key = os.environ.get("OPENAI_API_KEY")
    helicone_key = os.environ.get("HELICONE_API_KEY")

    if not api_key or not helicone_key:
        print("Error: Missing API keys in environment.", file=sys.stderr)
        return

    # Direct client to the Helicone gateway
    client = OpenAI(
        api_key=api_key,
        base_url="https://gateway.helicone.ai/v1",
        default_headers={
            "Helicone-Auth": f"Bearer {helicone_key}"
        }
    )

    try:
        response = client.chat.completions.create(
            model="gpt-5.5-preview",
            messages=[{"role": "user", "content": prompt_text}],
            extra_headers={
                "Helicone-Property-User-Plan": user_tier,
                "Helicone-Property-Feature-Flag": "beta-analytics",
                "Helicone-Cache-Enabled": "true" # Enables semantic gateway caching
            }
        )
        print("==> Completion Response Received:")
        print(response.choices[0].message.content)
    except APIError as e:
        print(f"API Error during completion: {e.message}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    execute_tracked_completion(
        prompt_text="Optimize this SQL query: SELECT * FROM users WHERE active = true;",
        user_tier="enterprise"
    )
```

### Logging Anthropic Traces with Custom Headers
Helicone seamlessly proxies Anthropic client requests. Below is a programmatic Python example:

```python
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    base_url="https://anthropic.helicone.ai",
    default_headers={
        "Helicone-Auth": f"Bearer {os.environ.get('HELICONE_API_KEY')}"
    }
)
# Call client.messages.create(...) using model 'claude-5-1-sonnet-20261022'
```

## Related tools / concepts
- [Langfuse](langfuse.md) - Open-source LLM engineering platform with strong evaluation tools.
- [AgentOps](agentops.md) - Specialized observability for autonomous agent workflows.
- [Portkey AI Gateway](../providers/portkey.md) - Enterprise-grade AI gateway and observability.
- [LiteLLM](../../services/litellm.md) - Lightweight LLM proxy that can also export to Helicone.
- [OpenRouter](../ai_knowledge/openrouter.md) - Aggregator that provides its own unified API and logging.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - Protocol for connecting agents to data/tools.
- [Claude](../ai_knowledge/claude.md) - Primary frontier model for agentic workflows.
- [GPT-5.5 Optimization](../ai_knowledge/openai.md) - Reference for OpenAI model performance tuning.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) - Frontier-grade open model for local deployments.

## Sources / references
- [Helicone Official Website](https://www.helicone.ai/)
- [Helicone Documentation](https://docs.helicone.ai/)
- [Helicone GitHub Repository](https://github.com/Helicone/helicone)

## Contribution Metadata
- Last reviewed: 2026-10-24
- Confidence: high
