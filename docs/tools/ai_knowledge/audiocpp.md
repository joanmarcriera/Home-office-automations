# AudioCPP

## What it is
AudioCPP is an open-weights, zero-dependency C++ native audio generation runtime optimized for ultra-low latency, professional-grade text-to-speech (TTS), and real-time voice synthesis. In early 2027, AudioCPP provides an execution environment capable of generating over 10 hours of high-fidelity stereo speech audio in under 3 minutes on consumer-grade hardware, utilizing SIMD, WebAssembly (WASM), and hardware acceleration.

## What problem it solves
Eliminates heavy Python dependency trees (PyTorch, Hugging Face Transformers, CUDA runtime overhead) for voice synthesis pipelines. AudioCPP enables local, offline voice generation with zero startup cold-start delays and minimal memory footprints, making it ideal for edge devices, embedded robotics, desktop applications, and offline smart home assistants.

## Where it fits in the stack
**AI & Knowledge / Multi-modal Audio Engine**. AudioCPP serves as the local audio output runtime layer for offline voice agents. It accepts text or phoneme streams from orchestrators or [Local LLMs](local_llms.md) (such as Llama 4 or Qwen 3.8 running on `llama.cpp`) and streams PCM audio directly to local sound hardware or low-latency websockets.

## Typical use cases
- **Fully Offline Local Voice Assistants**: Powering privacy-first, zero-latency voice agents on smart home controllers or Raspberry Pi / Jetson nodes.
- **High-Velocity Audiobook Generation**: Synthesizing hours of multi-speaker narrative audio in minutes without external cloud API costs.
- **Embedded Robotics & Screen Readers**: Delivering low-power, high-speed vocal responses on robotics platforms and offline accessibility hardware.
- **Low-Latency Game NPC Dialogue**: Generating real-time, zero-shot vocal responses for game characters with sub-50ms synthesis latency.

## Strengths
- **Zero Python Runtime Dependencies**: Pure C/C++ implementation with clean CMake build files for maximum portability.
- **Blazing Execution Speed**: Multi-threaded AVX-512, ARM NEON, and Metal SIMD optimizations achieve 200x+ real-time generation speeds.
- **Quantized Weights Support**: Native execution of 4-bit and 6-bit quantized audio models (e.g., Higgs Audio v3 4B), reducing model sizes below 150MB.
- **Zero-Shot Voice Cloning**: High-fidelity speaker cloning using a single 5-second reference `.wav` file.
- **FastMCP 3.1 & C++ Bindings**: Modern C++ library bindings and FastMCP integration for agentic orchestration.

## Limitations
- **Model Compilation Complexity**: Training or converting new specialized model architectures requires custom C++ kernel development.
- **Quantization Artifacts**: Extreme 3-bit or 4-bit quantization can occasionally introduce subtle robotic audio artifacts.
- **Platform Audio Drivers**: Managing cross-platform OS audio device backends (ALSA, PulseAudio, CoreAudio, WASAPI) requires platform-specific configuration.

## When to use it
- When building fully local, offline, or air-gapped interactive voice applications.
- When generating massive volumes of speech audio locally where cloud services like [ElevenLabs](elevenlabs.md) are cost-prohibitive.
- When deploying voice agents on edge hardware or Apple Silicon using C++ and [MLX](../infrastructure/mlx.md).

## When not to use it
- For standard web or mobile applications where a single cloud API call to [ElevenLabs](elevenlabs.md) is simpler.
- If your development team lacks C++ compilation experience (CMake/GCC/Clang) and prefers Python-native SDKs.

## Getting started

### Compilation
Build the `audiocpp` binary from source using CMake:

```bash
git clone https://github.com/audiocpp/audiocpp
cd audiocpp
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DAUDIOCPP_SIMD=ON
make -j$(nproc)
```

### Synthesis Command
Synthesize audio from text using a reference voice prompt:

```bash
./audiocpp-cli \
  --model ../models/audiocpp-higgs-v3-q4.bin \
  --voice ../voices/sample_narrator.wav \
  --text "Ultra low latency local speech synthesis is running natively in C++." \
  --output ./output.wav
```

## CLI examples

### Interactive Streaming Mode
```bash
# Launch interactive stdin streaming mode for local voice bots
./audiocpp-cli \
  --model ../models/audiocpp-higgs-v3-q4.bin \
  --voice ../voices/sample_narrator.wav \
  --interactive \
  --sample-rate 24000
```

### Voice Morphing & Speaker Conversion
```bash
# Convert input audio file directly to match target speaker voice
./audiocpp-morph \
  --source input_speech.wav \
  --target reference_voice.wav \
  --output converted_speech.wav
```

## API examples

### C++ Native API: Synthesis Execution
The following example shows initializing and invoking the AudioCPP C++ engine.

```cpp
#include "audiocpp.h"
#include <iostream>
#include <vector>

int main() {
    AudioCPPEngine engine;
    if (!engine.load_model("models/audiocpp-higgs-v3-q4.bin")) {
        std::cerr << "Error loading AudioCPP quantized model weights." << std::endl;
        return 1;
    }

    // Perform real-time voice synthesis
    std::vector<float> pcm_buffer = engine.synthesize(
        "Low latency local voice generation initialized.",
        "voices/reference_narrator.wav"
    );

    // Save generated audio
    if (engine.save_wav("output_speech.wav", pcm_buffer, 24000)) {
        std::cout << "Successfully generated speech file: output_speech.wav" << std::endl;
    }
    return 0;
}
```

### Python Bindings with Pydantic v2 Schema
Python applications can drive AudioCPP using C++ bindings with strict input configuration validated via **Pydantic v2**.

```python
import os
from pydantic import BaseModel, Field, FilePath


class AudioCPPSynthesisConfig(BaseModel):
    model_path: str = Field(..., description="Path to binary quantized model file")
    voice_path: str = Field(..., description="Path to reference speaker WAV file")
    output_path: str = Field(..., description="Destination WAV file path")
    sample_rate: int = Field(default=24000, ge=16000, le=48000)


def generate_local_speech(text_prompt: str, config: AudioCPPSynthesisConfig) -> bool:
    # Example wrapper demonstrating binding invocation pattern
    import audiocpp  # type: ignore

    engine = audiocpp.Engine(config.model_path)
    success = engine.synthesize_to_file(
        text=text_prompt,
        voice_path=config.voice_path,
        output_path=config.output_path,
        sample_rate=config.sample_rate
    )
    return bool(success)


if __name__ == "__main__":
    cfg = AudioCPPSynthesisConfig(
        model_path="models/audiocpp-higgs-v3-q4.bin",
        voice_path="voices/narrator.wav",
        output_path="output.wav"
    )
    print(f"Validated AudioCPP Config: {cfg.model_dump_json()}")
```

## Related tools / concepts
- [KokoClone](kokoclone.md) — Local neural voice cloning framework.
- [Fish Audio](fish-audio.md) — Open-weights multimodal audio model suite.
- [ElevenLabs](elevenlabs.md) — Cloud-based voice synthesis platform.
- [llama.cpp](../infrastructure/llama-cpp.md) — C++ LLM inference framework which inspired AudioCPP.
- [Whisper](../../services/whisper.md) — Open-source speech recognition counterpart.
- [MLX](../infrastructure/mlx.md) — Apple Silicon array framework.

## Sources / references
- [AudioCPP GitHub Repository](https://github.com/audiocpp/audiocpp)
- [Higgs Audio v3 Model Release (AudioCPP Release 0.4)](https://www.reddit.com/r/LocalLLaMA/comments/1v4w5cj/audiocpp_release_04_higgs_audio_v3_tts_4b_10x/)
- [Inflect v2 Release Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1v5ve6v/i_released_inflect_v2_two_ultratiny_complete_tts/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
