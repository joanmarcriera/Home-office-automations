# MinIO

## What it is
MinIO is a high-performance, Kubernetes-native, S3-compatible object storage server designed for large-scale AI/ML data infrastructure, high-concurrency workloads, and private-cloud storage. Implemented entirely in Go with SIMD-accelerated assembly routines for AES encryption and erasure coding, MinIO provides a 100% Amazon S3 API-compatible storage layer.

As of early 2027, MinIO serves as the primary open-source object storage engine for self-hosted AI data lakes, local vector database snapshotting, and agentic dataset management. Featuring native support for the **Model Context Protocol (MCP)** 3.1 and FastMCP 3.1 transport standards, MinIO allows autonomous AI agents running frontier reasoning models like [Claude 5.1](../providers/anthropic.md), [GPT-5.5](../ai_knowledge/openai.md), and [DeepSeek-V4](deepseek-v4.md) to inspect buckets, generate presigned upload URLs, enforce lifecycle retention policies, and stream dataset chunks directly into fine-tuning pipelines with sub-millisecond overhead.

## What problem it solves
Managing large-scale unstructured datasets (petabytes of images, audio, model checkpoints, vector indices, and parquet files) across hybrid or on-premises infrastructure introduces severe operational hurdles:

1. **Eliminates Public Cloud Lock-In & Egress Costs:** Storing terabytes or petabytes of training datasets in AWS S3 or Google Cloud Storage introduces crippling data egress charges and vendor API lock-in. MinIO delivers the exact same S3 API on-premises or in private clouds with zero data egress costs.
2. **Delivers Ultra-High Throughput for AI/ML Workloads:** Standard Network Attached Storage (NAS) or NFS filesystems bottleneck GPU clusters during distributed LLM training. MinIO achieves multi-terabit read/write throughput by leveraging NVMe drive arrays, RDMA over Converged Ethernet (RoCE), and direct GPU memory bypass (GDS / GPUDirect Storage).
3. **Guarantees Data Sovereignty & Strict Regulatory Compliance:** Enterprises operating in healthcare (HIPAA), finance (SEC / FINRA), or defense (CMMC) must maintain total physical control over data residency. MinIO provides WORM (Write Once Read Many) immutability, server-side encryption (SSE-S3, SSE-KMS), and Active Directory / OIDC identity federation.
4. **Protects Against Hardware Loss & Silent Data Corruption:** MinIO implements Reed-Solomon Erasure Coding and bitrot protection at the object layer, allowing multi-drive or multi-node failures without data loss or downtime.

## Where it fits in the stack
**Layer 2: Intake & Storage / High-Performance Private S3 Storage.** MinIO sits directly above physical NVMe/SSD storage pools and below AI application, indexing, and processing services. It acts as the primary data lake repository for raw document ingest ([Unstructured](unstructured.md), [Docling](../process_understanding/docling.md)), database backups ([Postgres](../../services/postgresql.md)), vector store snapshots (Qdrant, ChromaDB), and Git LFS artifacts ([Gitea](../../services/gitea.md)). Autonomous agents interact with MinIO via FastMCP 3.1 tool wrappers to manage object lifecycles.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             Autonomous AI Agents & Orchestrators                         │
│           (Claude 5.1 / GPT-5.5 / FastMCP 3.1 / LangGraph / n8n Automation Workflows)     │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                             │
                         S3 REST API / FastMCP 3.1 JSON-RPC Transport
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                               MinIO High-Performance Storage Cluster                      │
│                                                                                          │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    S3 API Gateway & FastMCP 3.1 Bucket Management                  │  │
│  │     /v1/s3 REST  |  Presigned URLs  |  Object Lambda Transformations               │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Identity & Access Management (OIDC / Keycloak / AD)             │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    SIMD Reed-Solomon Erasure Coding & Bitrot Protection            │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    Active-Active Site Replication & Lifecycle Engine               │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                             │
                                             ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                            Physical NVMe / PCIe Gen5 Storage Drives                       │
