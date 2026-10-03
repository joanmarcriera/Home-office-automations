# BigSwitch

## What it is
BigSwitch is an open, community-driven curation engine, algorithmic validation pipeline, and sovereign tech discovery directory focused on European alternatives to Big Tech platforms. Operating as an architectural registry and compliance verification framework as of 2027, BigSwitch cataloged EU-owned, GDPR-compliant, and open-source cloud, AI infrastructure, database, messaging, and orchestration tools. By strictly evaluating jurisdictional ownership, data residency, subprocessor lineage, and foreign surveillance exposure (specifically US Cloud Act, FISA 702, and non-EU extraterritorial discovery mandates), BigSwitch enables enterprise IT architects, devops engineers, and AI system integrators to assemble 100% sovereign technology stacks.

The platform goes beyond simple directory listings by maintaining structured JSON/YAML compliance schemas, hosting automated continuous integration benchmarks, and serving dynamic tool recommendations via FastMCP 3.1 Model Context Protocol servers. As enterprise AI adoption accelerates under the enforcement of the EU Artificial Intelligence Act (EU AI Act) and NIS2 directives, BigSwitch provides the definitive taxonomy and auditing engine for replacing proprietary foreign SaaS dependencies with sovereign European alternatives such as [Mistral AI](mistral.md), Scaleway, Hetzner, OVHcloud, Exoscale, Clever Cloud, and Infomaniak.

```
+---------------------------------------------------------------------------------------------------+
|                                  BIGSWITCH ARCHITECTURE OVERVIEW                                 |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +-----------------------+     +-------------------------------+     +-------------------------+  |
|  | Enterprise AI / App   |     | FastMCP 3.1 Server Gateway    |     | BigSwitch Registry DB   |  |
|  | Sovereign Client Agent| <-> | (mcp-server-bigswitch)         | <-> | (JSON / SQLite Engine)  |  |
|  +-----------------------+     +-------------------------------+     +-------------------------+  |
|              |                                 |                                  |               |
|              v                                 v                                  v               |
|  +---------------------------------------------------------------------------------------------+  |
|  |                            AUTOMATED COMPLIANCE & AUDITING PIPELINE                         |  |
|  +---------------------------------------------------------------------------------------------+  |
|  |  [Jurisdiction Checker]    [Datacenter Latency Auditor]    [GDPR & Subprocessor Validator]   |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                |                                                  |
|                                                v                                                  |
|  +---------------------------------------------------------------------------------------------+  |
|  |                               SOVEREIGN EU TARGET INFRASTRUCTURE                            |  |
|  +-------------------------------+-------------------------------+-----------------------------+  |
|  | LLM Inference Endpoints       | IaaS / Compute / K8s          | Managed Databases & Storage |  |
|  | (Mistral AI, Scaleway Nabius) | (Hetzner, OVHcloud, Exoscale) | (Clever Cloud, Infomaniak)  |  |
|  +-------------------------------+-------------------------------+-----------------------------+  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## What problem it solves
Transitioning enterprise workloads and agentic AI architectures away from monopolistic hyperscalers (e.g., AWS, Microsoft Azure, Google Cloud, OpenAI, Anthropic) introduces significant vendor lock-in, regulatory exposure, and operational complexity. Key challenges addressed by BigSwitch include:

- **US Cloud Act & Extraterritorial Data Exposure**: Cloud providers headquartered in foreign jurisdictions remain subject to government subpoenas regardless of where physical servers reside. BigSwitch identifies strictly EU-owned legal entities that operate without foreign parent oversight.
- **EU AI Act & Regulatory Non-Compliance**: The EU AI Act enforces stringent requirements on data lineage, model transparency, and risk management. BigSwitch catalogs models and infrastructure providers that supply verifiable audit trails and local data processing guarantees.
- **Fragmented European Tech Ecosystem**: European cloud and AI alternatives are historically dispersed across regional markets. BigSwitch unifies these offerings into an indexed, searchable catalog with standardized technical metrics.
- **Automated Sovereign Model Routing**: Modern AI agents require dynamic routing that guarantees sensitive data (e.g., healthcare, financial, civic records) never traverses foreign-owned infrastructure during inference. BigSwitch provides structured metadata to power FastMCP 3.1 routing tools.

## Where it fits in the stack
**Category**: Providers / Discovery Directory & Compliance Governance Gateway.

BigSwitch functions as the foundational compliance registry and routing metadata provider across the cloud and AI stack:

```
+-----------------------------------------------------------------------------------+
|                             ENTERPRISE STACK PLACEMENT                            |
+-----------------------------------------------------------------------------------+
| Application & Agent Layer | FastMCP 3.1 Tool Servers, Multi-Agent Orchestrators   |
+---------------------------+-------------------------------------------------------+
| Governance & Audit Gateway| BigSwitch Sovereign Registry & Dynamic MCP Router     |
+---------------------------+-------------------------------------------------------+
| AI & Model Layer          | Mistral AI, DeepSeek EU, Sovereign vLLM / TGI Nodes   |
+---------------------------+-------------------------------------------------------+
| Database & Data Store     | Managed PostgreSQL, Qdrant EU, MinIO EU Storage       |
+---------------------------+-------------------------------------------------------+
| Compute & Hosting (IaaS)  | Hetzner Cloud, OVHcloud, Scaleway, Exoscale           |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Sovereign AI Infrastructure Selection**: Architecting enterprise LLM deployments that strictly leverage European hosting providers (e.g., [Mistral AI](mistral.md), Scaleway GPU Instances, Hetzner Dedicated Servers).
- **Automated Jurisdictional Stack Auditing**: Scanning Terraform configurations, Kubernetes manifests, and Python dependency trees to detect non-EU SaaS calls or cloud APIs.
- **FastMCP 3.1 Sovereign Tool Integration**: Equipping autonomous Claude 5.1 / GPT-5.6 agents with tools to dynamically query BigSwitch for EU-compliant vector stores, database engines, and model endpoints.
- **GDPR & NIS2 Compliance Proofing**: Generating automated audit reports for Data Protection Officers (DPOs) proving that customer data remains strictly within EU/EEA boundaries under EU ownership.

