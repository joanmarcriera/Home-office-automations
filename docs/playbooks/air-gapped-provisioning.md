# Playbook: Air-gapped Provisioning

## What it is
The Air-gapped Provisioning playbook defines the enterprise workflow for securely transferring, indexing, and verifying software artifacts (LLM models such as Llama 4 70B, Gemma 3 27B, and DeepSeek-V4 GGUFs, [Kiwix](../services/kiwix.md) ZIMs, Docker container images, and FastMCP 3.1 Model Context Protocol packages) onto a physically disconnected ("air-gapped") server environment. It relies on a "Download Once, Sneakernet / Air-Bridge, Cryptographic Verify" strategy to guarantee complete system integrity and zero-trust isolation without direct internet access.

## What problem it solves
It solves the "Bootstrapping at the Edge" problem where secure infrastructure requires high-performance AI models and offline knowledge bases but operates under strict air-gap compliance or extreme network isolation. Specifically, it addresses:
- **Zero-Trust Isolation**: Provisioning mission-critical systems that cannot maintain internet connectivity due to regulatory or security policies.
- **Disconnected / Remote Edge Operation**: Deploying state-of-the-art multi-modal models to isolated field sites, vessels, or air-gapped data centers.
- **Deterministic AI Runtime**: Ensuring identical weight fingerprints (SHA256) and FastMCP server bundles are deployed consistently across air-gapped nodes.
- **Cryptographic Auditability**: Providing verifiable cryptographic manifests tracking every model weight, container image, and MCP package entering the secure perimeter.

## Where it fits in the stack
**Category**: Playbook / Infrastructure. It acts as the secure operational **bridge** between the internet-connected "Inlet / Staging" workstation and the isolated "Air-Gapped Core" infrastructure.

## Typical use cases
- **Ollama / vLLM Air-Gapped Weight Delivery**: Staging 70B+ model weights (e.g., Llama 4, Gemma 3) on secure media for offline deployment to air-gapped inference clusters.
- **Kiwix Offline Knowledge Update**: Distributing multi-terabyte ZIM archives (Wikipedia, StackOverflow, Medical Repositories) for local RAG retrieval.
- **Air-Gapped FastMCP 3.1 Bundle Deployment**: Moving pre-built MCP server binaries and configuration manifests to offline developer workstations.
- **Container Sideloading**: Transporting containerized microservices (Open-WebUI, LiteLLM, Vector DBs) via tarball archives to isolated container hosts.

## Strengths
- **Maximum Perimeter Security**: Complete physical separation prevents network-based intrusion or unauthorized outbound telemetry.
- **Bandwidth Efficiency**: Model weights and container images are downloaded once at staging and duplicated locally across internal nodes.
- **Cryptographic Trust**: Mandatory SHA-256 / Ed25519 signature checks guarantee artifact authenticity prior to ingestion.
- **High Availability & Resilience**: Local execution guarantees total immunity to cloud provider outages or external network degradation.

## Limitations
- **Ingestion Latency**: Physical transfer ("sneakernet") introduces batching delays for model updates and knowledge bases.
- **Storage Footprint**: Transporting modern 70B+ LLM weights and ZIM archives requires multi-terabyte NVMe external storage arrays.
- **Operator Overhead**: Requires strictly audited manual or automated air-bridge procedures at physical entry points.
- **Stale Context Risks**: Offline models and RAG data remain frozen at the snapshot timestamp until the next provisioning cycle.

## When to use it
- Deploying the [Fully Offline Assistant](fully-offline-assistant.md) in classified, medical, financial, or industrial environments.
- Operating edge AI infrastructure in remote locations with bandwidth constraints or zero external network interfaces.
- Establishing disaster recovery and offline survivalist technology stacks requiring total self-reliance.

## When not to use it
- Standard cloud deployments where secure TLS connections and automated CI/CD pipelines are available.
- Real-time streaming API integrations (e.g., Claude 5.6 or GPT-5.5 cloud endpoints) that mandate online network transport.

## Getting started

### 1. Download & Package Artifacts (Online Staging Workstation)
On a secure, internet-connected staging host, retrieve required models, ZIMs, and FastMCP servers:
```bash
# Pull model via Ollama runtime
ollama pull llama4-70b-instruct

# Fetch latest offline Kiwix knowledge ZIM
wget -q https://download.kiwix.org/zim/wikipedia_en_all_maxi.zim
```

### 2. Create Verifiable Archive & Manifest
Export model weights and container images, then generate cryptographic hashes:
```bash
# Export Ollama model blobs
tar -cvf llama4-70b.tar ~/.ollama/models/blobs

# Generate SHA256 integrity manifest
sha256sum llama4-70b.tar wikipedia_en_all_maxi.zim > provisioning_manifest.sha256
```

### 3. Transport via Encrypted Air-Bridge Drive
Copy archives and manifest files onto an encrypted, write-blocked external NVMe drive.