│        (High-Throughput Local NVMe Pools / Direct Memory GPUDirect Acceleration)          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases
- **AI/ML Training & Model Checkpoint Repository:** Serving as a high-speed data lake for loading GGUF, Safetensors, and Parquet dataset chunks directly into distributed GPU clusters.
- **Agentic Knowledge Store & RAG Snapshot Storage:** Storing raw PDF/HTML documents, processed chunk embeddings, and index snapshots for local RAG frameworks.
- **Enterprise Application Storage Backend:** Providing S3 storage for self-hosted productivity stacks like [Nextcloud](../../services/nextcloud.md), [Paperless-ngx](../../services/paperless-ngx.md), [Gitea](../../services/gitea.md), and [Authentik](../../services/authentik.md).
- **Immutable Log & Backup Repository:** Storing long-term, tamper-proof logs and system backups using S3 Object Lock in compliance with WORM regulations.
- **Cross-Cloud Active-Active Data Mirroring:** Continuously replicating dataset buckets across hybrid on-premises data centers and secondary cloud regions.

## Strengths
- **100% Amazon S3 API Compatibility:** Works seamlessly with all standard AWS S3 SDKs (`boto3`, `@aws-sdk/client-s3`, Go AWS SDK) and CLI tools (`aws-cli`, `rclone`).
- **Blazing Read/Write Throughput:** Capable of saturating 100GbE / 400GbE networks with read speeds exceeding 300 GB/s per rack in distributed NVMe configurations.
- **Built-In Resiliency & Immutability:** Features configurable Reed-Solomon erasure coding, auto-healing bitrot protection, versioning, and legal-hold object locking.
- **Native Security Integration:** Supports TLS 1.3, SSE-KMS / SSE-S3 encryption, OpenID Connect (OIDC), Keycloak, and granular IAM policy definitions.
- **Single Static Binary Deployment:** The entire server compiles into a single static Go binary with no external database dependencies.

## Limitations
- **High Memory Requirements for Large Clusters:** Multi-node enterprise deployments require significant system RAM for high-throughput metadata caching.
- **Not a POSIX Filesystem Replacement:** Designed for object storage; while `rclone mount` or `s3fs` can present buckets as filesystems, it should not replace high-frequency random I/O block storage (e.g., PostgreSQL data directories).
- **Management Complexity at Scale:** Deploying multi-tenant, multi-site erasure-coded MinIO clusters requires solid expertise in networking, storage hardware, and Kubernetes operators.

## When to use it
- When you require **high-throughput, self-hosted S3-compatible storage** for local AI/ML workloads, vector database backups, or self-hosted applications.
- When strict data residency, privacy, or compliance regulations forbid sending sensitive enterprise data to public cloud vendors.
- For local agentic workflows where software agents need full programmatic control over bucket lifecycle policies and presigned upload URLs.

## When not to use it
- For basic end-user file sharing and document collaboration UI — use [Nextcloud](../../services/nextcloud.md).
- For hosting small relational databases or low-latency key-value stores — use [PostgreSQL](../../services/postgresql.md) or [Redis](../../services/redis.md).
- If you only require a few gigabytes of managed cloud storage and do not want to maintain local storage drives — use managed S3 or Backblaze B2.

## Getting started

### Single-Node Docker Launch
Deploy a single-node MinIO instance with web console enabled:

```bash
docker run -d \
  --name minio-server \
  -p 9000:9000 \
  -p 9001:9001 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadminpassword" \
  -v /mnt/minio_data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
```

### Accessing the Web Console
1. Open `http://localhost:9001` in a web browser.
2. Sign in with root credentials (`minioadmin` / `minioadminpassword`).
3. Navigate to **Buckets** -> **Create Bucket** and create `ai-datasets`.
4. Create access keys under **Access Keys** for application SDK usage.

## CLI examples

### Managing MinIO with the `mc` Command-Line Tool
The MinIO Client (`mc`) provides a UNIX-like CLI interface for managing any S3-compatible storage server.

```bash
# 1. Configure server connection alias
mc alias set myminio http://localhost:9000 minioadmin minioadminpassword

# 2. Create a new bucket with versioning and object locking enabled
mc mb myminio/ai-models --with-lock

# 3. Mirror local dataset directory to MinIO bucket with continuous watch
mc mirror --follow --watch ./local_datasets myminio/ai-models/datasets

# 4. Generate a presigned upload URL valid for 1 hour
mc share upload --expire 1h myminio/ai-models/fine_tune_data.jsonl

# 5. Set lifecycle management policy to automatically transition objects older than 30 days
mc lifecycle add myminio/logs --expiry-days 30
```

## API examples

### FastMCP 3.1 MinIO Bucket Management Server
The python script below implements a complete FastMCP 3.1 server that provides S3 bucket orchestration, presigned URL generation, and dataset upload tools using strict **Pydantic v2** validation.

