# Storj

## What it is
Storj is a decentralized cloud storage provider that offers S3-compatible object storage. Unlike traditional cloud providers, Storj distributes data across thousands of independent nodes worldwide, ensuring high reliability, security, and performance.

## What problem it solves
It provides a cost-effective and highly private alternative to centralized object storage (like AWS S3). By using client-side encryption and distributed storage, it eliminates single points of failure and significantly reduces the risk of data breaches or downtime associated with single-region providers.

## Where it fits in the stack
**Category**: Service / Infrastructure / Storage. Storj acts as a remote object storage tier for backups, media hosting, or application data.

## Typical use cases
- Off-site backups for homelab data.
- Hosting static assets for websites or applications.
- Sharing large files securely without centralized tracking.
- Contributing excess local storage to the network to earn rewards.

## Strengths
- **Decentralized Architecture**: No single point of failure.
- **S3 Compatibility**: Works with existing S3-compatible tools and libraries.
- **Security**: Default client-side encryption.
- **Cost**: Often significantly cheaper than major cloud providers for both storage and egress.

## Limitations
- **Object Storage Only**: Not suitable for direct block storage or low-latency database files.
- **Internet Dependency**: Requires a stable internet connection for all operations.

## When to use it
- When you need high-performance, decentralized object storage.
- When you want to reduce storage costs compared to traditional cloud providers.
- When building applications that require S3 compatibility.

## When not to use it
- When you require block storage or file system mounting (use for object storage).
- If your workload requires absolute single-region data residency.

## Getting started

### Docker installation
Running a Storj node via Docker allows you to contribute storage to the network and earn rewards.

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

### Installation
Install the `uplink` CLI tool to manage your Storj buckets and objects:

```bash
curl -L https://github.com/storj/storj/releases/latest/download/uplink_linux_amd64.zip -o uplink.zip
unzip uplink.zip
sudo install uplink /usr/local/bin
```

### Setup
Configure the CLI with your Storj access credentials:

```bash
uplink setup
```

Follow the prompts to enter your access grant or API key.

### Hello World
1. Install and setup the `uplink` CLI as described above.
2. Create a new bucket: `uplink mb sj://hello-world`.
3. Create a small text file: `echo "Hello Storj" > hello.txt`.
4. Upload the file: `uplink cp hello.txt sj://hello-world/`.
5. Verify the upload: `uplink ls sj://hello-world/`.

## CLI examples

### Rclone Configuration
To use Storj as a backup target for Rclone (S3-compatible):
1. **Generate Credentials**: In the Storj console, create an S3 credential.
2. **Configure Rclone**:
```ini
[storj]
type = s3
provider = other
access_key_id = <your_access_key>
secret_access_key = <your_secret_key>
endpoint = https://gateway.storjshare.io
region = us1
```
3. **Verify**: `rclone lsd storj:`

The `uplink` tool supports standard object storage operations. Use the `sj://` protocol for buckets.

```bash
# Create a new bucket
uplink mb sj://my-bucket

# Upload a local file with a custom expiration date
uplink cp my-local-file.txt sj://my-bucket/ --expires 2026-12-31T23:59:59Z

# List objects and their sizes in a bucket
uplink ls sj://my-bucket/

# Share a specific path with a new access grant
uplink share sj://my-bucket/public-folder/ --readonly --not-after 2026-12-31T23:59:59Z
```

## API examples
Use the `boto3` library to interact with Storj via its S3-compatible Gateway.

### Python (Boto3)
```python
import boto3

# Configure the client for Storj S3 Gateway
s3 = boto3.client(
    "s3",
    endpoint_url="https://gateway.storjshare.io",
    aws_access_key_id="<your_access_key>",
    aws_secret_access_key="<your_secret_key>"
)

# Upload a file
s3.upload_file("local_image.png", "my-bucket", "cloud_image.png")

# List objects in a bucket
response = s3.list_objects_v2(Bucket="my-bucket")
for obj in response.get("Contents", []):
    print(f"Object: {obj['Key']}, Size: {obj['Size']} bytes")
```

## Links
- [Official Website](https://www.storj.io/)

## Related tools / concepts
- [S3 / S3-Compatible Storage](../tools/intake_storage/s3-storage.md)
- [Rclone Automation](rclone-automation.md)
- [Syncthing](syncthing.md)
- [Nextcloud](nextcloud.md)
- [n8n](n8n.md)
- [BorgBackup](borg.md)
- [MinIO](https://min.io/)
- [Backblaze B2](https://www.backblaze.com/b2/cloud-storage.html)
- [Paperless-ngx](paperless-ngx.md) — For off-site archival of sensitive documents.

## Backlog
- [ ] Perform quarterly technical freshness audit.
- [x] Configure as a backup target for Rclone.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-15

## Sources / References
- https://www.storj.io/
- https://aws.amazon.com/s3/
- https://www.backblaze.com/cloud-storage
- https://docs.storj.io/