## Strengths
- **Strict Jurisdictional Auditing**: Rigorous vendor vetting that distinguishes between local physical servers owned by foreign entities vs true EU-owned, EU-headquartered legal entities.
- **Structured MCP & API Ecosystem**: Exposes REST and FastMCP 3.1 endpoints for seamless integration into CI/CD pipelines and agentic toolkits.
- **Open Source & Transparent**: Community-driven repository where vendor evaluations, audit scripts, and benchmark methodologies are fully inspectable.
- **Granular Taxonomy**: Categories span LLM inference, vector databases, object storage, identity management (IAM), CI/CD build runners, and communication tools.

## Limitations
- **No Direct Billing Agreggation**: Operates as a discovery directory and compliance catalog rather than a unified cloud marketplace or reseller billing portal.
- **Feature Disparity in Niche Tooling**: Certain hyper-specialized hyperscaler services (e.g., proprietary real-time streaming engines) may lack 1:1 direct European equivalents, requiring modular architectural assembly.

## When to use it
- When designing AI agent workflows for defense, healthcare, government, or financial sectors in the EU.
- When configuring automated infrastructure routing where LLM requests must be filtered by jurisdiction before dispatch.
- When conducting third-party vendor risk assessments and GDPR subprocessor verification.

## When not to use it
- For workloads where jurisdictional sovereignty, data residency, and foreign surveillance laws are entirely irrelevant.
- For legacy enterprise applications that cannot be decoupled from proprietary single-vendor cloud stacks.

## Getting started

### Interactive Directory Browsing
1. Explore categories at `https://bigswitch.eu/`.
2. Filter providers by target jurisdiction (e.g., `DE`, `FR`, `SE`, `FI`, `EU-Wide`), GDPR certification, and deployment model (SaaS, PaaS, Self-Hosted).
3. Cross-reference selections with organizational security standards and [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md).

### Hetzner Sovereign Infrastructure Provisioning via Terraform
Deploying a GDPR-compliant, EU-sovereign FastMCP 3.1 node on Hetzner Cloud in Germany:

