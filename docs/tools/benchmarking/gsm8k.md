# GSM8K (Grade School Math 8K)

## What it is
GSM8K (Grade School Math 8K) is a canonical benchmark dataset containing 8,500 high-quality, linguistically diverse grade school math word problems. Originally created by OpenAI research teams to probe multi-step arithmetic reasoning in language models, it has evolved into the definitive industry standard for evaluating "Reasoning Density" and Chain-of-Thought (CoT) trajectory accuracy. Each problem requires between 2 and 8 sequential quantitative steps, combining elementary arithmetic operations (addition, subtraction, multiplication, division, fractions, percentages) with natural language problem formulation.

As of 2027, GSM8K is the fundamental baseline benchmark for validating both frontier multi-modal reasoning models (such as **Claude 5.1**, **GPT-5.5 / 5.6**, and **Gemini 4.0 Pro**) and local open-weights reasoning systems (such as **Llama 4 Maverick**, **Qwen 3.8**, and **DeepSeek-R1** derivative models). FastMCP 3.1 harness extensions enable real-time verification and trace inspection during model inference and evaluation loops.

## What problem it solves
In the evolution of natural language processing, early language models frequently failed when attempting multi-step mathematical calculations because they relied on direct surface-text pattern matching rather than step-by-step internal state transitions. Standard single-turn QA benchmarks could not distinguish between a model that possessed genuine quantitative reasoning capabilities and one that merely memorized surface associations.

GSM8K solves this by requiring:
- **Explicit Reasoning Traces**: Forcing models to generate explicit Chain-of-Thought (CoT) reasoning paths before stating the final answer.
- **Unambiguous Deterministic Scoring**: Terminating each solution with an explicit target token (`#### <number>`), enabling zero-ambiguity Exact Match (EM) automated validation.
- **Intermediate State Verification**: Providing a framework for training process-supervised reward models (PRMs) and verification agents that evaluate each individual step of logical deduction.
- **Standardized Multi-Step Planning Assessment**: Serving as a foundational predictor of an LLM's capacity for complex, multi-tool agentic planning and code execution.

## System Architecture

```
                                      GSM8K FastMCP 3.1 Benchmarking Pipeline

  +-----------------------+        +-----------------------------------+        +-----------------------------------+
  | GSM8K Dataset (8.5K)  | ---->  | FastMCP 3.1 Task Harness Runner   | ---->  | CoT Generation Engine             |
  | - 7,473 Train Set     |        | - Model Context Protocol (MCP)    |        | - Claude 5.1 / GPT-5.6 / Llama 4 |
  | - 1,319 Test Set      |        | - Concurrent Batch Orchestrator   |        | - Multi-step Reasoning Traces     |
  +-----------------------+        +-----------------------------------+        +-----------------------------------+
                                                                                                  |
                                                                                                  v
  +-----------------------+        +-----------------------------------+        +-----------------------------------+
  | Metric Aggregator     | <----  | Pydantic v2 Answer & CoT          | <----  | Process Reward Model / Verifier   |
  | - Exact Match (EM)    |        | Validation Schema                 |        | - Regex Answer Extractor          |
  | - Reasoning Tokens    |        | - Strict Output Verification      |        | - Step-level Logic Check          |
  +-----------------------+        +-----------------------------------+        +-----------------------------------+
```

## Where it fits in the stack
In the modern AI research and deployment stack, GSM8K occupies a foundational position within the **Benchmarking & Quality Assurance Layer**. It acts as a primary gatekeeping check during:
1. **Pre-training & Alignment Validation**: Measuring whether architecture tweaks or training dataset adjustments improve intermediate logic retention.
2. **Post-Training & Fine-Tuning**: Testing Reinforcement Learning from Human/AI Feedback (RLHF/RLAIF) and Direct Preference Optimization (DPO) routines targeting quantitative reasoning.
3. **Agentic System Baseline Evaluation**: Serving as a standardized micro-benchmark before deploying models into multi-agent frameworks, tool-calling pipelines, or autonomous code generation workflows.
4. **Quantization & Distillation Verification**: Assessing whether edge-quantized models (e.g., GGUF/EXL2 4-bit runs) retain mathematical accuracy relative to full-precision FP16/BF16 baselines.