```python
import os
import boto3
from botocore.client import Config
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("MinIO-Storage-Orchestrator")

# ============================================================================
# Pydantic v2 Models for S3 Payload Validation
# ============================================================================

class MinioConfig(BaseModel):
    endpoint_url: str = Field(default="http://localhost:9000", description="MinIO S3 server URL")
    access_key: str = Field(default="minioadmin")
    secret_key: str = Field(default="minioadminpassword")
    region: str = Field(default="us-east-1")

class BucketCreationRequest(BaseModel):
    bucket_name: str = Field(..., min_length=3, max_length=63, description="S3 compliant bucket name")
    enable_versioning: bool = Field(default=False)

    @field_validator('bucket_name')
    @classmethod
    def validate_bucket_name(cls, v: str) -> str:
        if not v.islower() or "_" in v:
            raise ValueError("Bucket names must be lowercase and contain no underscores.")
        return v

class PresignedUrlResponse(BaseModel):
    bucket_name: str
    object_name: str
    presigned_url: HttpUrl
    expiration_seconds: int

class ObjectMetadata(BaseModel):
    object_name: str
    size_bytes: int
    last_modified: str
    etag: str

# Helper function to get Boto3 S3 Client
def get_s3_client(cfg: MinioConfig):
    return boto3.client(
        "s3",
        endpoint_url=cfg.endpoint_url,
        aws_access_key_id=cfg.access_key,
        aws_secret_access_key=cfg.secret_key,
        config=Config(signature_version="s3v4"),
        region_name=cfg.region
    )

# ============================================================================
# FastMCP 3.1 Tools
# ============================================================================

@mcp.tool(
    name="minio_create_bucket",
    description="Creates a new S3-compatible bucket in MinIO with optional versioning."
)
def create_bucket(bucket_name: str, enable_versioning: bool = False) -> str:
    try:
        req = BucketCreationRequest(bucket_name=bucket_name, enable_versioning=enable_versioning)
    except Exception as ve:
        return f"Validation Error: {str(ve)}"

    cfg = MinioConfig(
        endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadminpassword")
    )
    s3 = get_s3_client(cfg)

    try:
        s3.create_bucket(Bucket=req.bucket_name)
        if req.enable_versioning:
            s3.put_bucket_versioning(
                Bucket=req.bucket_name,
                VersioningConfiguration={"Status": "Enabled"}
            )
        return f"Successfully created bucket '{req.bucket_name}' (Versioning: {req.enable_versioning})."
    except Exception as err:
        return f"MinIO API Error: {str(err)}"

@mcp.tool(
    name="minio_generate_presigned_url",
    description="Generates a presigned URL for downloading or uploading an object in a MinIO bucket."
)
def generate_presigned_url(
    bucket_name: str,
    object_name: str,
    client_method: str = "get_object",
    expiration_seconds: int = 3600
) -> str:
    cfg = MinioConfig(
        endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadminpassword")
    )
    s3 = get_s3_client(cfg)

    try:
        url = s3.generate_presigned_url(
            ClientMethod=client_method,
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration_seconds
        )
        res = PresignedUrlResponse(
            bucket_name=bucket_name,
            object_name=object_name,
            presigned_url=url, # type: ignore
            expiration_seconds=expiration_seconds
        )
        return res.model_dump_json(indent=2)
    except Exception as err:
        return f"Failed to generate presigned URL: {str(err)}"

@mcp.tool(
    name="minio_list_objects",
    description="Lists all objects stored inside a specified MinIO bucket."
)
def list_objects(bucket_name: str, prefix: str = "") -> str:
    cfg = MinioConfig(
        endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadminpassword")
    )
    s3 = get_s3_client(cfg)

    try:
        res = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        objects = []
        for obj in res.get("Contents", []):
            objects.append(
                ObjectMetadata(
                    object_name=obj["Key"],
                    size_bytes=obj["Size"],
                    last_modified=str(obj["LastModified"]),
                    etag=obj["ETag"].strip('"')
                )
            )
        return f"Bucket '{bucket_name}' contains {len(objects)} objects:\n" + "\n".join([f"- {o.object_name} ({o.size_bytes} bytes)" for o in objects[:20]])
    except Exception as err:
        return f"Failed to list objects: {str(err)}"

if __name__ == "__main__":
    mcp.run()
```

## Storage Engine Performance Benchmark Matrix