```hcl
# main.tf - Sovereign Infrastructure Deployment
terraform {
  required_version = ">= 1.8.0"
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.45.0"
    }
  }
}

variable "hcloud_token" {
  type        = string
  sensitive   = true
  description = "Hetzner Cloud API Token"
}

provider "hcloud" {
  token = var.hcloud_token
}

resource "hcloud_network" "sovereign_net" {
  name     = "sovereign-agent-net"
  ip_range = "10.0.0.0/16"
}

resource "hcloud_network_subnet" "sovereign_subnet" {
  type         = "cloud"
  network_id   = hcloud_network.sovereign_net.id
  netmask      = "255.255.255.0"
  ip_range     = "10.0.1.0/24"
  network_zone = "eu-central"
}

resource "hcloud_server" "sovereign_mcp_host" {
  name        = "sovereign-fastmcp-server-01"
  image       = "ubuntu-24.04"
  server_type = "cx32"
  location    = "fsn1" # Falkenstein, Germany (EU Data Center)

  labels = {
    "sovereignty-level" = "eu-strict"
    "jurisdiction"      = "DE"
    "gdpr-verified"     = "true"
    "managed-by"        = "bigswitch-architecture"
  }

  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }

  user_data = <<-EOF
              #!/bin/bash
              apt-get update && apt-get install -y docker.io python3-pip git
              systemctl enable --now docker
              echo "Sovereign FastMCP host initialized."
              EOF
}

output "server_ip" {
  value       = hcloud_server.sovereign_mcp_host.ipv4_address
  description = "Public IPv4 address of sovereign host"
}
```

## CLI examples

```bash
# 1. Inspect TLS certificate details and server routing headers for an EU provider
curl -v -X HEAD https://api.mistral.ai 2>&1 | grep -E "Server|location|x-served-by|CN="

# 2. Audit outbound TCP connections to confirm no foreign hyperscaler IPs are connected
netstat -tupn | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort -u

# 3. Query BigSwitch CLI tool to verify vendor compliance status
bigswitch-cli search --category "vector-db" --sovereignty "eu-strict" --format json

# 4. Perform DNS route traceability to verify EU datacenter hosting
traceroute api.scaleway.com

# 5. Fetch and validate BigSwitch catalog entries using cURL and jq
curl -s https://raw.githubusercontent.com/bigswitch-eu/catalog/main/providers.json \
  | jq '.providers[] | select(.jurisdiction == "FR" and .cloud_act_exposed == false)'
```

## API examples

### Sovereign Routing & Provider Discovery via FastMCP 3.1
The following FastMCP 3.1 Python server exposes tools for AI agents to query BigSwitch vendor entries and calculate workload compliance scores:

```python
"""
BigSwitch Sovereign Discovery & Compliance FastMCP 3.1 Server
Provides tools for agentic systems to discover EU software alternatives.
"""

import json
import logging
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bigswitch-mcp")

# Initialize FastMCP Server
mcp = FastMCP(
    "BigSwitch Sovereign Directory",
    version="3.1.0",
    description="MCP Server for querying European sovereign software and AI infrastructure"
)

# In-memory BigSwitch database mock
BIGSWITCH_DATABASE = [
    {
        "id": "mistral-ai",
        "name": "Mistral AI",
        "category": "ai-infrastructure",
        "jurisdiction": "FR",
        "datacenter_locations": ["FR", "DE"],
        "gdpr_audited": True,
        "cloud_act_exposed": False,
        "supported_models": ["mistral-large-2411", "pixtral-12b", "codestral-22b"]
    },
    {
        "id": "scaleway-cloud",
        "name": "Scaleway",
        "category": "iaas-compute",
        "jurisdiction": "FR",
        "datacenter_locations": ["FR", "NL", "PL"],
        "gdpr_audited": True,
        "cloud_act_exposed": False,
        "supported_models": []
    },
    {
        "id": "hetzner-cloud",
        "name": "Hetzner Online",
        "category": "iaas-compute",
        "jurisdiction": "DE",
        "datacenter_locations": ["DE", "FI"],
        "gdpr_audited": True,
        "cloud_act_exposed": False,
        "supported_models": []
    },
    {
        "id": "qdrant-eu-cloud",
        "name": "Qdrant Cloud (EU Region)",
        "category": "vector-database",
        "jurisdiction": "DE",
        "datacenter_locations": ["DE"],
        "gdpr_audited": True,
        "cloud_act_exposed": False,
        "supported_models": []
    }
]

class ProviderSearchQuery(BaseModel):
    category: Optional[str] = Field(None, description="Category filter (e.g., ai-infrastructure, iaas-compute, vector-database)")
    jurisdiction: Optional[str] = Field(None, description="Country code (e.g., FR, DE, SE)")
    require_zero_cloud_act: bool = Field(True, description="Strictly exclude entities subject to foreign surveillance acts")

class AuditRequestPayload(BaseModel):
    stack_name: str = Field(..., description="Name of the infrastructure stack being audited")
    active_providers: List[str] = Field(..., description="List of provider IDs or legal entity names")

class ComplianceReport(BaseModel):
    stack_name: str
    sovereign_score: float = Field(..., description="Percentage of compliant EU sovereign providers (0.0 to 100.0)")
    compliant_providers: List[str]
    flagged_providers: List[str]
    recommendations: List[str]

@mcp.tool()
def search_sovereign_providers(query: ProviderSearchQuery) -> str:
    """
    Search BigSwitch directory for EU-sovereign software and cloud providers.
    """
    results = []
    for item in BIGSWITCH_DATABASE:
        if query.category and item["category"] != query.category:
            continue
        if query.jurisdiction and item["jurisdiction"] != query.jurisdiction:
            continue
        if query.require_zero_cloud_act and item["cloud_act_exposed"]:
            continue
        results.append(item)

    return json.dumps({"count": len(results), "providers": results}, indent=2)

@mcp.tool()
def audit_stack_sovereignty(payload: AuditRequestPayload) -> str:
    """
    Audit an enterprise infrastructure stack and calculate EU digital sovereignty score.
    """
    sovereign_ids = {p["id"]: p for p in BIGSWITCH_DATABASE}
    sovereign_names = {p["name"].lower(): p for p in BIGSWITCH_DATABASE}

    compliant = []
    flagged = []
    recommendations = []

    for provider in payload.active_providers:
        p_lower = provider.lower()
        if provider in sovereign_ids or p_lower in sovereign_names:
            compliant.append(provider)
        else:
            flagged.append(provider)
            recommendations.append(f"Consider replacing '{provider}' with an audited EU alternative from BigSwitch.")

    total = len(payload.active_providers)
    score = (len(compliant) / total * 100.0) if total > 0 else 0.0

    report = ComplianceReport(
        stack_name=payload.stack_name,
        sovereign_score=round(score, 2),
        compliant_providers=compliant,
        flagged_providers=flagged,
        recommendations=recommendations
    )

    return report.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

### Sovereign Provider Audit Schema Validation using Pydantic v2
This production-grade script validates provider metadata payloads against strict BigSwitch certification rules:

```python
"""
BigSwitch Provider Validation & GDPR Metadata Verification System
Validates JSON catalog dumps using Pydantic v2 schemas.
"""

import json
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError, field_validator

class CertificationMetadata(BaseModel):
    gdpr_certified: bool = Field(..., description="Verified GDPR compliance status")
    iso_27001_certified: bool = Field(False, description="ISO 27001 Information Security Management standard")
    secnumcloud_certified: bool = Field(False, description="ANSSI SecNumCloud French sovereign cloud qualification")
    c5_certified: bool = Field(False, description="BSI C5 German cloud computing compliance criteria")

class DatacenterLocation(BaseModel):
    country_code: str = Field(..., min_length=2, max_length=2, description="ISO 3166-1 alpha-2 country code")
    city: str = Field(..., description="Datacenter city location")
    renewable_energy_percentage: float = Field(..., ge=0.0, le=100.0, description="Percentage of clean power")