## Typical use cases
- **Frontier Model Evaluation**: Benchmarking state-of-the-art models like **Claude 5.1 Opus** and **GPT-5.5** on zero-shot and few-shot reasoning tasks.
- **Process Reward Model (PRM) Training**: Fine-tuning verifiers that evaluate individual reasoning steps (step-level correctness) rather than solely checking the final outcome.
- **Prompt Engineering & Method Analysis**: Comparing standard zero-shot prompting, few-shot CoT prompting, Tree-of-Thoughts (ToT) exploration, and Self-Consistency sampling (e.g., majority vote across 64 reasoning runs).
- **Edge Model Optimization**: Quantifying the math accuracy degradation curve when distilling 70B+ open models into compressed 8B or 3B local runtimes.
- **Automated Synthetic Dataset Expansion**: Generating mathematical variations using rejection sampling for domain-specific downstream training.

## Strengths
- **Rigorous Step Decomposition**: Requires multi-step logical transitions, providing granular insights into where a model's reasoning chain breaks down.
- **Deterministic and Objective Evaluation**: Exact Match (EM) scoring against normalized numerical outputs eliminates evaluation subjectivities typical of open-ended LLM-as-a-judge scoring.
- **Universal Baseline Adoption**: Supported across all major benchmark execution frameworks, including `lm-eval-harness`, `DeepEval`, `Promptfoo`, and `FastMCP`.
- **High Correlation with General Reasoning**: Strong performance on GSM8K consistently correlates with superior coding capabilities, structured JSON generation, and tool-calling proficiency.
- **Process Verification Suitability**: Ideal for step-level verification research, as intermediate steps follow natural grade-school arithmetic rules.

## Limitations
- **Elementary Difficulty Ceiling**: Capped at middle-school math complexity; fails to differentiate performance on advanced calculus, linear algebra, or graduate-level problem solving (where [MATH Benchmark](math-benchmark.md) or [GPQA](gpqa.md) are required).
- **Data Contamination Sensitivity**: Due to its longevity and wide availability, widespread web scrapers have incorporated GSM8K test samples into web-scale pre-training datasets, requiring contamination audits.
- **Brittle Extracted Format**: Traditional parsing relies heavily on the presence of specific delimiters (like `####`), which models may omit if prompt instructions are not strictly structured.
- **Lack of Multi-Modal Support**: Original dataset is strictly text-based; multi-modal extensions (such as MathVista or VisualGSM8K) must be used for vision-language models.

## When to use it
- When performing baseline evaluation of new LLM checkpoints, fine-tuned adapters, or quantized model builds.
- When validating the effectiveness of Chain-of-Thought (CoT), Reasoning Tokens, or verifier-guided inference decoding.
- When testing the logical reasoning capabilities of local edge-deployed models (e.g., Llama 4 Maverick 8B).
- For automated CI/CD regression tests during prompt template modifications or agent system updates.

## When not to use it
- When assessing university-level or professional mathematical problem-solving (use [MATH Benchmark](math-benchmark.md)).
- When evaluating complex multi-modal chart/diagram interpretation (use MathVista or GeoQA).
- When assessing domain-specific programming skills (use [HumanEval](human-eval.md) or SWE-bench).
- When testing qualitative language comprehension, creative writing, or domain knowledge retrieval (use [MMLU](mmlu.md)).

## Getting started

### Standard Evaluation via LM Evaluation Harness
The `lm-evaluation-harness` by EleutherAI remains the reference framework for executing standard GSM8K evaluations against local or remote models.

```bash
# 1. Install evaluation harness with Hugging Face transformers support
pip install lm-eval[hf,anthropic,openai]

# 2. Run 5-shot Chain-of-Thought GSM8K evaluation on a local Hugging Face model
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-4-Maverick-70B,trust_remote_code=True \
    --tasks gsm8k \
    --num_fewshot 5 \
    --batch_size 8 \
    --device cuda:0 \
    --output_path ./gsm8k_results.json
```

### FastMCP 3.1 Microservice Benchmarking Architecture
Below is a production-ready FastMCP 3.1 server setup that exposes GSM8K evaluation tools for local or agentic test suites:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import re
import json

mcp = FastMCP("GSM8K-Benchmarking-Suite")

class EvaluationRequest(BaseModel):
    problem: str = Field(..., description="The GSM8K math problem text")
    model_solution: str = Field(..., description="The raw model output containing CoT and final answer")
    ground_truth: str = Field(..., description="The ground truth numeric answer or reference text")

