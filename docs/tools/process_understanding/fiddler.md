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

## Getting started

### Implementation
Typically involves integrating the Fiddler SDK into your inference pipeline to "publish" events to the Fiddler platform.

```python
# Conceptual example
from fiddler import FiddlerApi
client = FiddlerApi(url=URL, org_id=ORG, auth_token=TOKEN)
client.publish_event(project_id=PROJECT, model_id=MODEL, event_data=data)
```

## Related tools / concepts
- [Arize AI](arize-ai.md)
- [Weights & Biases](../process_understanding/wandb-weave.md)
- [Datadog](datadog.md)
- [LLM Security & Privacy](../../knowledge_base/llm_security_privacy.md)

## Sources / references
- [Fiddler AI Website](https://www.fiddler.ai/)
- [Fiddler LLM Observability Guide](https://www.fiddler.ai/llm-observability)

## Contribution Metadata
- Last reviewed: 2026-05-09
- Confidence: high
