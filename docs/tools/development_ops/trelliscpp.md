# TrellisCPP

## What it is
TrellisCPP is a high-performance C++ implementation of the Trellis 3D asset generation model architecture. Built for speed and edge execution, TrellisCPP enables developers to generate highly detailed, high-fidelity 3D assets (including meshes, textures, and normal maps) from single 2D images or prompts. Released in mid-2026, it utilizes advanced sparse convolution libraries and CUDA/ROCm acceleration to bypass slow, memory-intensive Python pipelines.

## What problem it solves
Generative 3D workflows are traditionally plagued by extreme latency, massive VRAM requirements, and heavy dependency on specific Python library versions (such as PyTorch and Diffusers). These bottlenecks prevent 3D generation from being run natively inside game engines, real-time creative tools, or offline rendering workflows. TrellisCPP solves this by optimizing the model forward pass in native C++, offering 5x to 10x faster generation times and drastically reducing VRAM usage.

## Where it fits in the stack
**Category**: Development Ops / Creative Pipelines. TrellisCPP serves as a core 3D generation microservice. It is triggered by creative agents, CAD pipelines, or automated droids to produce textured 3D assets on-demand. It integrates with runtime interfaces and creative tools like [ComfyUI](../ai_knowledge/comfyui.md) or custom game engines.

## Typical use cases
- **Procedural Game Asset Generation**: Generating textured 3D models from 2D sketches instantly inside game editors.
- **On-Demand CAD Prototyping**: Generating preliminary 3D structures from product design concepts.
- **VR/AR Scene Assembly**: Letting users generate 3D models via voice prompt and placing them in interactive spaces in real time.
- **Agentic Design Loops**: Enabling autonomous agents to generate, inspect, and refine virtual 3D components during developer sandbox trials.

## Strengths
- **Native C++ Performance**: Bypasses the Python runtime entirely for zero cold-start overhead.
- **Extreme Speed**: Multi-threaded execution and FlashAttention optimizations yield high-quality 3D assets in seconds.
- **Low Memory Footprint**: Optimized quantized model loading fits complex 3D generation within consumer-grade GPU memory (under 8GB VRAM).
- **Comprehensive Outputs**: Automatically generates structured meshes (.obj/.gltf), material textures, and normal maps.

## Limitations
- **Hardware Bound**: Requires modern NVIDIA/AMD GPUs with robust CUDA or ROCm drivers for peak performance; CPU execution is slow.
- **Compilation Complexity**: Compiling sparse convolution backends on some Windows systems requires managing complex compiler settings.
- **Texture resolution**: The default fast weights generate textures up to 2K resolution; higher resolutions require larger weights.

## When to use it
- When you are building a real-time, local 3D content creation engine.
- When you want to execute 3D generation pipelines entirely offline inside desktop applications.
- When VRAM is a major bottleneck on your edge hardware configurations.

## When not to use it
- If your pipeline is fully hosted on cloud instances with plenty of GPU power and simple Python endpoints.
- If you only need occasional 3D models and prefer standard web interfaces over local compilation.

## Getting started

### Installation
Ensure you have CUDA 12.x or ROCm 6.x installed on your host system.

```bash
git clone https://github.com/trellis-cpp/trellis.cpp
cd trellis.cpp
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DUSE_CUDA=ON ..
make -j$(nproc)
```

### Synthesis
Download the model weights and convert a 2D image into a GLTF 3D model:
```bash
./trellis-cli \
  --model ../models/trellis-base-q8.bin \
  --image ../inputs/couch_sketch.png \
  --output ../outputs/couch.gltf
```

## CLI examples

### Generate mesh from prompt
```bash
./trellis-cli --prompt "A medieval iron sword with gold engravings" --output sword.gltf
```

### Quantizing model weights
```bash
./trellis-quantize --input trellis-base.bin --output trellis-base-q4.bin --bits 4
```

## API examples

### C++ API: Basic 3D Reconstruction
The following code snippet demonstrates loading a 2D image and generating a 3D model path within a host application.

```cpp
#include "trelliscpp.h"
#include <iostream>

int main() {
    TrellisEngine engine;
    if (!engine.load_model("models/trellis-base-q8.bin")) {
        std::cerr << "Failed to load model weights." << std::endl;
        return 1;
    }

    // Set configuration
    TrellisConfig config;
    config.generate_textures = true;
    config.simplify_mesh_ratio = 0.5;

    // Run 3D generation
    bool success = engine.generate_from_image(
        "inputs/sketch.png",
        "outputs/model.gltf",
        config
    );

    if (success) {
        std::cout << "3D mesh successfully saved to outputs/model.gltf!" << std::endl;
    }
    return 0;
}
```

### Python: Binding Integration
```python
import trelliscpp

# Initialize the optimized C++ engine
generator = trelliscpp.Generator("models/trellis-base-q8.bin")

# Process image to 3D GLTF asset
generator.process(
    image_path="inputs/sketch.png",
    output_path="outputs/sword.gltf",
    format="gltf"
)
```

## Related tools / concepts
- [Aider](aider.md) — Coding agent companion.
- [Symbolic MCP](symbolic-mcp.md) — Model checking server.
- [Fuzzing MCP Server](fuzzing-mcp-server.md) — Security fuzzing integrations.
- [OpenClaw](openclaw.md) — Local agent system.
- [Melty](melty.md) — Intent-state tracking developer tool.
- [Sourcegraph Cody](sourcegraph_cody.md) — Code reasoning system.
- [Terminus 2](terminus-2.md) — Terminal-native bridging agent.
- [Droid](droid.md) — Autonomous pipeline manager.
- [ComfyUI](../ai_knowledge/comfyui.md) — Multi-modal workspace tool.
- [Local LLMs](../ai_knowledge/local_llms.md) — Standard offline reasoning foundation.

## Sources / references
- [TrellisCPP Repository](https://github.com/trellis-cpp/trellis.cpp)
- [Reddit LocalLLaMA Thread: TrellisCPP Announces High Quality 3D Assets](https://www.reddit.com/r/LocalLLaMA/comments/1uyw64s/trelliscpp_now_produces_high_quality_assets/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
