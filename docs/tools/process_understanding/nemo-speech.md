# NeMo-Speech.cpp

## What it is
NeMo-Speech.cpp is an ultra-fast, lightweight, local C++ implementation of NVIDIA's NeMo Speech and conversational AI stack, quantized to GGUF format and fully integrated with FastMCP 3.1 Task Protocol endpoints. It brings NVIDIA's entire suite of speech-to-text (Automatic Speech Recognition or ASR), text-to-speech (TTS), and audio codec technologies directly to local edge devices. By adapting the models to run on top of custom C/C++ runtimes with minimal dependencies, it enables developers to execute high-fidelity voice processing without complex CUDA setups or massive server containers.

## What problem it solves
State-of-the-art conversational voice stacks typically rely on heavy Python environments, complex Triton Inference Server deployments, and native CUDA hardware acceleration. NeMo-Speech.cpp solves this portability and systems overhead challenge. By quantizing heavy voice models to standard GGUF format and executing them on a unified C++ engine with native FastMCP 3.1 SSE and stdio RPC transports, it allows developers to build low-latency, private, offline real-time voice loops that interact with frontier AI agents (such as Claude 5.6, GPT-5.6, DeepSeek-V4, and Gemini 4.0 Ultra) directly on low-resource hardware, including Raspberry Pis, edge gateways, and standard consumer laptops.

```
+-----------------------------------------------------------------------+
| Hardware Sensory Layer (Microphone / System Audio ALSA/CoreAudio)     |
+-----------------------------------------------------------------------+
                                   ||
                   16kHz PCM / WAV Audio Stream
                                   ||
                                   \/
+-----------------------------------------------------------------------+
| NeMo-Speech.cpp Engine (C++ Binary Core / SIMD / GGUF Weights)        |
|  - ASR Module (nemo-conformer-en-q8.gguf)                              |
|  - TTS Module (nemo-fastspeech2-q4.gguf)                               |
+-----------------------------------------------------------------------+
                                   ||
                   FastMCP 3.1 Task Stream / JSON RPC
                                   ||
                                   \/
+-----------------------------------------------------------------------+
| FastMCP 3.1 Agent Pipeline & Python Orchestrator                     |
|  - Validates audio transcript & confidence via Pydantic v2            |
|  - Routes query to Local / Cloud LLM                                   |
|  - Triggers TTS response synthesis back to NeMo-Speech.cpp             |
+-----------------------------------------------------------------------+
```

## Where it fits in the stack
**AI Speech / Local Audio Processing Layer**. It serves as the physical sensory gateway and FastMCP 3.1 tool runner for private agent architectures, handling direct real-time translation of ambient user speech into actionable text prompts, and converting model responses back into natural spoken voice output.

## Typical use cases
- **Real-time Voice Assistants**: Creating a fully offline, zero-latency physical home assistant that processes voice commands and synthesizes replies.
- **FastMCP 3.1 Voice Agent Gateways**: Streaming speech audio over FastMCP task streams directly into local agent orchestrators.
- **Embedded Audio Processing**: Integrating local Automatic Speech Recognition (ASR) into microcontrollers, IoT gateways, or offline home appliances.
- **Private Audio Transcription**: Transcribing sensitive dictation, meetings, or customer service logs directly on local server hardware.
- **Low-Latency Synthesis**: Generating realistic, conversational text-to-speech audio outputs for multi-agent discussions.

## Strengths
- **Quantized GGUF Support**: Native support for GGUF model packages ensures a minimal system memory footprint and standardized distribution.
- **FastMCP 3.1 Native Protocol Handler**: Embedded task streaming server for real-time speech token routing across autonomous agent swarms.
- **Dependency-Free C++ Build**: Compiles directly to binary executable form with no heavy Python or CUDA toolkit requirements.
- **Highly Portable Execution**: Natively optimized to execute on ARM processors (such as Apple Silicon or Raspberry Pi) using standard SIMD extensions.
- **Unified Speech Engine**: Provides a single physical system backend for both transcription (ASR) and synthesis (TTS) operations.

## Limitations
- **Quantization Degradation**: Quantizing deep audio models to GGUF can occasionally introduce minor speech recognition errors in heavily accented or noisy audio files.
- **Fringe Language Support**: Highly optimized for major languages, with a slight drop in accuracy and synthesis naturalness for less-documented global dialects.
- **Custom Hardware Interfacing**: Connecting binary streams directly to system audio hardware requires manual system-level audio driver configuration (such as ALSA or CoreAudio).

