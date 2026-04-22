# Audio Transcription Research: Whisper Variants for Long-Form Audio

This document compares different Whisper variants for transcribing personal audiobooks and podcasts in a homelab environment, focusing on performance, accuracy, and hardware requirements for long-form audio.

## Comparison Table

| Model Variant | Engine | Speed (vs. Large-v3) | Memory (Approx.) | Multilingual | Best For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Whisper (Large-v3)** | Transformers/OpenAI | 1.0x (Baseline) | ~10GB VRAM | Yes | Maximum accuracy (multilingual) |
| **Faster-Whisper** | CTranslate2 | 2x - 4x | ~5GB VRAM | Yes | Standard homelab CPU/GPU use |
| **Distil-Whisper** | Transformers | ~6x | ~5GB VRAM | No (English) | Speed & hallucination resistance |
| **Faster-Distil-Whisper**| CTranslate2 | ~8x - 10x | ~3GB VRAM | No (English) | Best performance on limited hardware |
| **Whisper Turbo** | Transformers | ~6x | ~6GB VRAM | Yes | Fast multilingual transcription |

## Key Findings

### 1. Distil-Whisper (distil-large-v3)
- **Performance**: Up to 6x faster than `large-v3`.
- **Accuracy**: Within 1% Word Error Rate (WER) of the original model.
- **Long-Form**: Specifically optimized for long-form audio to reduce hallucinations (repeating phrases) often seen in vanilla Whisper during silence or background noise.
- **Limitation**: Currently only supports English.

### 2. Faster-Whisper
- **Implementation**: Uses CTranslate2, a fast inference engine for Transformer models.
- **Efficiency**: Significantly faster and more memory-efficient than the Hugging Face `transformers` implementation.
- **Flexibility**: Can load `distil-whisper` models, providing the best of both worlds (distilled architecture + CTranslate2 speed).

### 3. Hardware Requirements
- **GPU**: NVIDIA GPU with at least 8GB VRAM is recommended for `large` or `distil-large` models in float16.
- **CPU**: `faster-whisper` is highly optimized for CPU (using INT8 quantization), making it viable for NAS-based transcription without a dedicated GPU.

## Recommendations for Homelab

1. **Primary Choice (English)**: Use `faster-whisper` with the `distil-large-v3` model. This provides the best balance of speed, low resource usage, and accuracy for English podcasts/audiobooks.
2. **Multilingual Choice**: Use `faster-whisper` with `large-v3-turbo` or standard `large-v3` if accuracy is paramount for non-English content.
3. **Pipeline Strategy**: Use Voice Activity Detection (VAD) to skip silence in long-form audio, which further improves speed and prevents hallucinations. `faster-whisper` has integrated Silero VAD support.

- Last reviewed: 2025-05-15
- Confidence: high

## Sources / references
- [Distil-Whisper GitHub](https://github.com/huggingface/distil-whisper)
- [Faster-Whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [Transcription benchmark: Distil-Whisper Large v2 vs Whisper Large v3](https://blog.salad.com/distil-whisper-large-v2/)
- [Faster Whisper Accuracy and Speed Benchmark](https://www.transana.com/blog/2025/05/01/faster-whisper-in-transana-5-30-accuracy-and-processing-speed-3-of-3/)
