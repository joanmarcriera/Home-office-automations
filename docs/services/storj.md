# Storj

Storj is a decentralized, high-performance, S3-compatible cloud object storage platform that distributes encrypted data across a global network of independent storage nodes in early January 2027.

## What it is
Storj is a decentralized cloud object storage system that provides zero-knowledge encryption, global distribution, and native S3 compatibility. Operating on a peer-to-peer network of tens of thousands of storage nodes, Storj automatically encrypts, erasure-codes (e.g., 29/80 redundancy), and shards files across the network, providing high-availability storage for homelabs, media streaming clusters, and multi-agent AI ecosystems (**Claude 5.1**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro**, **DeepSeek-V4**).

## What problem it solves
It eliminates centralized cloud vendor lock-in, single-region outages, and exorbitant egress bandwidth costs associated with traditional object storage providers (AWS S3, Google Cloud Storage). Storj provides client-side zero-knowledge encryption that prevents storage providers or intermediaries from inspecting stored data, while delivering high throughput via parallel multi-node streaming.

## Where it fits in the stack
**Category**: Services / Infrastructure & Object Storage. Storj serves as the primary distributed persistence and off-site backup layer for media libraries, database snapshots, model weight mirrors, and long-term agent memory archives accessed via [FastMCP 3.1](../tools/automation_orchestration/mcp.md) servers and [Rclone](rclone-automation.md).

## Typical use cases
- **Multi-Agent Memory & State Persistence**: Storing long-term reasoning traces and session logs for autonomous AI agents via FastMCP 3.1 S3 tools.
- **Model Weight Mirroring**: High-bandwidth distribution of open-weight LLM checkpoints (**Gemma 3**, **Qwen 3.8**, **Llama 4**) to edge nodes.
- **Encrypted Homelab Backups**: Secure off-site targets for [Paperless-ngx](paperless-ngx.md), [Nextcloud](nextcloud.md), and PostgreSQL database dumps.
- **Media Asset Streaming**: S3-compatible backend storage for [Jellyfin](jellyfin.md) or Plex media servers.
- **Storage Node Hosting**: Monetizing excess homelab drive space and network bandwidth by operating a Storj storage node.

## Strengths
- **Decentralized High Throughput**: Multi-node parallel downloads saturate high-speed connections faster than centralized single-region buckets.
- **Zero-Knowledge Privacy**: Data is encrypted client-side using local keys before leaving the machine.
- **Native S3 Compatibility**: Seamless drop-in replacement for AWS S3 using standard SDKs (`boto3`, `@aws-sdk/client-s3`) and Rclone.
- **Predictable & Fair Pricing**: No hidden API request fees and up to 80% lower egress costs compared to legacy hyperscalers.
- **Extreme Fault Tolerance**: Reed-Solomon erasure coding enables complete data reconstruction even if 50+ nodes go offline simultaneously.

## Limitations
- **Object-Only Workloads**: Designed exclusively for object storage; cannot host live relational database block storage directly.
- **Local CPU Overhead**: Client-side encryption and erasure-code chunking consume CPU during high-throughput uploads.
- **Node Vetting Period**: Newly created storage nodes require a multi-week vetting phase before receiving full bandwidth traffic.

## When to use it
- When requiring cost-effective, high-bandwidth object storage with zero egress price penalties.
- When off-site backup strategies demand zero-knowledge client-side encryption.
- When backing up or retrieving large model weights, dataset archives, or agent memory logs across distributed nodes.

## When not to use it
- For live block-level storage requirements (e.g., direct SQLite or PostgreSQL data directory mounts).
- In environments with unstable or severely bandwidth-capped internet connections.

## Getting started

### Docker Compose: Hosting a Storage Node
Contribute excess storage capacity to the Storj network:

