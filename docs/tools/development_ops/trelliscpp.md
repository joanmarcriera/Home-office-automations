# TrellisCPP

## What it is
TrellisCPP is a ultra-high-performance C++23 implementation of the Trellis 3D asset generation model architecture. Built for latency-critical and edge-computing applications, TrellisCPP enables developers to generate highly detailed, high-fidelity 3D assets (including polygonal meshes, surface textures, and displacement/normal maps) from single 2D input images or natural language prompts. Operating on heavily optimized CUDA 12.6 and ROCm 6.3 runtimes, it leverages custom kernel fusion and sparse convolution libraries to eliminate the cold-start latencies and massive Python library dependencies traditionally associated with generative 3D pipelines.

## What problem it solves
Generative 3D creation historically suffered from significant execution barriers:
- **Excessive Latency & Overhead**: Standard PyTorch/Diffusers environments require substantial startup times, complicating real-time usage.
- **Enormous VRAM Demands**: Typical diffusion pipelines require high-end enterprise GPUs, preventing local desktop execution.
- **Fragile Python Dependencies**: Keeping conflicting versions of PyTorch, CUDA, xFormers, and Diffusers in sync is an operational bottleneck.

TrellisCPP solves these problems by rewriting the model's forward path, attention mechanisms, and sparse grid convolutions in optimized native C++. This achieves a 6x to 12x speedup, allows running highly quantized models under 6GB of VRAM, and fits seamlessly into standard C++ compilation workflows.

## Where it fits in the stack
**Category**: Development Ops / [Development & Ops](index.md). TrellisCPP operates as a high-speed local 3D compilation engine. It fits into game editor utilities, procedural design applications, and automated creative pipelines, exposing standardized **FastMCP 3.1** or gRPC interfaces that AI agents (such as Claude 5.1 or Gemini 4.0) can trigger programmatically during sandboxed asset assembly trials.

## Typical use cases
- **Runtime Procedural Generation**: Instantly generating textured game assets inside unreal/unity editor scripts from rough 2D concept doodles.
- **Multimodal AI CAD Tooling**: Using Gemini 4.0 or Qwen 3.6 to generate conceptual product meshes from design specification files.
- **Offline VR/AR Scene Synthesizers**: Letting users build immersive 3D rooms via voice commands entirely on-device with zero cloud latency.
- **Autonomous Agent Prototyping**: Enabling software droids to write, verify, and package 3D interface assets dynamically for virtual environments.

## Strengths
- **Bare-Metal C++23 Execution**: Bypasses the Python interpreter entirely, reducing cold starts to milliseconds.
- **Unrivaled Memory Efficiency**: Advanced 4-bit and 8-bit model weight quantization allows high-fidelity generation on low-end consumer hardware.
- **Extensive Output Architecture**: Outputs highly clean, optimized, and ready-to-render meshes (.gltf, .obj, .usd) with procedural PBR material textures.
- **MCP 3.1 Native Integrations**: Exposes dedicated tools for pipeline agents to inspect, manipulate, and generate 3D assets automatically.

## Limitations
- **Heavy Compilation Requirements**: Compiling highly optimized CUDA/ROCm sparse kernels requires modern, platform-specific compilers (MSVC 2022 / GCC 13) and precise toolkit bindings.
- **GPU Bound**: While CPU fallback exists, performance degrades significantly without modern Tensor-core or Matrix-core hardware.
- **Texture Resolutions**: Quantized weights optimized for speed focus on 2K texture maps; higher resolutions require higher-precision model weight profiles.

## When to use it
- When implementing a local, real-time 3D model generation service within consumer-facing software.
- When minimizing cloud inference hosting fees is a core architectural requirement.
- When building secure, offline-first 3D design workbenches that must run on portable devices or edge servers.

## When not to use it
- For cloud pipelines where infinite GPU resources are already provisioned and standard HuggingFace/Python endpoints are sufficient.
- If the creative pipeline relies solely on manual, non-agentic design tools (Maya, Blender) with no requirement for automated programmatic generation.

## Getting started

### Installation
Ensure you have CMake 3.28+, GCC 13+, and CUDA Toolkit 12.x or ROCm 6.x installed on your host system:

```bash
git clone --recursive https://github.com/trellis-cpp/trellis.cpp
cd trellis.cpp
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DUSE_CUDA=ON -DUSE_AVX2=ON ..
make -j$(nproc)
```

### Run basic generation
Transform a 2D sketch into a textured GLTF asset:
```bash
./trellis-cli \
  --model ../models/trellis-base-q8.bin \
  --image ../inputs/sci_fi_helmet.png \
  --output ../outputs/helmet.gltf \
  --texture-size 2048
```

