# NeMo-Speech.cpp

## What it is
NeMo-Speech.cpp is an ultra-fast, lightweight, local C++ implementation of NVIDIA's NeMo Speech and conversational AI stack, quantized to GGUF format. It brings NVIDIA's entire suite of speech-to-text (Automatic Speech Recognition or ASR), text-to-speech (TTS), and audio codec technologies directly to local edge devices. By adapting the models to run on top of custom C/C++ runtimes with minimal dependencies, it enables developers to execute high-fidelity voice processing without complex CUDA setups or massive server containers.

## What problem it solves
State-of-the-art conversational voice stacks typically rely on heavy Python environments, complex Triton Inference Server deployments, and native CUDA hardware acceleration. NeMo-Speech.cpp solves this portability and systems overhead challenge. By quantizing heavy voice models to standard GGUF format and executing them on a unified C++ engine, it allows developers to build low-latency, private, offline real-time voice loops that execute directly on low-resource hardware, including Raspberry Pis, edge gateways, and standard consumer laptops.

## Where it fits in the stack
**AI Speech / Local Audio Processing Layer**. It serves as the physical sensory gateway for private agent architectures, handling the direct real-time translation of ambient user speech into actionable text prompts, and converting model responses back into natural spoken voice output.

## Typical use cases
- **Real-time Voice Assistants**: Creating a fully offline, zero-latency physical home assistant that processes voice commands and synthesizes replies.
- **Embedded Audio Processing**: Integrating local Automatic Speech Recognition (ASR) into microcontrollers, IoT gateways, or offline home appliances.
- **Private Audio Transcription**: Transcribing sensitive dictation, meetings, or customer service logs directly on local server hardware.
- **Low-Latency Synthesis**: Generating realistic, conversational text-to-speech audio outputs for multi-agent discussions.

## Strengths
- **quantized GGUF Support**: Native support for GGUF model packages ensures a minimal system memory footprint and standardized distribution.
- **Dependency-Free C++ Build**: Compiles directly to binary executable form with no heavy Python or CUDA toolkit requirements.
- **Highly Portable Execution**: Natively optimized to execute on ARM processors (such as Apple Silicon or Raspberry Pi) using standard SIMD extensions.
- **Unified Speech Engine**: Provides a single physical system backend for both transcription (ASR) and synthesis (TTS) operations.

## Limitations
- **Quantization Degradation**: Quantizing deep audio models to GGUF can occasionally introduce minor speech recognition errors in heavily accented or noisy audio files.
- **Fringe Language Support**: Highly optimized for major languages, with a slight drop in accuracy and synthesis naturalness for less-documented global dialects.
- **Custom Hardware Interfacing**: Connecting binary streams directly to system audio hardware requires manual system-level audio driver configuration (such as ALSA or CoreAudio).

## When to use it
- When you want to construct a highly responsive, physical, fully private home AI assistant that runs entirely offline on consumer hardware.
- When Python environmental complexity, Triton server overhead, and enterprise deployment footprints must be avoided.
- For local system integrations running on Raspberry Pi, Apple M-series chips, or Intel/AMD consumer workstations.

## When not to use it
- If your system operates in high-throughput cloud environments that require parallel transcription of thousands of concurrent phone calls (use NVIDIA Riva or specialized GPU clusters).
- When absolute multi-speaker vocal inflection and hyper-realistic emotional voice cloning are the critical project success criteria.
- If your stack is already fully integrated with stable, standard cloud providers like AssemblyAI or ElevenLabs.

## Getting started
1. **Clone the Codebase**: Clone the repository and submodules:
   ```bash
   git clone --recursive https://github.com/NVIDIA/nemo-speech-cpp.git
   cd nemo-speech-cpp
   ```
2. **Build the Binary**: Compile the project using CMake:
   ```bash
   mkdir build && cd build
   cmake .. -DCMAKE_BUILD_TYPE=Release
   make -j
   ```
3. **Execute ASR**: Perform local speech-to-text transcription:
   ```bash
   ./nemo-asr -m ./models/nemo-conformer-en.gguf -i ./audio/input.wav
   ```

## CLI examples
NeMo-Speech.cpp provides simple commands for streaming audio transcription and generating speech from textual prompts.