```yaml
services:
  storagenode:
    image: storjlabs/storagenode:latest
    container_name: storagenode
    restart: unless-stopped
    stop_grace_period: 300s
    ports:
      - "28967:28967/tcp"
      - "28967:28967/udp"
      - "127.0.0.1:14002:14002"
    environment:
      - WALLET=0xYourEthereumOrSTORJWalletAddress
      - EMAIL=node-operator@example.com
      - ADDRESS=node.yourdomain.com:28967
      - STORAGE=2TB
    volumes:
      - ./identity:/app/identity
      - ./storage:/app/config
```

### Uplink CLI Setup
1. Download Uplink: `curl -L https://github.com/storj/storj/releases/latest/download/uplink_linux_amd64.zip -o uplink.zip && unzip uplink.zip`
2. Initialize access credentials: `./uplink setup`
3. Create bucket: `./uplink mb sj://agent-memory-archives`
4. Upload object: `./uplink cp memory-trace.json sj://agent-memory-archives/`

## CLI examples

```bash
# List all buckets on Storj network
uplink ls sj://

# Recursively mirror a local backup folder to Storj
uplink cp --recursive ./backups/ sj://homelab-backups/

# Generate a time-bound, read-only public sharing URL
uplink share sj://agent-memory-archives/trace-42.json --readonly --expire 24h

# Inspect Storage Node status dashboard
docker exec -it storagenode /app/dashboard.sh
```

## API examples

### Python: S3 Gateway Upload with Pydantic v2 Metadata Validation
Using `boto3` and Pydantic v2 to validate and upload agent memory archives to Storj:

```python
import boto3
from typing import Dict
from pydantic import BaseModel, Field, ValidationError

class StorjArchivePayload(BaseModel):
    bucket_name: str = Field(..., description="Target Storj S3 bucket name")
    object_key: str = Field(..., description="Destination S3 object key")
    content_type: str = Field("application/json", description="MIME content type")
    mcp_version: str = Field("3.1", description="FastMCP protocol version")
    tags: Dict[str, str] = Field(default_factory=dict, description="Custom metadata tags")

def upload_agent_archive(payload: dict, file_path: str):
    try:
        # Validate configuration using Pydantic v2
        config = StorjArchivePayload.model_validate(payload)

        # Initialize boto3 S3 client pointing to Storj S3 Gateway
        s3 = boto3.client(
            "s3",
            endpoint_url="https://gateway.storjshare.io",
            aws_access_key_id="YOUR_STORJ_ACCESS_KEY",
            aws_secret_access_key="YOUR_STORJ_SECRET_KEY"
        )

        s3.upload_file(
            file_path,
            config.bucket_name,
            config.object_key,
            ExtraArgs={
                "ContentType": config.content_type,
                "Metadata": {
                    "mcp-version": config.mcp_version,
                    **config.tags
                }
            }
        )
        print(f"Successfully uploaded {config.object_key} to Storj bucket {config.bucket_name}")
    except ValidationError as ve:
        print(f"Validation error: {ve}")
    except Exception as e:
        print(f"Storj upload error: {e}")

# Example payload invocation
payload_data = {
    "bucket_name": "agent-memory-archives",
    "object_key": "claude-5-1/session-20270107.json",
    "content_type": "application/json",
    "mcp_version": "3.1",
    "tags": {
        "agent": "claude-5-1",
        "status": "archived"
    }
}
```

## Related tools / concepts
- [Rclone](rclone-automation.md) — Multi-cloud sync tool for automated Storj transfers.
- [Paperless-ngx](paperless-ngx.md) — Off-site document storage backend target.
- [Jellyfin](jellyfin.md) — Media server capable of mounting Storj S3 buckets.
- [FastMCP](../tools/automation_orchestration/mcp.md) — Model Context Protocol for agentic storage operations.
- [Authentik](authentik.md) — Identity provider securing S3 gateway credentials.

## Sources / references
- [Storj Official Website](https://www.storj.io/)
- [Storj Developer Documentation](https://docs.storj.io/)
- [Storj GitHub Repository](https://github.com/storj/storj)
- [S3 Gateway Integration Guide](https://docs.storj.io/tools/s3-gateway)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
