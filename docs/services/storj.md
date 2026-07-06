# Storj

## What it is
Storj is a decentralized cloud storage platform that provides high-performance, S3-compatible object storage. Unlike traditional cloud providers, Storj distributes data across a global network of thousands of independent nodes. In the July 2026 landscape, Storj has become a cornerstone of the "Agentic Infrastructure," offering the low-latency, high-availability storage required for frontier AI models like **Gemma 3** and autonomous agents. It is licensed under AGPL-3.0 and operates on a usage-based pricing model with a generous free tier.

## What problem it solves
Centralized storage providers (AWS S3, Google Cloud Storage) represent single points of failure and often involve high egress costs. Storj eliminates these issues by encrypting, splitting, and distributing data globally. It solves the "egress tax" problem while ensuring maximum privacy and resilience against regional outages, making it ideal for distributed AI workloads and private homelab backups.

## Where it fits in the stack
**Category**: Service / Infrastructure / Storage. Storj serves as the **distributed persistence layer**, providing a scalable and cost-effective backend for media archives, model weights, and agentic memory stores. It integrates with the **MCP 3.0 Task Protocol** for standardized state persistence across distributed agent clusters.

## Typical use cases
- **Distributed Model Storage**: Hosting LLM weights (**Gemma 3**, Llama 4) for rapid edge deployment.
- **Agentic Memory Archival**: Storing long-term reasoning traces and session logs for autonomous agents using MCP 3.0.
- **Private Homelab Backups**: Off-site, encrypted backups for [Paperless-ngx](paperless-ngx.md) and [Nextcloud](nextcloud.md).
- **High-Performance Content Delivery**: Serving media assets for [Plex](plex.md) or [Jellyfin](jellyfin.md) with global low-latency access.
- **Excess Storage Monetization**: Contributing idle local storage to the Storj network via a Storage Node.

## Strengths
- **Decentralized Performance**: Parallel downloads from multiple edge nodes often outperform centralized CDNs.
- **Zero-Knowledge Encryption**: Data is encrypted on the client-side; only the owner holds the keys.
- **S3 Compatibility**: Seamless integration with existing tools like [Rclone](rclone-automation.md) and [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).
- **High Availability**: Erasure coding (e.g., 29/80) ensures data is retrievable even if dozens of nodes go offline simultaneously.
- **Cost Efficiency**: Significant savings on storage and egress compared to traditional cloud providers.

## Limitations
- **Object Storage Focus**: Not designed for low-latency block storage or direct database file mounting.
- **Client Processing**: Encryption and erasure coding require local CPU cycles during upload/download.
- **Node Reputation**: Initial node setup requires a "vetting" period before significant traffic is received.

## When to use it
- When you need high-performance, decentralized object storage with global availability for **Gemma 3** weights.
- To reduce cloud storage costs, particularly egress fees for frequently accessed data.
- For privacy-sensitive data where zero-knowledge encryption is a mandatory requirement.
- As a resilient off-site backup target for local homelab services.

## When not to use it
- For workloads requiring block-level storage (e.g., running a live database file).
- If your environment lacks a stable, high-bandwidth internet connection.

## Getting started

### Docker: Running a Storage Node
Contribute storage to the network using the official Docker image:

```bash
docker run -d --restart unless-stopped --stop-timeout 300 \
  -p 28967:28967/tcp \
  -p 28967:28967/udp \
  -p 127.0.0.1:14002:14002 \
  -e WALLET="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
  -e EMAIL="user@example.com" \
  -e ADDRESS="domain.ddns.net:28967" \
  -e STORAGE="2TB" \
  --mount type=bind,source="/path/to/identity",target=/app/identity \
  --mount type=bind,source="/path/to/storage",target=/app/config \
  --name storagenode storjlabs/storagenode:latest
```

### Hello World (CLI)
1. Install the `uplink` CLI: `curl -L https://github.com/storj/storj/releases/latest/download/uplink_linux_amd64.zip -o uplink.zip && unzip uplink.zip`.
2. Configure credentials: `uplink setup`.
3. Create a bucket: `uplink mb sj://my-homelab-backup`.
4. Upload a file: `uplink cp local-file.txt sj://my-homelab-backup/`.

## CLI examples
The `uplink` tool provides a powerful interface for bucket management.

```bash
# List all buckets
uplink ls sj://

# Recursively copy a directory to Storj
uplink cp --recursive ./my-data/ sj://my-bucket/

# Create a shareable, public link for an object
uplink share sj://my-bucket/public-image.png --readonly

# Check node status (if running a storage node)
docker exec -it storagenode /app/dashboard.sh
```

## API examples
Storj is fully S3-compatible, allowing use of standard libraries like `boto3`.

### Python: S3 Gateway Integration
```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="https://gateway.storjshare.io",
    aws_access_key_id="YOUR_ACCESS_KEY",
    aws_secret_access_key="YOUR_SECRET_KEY"
)

# Upload an agent's reasoning trace (MCP 3.0 compatible)
s3.upload_file("trace.json", "agent-memory", "session-42/trace.json")

# List files in a prefix
response = s3.list_objects_v2(Bucket="agent-memory", Prefix="session-42/")
for obj in response.get("Contents", []):
    print(f"Stored Object: {obj['Key']}")
```

## Related tools / concepts
- [Rclone](rclone-automation.md) — The preferred tool for syncing local data to Storj.
- [Nextcloud](nextcloud.md) — Can use Storj as a primary or external storage backend.
- [Paperless-ngx](paperless-ngx.md) — For off-site archival of sensitive documents.
- [Syncthing](syncthing.md) — For peer-to-peer sync that can be complemented by Storj backups.
- [n8n](n8n.md) — For automating data movement between Storj and other services.
- [BorgBackup](borg.md) — For deduplicated, encrypted backups that can be stored on Storj via S3.
- [Authentik](authentik.md) — For securing access to the Storj management console.
- [Tailscale](tailscale.md) — For secure access to storage nodes in a private mesh.
- [Plex](plex.md) — Can mount Storj buckets for media streaming.
- [Jellyfin](jellyfin.md) — Alternative media server for Storj-hosted content.
- [Ollama](ollama.md) — For running AI models that utilize Storj for weight storage.
- [MCP 3.0](../tools/automation_orchestration/mcp.md) — The protocol used for agentic storage orchestration.

## Sources / references
- [Official Website](https://www.storj.io/)
- [Storj Documentation](https://docs.storj.io/)
- [Storj GitHub](https://github.com/storj/storj)
- [S3 Compatibility Guide](https://docs.storj.io/tools/s3-gateway)

## Contribution Metadata
- Last reviewed: 2026-07-06
- Confidence: high
