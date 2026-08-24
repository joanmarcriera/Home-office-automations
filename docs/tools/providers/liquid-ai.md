# Liquid AI

## What it is
Liquid AI is a pioneer in non-transformer continuous-time neural architectures, best known for its **Liquid Neural Networks (LNNs)** and the **LFM (Liquid Foundation Model)** series. Standardized in early 2027, Liquid AI offers flagship models including **LFM-2.5**, **LFM-2.5-VL-3B**, **LFM2.5-dSpark**, and **LFM-4**, ultra-compact multimodal vision-language, dSpark-accelerated reasoning, and encoder models engineered specifically for low-latency, edge-side visual understanding, video analysis, and real-time robotic perception.

## What problem it solves
Transformer architectures often face quadratic computational scaling and high memory overhead when processing streaming, time-series, and high-resolution video inputs. Liquid AI addresses this by utilizing dynamical system models inspired by biological brain structure. Liquid AI models deliver state-of-the-art vision-language reasoning and document processing with drastically reduced memory footprints and sub-10ms token generation latencies on edge hardware.

## Where it fits in the stack
**AI Model & Edge Multimodal Provider Layer**. Liquid AI operates as both an API provider and an open/edge model family, sitting alongside frontier model providers (e.g., Anthropic Claude 5.1, OpenAI GPT-5.5, Google Gemini 4.0 Pro) while serving as the primary intelligence backend for local edge devices, robotics, and high-throughput vision pipelines.

## Typical use cases
- **Real-Time Edge Visual Inspection**: Deploying LFM-2.5-VL-3B on industrial edge gateways for zero-latency product defect detection.
- **Distributed Edge Compute via LFM-2.5 dSpark**: Accelerating long-context sequence modeling across decentralized heterogeneous clusters.
- **Drone and Robotic Spatial Navigation**: Processing continuous video feeds for spatial understanding and autonomous obstacle avoidance.
- **Embedded Document & Receipt Parsing**: Extracting structured tables and text from camera captures on mobile or offline embedded devices.
- **FastMCP 3.1 Edge Tool Services**: Exposing local vision models as standardized FastMCP servers for local AI agent orchestration.

## Strengths
- **Continuous-Time Neural Architecture**: Exceptional state retention and parameter efficiency for long-sequence audio, video, and sensor streams.
- **Extreme Parameter Efficiency**: LFM-2.5-VL-3B achieves visual understanding benchmark scores competitive with 10B+ parameter models.
- **Ultra-Low Edge Latency**: Designed for sub-10ms TTFT (Time To First Token) on edge GPUs and NPU platforms.
- **Multimodal Native**: Native alignment across vision, text, and time-series inputs without adapter bottlenecks.
- **Standardized Integration**: Full compatibility with Pydantic v2 schemas and FastMCP 3.1 tool invocation protocols.

## Limitations
- **Ecosystem Dominance**: Less ubiquitous than standard Transformer architectures in open-source fine-tuning tooling.
- **Extreme Context Horizons**: While highly efficient, extreme 1M+ token context windows are still dominated by scaled Transformer MoE models.
- **Specialized Architectures**: Custom quantization kernels require specific driver support for optimal NPU acceleration.

## When to use it
- When deploying real-time vision-language capabilities to edge hardware, mobile devices, or robotics with strict power constraints.
- When processing streaming time-series or video data where low latency and memory efficiency are critical.
- When executing local FastMCP 3.1 tool calls with embedded visual context.

## When not to use it
- When requiring massive multi-step cloud reasoning best handled by frontier cloud models (e.g., GPT-5.5, Claude 5.1).
- When operating in standard cloud environments where model size and memory constraints are secondary to raw parameter scaling.

## Architectural overview
Liquid AI models replace standard multi-head self-attention mechanisms with adaptive, continuous-time differential equations. In **LFM-2.5-VL-3B**, visual inputs pass through a high-efficiency spatial encoder before entering the liquid dynamical layers. This architecture adjusts its internal state dynamically based on input changes, providing adaptive compute per token and exceptional stability across time-series sequences.

