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

## CLI examples
The `uplink` tool supports standard object storage operations:

```bash
# List all buckets
uplink ls

# Upload a local file to a bucket
uplink cp my-local-file.txt sj://my-bucket/

# Create a shareable URL for an object
uplink share sj://my-bucket/my-local-file.txt
```

## API examples
Use the `boto3` library to interact with Storj via its S3-compatible Gateway:

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
    print(obj["Key"])
```

## Links
- [Official Website](https://www.storj.io/)

## Alternatives
- [Amazon S3](https://aws.amazon.com/s3/)
- [Backblaze B2](https://www.backblaze.com/cloud-storage)

## Backlog
- Configure as a backup target for Rclone.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://www.storj.io/
- https://aws.amazon.com/s3/
- https://www.backblaze.com/cloud-storage
- https://docs.storj.io/
