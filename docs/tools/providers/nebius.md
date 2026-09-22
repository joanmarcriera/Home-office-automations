# Nebius Group

## What it is
Nebius Group (Nebius AI Cloud) is an AI infrastructure and cloud platform provider delivering high-performance GPU clusters (NVIDIA H100, H200, B200), managed Kubernetes, managed databases, and AI developer services (including [Tavily](tavily.md) for agentic web search). As of early January 2027, Nebius operates enterprise AI data centers across Europe and North America, supporting frontier model training, fine-tuning, and high-throughput FastMCP 3.1 inference workloads.

## What problem it solves
Training frontier models and deploying multi-agent applications requires specialized AI cloud infrastructure that traditional hyperscalers often struggle to deliver efficiently:
- **GPU Cluster Orchestration**: Delivers ultra-low latency InfiniBand inter-node connections for distributed model training (PyTorch, DeepSpeed).
- **Integrated Agent Services**: Hosts agentic search capabilities through parent ownership of [Tavily](tavily.md).
- **Cost-Optimized AI Compute**: Offers competitive GPU instance rates with flexible commitment terms for AI startups and enterprise AI labs.
- **FastMCP 3.1 & Model Serving**: Managed Slurm, Kubernetes, and inference server deployments optimized for FastMCP 3.1 tool-calling streaming APIs.

## Where it fits in the stack
**Providers / AI Cloud Infrastructure**. Nebius sits alongside GPU cloud providers (Lambda Labs, CoreWeave, RunPod, AWS Bedrock) and specialized AI service stacks.

## Typical use cases
- **Frontier LLM Training & Fine-Tuning**: Running large-scale distributed training jobs using Axolotl, Llama-Factory, or PyTorch FSDP across NVIDIA H100/B200 clusters.
- **Agentic Search Integration**: Deploying agent search workloads via Tavily API hosted on Nebius AI Cloud.
- **High-Throughput Inference Clusters**: Provisioning vLLM or Aphrodite Engine deployments on Nebius Kubernetes with FastMCP 3.1 streaming support.
- **Private Enterprise Deployment**: Hosting air-gapped AI workloads with GDPR and SOC2 compliance.

## Strengths
- **Bare-Metal & Managed GPU Compute**: Native InfiniBand connectivity with minimal virtualization overhead.
- **Developer-Friendly API & CLI**: Infrastructure provisioning via Terraform, Ansible, and the `nebius` CLI.
- **Ecosystem Integration**: Native parent-company integration with Tavily AI agent search services.
- **High Availability**: Redundant Tier-3 data centers across major European and American regions.

## Limitations
- **Focus on AI Compute**: Optimized specifically for AI/ML workloads rather than general web app hosting or legacy enterprise IT services.
- **Regional Footprint**: Geographic availability expands rapidly but is concentrated in key AI cloud hubs.

## When to use it
- When requiring multi-GPU or multi-node clusters for LLM training and fine-tuning.
- When seeking a cloud provider with native integration for agentic web search (Tavily).
- When looking for cost-effective NVIDIA H100/B200 GPU compute with InfiniBand interconnects.

## When not to use it
- When hosting general web applications, traditional monolithic SQL databases, or legacy non-AI enterprise software.
- When requiring local on-premise deployments without public cloud interconnects.

## Getting started
1. Create a Nebius AI Cloud account at [nebius.com](https://nebius.com).
2. Install the Nebius CLI or Terraform provider.
3. Authenticate with your cloud credentials: `nebius auth login`.

## CLI examples

### Authenticating via Nebius CLI
```bash
nebius auth login --iam-token $NEBIUS_IAM_TOKEN
```

### Listing Available GPU Instances via CLI
```bash
nebius compute instance list --folder-id $NEBIUS_FOLDER_ID
```

## API examples

### Provisioning a Nebius GPU Instance via Terraform
```hcl
terraform {
  required_providers {
    nebius = {
      source = "nebius/nebius"
      version = ">= 0.4.0"
    }
  }
}

provider "nebius" {
  region = "eu-west-1"
}

resource "nebius_compute_instance" "gpu_node" {
  name        = "llm-training-h100-node"
  zone        = "eu-west-1-a"
  platform_id = "gpu-h100-sxm5"

  resources {
    cores  = 64
    memory = 512
    gpus   = 8
  }

  boot_disk {
    initialize_params {
      image_id = "ubuntu-24-04-cuda-12-8"
      size     = 1000
    }
  }

  network_interface {
    subnet_id = "subnet-ai-cluster-01"
    nat       = true
  }
}
```

### Checking Nebius API Service Health with Python
```python
import requests

NEBIUS_API_KEY = "your_nebius_cloud_api_key"
HEADERS = {
    "Authorization": f"Bearer {NEBIUS_API_KEY}",
    "Content-Type": "application/json"
}

# Fetch active GPU compute clusters
response = requests.get("https://api.nebius.cloud/v1/compute/instances", headers=HEADERS)
if response.status_code == 200:
    instances = response.json().get("instances", [])
    print(f"Active Nebius GPU Instances: {len(instances)}")
    for inst in instances:
        print(f" - ID: {inst['id']} | Status: {inst['status']} | GPU Type: {inst.get('gpu_type')}")
else:
    print(f"Failed to query Nebius API: {response.status_code}")
```

## Related tools / concepts
- [Tavily](tavily.md)
- [vLLM](../infrastructure/vllm.md)
- [DeepSpeed](../frameworks/deepspeed.md)
- [Axolotl](../frameworks/axolotl.md)
- [CoreWeave](coreweave.md)

## Sources / references
- [Nebius Official Website](https://nebius.com)
- [Nebius Cloud Documentation](https://docs.nebius.com/)
- [Tavily Acquisition Notice](https://nebius.com/news/tavily-acquisition)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
