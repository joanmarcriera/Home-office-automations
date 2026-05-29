# SharpAI Security Benchmark

## What it is
The **SharpAI Security Benchmark** (SHARP) is a systemic high-level evaluation framework designed to quantify the resilience of Large Language Models (LLMs) and agentic systems against complex security threats. Unlike traditional performance benchmarks (e.g., MMLU), SHARP focuses on the **adversarial robustness** of models when they are given tool-access and delegated autonomy.

## What problem it solves
As AI agents move from "chatting" to "acting" (executing code, calling APIs, managing files), the risk of malicious exploitation grows exponentially. SHARP provides a standardized methodology to measure how effectively a model can resist instruction overrides (prompt injection), maintain data boundaries, and refuse unauthorized tool usage in high-stakes environments.

## Where it fits in the stack
**Category**: Tool / Benchmarking / Security Operations (SecOps). It serves as a final validation gate before deploying an agent into a production environment with write-access to sensitive data.

## Key Evaluation Categories (2026 Standards)
- **Indirect Prompt Injection**: Resilience against malicious instructions hidden in external data (e.g., a PDF or a website the agent reads).
- **Cross-Domain Leakage**: Ensuring an agent doesn't leak context from a 'High Trust' session into a 'Low Trust' response.
- **Recursive Tool Exploitation**: Testing if an agent can be tricked into using a tool to gain access to a second, more sensitive tool (e.g., using `read_file` to find a `db_password`).
- **Chain-of-Thought (CoT) Integrity**: Verifying that the model's internal reasoning cannot be manipulated to bypass safety filters.
- **Model Stealth**: Evaluating the model's ability to identify and report that it is being targeted by an adversarial attack.

## Typical use cases
- **Agent Red Teaming**: Automated stress-testing of custom agents built on platforms like [n8n](../../services/n8n.md) or [Dify](../frameworks/dify.md).
- **Model Hardening**: Identifying specific failure modes in a model's system prompt to refine its guardrails.
- **Vendor Selection**: Comparing the safety-to-utility ratio of frontier models (e.g., Claude 4.7 vs GPT-5 Preview).
- **Compliance Audits**: Generating safety reports for internal governance or external regulatory bodies (e.g., EU AI Act compliance).

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

## Getting started (CLI)

The SHARP runner is typically deployed as a containerized evaluation engine.

### Installation
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

## API examples (Python)

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
- [Agentic Security Patterns](../../knowledge_base/patterns/openclaw-security-operations.md) — Implementation strategies for SHARP findings.
- [Promptfoo](promptfoo.md) — Alternative testing framework for prompt regression.
- [Giskard](giskard.md) — AI quality and security platform.
- [Lakera Guard](lakera-guard.md) — Real-time protection layer that works alongside SHARP validation.
- [n8n Error Handling](../../knowledge_base/patterns/n8n-error-handling.md) — Practical application of security guardrails.

## Sources / References
- [SharpAI Benchmark Official Site](https://www.sharpai.org/benchmark/)
- [State of LLM Security 2026 Report](https://brightsec.com/blog/the-2026-state-of-llm-security-key-findings-and-benchmarks/)
- [GitHub: Adversarial Examples Papers (2026 Updates)](https://github.com/Trustworthy-AI-Group/Adversarial_Examples_Papers)

## Contribution Metadata
- Last reviewed: 2026-05-29
- Confidence: high