## CLI examples

### Quantize raw model weights
Convert raw model weights to high-speed quantized binaries:
```bash
./trellis-quantize \
  --input ../weights/trellis-fp16.bin \
  --output ../weights/trellis-base-q4.bin \
  --bits 4
```

### Batch generation via manifest
```bash
./trellis-cli --batch --manifest ./manifest.json --out-dir ./outputs/
```

## API examples

### C++23 API integration
The following example illustrates programmatically initializing the generator and running a reconstruction task within a hosting C++ application:

```cpp
#include "trelliscpp.hpp"
#include <iostream>
#include <memory>

int main() {
    // Initialize the thread-safe generation engine
    auto engine = std::make_unique<Trellis::TrellisEngine>();

    if (!engine->load_model_weights("models/trellis-base-q8.bin")) {
        std::cerr << "CRITICAL: Failed to load model weights." << std::endl;
        return 1;
    }

    // Configure generator limits
    Trellis::TrellisConfig config{
        .generate_materials = true,
        .mesh_decimation_ratio = 0.45f,
        .target_texture_resolution = 2048,
        .quantization_level = Trellis::Quantization::INT8
    };

    // Execute generation pipeline
    bool result = engine->reconstruct_3d_mesh(
        "inputs/sword_sketch.png",
        "outputs/sword.gltf",
        config
    );

    if (result) {
        std::cout << "SUCCESS: Textured GLTF asset successfully compiled to outputs/sword.gltf!" << std::endl;
    } else {
        std::cerr << "ERROR: 3D reconstruction failed during kernel execution." << std::endl;
    }
    return 0;
}
```

### Python FastMCP 3.1 wrapper with Pydantic v2 validation
The following code defines a structured, type-safe Python API used by autonomous agents (such as Claude 5.1) to configure TrellisCPP generation jobs via Pydantic v2 schemas.

```python
from pydantic import BaseModel, Field, filepath_validator
from typing import Optional, Literal
import json
import os

class TrellisJobConfig(BaseModel):
    image_path: str = Field(..., description="Absolute path to the 2D input image.")
    output_path: str = Field(..., description="Target filepath for the compiled GLTF asset.")
    quantization: Literal["FP16", "INT8", "INT4"] = Field("INT8", description="Target model weight quantization.")
    mesh_simplification: float = Field(0.5, ge=0.1, le=1.0, description="Mesh polygon decimation ratio.")
    texture_resolution: int = Field(2048, description="Output texture size (e.g., 1024, 2048, 4096).")

    @filepath_validator("image_path")
    @classmethod
    def verify_input_exists(cls, value: str) -> str:
        if not os.path.exists(value):
            raise ValueError(f"Input image path does not exist: {value}")
        return value

def submit_trellis_job(job_payload: dict) -> str:
    """Validates the creative agent configuration via Pydantic v2 and prepares execution parameters."""
    try:
        # Pydantic v2 validation trigger
        job = TrellisJobConfig.model_validate(job_payload)

        # Build optimized CLI invocation command
        cmd = [
            "./trellis-cli",
            f"--model models/trellis-base-{job.quantization.lower()}.bin",
            f"--image {job.image_path}",
            f"--output {job.output_path}",
            f"--texture-size {job.texture_resolution}"
        ]

        return json.dumps({
            "status": "validated",
            "command_string": " ".join(cmd),
            "config": job.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": "Validation failed for TrellisCPP job parameters.",
            "errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    # Example validation test
    mock_payload = {
        "image_path": "README.md",  # Exists in repo root, using as file placeholder for test
        "output_path": "outputs/test.gltf",
        "quantization": "INT4",
        "mesh_simplification": 0.45,
        "texture_resolution": 2048
    }
    print(submit_trellis_job(mock_payload))
```

## Related tools / concepts
- [ComfyUI](../ai_knowledge/comfyui.md) — Visual stable-diffusion and generative workflow interface.
- [Aider](aider.md) — Highly performant repository-editing assistant.
- [Local LLMs](../ai_knowledge/local_llms.md) — Offline models (like Gemma 3) providing the layout and design instructions.
- [Tool Calling and MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Architectural pattern for model-tool interactions.

## Sources / references
- [TrellisCPP Core Repository](https://github.com/trellis-cpp/trellis.cpp)
- [NVIDIA TensorRT Acceleration Guides](https://developer.nvidia.com/tensorrt)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2026-12-13
- Confidence: high