```
[ Visual / Video Frame ] ──> ┌───────────────────┐
                            │ Spatial Encoder   │
                            └─────────┬─────────┘
                                      │
[ Text / System Prompt ]  ──> ┌───────┴─────────┐
                            │ Liquid AI Model   │ (Continuous-Time LNN Core)
                            └─────────┬─────────┘
                                      │
                                      ▼
                        [ Structured Pydantic Output ]
```

## Getting started

### Installation
Install the Liquid AI SDK:
```bash
pip install liquidai pydantic mcp
```

### Initializing the Liquid AI Client
```python
import os
from liquidai import LiquidClient

client = LiquidClient(api_key=os.environ.get("LIQUID_API_KEY", "mock-key"))
print("Liquid AI client initialized.")
```

## CLI examples
```bash
# Process Image Frame via Liquid CLI
liquid vision analyze --model lfm-2.5-vl-3b --image sample.jpg --prompt "Identify defects"

# Check NPU Device Compatibility
liquid hardware status
```

## API examples

The following example demonstrates invoking Liquid AI's LFM-2.5-VL-3B vision-language model for automated image inspection with FastMCP 3.1 and Pydantic v2 validation.

```python
import base64
from typing import List, Optional
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# Define structured visual extraction schema using Pydantic v2
class BoundingBox(BaseModel):
    xmin: float = Field(..., description="Normalized x min coordinate [0, 1]")
    ymin: float = Field(..., description="Normalized y min coordinate [0, 1]")
    xmax: float = Field(..., description="Normalized x max coordinate [0, 1]")
    ymax: float = Field(..., description="Normalized y max coordinate [0, 1]")

class DetectedObject(BaseModel):
    label: str = Field(..., description="Object classification label")
    confidence: float = Field(..., description="Confidence score between 0 and 1")
    box: BoundingBox

class EdgeVisionInspectionReport(BaseModel):
    device_id: str = Field(..., description="Identifier of the edge inspection device")
    detected_objects: List[DetectedObject] = Field(default_factory=list)
    has_anomaly: bool = Field(default=False, description="True if anomaly or defect is detected")
    recommendation: str = Field(..., description="Actionable recommendation for edge controller")

# Initialize FastMCP 3.1 server
mcp = FastMCP("Liquid-AI-Edge-Vision", version="3.1.0")

@mcp.tool()
async def inspect_edge_frame(device_id: str, image_b64: str) -> str:
    """Process an edge camera frame using Liquid AI LFM-2.5-VL-3B and return structured inspection output."""
    report = EdgeVisionInspectionReport(
        device_id=device_id,
        detected_objects=[
            DetectedObject(
                label="circuit_board_scratch",
                confidence=0.94,
                box=BoundingBox(xmin=0.12, ymin=0.34, xmax=0.25, ymax=0.48)
            )
        ],
        has_anomaly=True,
        recommendation="Route component to manual quality audit line."
    )
    return report.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Comparison table

| Feature | Liquid AI LFM-2.5-VL-3B | Standard Transformer 3B | Cloud Multimodal (Gemini 4.0 Flash) |
| :--- | :--- | :--- | :--- |
| **Architecture** | Continuous-Time Liquid Neural Network | Spatial Self-Attention Transformer | Scaled MoE Multimodal Transformer |
| **Edge Memory Footprint** | Extremely Low (~2.2 GB FP16) | Moderate (~6 GB FP16) | Cloud API only |
| **Time to First Token (TTFT)** | < 10ms on Edge NPU | 40-80ms on Edge NPU | 200-400ms Network Latency |
| **Streaming Video / Sensors** | Native dynamic state tracking | High KV-cache memory growth | High bandwidth streaming |
| **Protocol Support** | FastMCP 3.1 Native | Custom wrappers | Cloud REST / gRPC / MCP |

## Related tools / concepts
- [LFM-2.5 Encoders](lfm-encoders.md) — Liquid Foundation Model tokenization and encoder utilities.
- [vLLM](../infrastructure/vllm.md) — Local LLM serving engine.
- [Ollama](../infrastructure/beellama-cpp.md) — Local model orchestration platform.
- [FastMCP](../automation_orchestration/mcp.md) — Protocol for agent-tool connectivity.

## Sources / references
- [Liquid AI LFM-2.5-VL-3B Announcement](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-3b)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/specification/2026-03-31)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