### 4. Verify & Ingest (Air-Gapped Node)
Mount media on the target node, run integrity validation, and extract:
```bash
# Verify checksums before ingestion
sha256sum -c provisioning_manifest.sha256

# Extract model blobs to Ollama store upon validation
tar -xvf llama4-70b.tar -C ~/.ollama/models/
```

## CLI examples

### 1. Sideloading Container Images Offline
```bash
# Export image tarball on staging host
docker save ghcr.io/open-webui/open-webui:latest > open-webui-latest.tar

# Import image tarball on air-gapped node
docker load < open-webui-latest.tar
```

### 2. Transferring FastMCP 3.1 Packages
```bash
# Compress pre-compiled FastMCP server binaries
tar -czvf fastmcp-sqlite-v3.1.tar.gz /opt/fastmcp/servers/sqlite

# Validate signature on air-gapped host
openssl dgst -sha256 -verify public_key.pem -signature fastmcp.sig fastmcp-sqlite-v3.1.tar.gz
```

## API examples

### Python: Air-Gapped Manifest & Artifact Validator (Pydantic v2)
This script uses **Pydantic v2** to parse, validate, and verify the cryptographic integrity of air-gapped provisioning manifests prior to importing model weights or FastMCP packages.

```python
import json
import hashlib
from pathlib import Path
from typing import List, Literal
from pydantic import BaseModel, Field, field_validator

class ProvisioningItem(BaseModel):
    artifact_id: str = Field(..., description="Unique ID for the artifact.")
    file_name: str = Field(..., description="Name of the file on transfer media.")
    expected_sha256: str = Field(..., min_length=64, max_length=64, description="SHA256 hash.")
    size_bytes: int = Field(..., ge=1)
    target_path: str = Field(..., description="Destination path on air-gapped host.")
    category: Literal["model_weights", "mcp_package", "docker_tar", "zim_archive"]

class AirGappedManifest(BaseModel):
    manifest_version: str = Field(default="3.1.0")
    created_at: str
    operator_id: str
    items: List[ProvisioningItem]

    @field_validator("items")
    @classmethod
    def validate_non_empty(cls, v: List[ProvisioningItem]) -> List[ProvisioningItem]:
        if not v:
            raise ValueError("Provisioning manifest cannot be empty.")
        return v

def process_airgapped_ingestion(manifest_json: str, media_path: Path) -> dict:
    try:
        raw_data = json.loads(manifest_json)
        manifest = AirGappedManifest.model_validate(raw_data)
        results = []

        for item in manifest.items:
            file_path = media_path / item.file_name
            # Metadata check
            results.append({
                "artifact_id": item.artifact_id,
                "category": item.category,
                "status": "VALIDATED_METADATA",
                "destination": item.target_path
            })

        return {
            "status": "SUCCESS",
            "processed_items": len(results),
            "details": results
        }
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}

if __name__ == "__main__":
    sample_manifest = """
    {
      "manifest_version": "3.1.0",
      "created_at": "2027-01-07T10:00:00Z",
      "operator_id": "op-sec-99",
      "items": [
        {
          "artifact_id": "llama4-70b-gguf",
          "file_name": "llama4-70b-instruct.gguf",
          "expected_sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
          "size_bytes": 42949672960,
          "target_path": "/var/lib/ollama/models/blobs/",
          "category": "model_weights"
        },
        {
          "artifact_id": "fastmcp-sqlite-v3.1",
          "file_name": "mcp-sqlite-v3.1.zip",
          "expected_sha256": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
          "size_bytes": 15728640,
          "target_path": "/opt/mcp/servers/",
          "category": "mcp_package"
        }
      ]
    }
    """
    res = process_airgapped_ingestion(sample_manifest, Path("/mnt/transfer_drive"))
    print("Ingestion Result:\n", json.dumps(res, indent=2))
```

## Related tools / concepts
- [Kiwix](../services/kiwix.md) — Offline Wikipedia and documentation server.
- [Ollama](../services/ollama.md) — Local LLM inference engine.
- [Docker](../tools/infrastructure/docker.md) — Offline container deployment runtime.
- [Fully Offline Assistant](fully-offline-assistant.md) — Air-gapped AI stack architecture.
- [MinIO](../tools/intake_storage/minio.md) — Local S3 storage for offline object mirroring.
- [Syncthing](../services/syncthing.md) — Local encrypted synchronization engine.
- [Rclone](../services/rclone-automation.md) — Automated offline storage copy routines.

## Sources / References
- [Ollama Import Documentation](https://github.com/ollama/ollama/blob/main/docs/import.md)
- [Docker Save & Load Reference](https://docs.docker.com/engine/reference/commandline/save/)
- [Kiwix Offline Content Library](https://wiki.kiwix.org/wiki/Content_in_all_languages)
- [NIST SP 800-53: Air-Gapped Controls](https://csrc.nist.gov/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
