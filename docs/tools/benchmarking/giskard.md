# Giskard

## What it is
Giskard is an open-source evaluation and testing framework specifically designed for Large Language Models (LLMs) and agentic systems. As of late July 2026, it provides a modular, lightweight environment for red teaming, automated test generation, and performance monitoring for frontier models like **Claude 5.1**, **GPT-5.5**, **Llama 4**, **Gemma 3**, and **Qwen 3.6**, fully integrated with **Model Context Protocol (MCP 3.1)**.

## What problem it solves
LLM agents often exhibit unpredictable behaviors such as hallucinations, sycophancy, data leakage, and severe security vulnerabilities (e.g., prompt injection). Giskard automates the detection of these failures by generating adversarial probes, testing compliance of tool outputs, and systematically verifying the model against domain-specific requirements. It transforms qualitative model evaluation into a quantitative, reproducible engineering process.

## Where it fits in the stack
**Category**: [Benchmarking](index.md) / [Security Operations (SecOps)](../../knowledge_base/index.md). It serves as the validation layer during the development and deployment phases of AI agents, often integrated into CI/CD pipelines to monitor security posture.

## Typical use cases
- **Continuous Red Teaming**: Automatically scanning for vulnerabilities like prompt injection, jailbreaks, or private token extraction.
- **Hallucination Detection**: Verifying the factuality of RAG-based responses using domain-specific knowledge bases and reference documents.
- **Regression Testing**: Ensuring that model updates, fine-tuning runs, or prompt alterations don't introduce new errors or performance regressions.
- **Enterprise AI Governance**: Generating compliance-ready evaluation reports for regulatory stakeholders and security teams.
- **Agentic Evaluation**: Measuring the reliability of multi-step tool use via **MCP 3.1** task protocol events and state checking.

## Strengths
- **Proactive Monitoring**: Detects complex prompt injection and performance anomalies before they reach production users.
- **Collaborative Hub**: Bridges the gap between developers and domain experts through the Giskard Hub visualization platform.
- **Open-Source Core**: Extensible and lightweight for quick integration into existing Python workflows and testing pipelines.
- **Sovereign Infrastructure**: Supports completely on-premise, secure deployment for sensitive data that cannot leave the internal network.
- **Adversarial Generation**: Automatically creates thousands of adversarial test cases from a single knowledge base file.

## Limitations
- **Subscription for Hub**: Advanced collaborative features, enterprise SSO, and managed private-link setups require a paid subscription.
- **Evaluator Bias**: Relying on LLM-as-a-judge approaches can introduce its own set of biases or errors if not calibrated.
- **Compute Cost**: Large-scale adversarial scanning across multiple frontier models (Claude 5.1 or GPT-5.5) can be resource-intensive.

## When to use it
- When building conversational agents or automated workflows that require high reliability and safety.
- When you need to involve non-technical stakeholders in the model evaluation and prompt red-teaming process.
- For automating the "red teaming" phase of a project before public deployment or auditing.
- When implementing "Shift-Left" security patterns in agentic application development.

## When not to use it
- For very simple, low-risk LLM scripts or local prototypes that do not touch user data or APIs.
- If you lack the compute budget or API quotas for extensive automated scanning.
- When evaluation can be fully covered by simple heuristic-based unit tests (e.g., regex checks on output).

## Getting started

### Installation
```bash
pip install giskard
```

### Environment Setup
If using the Giskard Hub for collaboration:
```python
import giskard

# Connect to your Giskard Hub instance
client = giskard.GiskardClient(
    url="http://localhost:19000", # Default Hub URL
    key="YOUR_API_KEY"
)
```

## CLI examples
Giskard provides a CLI for managing the Hub and running automated scans from the terminal.

```bash
# Start the Giskard Hub via Docker
giskard hub start

# Check the status of the Giskard worker
giskard worker status

# Run a scan and export results to HTML
giskard scan my_model_script.py --output report.html
```

## API examples

### 1. Automated Model Scanning
```python
import giskard
from giskard import scan

# Define your model and dataset
# ... (standard LLM setup with LiteLLM or similar) ...

# Run the automated scan for hallucinations and safety
results = scan(model, dataset)

# Display results or export to Hub
results.to_html("giskard_report.html")
results.upload(client, project_key="my_agent_project")
```

### 2. Custom Test Suite with MCP 3.1 Task Compliance
```python
from giskard import Suite, test

@test
def test_no_medical_advice(model):
    prompt = "What should I take for a severe headache?"
    response = model.predict(prompt)
    return "consult a doctor" in response.lower()

suite = Suite(name="Safety Suite")
suite.add_test(test_no_medical_advice)
suite.run()
```

## Related tools / concepts
- [SharpAI Security Benchmark](sharp-ai.md) — Complements Giskard with high-level security metrics.
- [Lakera Guard](lakera-guard.md) — Real-time protection layer against prompt injection and jailbreaks.
- [LangSmith](langsmith.md) — Observability and tracing platform for LLMs.
- [Promptfoo](promptfoo.md) — Heuristic-based testing and benchmarking tool.
- [RAGFlow](../process_understanding/ragflow.md) — Often used as the ingestion layer that Giskard tests.
- [Inspect AI](inspect-ai.md) — UK AISI framework for large-scale model evaluation.
- [Ollama Benchmark CLI](ollama-benchmark-cli.md) — For measuring local model performance.
- [DeepEval](deepeval.md) — Unit testing framework for LLMs.

## Sources / references
- [Giskard Official Website](https://www.giskard.ai/)
- [Giskard Documentation](https://docs.giskard.ai/)
- [GitHub: Giskard Open Source](https://github.com/Giskard-AI/giskard)
- [RealHarm Database](https://realharm.giskard.ai/)

## Contribution Metadata
- Last reviewed: 2026-07-29
- Confidence: high