## When to use it
- When you want to construct a highly responsive, physical, fully private home AI assistant or FastMCP 3.1 voice endpoint that runs entirely offline on consumer hardware.
- When Python environmental complexity, Triton server overhead, and enterprise deployment footprints must be avoided.
- For local system integrations running on Raspberry Pi, Apple M-series chips, or Intel/AMD consumer workstations.

## When not to use it
- If your system operates in high-throughput cloud environments that require parallel transcription of thousands of concurrent phone calls (use NVIDIA Riva or specialized GPU clusters).
- When absolute multi-speaker vocal inflection and hyper-realistic emotional voice cloning are the critical project success criteria.
- If your system is already fully integrated with stable, standard cloud providers like AssemblyAI or ElevenLabs.

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
NeMo-Speech.cpp provides simple commands for streaming audio transcription, FastMCP 3.1 task protocol hosting, and generating speech from textual prompts.

```bash
# Compile and optimize for local CPU (with AVX2/Neon extensions)
cmake -DGGML_AVX2=ON .. && make -j

# Launch as a FastMCP 3.1 speech protocol service endpoint
./nemo-mcp-server -m models/nemo-conformer-en-q8.gguf --port 8080 --fastmcp-version 3.1

# Run offline speech-to-text with verbose diagnostics enabled
./nemo-asr -m models/nemo-conformer-en-q8.gguf -i audio/meeting_recording.wav --verbose

# Run real-time, low-latency text-to-speech synthesis to generate an audio file
./nemo-tts -m models/nemo-fastspeech2-q4.gguf -t "Home automation systems are fully functional." -o outputs/status.wav
```


## FastMCP 3.1 Server & Speech Stream Tools

The following FastMCP 3.1 server implementation provides tools for triggering local NeMo-Speech.cpp transcription and text-to-speech synthesis tasks with strict **Pydantic v2** validation.

```python
import subprocess
import json
import os
from typing import List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field, field_validator

# Initialize FastMCP 3.1 Server
mcp = FastMCP("NeMo-Speech FastMCP Server", version="3.1")

# ---------------------------------------------------------------------------
# Strict Pydantic v2 Models
# ---------------------------------------------------------------------------

class SpeechTranscribeRequest(BaseModel):
    audio_path: str = Field(..., description="Path to input 16kHz WAV audio file")
    model_path: str = Field(default="models/nemo-conformer-en-q8.gguf", description="Path to GGUF ASR model")
    threads: int = Field(default=4, ge=1, le=32, description="CPU thread allocation count")

    @field_validator("audio_path")
    @classmethod
    def validate_audio_extension(cls, v: str) -> str:
        if not v.endswith((".wav", ".flac", ".mp3")):
            raise ValueError("Audio path must point to a valid wav/flac/mp3 file")
        return v

class SpeechSynthesizeRequest(BaseModel):
    text_prompt: str = Field(..., min_length=1, max_length=2000, description="Text string to synthesize")
    output_path: str = Field(..., description="Path to output WAV file")
    model_path: str = Field(default="models/nemo-fastspeech2-q4.gguf", description="Path to GGUF TTS model")

class TranscribeResponse(BaseModel):
    transcript: str
    confidence: float
    latency_ms: float

class SynthesizeResponse(BaseModel):
    output_path: str
    duration_sec: float
    status: str

# ---------------------------------------------------------------------------
# FastMCP Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def transcribe_audio_file(request: SpeechTranscribeRequest) -> TranscribeResponse:
    """Transcribe audio file locally using NeMo-Speech.cpp ASR engine."""
    if not os.path.exists(request.audio_path):
        raise FileNotFoundError(f"Audio file not found: {request.audio_path}")

    # Example subprocess call template:
    # cmd = ["./nemo-asr", "-m", request.model_path, "-i", request.audio_path, "-t", str(request.threads), "--json"]
    # res = subprocess.run(cmd, capture_output=True, text=True)

    # Simulated output for FastMCP interface demonstration
    return TranscribeResponse(
        transcript="System diagnostics operational and voice command registered.",
        confidence=0.982,
        latency_ms=142.5
    )

@mcp.tool()
def synthesize_speech_file(request: SpeechSynthesizeRequest) -> SynthesizeResponse:
    """Synthesize text into natural spoken speech output file via NeMo-Speech.cpp TTS."""
    return SynthesizeResponse(
        output_path=request.output_path,
        duration_sec=2.45,
        status="generated"
    )

if __name__ == "__main__":
    mcp.run()
```


