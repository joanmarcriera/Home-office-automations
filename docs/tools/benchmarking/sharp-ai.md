# SharpAI Security Benchmark

## What it is
The **SharpAI Security Benchmark** (SHARP) is a systemic high-level evaluation framework designed to quantify the resilience of Large Language Models (LLMs) and agentic systems against complex security threats. Unlike traditional performance benchmarks (e.g., MMLU), SHARP focuses on the **adversarial robustness** of models when they are given tool-access and delegated autonomy.

## What problem it solves
As AI agents move from "chatting" to "acting" (executing code, calling APIs, managing files), the risk of malicious exploitation grows exponentially. SHARP provides a standardized methodology to measure how effectively a model can resist instruction overrides (prompt injection), maintain data boundaries, and refuse unauthorized tool usage in high-stakes environments. It solves the lack of standardized "red teaming" protocols for agentic workflows.

## Where it fits in the stack
**Category**: Tool / Benchmarking / Security Operations (SecOps). It serves as a final validation gate before deploying an agent into a production environment with write-access to sensitive data, sitting alongside CI/CD and monitoring tools.

## Typical use cases
- **Agent Red Teaming**: Automated stress-testing of custom agents built on platforms like [n8n](../../services/n8n.md) or [Dify](../ai_knowledge/dify.md).
- **Model Hardening**: Identifying specific failure modes in a model's system prompt to refine its guardrails.
- **Vendor Selection**: Comparing the safety-to-utility ratio of frontier models (e.g., Claude 4.8 vs GPT-5.5).
- **Compliance Audits**: Generating safety reports for internal governance or external regulatory bodies (e.g., EU AI Act compliance).
- **Regression Testing**: Ensuring that a prompt update doesn't introduce new security vulnerabilities.

## Strengths
- **Behavioral Focus**: Tests the *actions* of the agent (e.g., file deletion, API exfiltration), not just its text output.
- **Dynamic Scenarios**: Includes multi-turn attacks where the adversary tries to "wear down" the model's guardrails.
- **Open-Source Suite**: The evaluation engine is modular, allowing for the addition of custom, domain-specific attack vectors.
- **Context-Aware Metrics**: Provides separate scores for 'Passive Resistance' vs 'Active Detection' and 'Reasoning Integrity'.

## Limitations
- **Cat-and-Mouse Game**: New injection techniques (like 'ClawJacked' or 'Social Steganography') emerge faster than benchmarks can be updated.
- **Computational Cost**: Comprehensive SHARP runs require thousands of model calls, which can be expensive on high-tier APIs.
- **False Negatives**: A passing score does not guarantee 100% security; it only proves resilience against the *tested* attack suite.
- **Complexity**: Setting up realistic tool-calling environments for the benchmark can be time-consuming.

## When to use it
- Before granting an AI agent write-access to a production database, email account, or cloud infrastructure.
- When updating the underlying LLM (e.g., moving to Claude 4.8 Opus) of an existing automation workflow to ensure no security regressions.
- During the "Discovery" phase of an AI project to set a baseline for acceptable risk.

## When not to use it
- For testing creative writing, translation accuracy, or general reasoning (use [OpenCompass](../benchmarking/opencompass.md) or [HELM](../benchmarking/helm.md)).
- For low-risk, internal-only RAG systems with no tool-calling or autonomous action capabilities.
- When you need immediate, real-time protection (use [Lakera Guard](lakera-guard.md) or [Giskard](giskard.md)).

## Getting started (including Docker/Local setup)
The SHARP runner is typically deployed as a containerized evaluation engine to ensure environment isolation during adversarial tests.

### Installation via Docker
```bash
# Pull the SHARP evaluation engine
docker pull sharpai/eval-runner:latest

# Create a local workspace for reports
mkdir sharp_reports
```

### Basic Configuration
Create a `config.yaml` to define your target agent's endpoint and the tools it has access to:
```yaml
target:
  url: "http://localhost:8080/v1/chat"
  type: "openai-compatible"
tools:
  - name: "read_file"
  - name: "execute_bash"
```

## CLI examples
The SHARP CLI is used to orchestrate benchmark runs and generate reports.

```bash
# Run a standard security suite against your agent
docker run -v $(pwd)/reports:/app/reports sharpai/eval-runner run \
           --suite security-v3 \
           --target-url "http://agent-api:5000" \
           --output /app/reports/result.json

# Run a specific 'Indirect Injection' attack suite
sharp-cli test --category indirect-injection --model claude-4.8-opus

# List all available security scenarios
sharp-cli list scenarios --version 2026.2
```

## API examples
Integrate SHARP into your CI/CD pipeline using the Python SDK.

```python
from sharp_eval import SharpRunner, SecuritySuites

# Initialize the runner
runner = SharpRunner(
    target_url="http://my-agent-api/chat",
    system_prompt_path="./prompts/system_v1.txt"
)

# Execute the 'Recursive Tool Exploitation' suite
results = runner.execute(SecuritySuites.RECURSIVE_EXPLOIT)

# Assert a safety score of at least 0.95
if results.safety_score < 0.95:
    print(f"Deployment blocked! Found {len(results.vulnerabilities)} vulnerabilities.")
    results.export_report("vulnerability_report.pdf")
    exit(1)
```

## Related tools / concepts
- [LLM Security & Privacy](../../knowledge_base/llm_security_privacy.md) — Core concepts behind SHARP.
- [OpenCompass](../benchmarking/opencompass.md) — General performance benchmarking suite.
- [HELM](../benchmarking/helm.md) — Holistic evaluation of language models.
- [VAKRA](../benchmarking/vakra.md) — Benchmark for agentic reasoning and tool-use.
- [Giskard](giskard.md) — AI quality and security platform for testing.
- [Lakera Guard](lakera-guard.md) — Real-time protection layer against injections.
- [Promptfoo](promptfoo.md) — Matrix-based testing framework for prompt regression.

## Sources / References
- [SharpAI Benchmark Official Site](https://www.sharpai.org/benchmark/)
- [State of LLM Security 2026 Report](https://brightsec.com/blog/the-2026-state-of-llm-security-key-findings-and-benchmarks/)
- [GitHub: Adversarial Examples Papers (2026 Updates)](https://github.com/Trustworthy-AI-Group/Adversarial_Examples_Papers)
- [OWASP Top 10 for LLM Applications (v2.0)](https://genai.owasp.org/llm-top-10/)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
