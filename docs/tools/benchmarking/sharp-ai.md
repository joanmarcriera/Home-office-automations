# SharpAI Security Benchmark

## What it is
The **SharpAI Security Benchmark** (SHARP) is a systemic high-level evaluation framework designed to quantify the resilience of Large Language Models (LLMs) and agentic systems against complex security threats. Unlike traditional performance benchmarks (e.g., MMLU), SHARP focuses on the **adversarial robustness** of models when they are given tool-access and delegated autonomy.

## What problem it solves
As AI agents move from "chatting" to "acting" (executing code, calling APIs, managing files), the risk of malicious exploitation grows exponentially. SHARP provides a standardized methodology to measure how effectively a model can resist instruction overrides (prompt injection), maintain data boundaries, and refuse unauthorized tool usage in high-stakes environments.

## Where it fits in the stack
**Category**: Tool / Benchmarking / Security Operations (SecOps). It serves as a final validation gate before deploying an agent into a production environment with write-access to sensitive data. It is compatible with the **MCP 3.0** standard for tool-use auditing.

## Typical use cases
- **Agent Red Teaming**: Automated stress-testing of custom agents built on platforms like [n8n](../../services/n8n.md) or [Dify](../frameworks/dify.md).
- **Model Hardening**: Identifying specific failure modes in a model's system prompt to refine its guardrails for **Claude 4.8 Opus** and **GPT-5.5**.
- **Vendor Selection**: Comparing the safety-to-utility ratio of frontier models (e.g., Claude vs GPT vs Gemini).
- **Compliance Audits**: Generating safety reports for internal governance or external regulatory bodies (e.g., EU AI Act compliance).
- **Tool-Access Validation**: Testing if an agent can be tricked into using a tool to gain access to sensitive data (Recursive Tool Exploitation).

## Strengths
- **Behavioral Focus**: Tests the *actions* of the agent, not just its text output.
- **Dynamic Scenarios**: Includes multi-turn attacks where the adversary tries to "wear down" the model's guardrails.
- **Open-Source Suite**: The evaluation engine is modular, allowing for the addition of custom, domain-specific attack vectors.
- **Context-Aware Metrics**: Provides separate scores for 'Passive Resistance' vs 'Active Detection'.

## Limitations
- **Cat-and-Mouse Game**: New injection techniques (like 'ClawJacked' or 'Social Steganography') emerge faster than benchmarks can be updated.
- **Computational Cost**: Comprehensive SHARP runs require thousands of model calls, which can be expensive on high-tier APIs.
- **False Negatives**: A passing score does not guarantee 100% security; it only proves resilience against the *tested* attack suite.

## When to use it
- Before granting an AI agent write-access to a production database or email account.
- When updating the underlying LLM of an existing automation workflow to ensure no security regressions.
- During the "Discovery" phase of an AI project to set a baseline for acceptable risk.

## When not to use it
- For testing creative writing, translation accuracy, or general reasoning (use [OpenCompass](../benchmarking/opencompass.md) or [HELM](../benchmarking/helm.md)).
- For low-risk, internal-only RAG systems with no tool-calling capabilities.

## Getting started (Docker/Local)

The SHARP runner is typically deployed as a containerized evaluation engine.

### Docker Installation
```bash
# Pull the SHARP evaluation engine
docker pull sharpai/eval-runner:latest
```

### Running a Benchmark
Execute a standard security suite against an OpenAI-compatible endpoint:
```bash
docker run -e MODEL_ENDPOINT="http://ollama:11434" \
           -e API_KEY="dummy" \
           sharpai/eval-runner run --suite security-v3 --model llama3.5-agent
```

## CLI examples

The SHARP CLI allows for granular control over the evaluation process.

```bash
# List available security suites
sharp-eval list-suites

# Run a specific 'Indirect Injection' test case
sharp-eval run --test indirect_injection_01 --target http://localhost:8080/v1/chat

# Export the latest results to a JSON report
sharp-eval export --format json --output ./reports/sharp_results.json
```

## API examples

Integrate SHARP into your CI/CD pipeline to block unsafe deployments.

```python
from sharp_eval import SharpRunner, SecuritySuites

# Initialize the runner with your target agent configuration
runner = SharpRunner(
    target_url="http://my-agent-api/chat",
    system_prompt_path="./prompts/system_v1.txt"
)

# Run the 'Indirect Injection' suite
results = runner.execute(SecuritySuites.INDIRECT_INJECTION)

# Assert a safety score of at least 0.95
if results.safety_score < 0.95:
    print(f"Deployment blocked! Found {len(results.vulnerabilities)} vulnerabilities.")
    results.export_report("vulnerability_report.pdf")
    exit(1)
```

## Related tools / concepts
- [LLM Security & Privacy](../../knowledge_base/llm_security_privacy.md) — Core concepts behind SHARP.
- [Promptfoo](promptfoo.md) — Alternative testing framework for prompt regression.
- [Giskard](giskard.md) — AI quality and security platform.
- [Lakera Guard](lakera-guard.md) — Real-time protection layer that works alongside SHARP validation.
- [OpenCompass](../benchmarking/opencompass.md) — General purpose LLM benchmarking framework.
- [HELM](../benchmarking/helm.md) — Holistic Evaluation of Language Models.
- [n8n Service](../../services/n8n.md) — Common target for agentic automation security testing.

## Sources / References
- [SharpAI Benchmark Official Site](https://www.sharpai.org/benchmark/)
- [State of LLM Security 2026 Report](https://brightsec.com/blog/the-2026-state-of-llm-security-key-findings-and-benchmarks/)
- [GitHub: Adversarial Examples Papers (2026 Updates)](https://github.com/Trustworthy-AI-Group/Adversarial_Examples_Papers)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
