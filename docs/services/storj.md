# Storj

Storj is a decentralized cloud storage provider.

## Description
It offers S3-compatible storage that is distributed across thousands of nodes worldwide, providing high reliability and security.

## When to use it
- When you need high-performance, decentralized object storage.
- When you want to reduce storage costs compared to traditional cloud providers.
- When building applications that require S3 compatibility.

## When not to use it
- When you require block storage or file system mounting (use for object storage).
- If your workload requires absolute single-region data residency.

## Getting started

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
The `uplink` tool supports standard object storage operations. Use the `sj://` protocol for buckets.

```bash
# Create a new bucket
uplink mb sj://my-bucket

# Upload a local file with a custom expiration date
uplink cp my-local-file.txt sj://my-bucket/ --expires 2026-12-31T23:59:59Z

# List objects and their sizes in a bucket
uplink ls sj://my-bucket/
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
- [S3 / S3-Compatible Storage](../tools/intake_storage/s3-storage.md) (Core protocol)
- [Rclone Automation](rclone-automation.md) (Common tool for Storj sync)
- [Syncthing](syncthing.md) (Local sync alternative)
- [Nextcloud](nextcloud.md) (Can use Storj as external storage)
- [n8n](n8n.md) (For automating bucket operations)

## Backlog
- Configure as a backup target for Rclone.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-12

## Sources / References
- https://www.storj.io/
- https://aws.amazon.com/s3/
- https://www.backblaze.com/cloud-storage
- https://docs.storj.io/