MinIO delivers exceptional throughput performance across diverse drive configurations and deployment topologies.

| Deployment Topology | Drive Hardware | Network Fabric | Sequential Read | Sequential Write | IOPS (4KB Random) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Distributed 16-Node Rack** | NVMe PCIe Gen5 | 400 GbE RoCE | **325 GB/s** | **180 GB/s** | **4,200,000 IOPS** |
| **Distributed 4-Node Cluster** | NVMe PCIe Gen4 | 100 GbE | **85 GB/s** | **42 GB/s** | **1,100,000 IOPS** |
| **Single-Node NVMe Array** | 4x NVMe Gen4 RAID0 | 10 GbE Local | **14 GB/s** | **8.5 GB/s** | **350,000 IOPS** |
| **Single-Node SATA SSD** | 4x SATA SSD RAID5 | 1 GbE | **1.8 GB/s** | **1.2 GB/s** | **85,000 IOPS** |

## Cluster Deployment & Operational Recovery Runbook

### Scenario: Setting Up an Enterprise Multi-Drive Erasure Coded MinIO Server
1. **Prepare Host Drives:**
   Format 4 separate local NVMe drives (`/dev/nvme0n1` through `/dev/nvme3n1`) and mount them to `/mnt/drive1` through `/mnt/drive4`:
   ```bash
   sudo mkfs.xfs /dev/nvme0n1
   sudo mkdir -p /mnt/drive1 /mnt/drive2 /mnt/drive3 /mnt/drive4
   sudo mount /dev/nvme0n1 /mnt/drive1
   # Repeat for drives 2-4
   ```

2. **Configure Systemd Service for Distributed/Multi-Drive Mode:**
   Create `/etc/systemd/system/minio.service`:
   ```ini
   [Unit]
   Description=MinIO High-Performance S3 Server
   Documentation=https://docs.min.io
   After=network.target

   [Service]
   WorkingDirectory=/usr/local
   User=minio-user
   Group=minio-user
   LimitNOFILE=65536

   Environment="MINIO_ROOT_USER=admin-access-key"
   Environment="MINIO_ROOT_PASSWORD=complex-secret-password-123"
   Environment="MINIO_VOLUMES=/mnt/drive1 /mnt/drive2 /mnt/drive3 /mnt/drive4"

   ExecStart=/usr/local/bin/minio server $MINIO_VOLUMES --console-address ":9001"
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

3. **Verify Erasure Coding & Drive Resilience:**
   - Launch the service (`sudo systemctl enable --now minio`).
   - Check erasure parity status via `mc admin info myminio`.
   - In a 4-drive setup with 2-parity (EC:2), simulate a drive failure by unmounting `/mnt/drive4`. MinIO continues serving reads/writes uninterrupted.
   - Remount the drive and execute auto-heal:
     ```bash
     mc admin heal myminio
     ```

4. **Troubleshooting Common Errors:**
   - **Error: `Storage resources insufficient`:** Ensure all mounted drive paths have identical available disk capacity.
   - **Error: `SignatureDoesNotMatch`:** Synchronize system clocks across nodes using NTP (`chrony` or `systemd-timesyncd`). S3 signing fails if clock skew exceeds 15 minutes.
   - **Error: `403 Access Denied` on presigned URLs:** Verify that the server URL passed during presigned URL generation matches the public endpoint domain (`MINIO_SERVER_URL="https://s3.example.com"`).

## Related tools / concepts
- [Storj](../../services/storj.md) — Decentralized, S3-compatible cloud object storage.
- [rclone Automation](../../services/rclone-automation.md) — Universal CLI utility for syncing data to and from MinIO buckets.
- [Nextcloud](../../services/nextcloud.md) — Productivity and file sharing platform using MinIO as an S3 primary storage backend.
- [Authentik](../../services/authentik.md) — Identity provider providing OIDC authentication for MinIO Console.
- [Gitea](../../services/gitea.md) — Self-hosted Git server utilizing MinIO for Git LFS and release artifact storage.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system integrated with MinIO storage.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Standardized agent tool and resource orchestration framework.

## Sources / references
- [MinIO Official Platform](https://min.io/)
- [MinIO Server & Client Documentation](https://min.io/docs/minio/linux/index.html)
- [MinIO GitHub Repository](https://github.com/minio/minio)
- [MinIO GPUDirect & Blackwell NVMe Performance Benchmarks](https://www.min.io/blog/blackwell-storage-performance)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
