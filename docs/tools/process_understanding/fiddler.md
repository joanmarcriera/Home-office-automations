# Fiddler AI

## What it is
Fiddler is an Enterprise-grade Model Performance Management (MPM) platform that has expanded to include specialized tools for LLM observability and monitoring (Fiddler Auditor and Fiddler AI Observability).

## What problem it solves
For enterprises, AI reliability isn't just about accuracy; it's about governance, safety, and bias. Fiddler provides a robust framework for monitoring AI models in production, detecting drift, and ensuring models remain compliant and safe.

## Where it fits in the stack
**Category**: Process & Understanding / Enterprise AI Observability

## Typical use cases
- **LLM Safety Monitoring**: Detecting PII, toxicity, and hallucinations in production LLM traffic.
- **Drift Detection**: Identifying when model performance begins to degrade over time as real-world data changes.
- **Root Cause Analysis**: Using "Explainable AI" (XAI) features to understand why a model made a specific prediction or generated a specific response.
- **Bias Auditing**: Ensuring AI applications are fair and non-discriminatory.

## Strengths
- **Enterprise-Ready**: Robust security, RBAC, and scalability for large organizations.
- **Multimodal Support**: Can monitor traditional ML models as well as modern LLMs.
- **Specialized LLM Metrics**: Includes advanced metrics for faithfulness and grounding.
- **Focus on Trust**: Strong emphasis on AI ethics and governance.

## Limitations
- **Target Audience**: Primarily built for large enterprises and data science teams; might be complex for individual developers.
- **Commercial Focus**: It is a commercial platform, though they offer trials and community tiers.

## When to use it
- When deploying high-stakes AI models in regulated industries (Finance, Healthcare).
- When you need enterprise-grade governance and explainability.

## When not to use it
- For early-stage prototyping or solo hobby projects.

## Getting started

Install the Fiddler Python client:

```bash
pip install fiddler-client
```

Connect to your Fiddler instance:

```python
import fiddler as fdl
client = fdl.FiddlerApi(url="YOUR_URL", org_id="YOUR_ORG", auth_token="YOUR_TOKEN")
```

## CLI examples

### fiddler-client
(Note: Fiddler primarily uses a Python SDK; CLI is often used via `pip` or custom wrappers.)
```bash
pip show fiddler-client
```

### curl (Publish Events)
Publishing an event to the Fiddler API:
```bash
curl -X POST https://app.fiddler.ai/api/v1/events \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{"project_id": "p1", "model_id": "m1", "data": {...}}'
```

### python -m fiddler
Checking version and connectivity:
```bash
python -m fiddler --version
```

## API examples

### Python (Evaluating Answer Relevance)
```python
import fiddler as fdl

# Initialize evaluator
evaluator = fdl.AnswerRelevance()

# Run evaluation
result = evaluator.evaluate(
    question="What is Fiddler?",
    answer="Fiddler is an AI observability platform."
)
print(result)
```

## Related tools / concepts
- [Arize AI](./arize-ai.md)
- [Weights & Biases](./wandb-weave.md)
- [Datadog](./datadog.md)
- [Sentry](./sentry.md)
- [LLM Security & Privacy](../../knowledge_base/llm_security_privacy.md)

## Sources / references
- [Fiddler AI Website](https://www.fiddler.ai/)
- [Fiddler SDK Documentation](https://docs.fiddler.ai/api)
- [Fiddler LLM Observability Guide](https://www.fiddler.ai/llm-observability)

## Contribution Metadata
- Last reviewed: 2026-05-26
- Confidence: high
