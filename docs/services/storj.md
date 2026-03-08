# Storj

Storj is a decentralized cloud storage provider.

## Description
It offers S3-compatible storage that is distributed across thousands of nodes worldwide, providing high reliability and security.

## When to use it
- When you need secure, decentralized cloud storage with S3 compatibility.
- When you want to avoid single-provider lock-in and benefit from a distributed network.
- When you are looking for cost-effective alternatives to traditional cloud providers like AWS or Google Cloud.

## When not to use it
- When your application requires ultra-low latency (ms) and very high-speed data access.
- When you prefer a centralized, single-provider storage solution.
- For workloads that don't benefit from a decentralized architecture.

## Getting started

### Installation
The `uplink` CLI is the official tool for interacting with the Storj network. To install it on Linux:

```bash
curl -L https://github.com/storj/storj/releases/latest/download/uplink_linux_amd64.zip -o uplink.zip
unzip uplink.zip
sudo mv uplink /usr/local/bin/
```

### Configuration
After installation, configure the CLI with your access grant:

```bash
# Import an access grant
uplink access import main <your_access_grant_string>
```

## CLI examples
The `uplink` CLI supports common object storage operations:

```bash
# List all buckets
uplink ls

# List objects in a bucket
uplink ls sj://my-bucket

# Upload a file to a bucket
uplink cp /path/to/local-file.txt sj://my-bucket/remote-file.txt

# Download a file from a bucket
uplink cp sj://my-bucket/remote-file.txt ./local-file.txt
```

## API examples
Storj is S3-compatible, so you can use standard libraries like `boto3` in Python:

```python
import boto3

# Configure the S3 client for Storj
s3 = boto3.client(
    "s3",
    endpoint_url="https://gateway.storjshare.io",
    aws_access_key_id="<your_access_key>",
    aws_secret_access_key="<your_secret_key>"
)

# List objects in a bucket
response = s3.list_objects_v2(Bucket="my-bucket")
for obj in response.get("Contents", []):
    print(obj["Key"])
```

## Links
- [Official Website](https://www.storj.io/)
- [Storj Documentation](https://docs.storj.io/)

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
- [S3 Compatibility](https://storj.dev/learn/concepts/s3-compatibility)