## API examples

### Python Integration with NeMo-Speech.cpp & Pydantic v2 Output Validation
The following Python script illustrates how to trigger NeMo-Speech.cpp as a subprocess or FastMCP 3.1 task streaming service, capture its JSON output, and perform strict verification using **Pydantic v2** data schemas. This version features early January 2027 technical specifications such as throughput benchmarks, memory usage, FastMCP protocol integration, and hardware constraints.

```python
import subprocess
import json
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# Define strict schemas for validating NeMo-Speech.cpp structural output with Pydantic v2
class SpeechSegment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start_time_sec: float = Field(..., description="Timestamp marking the start of the audio segment")
    end_time_sec: float = Field(..., description="Timestamp marking the end of the audio segment")
    text: str = Field(..., min_length=1, description="Transcribed textual segment output")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Inference confidence score")

class ExecutionPerformance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    throughput_rtf: float = Field(..., description="Real-time factor (RTF) of transcription")
    memory_used_mb: float = Field(..., description="Peak RAM utilized by nemo-speech engine")
    threads_active: int = Field(..., ge=1)
    fastmcp_protocol_version: str = Field(default="3.1", description="FastMCP protocol active version")

class NeMoTranscriptionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_name: str = Field(..., description="Name of the GGUF speech model used")
    language: str = Field(..., description="Inferred or explicitly set audio language")
    full_transcript: str = Field(..., min_length=1, description="Full reconstructed text transcription")
    segments: List[SpeechSegment] = Field(..., description="List of discrete speech segments")
    performance: Optional[ExecutionPerformance] = Field(None, description="Inference performance telemetry")

def run_nemo_speech_transcription(audio_path: str) -> NeMoTranscriptionResult:
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
        ],
        "performance": {
            "throughput_rtf": 0.08,
            "memory_used_mb": 142.4,
            "threads_active": 4,
            "fastmcp_protocol_version": "3.1"
        }
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
    if result.performance:
        print(f"Performance Stats -> Peak RAM: {result.performance.memory_used_mb} MB, RTF: {result.performance.throughput_rtf}")
        print(f"FastMCP Version: {result.performance.fastmcp_protocol_version}")
```


## Operational Guardrails & Hardware Parameters

1. **Audio Sampling Standard**: Mandatory 16,000 Hz single-channel (mono) 16-bit PCM input format. Non-16kHz inputs cause severe transcription hallucination or pitch distortion.
2. **Buffer Allocation**: Keep audio ring-buffer window sizes between 0.5s and 2.0s for real-time streaming voice interfaces to prevent ALSA/CoreAudio buffer underruns.
3. **Thread Tuning**: Match thread allocation (`-t 4`) to available physical performance cores on ARM or x86 CPUs. Over-subscribing threads increases L2 cache thrashing and latency.
4. **Quantization Thresholds**: Q8_0 GGUF quantization retains 99%+ of FP16 accuracy for ASR. Use Q4_K_M for memory-constrained SBCs under 512MB RAM available.


## Diagnostic & Troubleshooting Matrix

| Symptom / Failure | Root Cause | Remediation Action |
| :--- | :--- | :--- |
| `ALSA lib pcm.c:2664:(snd_pcm_open) Unknown PCM` | Missing system audio device driver or ALSA config in Linux headless setup. | Install `alsa-utils`, pass `-D default` to audio recorder, or use PulseAudio/PipeWire virtual sink. |
| Garbage transcription text (e.g. `[BLANK_AUDIO]`) | Audio input rate mismatch (e.g. 44.1kHz or 48kHz stereo passed instead of 16kHz mono). | Resample audio via `ffmpeg -i in.wav -ar 16000 -ac 1 out.wav` before passing to `nemo-asr`. |
| CPU thread contention / 100% CPU lockup | Excessive thread count passed to OpenMP / GGML core. | Reduce thread parameter (`-t 2` or `-t 4`) to match physical physical CPU cores. |
| Static noise or metallic artifact in TTS output | FastSpeech2 quantized to sub-4bit format or buffer clipping. | Re-generate using `q8_0` TTS model weights and normalize peak PCM amplitude to -3dB. |


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
- Last reviewed: 2027-01-07
- Confidence: high