```bash
# Compile and optimize for local CPU (with AVX2/Neon extensions)
cmake -DGGML_AVX2=ON .. && make -j

# Run offline speech-to-text with verbose diagnostics enabled
./nemo-asr -m models/nemo-conformer-en-q8.gguf -i audio/meeting_recording.wav --verbose

# Run real-time, low-latency text-to-speech synthesis to generate an audio file
./nemo-tts -m models/nemo-fastspeech2-q4.gguf -t "Home automation systems are fully functional." -o outputs/status.wav
```

## API examples

### Python Integration with NeMo-Speech.cpp & Pydantic v2 Output Validation
The following Python script illustrates how to trigger NeMo-Speech.cpp as a subprocess, capture its JSON output, and perform strict verification using **Pydantic v2** data schemas.

```python
import subprocess
import json
from typing import List, Optional
from pydantic import BaseModel, Field

# Define strict schemas for validating NeMo-Speech.cpp structural output
class SpeechSegment(BaseModel):
    start_time_sec: float = Field(..., description="Timestamp marking the start of the audio segment")
    end_time_sec: float = Field(..., description="Timestamp marking the end of the audio segment")
    text: str = Field(..., min_length=1, description="Transcribed textual segment output")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Inference confidence score")

class NeMoTranscriptionResult(BaseModel):
    model_name: str = Field(..., description="Name of the GGUF speech model used")
    language: str = Field(..., description="Inferred or explicitly set audio language")
    full_transcript: str = Field(..., min_length=1, description="Full reconstructed text transcription")
    segments: List[SpeechSegment] = Field(..., description="List of discrete speech segments")

def run_nemo_speech_transcription(audio_path: str) -> NeMoTranscriptionResult:
    # command = ["./nemo-asr", "-m", "models/nemo-conformer-en-q8.gguf", "-i", audio_path, "--json"]
    # process = subprocess.run(command, capture_output=True, text=True)
    # output_data = json.loads(process.stdout)

    # Simulated system stdout block from a NeMo-Speech.cpp JSON output execution
    simulated_json_output = {
        "model_name": "nemo-conformer-en-q8.gguf",
        "language": "en",
        "full_transcript": "turn on the kitchen lights",
        "segments": [
            {
                "start_time_sec": 0.12,
                "end_time_sec": 1.45,
                "text": "turn on the kitchen lights",
                "confidence": 0.985
            }
        ]
    }

    # Validate against Pydantic v2 schema
    validated_result = NeMoTranscriptionResult(**simulated_json_output)
    return validated_result

if __name__ == "__main__":
    audio_file_path = "audio/voice_command.wav"
    result = run_nemo_speech_transcription(audio_file_path)

    print("--- NeMo-Speech.cpp Transcription Verified ---")
    print(f"Model: {result.model_name}")
    print(f"Language: {result.language}")
    print(f"Full Transcript: {result.full_transcript}")
    for idx, seg in enumerate(result.segments):
        print(f" Segment {idx+1}: [{seg.start_time_sec}s - {seg.end_time_sec}s] {seg.text} (conf: {seg.confidence})")
```

## Related tools / concepts
- [Whisper](../../services/whisper.md) — SOTA audio transcription tool; often compared to NeMo-Speech.cpp for local performance.
- [Ollama](../../services/ollama.md) — The standard local engine for model weights management and serving.
- [Local LLMs](../ai_knowledge/local_llms.md) — Ecosystem of fully offline, local language and reasoning model systems.
- [Llama.cpp](../infrastructure/llama-cpp.md) — The underlying C++ execution framework that inspired the design of NeMo-Speech.cpp.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard routing interface used to connect local speech devices to processing agents.

## Sources / references
- [GitHub Repository: NVIDIA NeMo Project Codebase](https://github.com/NVIDIA/NeMo)
- [Reddit r/LocalLLaMA: NVIDIA Speech Stack Goes GGUF and Local](https://www.reddit.com/r/LocalLLaMA/comments/1vhjeqy/nvidias_whole_speech_stack_just_went_local_asr/)
- [NVIDIA NeMo Conversational AI Architecture Documentation](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/core/core.html)
- [Parakeet-WGSL Browser ASR](https://www.reddit.com/r/LocalLLaMA/comments/1vi77dr/parakeetwgsl_fast_accurate_asr_in_the_browser_via/)

## Contribution Metadata
- Last reviewed: 2026-08-10
- Confidence: high
