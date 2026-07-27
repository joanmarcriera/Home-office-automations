# AudioCPP

## What it is
AudioCPP is a high-performance, C++ native audio generation engine optimized for ultra-low latency, professional-grade text-to-speech (TTS) and voice synthesis. Developed under the open-weights movement and released in mid-2026, AudioCPP features extreme execution speed, achieving an output ratio where 10 hours of high-fidelity stereo audio can be generated in less than 3 minutes on consumer-grade hardware.

## What problem it solves
Existing audio synthesis frameworks are heavily reliant on large Python dependency trees (e.g., PyTorch, Hugging Face Transformers) and specialized GPU configurations, making them complex to integrate into embedded systems, offline desktop applications, and real-time edge devices. AudioCPP removes these dependencies, offering a pure, zero-dependency C++ implementation that significantly reduces both the startup cold-start times and runtime memory footprints.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge. AudioCPP serves as the audio-synthesis output layer of a locally deployed voice agent. It receives textual or phoneme strings from local orchestrators or [Local LLMs](local_llms.md), and streams high-fidelity waveform data to the host operating system's audio output device or client.

## Typical use cases
- **Real-Time Offline Assistants**: Creating fast voice-response systems on smart home systems.
- **Large-Scale Audiobook Generation**: Generating hours of high-quality narrative speech in minutes rather than hours.
- **Embedded Screen Readers**: Implementing accessible voice navigation on low-power devices.
- **Interactive NPC Dialogues**: Powering real-time video game characters with rich, low-latency vocal synthesis.

## Strengths
- **Zero Python Dependency**: Pure C/C++ codebase makes it lightweight and extremely portable.
- **Extreme Speed**: Multi-threaded SIMD optimizations generate audio at up to 200x real-time speed.
- **Quantized Audio Weights**: Native support for 4-bit and 6-bit weight quantization, reducing model size to less than 150MB.
- **Natural Voice Clones**: Integrates high-fidelity zero-shot voice cloning capabilities using a single 5-second voice prompt.

## Limitations
- **Fine-Tuning Complexity**: Compiling and training new vocal models from scratch requires deep audio engineering knowledge and is not as simple as Python-based frameworks.
- **Output Artifacts**: High quantization levels (under 4-bit) can sometimes introduce metallic artifacts in the generated speech.
- **Platform-Specific Audio Backends**: Handling low-level audio device integration across Windows, Linux, and macOS requires managing distinct driver libraries.

## When to use it
- When you are building a fully offline, local-first interactive voice assistant.
- When generating massive volumes of speech audio and cloud-based services like [ElevenLabs](elevenlabs.md) are cost-prohibitive.
- When deploying synthesis engines on low-powered edge devices or Apple Silicon where [MLX](../infrastructure/mlx.md) and C++ can be utilized together.

## When not to use it
- For simple web-based web-apps where a simple API call to a cloud TTS provider is more practical.
- If you lack experience with C++ build chains (such as CMake, GCC, or MSVC) and prefer a quick, Python-native setup.

## Getting started

### Compilation
Build the `audiocpp` binary from source using CMake:
```bash
git clone https://github.com/audiocpp/audiocpp
cd audiocpp
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

### Synthesis
Provide a voice prompt and a text string to synthesize audio:
```bash
./audiocpp-cli \
  --model ../models/audiocpp-base-q4.bin \
  --voice ../voices/sample_narrator.wav \
  --text "Welcome to high performance local audio synthesis." \
  --output ./welcome.wav
```

## CLI examples

### Interactive TTS mode
```bash
# Start the CLI in interactive standard-in listening mode
./audiocpp-cli --model ../models/audiocpp-base-q4.bin --interactive
```

### Voice morphing and translation
```bash
# Convert source audio to target speaker voice directly
./audiocpp-morph --source input.wav --target narrator.wav --output morphed.wav
```

## API examples

### C++ API: Simple Waveform Synthesis
The following code snippet demonstrates how to initialize and run synthesis inside a C++ application.

```cpp
#include "audiocpp.h"
#include <iostream>

int main() {
    // Initialize the engine and load weights
    AudioCPPEngine engine;
    if (!engine.load_model("models/audiocpp-base-q4.bin")) {
        std::cerr << "Failed to load audio model." << std::endl;
        return 1;
    }

    // Synthesize speech to memory
    std::vector<float> audio_buffer = engine.synthesize(
        "Low latency speech synthesis is now active.",
        "voices/sample_narrator.wav"
    );

    // Save output wav file
    engine.save_wav("output.wav", audio_buffer);
    std::cout << "Audio synthesized successfully!" << std::endl;
    return 0;
}
```

### Python: Binding Integration
```python
import audiocpp

# Load local weights
engine = audiocpp.Engine("models/audiocpp-base-q4.bin")

# Synthesize directly to file
engine.synthesize_to_file(
    text="Synthesized from high-performance python binding.",
    voice_path="voices/sample_narrator.wav",
    output_path="python_output.wav"
)
```

## Related tools / concepts
- [kokoclone](kokoclone.md) — Fast local voice clone reference.
- [fish-audio](fish-audio.md) — Open-weights multimodal audio models.
- [ElevenLabs](elevenlabs.md) — Industry-standard cloud-based vocal synthesis.
- [Google Lyria](google-lyria.md) — Multimodal generative audio ecosystem.
- [personaplex](personaplex.md) — High-fidelity vocal generation agent workbench.
- [Local LLMs](local_llms.md) — Edge reasoning models.
- [llama.cpp](../infrastructure/llama-cpp.md) — C++ runtime which inspired AudioCPP architecture.
- [Whisper](../../services/whisper.md) — SOTA speech-to-text transcription engine.

## Sources / references
- [AudioCPP Repository](https://github.com/audiocpp/audiocpp)
- [Reddit LocalLLaMA Thread: AudioCPP 10 hours of audio in 3 minutes](https://www.reddit.com/r/LocalLLaMA/comments/1uwpvt9/audiocpp_10_hours_of_audio_generated_in_3_minutes/)
- [Higgs Audio v3 Model Release (AudioCPP Release 0.4)](https://www.reddit.com/r/LocalLLaMA/comments/1v4w5cj/audiocpp_release_04_higgs_audio_v3_tts_4b_10x/) — Higgs Audio v3 TTS 4B model for high-speed audio generation on AudioCPP.
- [Inflect v2 Release](https://www.reddit.com/r/LocalLLaMA/comments/1v5ve6v/i_released_inflect_v2_two_ultratiny_complete_tts/) — Two ultra-tiny complete text-to-speech (TTS) models.

## Contribution Metadata
- Last reviewed: 2026-10-01
- Confidence: high
