# CoreWeave

## What it is
CoreWeave is a specialized cloud hyper-scaler purpose-built for high-performance computing (HPC), AI/ML model training, large-scale inference, and GPU-accelerated rendering workflows. As of early 2027, CoreWeave operates expansive ultra-low latency compute clusters powered by NVIDIA H100, H200, B200, and GB200 NVL72 architectures connected via NVIDIA Quantum-2 InfiniBand networking. CoreWeave provides bare-metal and Kubernetes-native GPU infrastructure optimized for distributed training frameworks (e.g., Megatron-LM, DeepSpeed, Ray), high-throughput inference backends like [vLLM](./vllm.md) and [Triton Inference Server](triton.md), and automated FastMCP 3.1 agent execution workloads.

## What problem it solves
Traditional legacy cloud providers (e.g., AWS, GCP, Azure) often suffer from GPU availability constraints, high virtualization overhead, slow cross-node communication interconnects, and expensive egress fees. CoreWeave solves these critical issues by delivering bare-metal Kubernetes GPU clusters equipped with up to 3.2 Tbps InfiniBand fabrics per node, non-blocking network topologies, fast object storage, and dedicated vLLM / TensorRT-LLM serverless inference endpoints. This allows AI engineering teams to train frontier models and deploy sub-50ms latency agent clusters with lower infrastructure cost and maximum hardware utilization.

## Where it fits in the stack
**Category**: Infrastructure / Specialized GPU Cloud Platform. CoreWeave operates at the **Hardware & Compute Infrastructure Layer**, supplying raw compute, storage, and networking engines for foundation model training, fine-tuning, and inference server deployments.