class SovereignProviderEntry(BaseModel):
    provider_id: str = Field(..., description="Unique slug identifier (e.g. hetzner-cloud)")
    legal_name: str = Field(..., description="Full legal entity registered name")
    category: str = Field(..., description="Service classification code")
    website_url: HttpUrl = Field(..., description="Official provider URL")
    jurisdiction_country: str = Field(..., min_length=2, max_length=2, description="Legal entity registration country")
    parent_company_jurisdiction: Optional[str] = Field(None, description="Parent company country if applicable")
    us_cloud_act_exposed: bool = Field(..., description="True if subject to foreign subpoena laws")
    certifications: CertificationMetadata = Field(..., description="Security and regulatory certifications")
    datacenters: List[DatacenterLocation] = Field(..., min_items=1, description="Physical server location details")
    last_audit_timestamp: datetime = Field(..., description="ISO timestamp of last BigSwitch audit")

    @field_validator("jurisdiction_country", "parent_company_jurisdiction")
    @classmethod
    def validate_eu_jurisdiction(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        eu_countries = {
            "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI",
            "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
            "NL", "PL", "PT", "RO", "SE", "SI", "SK"
        }
        if value.upper() not in eu_countries:
            raise ValueError(f"Country code '{value}' is outside strict EU jurisdiction.")
        return value.upper()

class BigSwitchCatalogPayload(BaseModel):
    catalog_version: str = Field(..., description="Catalog semver string")
    generated_at: datetime = Field(..., description="Generation date")
    providers: List[SovereignProviderEntry] = Field(..., description="List of validated sovereign entries")

def process_catalog_file(raw_json: str) -> Optional[BigSwitchCatalogPayload]:
    try:
        data = json.loads(raw_json)
        catalog = BigSwitchCatalogPayload.model_validate(data)
        print(f"Successfully validated catalog v{catalog.catalog_version} containing {len(catalog.providers)} providers.")
        return catalog
    except ValidationError as err:
        print("Schema Validation Error:")
        print(err.json(indent=2))
        return None
    except json.JSONDecodeError:
        print("Error: Input is not valid JSON.")
        return None

if __name__ == "__main__":
    sample_json = json.dumps({
        "catalog_version": "2027.1.0",
        "generated_at": "2027-01-07T12:00:00Z",
        "providers": [
            {
                "provider_id": "scaleway-bare-metal",
                "legal_name": "Scaleway SAS",
                "category": "iaas-compute",
                "website_url": "https://www.scaleway.com",
                "jurisdiction_country": "FR",
                "parent_company_jurisdiction": "FR",
                "us_cloud_act_exposed": False,
                "certifications": {
                    "gdpr_certified": True,
                    "iso_27001_certified": True,
                    "secnumcloud_certified": True,
                    "c5_certified": False
                },
                "datacenters": [
                    {
                        "country_code": "FR",
                        "city": "Paris",
                        "renewable_energy_percentage": 100.0
                    }
                ],
                "last_audit_timestamp": "2027-01-07T08:30:00Z"
            }
        ]
    })

    process_catalog_file(sample_json)
```

## Related tools / concepts
- [Mistral AI](mistral.md) — Premier European open-weights and commercial frontier LLM provider.
- [Hugging Face](huggingface.md) — European-headquartered open-source model hub and collaboration platform.
- [DeepSeek](deepseek.md) — Advanced open-weights foundation models and inference runtime patterns.
- [Replicate](replicate.md) — Multi-modal cloud inference and serverless deployment platform.
- [Together AI](together.md) — High-throughput open model inference and fine-tuning platform.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized protocol for connecting AI models to local/remote tools.
- [Groq](groq.md) — Ultra-low-latency LPU hardware inference engine.
- [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md) — Architectural taxonomy for classifying data confidentiality and compliance risks.

## Sources / references
- [BigSwitch Official Portal](https://bigswitch.eu/)
- [BigSwitch Community Directory Repository](https://github.com/bigswitch-eu)
- [EU Digital Sovereignty Framework & Priorities](https://ec.europa.eu/info/strategy/priorities-2019-2024/europe-fit-digital-age_en)
- [GDPR Article 44 - General Principle for Data Transfers](https://gdpr-info.eu/art-44-gdpr/)
- [EU Artificial Intelligence Act Official Text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
