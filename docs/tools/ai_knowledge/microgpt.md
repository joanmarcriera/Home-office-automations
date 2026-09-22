# MicroGPT

## What it is
MicroGPT is a minimalistic, educational implementation of a GPT-style autoregressive transformer model, originally created by Andrej Karpathy. It strips away complex distributed training infrastructure, heavy framework abstractions, and production optimisations to present the core mechanics of transformer-based language modelling in a clear, self-contained, and highly accessible codebase.

## What problem it solves
Modern deep learning frameworks like PyTorch and TensorFlow introduce extensive abstractions, distributed training mechanics, and hardware acceleration layers that can obscure the underlying mathematics of attention mechanisms and token generation. MicroGPT provides a pure, unencumbered reference model that allows developers, researchers, and students to inspect and step through every tensor operation, matrix multiplication, and positional encoding step in a language model.

## Where it fits in the stack
**AI & Knowledge / Educational Framework**. It serves as an architectural blueprint and educational reference model at the fundamental layer of the AI stack, providing the conceptual foundation for lightweight edge inference engines such as [ansigpt](ansigpt.md) and custom tiny model implementations.

## Typical use cases
- **Pedagogical Study**: Stepping through the forward and backward passes of a transformer model to understand self-attention, query-key-value projections, and causal masking.
- **Algorithm Prototyping**: Testing novel attention mechanisms, activation functions, or tokenization approaches on a lightweight, fast-executing baseline.
- **Embedded Model Distillation**: Serving as the target topology for training hyper-compact domain-specific language models to be compiled into zero-dependency C implementations.
- **Architectural Auditing**: Verifying mathematical correctness against full-scale transformer implementations in production frameworks.

## Strengths
- **Minimal Codebase**: Consists of a tiny, self-contained implementation that can be read and fully understood in a single sitting.
- **Zero External Overhead**: Minimal dependencies allow immediate execution without complex CUDA or environment configurations.
- **Transparent Operations**: Every step from token embedding to logit computation and sampling is explicit and inspectable.
- **Foundation for Compilers**: Simple execution graph makes it ideal for porting to standard C, WASM, or embedded microcontrollers.

## Limitations
- **Not Built for Scale**: Lacks distributed multi-GPU training, FlashAttention, PagedAttention, or distributed tensor parallelism.
- **Inference Latency**: Unoptimised Python execution loop makes it unsuitable for production-grade, low-latency LLM serving.
- **Context Window Restrictions**: Best suited for micro models with small sequence lengths and vocabulary sizes.

## When to use it
- When learning or teaching the mathematical inner workings of GPT transformers without framework overhead.
- When prototyping experimental architectural tweaks before scaling to larger models.
- When creating reference implementations to verify edge runtime ports like [ansigpt](ansigpt.md).

## When not to use it
- For production serving of multi-billion parameter open-weights models (e.g., [Llama](llama.md), [Qwen](qwen.md), or [Gemma](gemma.md)).
- When requiring high-throughput batching, streaming APIs, or GPU-accelerated inference pipelines.
- For complex multi-modal or agentic workflows requiring tool calling and structured outputs out-of-the-box.

## Getting started

### Cloning and Running
MicroGPT can be cloned directly from GitHub and executed using standard Python 3.11+.

```bash
# Clone the official repository
git clone https://github.com/karpathy/microGPT.git
cd microGPT

# Run the training script directly
python3 microgpt.py
```

### Environment Requirements
A minimal Python 3.10+ environment with PyTorch or standard NumPy is sufficient:

```bash
pip install torch numpy
```

## CLI examples

### Training a Micro Model
```bash
# Train on character-level input data
python3 microgpt.py --data_path input.txt --max_iters 1000 --batch_size 32
```

### Generating Text Samples
```bash
# Generate completion from trained checkpoint
python3 sample.py --checkpoint microgpt.pt --prompt "Once upon a time" --temperature 0.8
```

## API examples

### Python (Config Validation with Pydantic v2)
The following example demonstrates defining and validating MicroGPT model hyperparameters using strict **Pydantic v2** schemas before initialising the network execution graph.

```python
from pydantic import BaseModel, Field, conint

class MicroGPTConfig(BaseModel):
    vocab_size: conint(gt=0) = Field(65, description="Vocabulary size for character-level tokenization")
    n_embd: conint(gt=0, le=1024) = Field(64, description="Embedding dimension")
    n_head: conint(gt=0, le=32) = Field(4, description="Number of attention heads")
    n_layer: conint(gt=0, le=32) = Field(4, description="Number of transformer blocks")
    block_size: conint(gt=0, le=2048) = Field(128, description="Maximum sequence length")
    dropout: float = Field(0.0, ge=0.0, lt=1.0, description="Dropout probability")

# Validate configuration for a tiny educational model
config = MicroGPTConfig(
    vocab_size=128,
    n_embd=128,
    n_head=4,
    n_layer=4,
    block_size=256,
    dropout=0.1
)

print(f"Validated MicroGPT Config: {config.n_layer} layers, {config.n_embd} embedding dim")
```

### PyTorch Model Initialization Fragment
```python
import torch
import torch.nn as nn
from torch.nn import functional as F

class MicroBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.sa = nn.MultiheadAttention(config.n_embd, config.n_head, batch_first=True)
        self.ffwd = nn.Sequential(
            nn.Linear(config.n_embd, 4 * config.n_embd),
            nn.ReLU(),
            nn.Linear(4 * config.n_embd, config.n_embd),
        )
        self.ln1 = nn.LayerNorm(config.n_embd)
        self.ln2 = nn.LayerNorm(config.n_embd)

    def forward(self, x):
        attn_out, _ = self.sa(self.ln1(x), self.ln1(x), self.ln1(x))
        x = x + attn_out
        x = x + self.ffwd(self.ln2(x))
        return x
```

## Related tools / concepts
- [ansigpt](ansigpt.md) — Portable C89 ANSI C implementation inspired by MicroGPT.
- [bettergpt-150m](bettergpt-150m.md) — Compact GPT model for lightweight edge experimentation.
- [aitmpl](aitmpl.md) — Minimalist AI templates and reference architectures.
- [gemma](gemma.md) — Open weights model family by Google.
- [qwen](qwen.md) — Open weights LLM series by Alibaba Cloud.
- [llama](llama.md) — Meta's open weights foundation LLMs.
- [claude](claude.md) — Frontier AI language models by Anthropic.

## Sources / references
- [MicroGPT GitHub Repository](https://github.com/karpathy/microGPT)
- [Karpathy's Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
