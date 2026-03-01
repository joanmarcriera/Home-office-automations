# Classes of Large Language Models

Large Language Models (LLMs) can be categorized into several classes based on their architecture, training objectives, and specialized capabilities.

## 1. Chat & Conversational Models
General-purpose models optimized for dialogue and following instructions.
- **Purpose**: General assistance, creative writing, Q&A.
- **Examples**: GPT-4o, Claude 3.5 Sonnet, Llama 3.1.

## 2. Reasoning & Logic Models
Models specifically designed or fine-tuned for complex multi-step reasoning, mathematical problem-solving, and logic.
- **Purpose**: Scientific research, complex coding, advanced mathematics.
- **Examples**: OpenAI o1-preview, o1-mini.

## 3. Mixture of Experts (MoE)
Architecture that uses a sparse execution path, activating only a subset of parameters for each token.
- **Purpose**: Efficiency and high performance without the cost of a full dense model.
- **Examples**: Mixtral 8x7B, DeepSeek-V2, GPT-4 (widely believed to be MoE).

## 4. Code Generation & Analysis Models
Models specialized in programming languages, debugging, and software architecture.
- **Purpose**: AI coding assistants, automated code review.
- **Examples**: CodeLlama, StarCoder2, DeepSeek-Coder-V2.

## 5. Vision-Language Models (Multimodal)
Models that can process and understand both text and images.
- **Purpose**: Image captioning, visual Q&A, document analysis (OCR).
- **Examples**: GPT-4o, Claude 3.5 Sonnet, Llama 3.2-Vision.

## 6. Audio-Native & Multimodal Audio Models
Models that can directly process or generate audio/speech without intermediate text conversion.
- **Purpose**: Real-time translation, emotion-aware voice assistants.
- **Examples**: GPT-4o (Advanced Voice), Gemini 1.5 Pro.
- **Sources**: [Current Large Audio Language Models largely transcribe rather than listen](https://arxiv.org/abs/2510.10444) (Analysis of auditory understanding vs transcription).

## 7. State Space Models (SSM) & Hybrids
Alternatives to the Transformer architecture (like Mamba) designed for very long context and linear scaling.
- **Purpose**: Processing extremely long documents, efficient inference.
- **Examples**: Jamba (Hybrid Transformer-Mamba), Mamba-2.

## 8. Embedding Models
Models that represent text as high-dimensional vectors.
- **Purpose**: Semantic search, RAG, document clustering.
- **Examples**: text-embedding-3-small, Voyage AI, BGE-M3.

## 9. Small Language Models (SLM)
Highly optimized models with fewer parameters (typically <10B) designed to run on-device.
- **Purpose**: Edge computing, privacy-sensitive local tasks.
- **Examples**: Phi-3.5, Gemma 2 2B, Llama 3.2 1B/3B.

## 10. Long-Context Models
Models specifically optimized to handle 100K+ tokens in their active window.
- **Purpose**: Analyzing entire codebases, long novels, or legal documents.
- **Examples**: Gemini 1.5 Pro (2M context), Claude 3 (200K context).

## 11. Tool-Use & Agentic Models
Models fine-tuned for reliable function calling and tool interaction.
- **Purpose**: Autonomous agents, complex workflow automation.
- **Examples**: NexusRaven-V2, Berkeley Function Calling Leaderboard (BFCL) top models.
- **Sources**: [The First Fully General Computer Action Model](https://si.inc/posts/fdm1) (Shift towards autonomous system interaction).

## 12. Variational Autoencoders (VAE)
Generative models that learn a compressed latent representation of data, often used for image and video synthesis.
- **Purpose**: Image/video reconstruction, generative diversity, latent space exploration.
- **Sources**: [Learnings from 4 months of Image-Video VAE experiments](https://www.linum.ai/field-notes/vae-reconstruction-vs-generation).

## Backlog
- Add comparison table of model architectures (Dense vs MoE vs SSM).
- Include details on "Reasoning Tokens" and "Chain of Thought" native models.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://arxiv.org/abs/2510.10444
- https://si.inc/posts/fdm1
- https://www.linum.ai/field-notes/vae-reconstruction-vs-generation