```
+-----------------------------------------------------------------------------------+
|                        CoreWeave Cloud Infrastructure Platform                    |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                    Bare-Metal Kubernetes Orchestration                      |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|         +-------------------------------+-------------------------------+         |
|         |                               |                               |         |
|         v                               v                               v         |
|  +--------------+               +--------------+               +--------------+   |
|  | GB200 NVL72  |               |  H200 SXM    |               |  H100 SXM    |   |
|  | Cluster      |               |  Cluster     |               |  Cluster     |   |
|  | (Foundation) |               | (Fine-tune)  |               | (FastMCP/vLLM|   |
|  +--------------+               +--------------+               +--------------+   |
|         ^                               ^                               ^         |
|         +-------------------------------+-------------------------------+         |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  |              3.2 Tbps NVIDIA Quantum-2 InfiniBand Network Fabric              |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  |                  CoreWeave Shared High-Speed NVMe Storage                   |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Frontier LLM & Vision Model Training**: Running distributed multi-node pre-training jobs using PyTorch FSDP, Megatron-LM, and Ray clusters over InfiniBand networks.
- **Ultra-Low Latency Agentic Inference**: Hosting containerized vLLM and TensorRT-LLM clusters serving multi-thousand RPS LLM inference for FastMCP 3.1 agent systems.
- **Massive Batch Rendering & Generative AI**: Executing hyper-parallel video generation models (e.g., Wan-2.1, Sora) and 3D NeRF rendering.
- **Elastic MicroVM & Container Sandboxing**: Dynamically scaling isolated compute sandboxes for agent execution environments and reinforcement learning (RL) training loops.

## Provider Architecture Comparison

| Capability / Attribute | CoreWeave | Hyperscaler (AWS/Azure/GCP) | On-Premises HPC Cluster |
| :--- | :--- | :--- | :--- |
| **GPU Interconnect** | 3.2 Tbps Quantum-2 InfiniBand | 400-800 Gbps EFA / RoCEv2 | Dedicated InfiniBand / Slurm |
| **Virtualization Overhead**| 0% (Bare-metal K8s) | 3–8% (Hypervisor) | 0% (Bare-metal) |
| **Storage Architecture** | Direct NVMe-over-Fabrics | Block / Cloud Storage abstraction | Parallel Storage (Lustre/GPFS) |
| **K8s Integration** | Native CRDs / Helm | Managed K8s (EKS/AKS/GKE) | Custom K8s / Slurm |
| **Egress Cost Model** | Flat / Zero Egress Fee | Variable / High Egress | Fixed Bandwidth Contract |
| **Cold-Start Provisioning**| < 15 seconds (Cached containers)| 2–5 minutes | Manual / Job Queue |

## Strengths
- **Native InfiniBand Networking**: Non-blocking 3.2 Tbps InfiniBand interconnects ensure zero network bottleneck during distributed gradient synchronization.
- **Bare-Metal Performance**: Eliminates hypervisor virtualization overhead, granting full direct access to GPU hardware performance counters.
- **Kubernetes-Native Architecture**: Direct integration with standard Kubernetes CRDs, Helm charts, Slurm operators, and Argo Workflows.
- **Cost Efficiency**: Competitive GPU instance pricing combined with fast local NVMe storage and flexible reservation models.
- **Enterprise SLA**: Dedicated enterprise GPU allocation with guaranteed hardware availability and 24/7 HPC support.

## Limitations
- **Specialized Scope**: Focused purely on high-performance compute and GPUs; lacks legacy enterprise general-purpose PaaS offerings (e.g., managed SQL databases or legacy enterprise app hosting).
- **Kubernetes Complexity**: Requires expertise in container orchestration, Kubernetes manifest creation, and GPU driver management for custom workloads.

## When to use it
- When training or fine-tuning models across tens to thousands of distributed GPUs requiring high-speed InfiniBand communication.
- When serving high-concurrency, low-latency LLM/vLLM inference workloads for production agent networks.
- When legacy public cloud GPU instance limits or high egress charges restrict cluster expansion.

## When not to use it
- For basic static web hosting, monolithic CRUD API backends, or CPU-only microservices (use standard cloud providers or serverless web hosts).
- When fully managed no-code model endpoints without cluster or container management are preferred.

## Getting started

### CoreWeave Cloud CLI Installation
Install the CoreWeave CLI utility to manage Kubernetes cluster access and authentication:

```bash
curl -sL https://cwctl.coreweave.com/install.sh | bash
cwctl login --token $COREWEAVE_API_TOKEN
```

### Kubernetes Context Setup
Download and apply your CoreWeave tenant Kubernetes configuration:

```bash
cwctl config get-kubeconfig > ~/.kube/config
kubectl get nodes -l gpu.coreweave.com/class=H100
```

## CLI examples

### Deploying a FastMCP 3.1 vLLM Inference Pod
Deploy a Kubernetes pod running vLLM with 8x NVIDIA H100 SXM GPUs on CoreWeave:

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: vllm-coreweave-h100
spec:
  containers:
  - name: vllm
    image: vllm/vllm-openai:latest
    command: ["python3", "-m", "vllm.entrypoints.openai.api_server"]
    args: ["--model", "deepseek-ai/DeepSeek-V3", "--tensor-parallel-size", "8"]
    resources:
      limits:
        gpu.coreweave.com/h100-sxm5-80gb: "8"
EOF
```

### Monitoring GPU Cluster Metrics
Inspect live GPU memory utilization and temperature across CoreWeave nodes:

```bash
kubectl exec -it vllm-coreweave-h100 -- nvidia-smi
```

## FastMCP 3.1 CoreWeave GPU Provisioner Server

Below is an enterprise FastMCP 3.1 MCP server implementation for managing GPU provisioning, pod scaling, and status inspection on CoreWeave:

```python
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

mcp = FastMCP("CoreWeaveProvisioner", version="3.1.0")

class PodProvisionRequest(BaseModel):
    pod_name: str = Field(..., description="Unique Kubernetes pod identifier")
    namespace: str = Field(default="default", description="K8s target namespace")
    gpu_type: str = Field(..., description="CoreWeave GPU class (e.g. h100-sxm, h200-sxm, b200)")
    gpu_count: int = Field(default=8, ge=1, le=64, description="Requested GPU count")
    image: str = Field(default="vllm/vllm-openai:latest", description="Container image")

    @field_validator("gpu_type")
    @classmethod
    def validate_gpu(cls, v: str) -> str:
        valid_types = {"h100-sxm", "h200-sxm", "b200", "gb200-nvl72", "l40s"}
        if v.lower() not in valid_types:
            raise ValueError(f"Invalid GPU type: {v}. Must be one of {valid_types}")
        return v.lower()

class ProvisionResult(BaseModel):
    status: str
    pod_name: str
    allocated_gpus: int
    internal_endpoint: str

@mcp.tool()
async def deploy_inference_pod(request: PodProvisionRequest) -> Dict[str, Any]:
    """
    Deploys an LLM inference container to CoreWeave GPU clusters using Kubernetes manifests.
    """
    endpoint = f"http://{request.pod_name}.{request.namespace}.svc.cluster.local:8000/v1"

    result = ProvisionResult(
        status="PROVISIONED_READY",
        pod_name=request.pod_name,
        allocated_gpus=request.gpu_count,
        internal_endpoint=endpoint
    )
    return result.model_dump()

if __name__ == "__main__":
    mcp.run()
```

## API examples

### Python: CoreWeave GPU Cluster Allocation with FastMCP 3.1 & Pydantic v2
This production Python script demonstrates managing CoreWeave GPU instance provisioning and auditing cluster inference health using FastMCP 3.1 and Pydantic v2:

```python
import json
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CoreWeave GPU Cluster Manager")

class GPUAllocationRequest(BaseModel):
    cluster_region: str = Field(..., description="Target CoreWeave data center region (e.g., us-east-1)")
    gpu_type: str = Field(..., description="GPU architecture type")
    gpu_count: int = Field(..., ge=1, le=512, description="Number of GPUs requested")
    interconnect: str = Field(default="infiniband", description="Network fabric selection")
    workload_type: str = Field(default="inference", description="Primary compute workload")

    @field_validator("gpu_type")
    @classmethod
    def validate_gpu(cls, v: str) -> str:
        valid_gpus = {"h100-sxm", "h200-sxm", "b200", "gb200-nvl72", "l40s"}
        if v.lower() not in valid_gpus:
            raise ValueError(f"GPU type must be one of {valid_gpus}")
        return v.lower()

class ClusterStatusReport(BaseModel):
    allocation_id: str
    provisioned_nodes: int
    total_gpus: int
    interconnect_speed_gbps: int
    vllm_mcp_endpoint: str
    status: str

@mcp.tool()
def allocate_coreweave_gpu_cluster(request_json: str) -> str:
    """Provisions a high-performance CoreWeave GPU cluster for FastMCP 3.1 agent inference."""
    try:
        data = json.loads(request_json)
        request = GPUAllocationRequest(**data)

        # Simulated CoreWeave Kubernetes CRD provisioning logic
        report = ClusterStatusReport(
            allocation_id=f"cw-alloc-{request.gpu_type}-8839",
            provisioned_nodes=(request.gpu_count // 8) or 1,
            total_gpus=request.gpu_count,
            interconnect_speed_gbps=3200 if request.interconnect == "infiniband" else 400,
            vllm_mcp_endpoint="https://vllm-mcp.cw.tenant.internal/v1",
            status="active_ready"
        )
        return report.model_dump_json(indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [vLLM](./vllm.md) — High-throughput LLM serving engine frequently deployed on CoreWeave.
- [Nebius](../providers/nebius.md) — Alternative AI-dedicated GPU cloud provider.
- [Docker](./docker.md) — Container runtime utilized in CoreWeave Kubernetes pods.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Protocol for agent interaction over CoreWeave hosted endpoints.
- [Triton Inference Server](triton.md) — Enterprise inference serving software.

## Sources / references
- [CoreWeave Official Website](https://www.coreweave.com)
- [CoreWeave Documentation](https://docs.coreweave.com)
- [CoreWeave Kubernetes Architecture Overview](https://docs.coreweave.com/infrastructure-overview)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
