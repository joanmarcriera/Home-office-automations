# BigSwitch

## What it is
BigSwitch is a community-driven curation engine and discovery directory focused on European alternatives to Big Tech platforms. As of early January 2027, it promotes digital sovereignty and data residency by vetting GDPR-compliant, EU-owned, and open-source cloud, infrastructure, and AI tools for enterprise and homelab deployments.

## What problem it solves
It simplifies the transition from US-centric SaaS and cloud AI providers to European alternatives, mitigating US Cloud Act exposure and ensuring compliance with strict European regulations (GDPR, EU AI Act). BigSwitch provides vetted alternatives for hosting frontier models (Claude 5.1, GPT-5.6, Gemini 4.0 Pro) and sovereign FastMCP 3.1 agent tool pipelines.

## Where it fits in the stack
**Category**: Providers / Discovery Directory. It serves as an architectural selection resource and compliance registry for infrastructure, database, messaging, and AI tool selection across European enterprise environments.

## Typical use cases
- **Sourcing GDPR/EU AI Act Compliant Providers**: Identifying cloud hosting, database, and storage options operating strictly within EU jurisdiction.
- **Sovereign AI Infrastructure Selection**: Discovering European AI infrastructure providers (e.g., [Mistral AI](mistral.md), Scaleway, Hetzner, OVHcloud).
- **Jurisdictional Stack Auditing**: Evaluating existing AI infrastructure for US Cloud Act exposure and data transfer risks.
- **Sovereign Model Routing**: Configuring intelligent routers to direct sensitive user queries strictly to EU-hosted inference endpoints.

## Strengths
- **Digital Sovereignty Focus**: Curation restricted to software and hosting providers owned and operating under EU jurisdiction.
- **Regulatory Compliance First**: Clear transparency around GDPR adherence, data residency locations, and legal entity structures.
- **Community-Driven Curation**: Independent vendor auditing that avoids vendor lock-in and biased endorsements.
- **Broad Category Depth**: Covers everything from raw compute/IaaS to AI agent frameworks, storage, and developer tools.

## Limitations
- **Discovery Directory Only**: Offers curation and discovery metadata, but does not provide a unified managed billing or proxy layer.
- **Feature Disparity**: Some specialized niche US cloud services may not have a 1:1 functional equivalent in the EU ecosystem.

## When to use it
- When building sovereign AI stacks that require strict data residency within EU borders under GDPR and the EU AI Act.
- When selecting infrastructure for self-hosted agent hubs and FastMCP 3.1 tool servers in European datacenters.
- For conducting security and jurisdictional audits of enterprise tech stacks.

## When not to use it
- If your workload operates outside European jurisdiction and has no data residency constraints.
- If you rely exclusively on proprietary US cloud managed services with no local alternatives.

## Getting started

### Browsing Directory
1. Visit [bigswitch.eu](https://bigswitch.eu/) to explore curated tech categories.
2. Select categories such as **AI & Infrastructure**, **Databases**, or **Communication**.
3. Evaluate listed providers against your organizational [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md).

### Hetzner Sovereign Infrastructure Provisioning (Terraform)
Deploying infrastructure via an EU sovereign host like Hetzner:

```hcl
provider "hcloud" {
  token = var.hcloud_token
}

resource "hcloud_server" "sovereign_mcp_host" {
  name        = "sovereign-fastmcp-server"
  image       = "ubuntu-24.04"
  server_type = "cx22"
  location    = "fsn1" # Falkenstein, Germany (EU Data Center)
  labels = {
    "sovereignty" = "eu-strict"
    "gdpr"        = "verified"
  }
}
```

## CLI examples

```bash
# Verify headers and server location for a recommended EU provider (e.g., Mistral AI)
curl -I https://api.mistral.ai | grep -i "server"

# Inspect TLS certificate details for EU data center routing verification
curl -v -X HEAD https://bigswitch.eu/ 2>&1 | grep -E "Server|location|x-served-by"

# Audit outgoing connections to verify no unauthorized US Cloud endpoints are invoked
netstat -tupn | grep ESTABLISHED
```

## API examples

### Automated Stack Sovereignty Audit

```python
import json

# Define active provider stack
CURRENT_STACK = [
    {"service": "LLM Inference", "provider": "Mistral AI", "country": "FR"},
    {"service": "Database", "provider": "Hetzner Cloud", "country": "DE"},
    {"service": "Storage", "provider": "OVHcloud", "country": "FR"},
]

EU_SOVEREIGN_PROVIDERS = {"Mistral AI", "Hetzner Cloud", "OVHcloud", "Scaleway", "Infomaniak"}

def audit_sovereignty(stack):
    compliant = []
    non_compliant = []
    for item in stack:
        if item["provider"] in EU_SOVEREIGN_PROVIDERS:
            compliant.append(item)
        else:
            non_compliant.append(item)
    return {"compliant": compliant, "non_compliant": non_compliant}

print(json.dumps(audit_sovereignty(CURRENT_STACK), indent=2))
```

### Sovereign Provider Curation Validation using Pydantic v2
This Python script validates provider sovereignty metadata and GDPR compliance using **Pydantic v2**:

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class SovereignProvider(BaseModel):
    name: str = Field(..., description="Legal entity name of the provider")
    category: str = Field(..., description="Tech classification, e.g., AI & Infrastructure, Database")
    jurisdiction: str = Field(..., description="Primary legal jurisdiction country code (e.g., DE, FR, SE)")
    data_residency_country: str = Field(..., description="Physical datacenter location country code")
    gdpr_compliant: bool = Field(..., description="Indicates whether provider is GDPR audited")
    cloud_act_exposed: bool = Field(False, description="True if entity is subject to US Cloud Act requests")

class BigSwitchAuditBatch(BaseModel):
    audit_id: str = Field(..., description="Audit run tracking identifier")
    audit_date: str = Field(..., description="ISO date of the audit execution")
    providers: List[SovereignProvider] = Field(..., description="List of audited providers")

def validate_audit_batch(raw_json: str) -> Optional[BigSwitchAuditBatch]:
    try:
        data = json.loads(raw_json)
        batch = BigSwitchAuditBatch.model_validate(data)
        print(f"Audit Batch {batch.audit_id} successfully validated {len(batch.providers)} providers.")
        return batch
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None

if __name__ == "__main__":
    test_payload = json.dumps({
        "audit_id": "audit-20270107-eu01",
        "audit_date": "2027-01-07",
        "providers": [
            {
                "name": "Mistral AI",
                "category": "AI & Infrastructure",
                "jurisdiction": "FR",
                "data_residency_country": "FR",
                "gdpr_compliant": True,
                "cloud_act_exposed": False
            }
        ]
    })
    validate_audit_batch(test_payload)
```

## Related tools / concepts
- [Mistral AI](mistral.md) — Premier European open-weights and commercial LLM provider.
- [Hugging Face](huggingface.md) — European-headquartered open source repository and hub.
- [DeepSeek](deepseek.md) — Open weights foundation models.
- [Replicate](replicate.md) — Multi-modal cloud inference platform.
- [Together AI](together.md) — High-throughput open model inference platform.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open protocol for agentic tool integrations.
- [Groq](groq.md) — Low latency LPU inference engine.
- [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md) — Architecture pattern for security audits.

## Sources / references
- [BigSwitch Official Website](https://bigswitch.eu/)
- [BigSwitch Community Directory Repository](https://github.com/bigswitch-eu)
- [EU Digital Sovereignty Framework](https://ec.europa.eu/info/strategy/priorities-2019-2024/europe-fit-digital-age_en)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
