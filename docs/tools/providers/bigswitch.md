# BigSwitch

## What it is
BigSwitch is a community-driven directory focused on European alternatives to Big Tech. It promotes digital sovereignty by highlighting GDPR-compliant, EU-owned, and often open-source tools. It serves as a curation engine for developers and organizations who prioritize jurisdictional safety and data residency within the European Union.

## What problem it solves
It helps individuals and organizations navigate the transition from US-centric SaaS platforms to European alternatives, addressing concerns around digital sovereignty, data residency, and GDPR compliance. It mitigates the risk of "Cloud Act" exposure by identifying providers that operate entirely under European law, which is increasingly critical for frontier models like `claude-4-8-opus-20260528` and GPT-5.5 when processing sensitive EU data.

## Where it fits in the stack
**Providers / Discovery Directory**. It is a selection and vetting resource for European tech providers, influencing the choice of infrastructure, storage, and communication layers in the [Knowledge Base](../../knowledge_base/README.md).

## Typical use cases
- **Sourcing GDPR-compliant alternatives**: Finding business communication and cloud storage solutions that guarantee data residency in the EU.
- **Identifying EU-based AI**: Discovering infrastructure providers like [Mistral](mistral.md) or Scaleway.
- **Auditing a tech stack**: Evaluating existing services for digital sovereignty and jurisdictional risk using the [Sovereignty Audit Pattern](#sovereignty-audit-pattern).
- **Privacy-First Procurement**: Using the directory to find tools that prioritize user privacy and open standards.

## Strengths
- **Sovereignty Focus**: Prioritizes tools owned and operated within the EU.
- **Broad Coverage**: Covers multiple tech categories from infrastructure to end-user apps.
- **Community-Driven**: Transparent curation process that avoids vendor lock-in.
- **GDPR-First**: All listed tools are vetted for European data protection standards.
- **Jurisdictional Transparency**: Provides clear info on where the company is headquartered and where data is stored.

## Limitations
- **Discovery Only**: Does not provide direct technical integration or managed service layers.
- **Manual Maintenance**: As a community directory, the freshness of data depends on active contributors.
- **Niche Availability**: Some highly specialized US-based tools may not have an exact 1:1 European equivalent.

## When to use it
- When seeking tech providers that operate under European jurisdiction and GDPR.
- When digital sovereignty and local data residency are priority requirements for a [Homelab](../../architecture/infrastructure.md) or enterprise stack.
- For finding alternatives to dominant US-based SaaS platforms to mitigate jurisdictional risk for agents.

## When not to use it
- When you are already satisfied with your current provider and digital sovereignty is not a critical factor.
- When you require extremely niche or deep technical integration that only a specific global incumbent provides.

## Getting started
1. Visit [bigswitch.eu](https://bigswitch.eu/) to browse the directory.
2. Filter by category (e.g., "Infrastructure" or "Communication").
3. Compare potential providers against your current stack's [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md).
4. Implement one alternative at a time to ensure stability.

## CLI examples
While BigSwitch is a directory, users can use standard CLI tools to verify the headers and hosting location of recommended providers.

```bash
# Verify the hosting location of a recommended provider (e.g., Mistral)
curl -I https://api.mistral.ai | grep -i "server"

# Check if a site is using a European CDN or origin
curl -v -X HEAD https://bigswitch.eu/ 2>&1 | grep -E "Server|location|x-served-by"
```

### Infrastructure Configuration (Hetzner Cloud)
Using BigSwitch recommendations often involves switching to providers like Hetzner. Below is a Terraform snippet for an EU-sovereign server deployment.

```hcl
# Example Terraform for Hetzner Cloud (EU-Based)
provider "hcloud" {
  token = var.hcloud_token
}

resource "hcloud_server" "sovereign_node" {
  name        = "sovereign-agent-host"
  image       = "ubuntu-22.04"
  server_type = "cx11"
  location    = "nbg1" # Nuremberg, Germany (EU Data Center)
  labels = {
    "sovereignty" = "high"
  }
}
```

## API examples
Developers can use the BigSwitch directory concepts to perform a jurisdictional audit. Below is the **Sovereignty Audit Pattern** for automating a basic sovereignty check.

```python
import json

# Example: List of providers used in the current project
MY_STACK = [
    {"name": "Mistral AI", "role": "LLM Provider"},
    {"name": "AWS", "role": "Hosting"},
    {"name": "Hetzner", "role": "Hosting"},
]

# Example: Data sourced from BigSwitch recommendations (simplified)
EU_PROVIDERS = ["Mistral AI", "Hetzner", "Scaleway", "OVHcloud", "Infomaniak"]

def run_sovereignty_audit(stack, eu_list):
    report = {"eu_compliant": [], "non_eu": []}
    for provider in stack:
        if provider["name"] in eu_list:
            report["eu_compliant"].append(provider)
        else:
            report["non_eu"].append(provider)
    return report

audit_results = run_sovereignty_audit(MY_STACK, EU_PROVIDERS)
print(f"Sovereignty Audit Results: {json.dumps(audit_results, indent=2)}")
```

## Related tools / concepts
- [Mistral](mistral.md) — Premier European LLM provider.
- [Hugging Face](huggingface.md) — European-headquartered AI community hub.
- [Hetzner](https://www.hetzner.com/) — German cloud provider often recommended by BigSwitch.
- [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md) — Critical for sovereignty audits.
- [DeepSeek](deepseek.md) — Cross-jurisdictional alternative.
- [Replicate](replicate.md) — Multi-modal hub with diverse hosting.
- [Together AI](together.md) — Serverless endpoints for open models.
- [AWS Bedrock](aws-bedrock.md) — Comparison for trust boundaries.

## Sources / references
- [Official Website](https://bigswitch.eu/)
- [GitHub (Meta/Community)](https://github.com/bigswitch-eu)
- [EU Digital Sovereignty Strategy](https://ec.europa.eu/info/strategy/priorities-2019-2024/europe-fit-digital-age_en)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
