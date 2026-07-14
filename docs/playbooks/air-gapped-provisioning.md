# Playbook: Air-gapped Provisioning

## What it is
The Air-gapped Provisioning playbook defines the workflow for securely transferring and verifying software artifacts (LLM models, GGUFs, [Kiwix](../services/kiwix.md) ZIMs, Docker images) onto a physically disconnected ("air-gapped") server. It relies on a "Download Once, Sneakernet, Verify" strategy to ensure system integrity without internet access.

## What problem it solves
It solves the "Bootstrapping at the Edge" problem where a server requires high-bandwidth data but lacks a persistent or secure internet connection. Specifically, it addresses:
- **Security Isolation**: Provisioning systems that cannot be connected to the internet for security reasons.
- **Limited Connectivity**: Setting up systems in remote areas with no or expensive internet access.
- **Predictable Environment**: Ensuring the exact same model or knowledge version is deployed across multiple air-gapped nodes.
- **Audit Trails**: Providing a verifiable manifest of all data entering the secure environment.

## Where it fits in the stack
**Category**: Playbook / Infrastructure. It acts as the **bridge** between the internet-connected "Inlet" machine and the air-gapped "Private" machine.

## Typical use cases
- **Ollama Model Sneakernet**: Downloading a 70B parameter model once and transferring it via external drive to an air-gapped Mac Studio.
- **Kiwix Knowledge Update**: Pre-staging the latest English Wikipedia ZIM (100GB+) for offline search.
- **Docker Image Sideloading**: Saving Docker images as `.tar` files to be loaded onto a disconnected cluster.
- **Firmware & OS Updates**: Transferring critical security patches to air-gapped infrastructure.

## Strengths
- **Maximum Security**: The air-gapped machine remains untethered from the internet.
- **Bandwidth Efficient**: Only downloads what is necessary; no repeated downloads for multi-node setups.
- **Verifiable**: Uses SHA256 checksums to ensure data wasn't corrupted or tampered with during transit.
- **Resilient**: Not affected by ISP outages or cloud service blocks.

## Limitations
- **High Latency**: The "human transport" (sneakernet) speed is the primary bottleneck.
- **Storage Requirement**: Requires large external drives (2TB+) to move modern models and ZIMs.
- **Manual Effort**: Requires physical presence at both the source and destination machines.
- **Version Stale-ness**: Knowledge bases (Kiwix) and models are only as current as the last transfer.

## When to use it
- When setting up a [Fully Offline Assistant](fully-offline-assistant.md).
- In secure environments (financial, research, home security) where internet access is prohibited.
- For disaster preparedness kits (Survivalist Tech Stack).

## When not to use it
- When a fast, reliable, and secure internet connection is available.
- For small files or updates where the overhead of a physical transfer is excessive.

## Getting started

### 1. Identify and Download (Connected Machine)
On a machine with internet access, download the required artifacts:
```bash
# Download Ollama model
ollama pull gemma3-27b-it
# Download Kiwix ZIM
wget https://download.kiwix.org/zim/wikipedia_en_all_maxi.zim
```

### 2. Export and Hash
Export the artifacts and generate checksums:
```bash
# Export Ollama model (manual copy of ~/.ollama/models)
tar -cvf gemma3.tar ~/.ollama/models/blobs
# Generate checksum
sha256sum gemma3.tar > gemma3.tar.sha256
```

### 3. Transfer (Sneakernet)
Copy the `.tar` and `.sha256` files to a formatted external drive (exFAT or ext4).

### 4. Verify and Import (Air-gapped Machine)
Mount the drive and verify integrity:
```bash
sha256sum -c gemma3.tar.sha256
# If OK, extract to the local Ollama directory
tar -xvf gemma3.tar -C ~/.ollama/models/
```

## CLI examples

### 1. Saving a Docker Image for Transfer
```bash
docker save ghcr.io/open-webui/open-webui:main > open-webui.tar
```

### 2. Loading a Docker Image Offline
```bash
docker load < open-webui.tar
```

### 3. Verifying a Kiwix ZIM file
```bash
sha256sum -c wikipedia_en_all_maxi.zim.sha256
```

## API examples

### Python: Automated Checksum Generation for Manifests
Automate the creation of a transfer manifest.
```python
import hashlib
import json
import os

def generate_manifest(directory):
    manifest = {}
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            sha256_hash = hashlib.sha256()
            with open(path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            manifest[filename] = sha256_hash.hexdigest()

    with open("transfer_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

generate_manifest("/mnt/sneakernet_drive")
```

### Verification Script (Air-gapped Machine)
A script to be run on the destination to verify the entire drive.
```python
import json
import hashlib

def verify_manifest(manifest_path):
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    for filename, expected_hash in manifest.items():
        # ... (similar hashing logic as above)
        if actual_hash == expected_hash:
            print(f"✅ {filename} verified.")
        else:
            print(f"❌ {filename} FAILED verification!")
```

## Related tools / concepts
- [Kiwix](../services/kiwix.md) — Offline knowledge libraries.
- [Ollama](../services/ollama.md) — Local inference engine.
- [Docker](../tools/infrastructure/docker.md) — Containerization for offline deployment.
- [Fully Offline Assistant](fully-offline-assistant.md) — The target architecture.
- [MinIO](../tools/intake_storage/minio.md) — S3-compatible storage for local mirrors.
- [Syncthing](../services/syncthing.md) — Semi-automated local sync.
- [Rclone](../services/rclone-automation.md) — Moving files between storage providers.

## Sources / References
- [Ollama: Custom Model Guide](https://github.com/ollama/ollama/blob/main/docs/import.md)
- [Docker: Save and Load Images](https://docs.docker.com/engine/reference/commandline/save/)
- [Kiwix: Offline Content Downloads](https://wiki.kiwix.org/wiki/Content_in_all_languages)
- [NIST Guide to Air-Gapped Network Security](https://csrc.nist.gov/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