class EvaluationResult(BaseModel):
    is_correct: bool = Field(..., description="Whether the extracted numeric answer matches ground truth")
    extracted_answer: str = Field(..., description="The answer string parsed from model solution")
    expected_answer: str = Field(..., description="The cleaned ground truth answer")
    reasoning_trace: str = Field(..., description="Extracted step-by-step reasoning text")

def clean_answer(text: str) -> str:
    """Extracts numeric values from GSM8K ground truth or target strings."""
    match = re.search(r"####\s*(-?[\d,]+(?:\.\d+)?)", text)
    if match:
        return match.group(1).replace(",", "")
    numbers = re.findall(r"-?[\d,]+(?:\.\d+)?", text)
    if numbers:
        return numbers[-1].replace(",", "")
    return text.strip()

@mcp.tool()
def evaluate_gsm8k_sample(req: EvaluationRequest) -> str:
    """Evaluates a single GSM8K model output against ground truth using FastMCP 3.1."""
    parsed_model_ans = clean_answer(req.model_solution)
    parsed_truth_ans = clean_answer(req.ground_truth)

    is_correct = (parsed_model_ans == parsed_truth_ans)

    # Extract reasoning trace prior to final delimiter
    trace_parts = req.model_solution.split("####")
    reasoning_trace = trace_parts[0].strip() if trace_parts else req.model_solution

    result = EvaluationResult(
        is_correct=is_correct,
        extracted_answer=parsed_model_ans,
        expected_answer=parsed_truth_ans,
        reasoning_trace=reasoning_trace
    )
    return result.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## CLI examples

### 1. Zero-Shot Evaluation with Ollama Local Runtime
Run zero-shot evaluation on locally served Ollama models:

```bash
lm_eval --model ollama \
    --model_args base_url=http://localhost:11434,model=qwen3.8-instruct \
    --tasks gsm8k_cot \
    --num_fewshot 0 \
    --output_path ./results_qwen38.json
```

### 2. Multi-GPU Distributed Evaluation with vLLM
Execute high-throughput benchmark runs across tensor-parallel GPU clusters:

```bash
python3 -m lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-4-Maverick-70B,tensor_parallel_size=4,dtype=bfloat16 \
    --tasks gsm8k \
    --num_fewshot 8 \
    --batch_size auto
```

### 3. Extracting EM Accuracy Metrics via Command Line
Parse raw results JSON produced by the benchmarking runner:

```bash
python3 -c "
import json, sys
data = json.load(open('results_qwen38.json'))
results = data.get('results', {}).get('gsm8k', {})
acc = results.get('exact_match,none', results.get('acc', 0.0))
print(f'GSM8K Exact Match Accuracy: {acc * 100:.2f}%')
"
```

## API examples

### 1. Python: FastMCP 3.1 Async CoT Evaluator with Pydantic v2
The following complete script demonstrates how to execute multi-step CoT reasoning evaluations against frontier APIs like **Claude 5.1** or **GPT-5.5**, validate responses with Pydantic v2 schemas, and track intermediate reasoning tokens:

```python
import os
import re
import asyncio
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from anthropic import AsyncAnthropic

class ReasoningStep(BaseModel):
    step_number: int
    content: str
    intermediate_value: Optional[float] = None

class BenchmarkEvaluationSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

    problem_id: str = Field(..., description="Unique dataset item key")
    problem_text: str = Field(..., description="GSM8K problem statement")
    extracted_steps: List[ReasoningStep] = Field(default_factory=list)
    final_numeric_answer: Optional[float] = Field(None, description="Parsed numeric result")
    ground_truth_numeric: float = Field(..., description="Target reference numeric result")
    is_exact_match: bool = Field(..., description="Exact match evaluation result")
    raw_response_text: str = Field(..., description="Full model completion string")

class GSM8KAsyncEvaluator:
    def __init__(self, api_key: Optional[str] = None):
        self.client = AsyncAnthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    def parse_final_number(self, text: str) -> Optional[float]:
        # Search for explicit #### format or last numeric sequence
        match = re.search(r"####\s*(-?[\d,]+(?:\.\d+)?)", text)
        if match:
            clean_str = match.group(1).replace(",", "")
            return float(clean_str)

        matches = re.findall(r"-?[\d,]+(?:\.\d+)?", text)
        if matches:
            clean_str = matches[-1].replace(",", "")
            try:
                return float(clean_str)
            except ValueError:
                return None
        return None

    async def evaluate_sample(
        self,
        problem_id: str,
        question: str,
        ground_truth_str: str,
        model_name: str = "claude-5-1-opus-20261031"
    ) -> BenchmarkEvaluationSchema:
        prompt = (
            f"Solve the following grade-school math problem step-by-step.\n"
            f"At the end of your response, write the final numerical answer clearly following "
            f"the format '#### <number>'.\n\n"
            f"Question: {question}\n\nAnswer:"
        )

        response = await self.client.messages.create(
            model=model_name,
            max_tokens=1024,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )

        completion = response.content[0].text
        extracted_num = self.parse_final_number(completion)
        target_num = self.parse_final_number(ground_truth_str) or 0.0

        exact_match = (
            extracted_num is not None and abs(extracted_num - target_num) < 1e-5
        )

        # Decompose lines into structured reasoning steps
        lines = [line.strip() for line in completion.split("\n") if line.strip()]
        steps = []
        for idx, line in enumerate(lines[:-1], start=1):
            steps.append(ReasoningStep(step_number=idx, content=line))

        return BenchmarkEvaluationSchema(
            problem_id=problem_id,
            problem_text=question,
            extracted_steps=steps,
            final_numeric_answer=extracted_num,
            ground_truth_numeric=target_num,
            is_exact_match=exact_match,
            raw_response_text=completion
        )

async def main():
    evaluator = GSM8KAsyncEvaluator()
    sample_q = "Janet has 30 apples. She gives 10 to her neighbor and then buys 15 more. How many apples does she have now?"
    sample_gt = "Janet starts with 30 apples. Gives away 10: 30 - 10 = 20. Buys 15 more: 20 + 15 = 35. #### 35"

    result = await evaluator.evaluate_sample(
        problem_id="gsm8k_val_001",
        question=sample_q,
        ground_truth_str=sample_gt
    )

    print("--- Benchmark Result ---")
    print(f"Exact Match: {result.is_exact_match}")
    print(f"Parsed Value: {result.final_numeric_answer}")
    print(f"Expected Value: {result.ground_truth_numeric}")
    print(f"Reasoning Steps Count: {len(result.extracted_steps)}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Standard Frontier Model Performance Baselines (2027)

| Model Name | Provider / Architecture | Evaluation Strategy | GSM8K Exact Match (EM) | Average CoT Tokens |
| :--- | :--- | :--- | :--- | :--- |
| **Claude 5.1 Opus** | Anthropic | Zero-Shot CoT | **99.3%** | 185 tokens |
| **GPT-5.6 / Reasoning** | OpenAI | Adaptive Thinking | **99.1%** | 210 tokens |
| **Gemini 4.0 Pro** | Google DeepMind | Dynamic Chain | **98.8%** | 195 tokens |
| **Llama 4 Maverick (70B)** | Meta AI (Open-Weights) | 5-Shot CoT | **96.8%** | 240 tokens |
| **DeepSeek-R1 Distill (32B)** | DeepSeek / Open-Weights | Self-Consistency (Maj@8) | **96.2%** | 310 tokens |
| **Qwen 3.8 Instruct (14B)** | Alibaba Cloud | 5-Shot CoT | **95.5%** | 225 tokens |

## Related tools / concepts
- [MATH Benchmark](math-benchmark.md) — Advanced high-school and competition level mathematics evaluation.
- [GPQA](gpqa.md) — Graduate-level biology, physics, and chemistry reasoning dataset.
- [MMLU](mmlu.md) — Multi-task language understanding across 57 academic subjects.
- [HumanEval](human-eval.md) — Standardized Python functional code generation benchmark.
- [DREAM](dream.md) — Deep research evaluation with agentic metrics.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for extending model capabilities with live tool runners.
- [Claude](../ai_knowledge/claude.md) — High-performing frontier intelligence platform for reasoning tasks.
- [GPT-5.5](../ai_knowledge/openai.md) — State-of-the-art multimodal reasoning model series.

## Sources / references
- [OpenAI GSM8K GitHub Repository](https://github.com/openai/grade-school-math)
- [Hugging Face GSM8K Dataset Hub](https://huggingface.co/datasets/openai/gsm8k)
- [Arxiv: Training Verifiers to Solve Math Word Problems (Cobbe et al., 2021)](https://arxiv.org/abs/2110.14168)
- [EleutherAI LM Evaluation Harness Documentation](https://github.com/EleutherAI/lm-evaluation-harness)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
