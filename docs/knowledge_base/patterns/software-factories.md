# Software Factories Pattern

## What it is
The Software Factory is an architectural pattern for non-interactive software development where agents write code, run validation harnesses, and converge on solutions without human review. It treats code as a commodity ("tokens are the fuel") and shifts the human role from writing code to defining the "seeds" and "validation harnesses."

## What problem it solves
- **Review Bottleneck**: Traditional AI-assisted development still requires human review, which becomes the primary throughput limit as models get faster and cheaper.
- **Inhuman Mistakes**: By replacing human review with rigorous, automated end-to-end validation (scenarios), it catches "inhuman" mistakes that a human might miss in thousands of lines of generated code.
- **Economic Feasibility**: Enables the creation of "Digital Twins" or complex simulators that were previously too expensive to build manually.

## Where it fits in the stack
**Pattern**. This belongs in the upper layers of the agentic stack, specifically under **Orchestration** and **Quality Assurance**. It defines the workflow loop for high-autonomy coding agents.

## Typical use cases
- Developing complex security software with unreviewed code.
- Building high-fidelity clones (Digital Twins) of SaaS services (Okta, Slack, Jira) for safe, high-volume testing.
- "Gene Transfusion": Extracting patterns from legacy systems and porting them to new architectures autonomously.

## Strengths
- **Compounding Correctness**: Long-horizon agentic workflows can self-correct when guided by a strong validation loop.
- **Extreme Scale**: Validation can run at volumes and rates far exceeding production limits or human review capacity.
- **Cost-Efficiency (at scale)**: While token-heavy, it eliminates the expensive human-in-the-loop for every PR.

## Limitations
- **Token Intensive**: Can require significant spending on frontier models (e.g., $1,000/day per engineer in enterprise settings).
- **Bootstrap Requirement**: Requires an initial "seed" (PRD, spec, or screenshot) and a high-fidelity validation environment.
- **Probabilistic Success**: Shifts from boolean "test green" to probabilistic "satisfaction" based on multiple trajectories through scenarios.

## When to use it
- When building systems where the cost of a human reviewer is higher than the cost of exhaustive automated validation.
- For "Dark Factory" projects where the goal is zero hand-coded software.
- When you need to test against complex external integrations that require a "Digital Twin."

## When not to use it
- Small, simple projects where a human can easily verify the output.
- Low-budget environments where token costs for exhaustive loops are prohibitive (unless using local LLMs).
- Systems where the validation harness cannot be reliably automated.

## Local & Free Adaptations
To implement the Software Factory pattern in local, free-as-in-beer environments:

### 1. Local Backend Orchestration
- **Inference Engine**: Use [Ollama](../../services/ollama.md) or [vLLM](../../tools/infrastructure/vllm.md) to serve open-weights models locally.
- **Specialized Models**: Utilize coding-optimized models like **Qwen 2.5 Coder** (32B or 72B) which rival frontier models in coding tasks while running on consumer hardware.
- **LiteLLM Routing**: Use [LiteLLM](../../services/litellm.md) to route between local models and free tier APIs (Groq, Gemini Free) to maximize value-per-token.

### 2. Local Digital Twins
- Instead of paying for SaaS API access during testing, use coding agents to build **Local Mocks** or simulators of your dependencies.
- Use agents to "gene transfuse" the public API documentation of a service into a lightweight Go or Python simulator.
- Run these twins in Docker containers locally to enable 24/7 stress testing without rate limits or costs.

### 3. Satisfaction-Based Validation
- Replace expensive frontier model "judges" with local "small but mighty" models (like Llama 3.1 8B or Qwen 2.5 7B) for the first 90% of validation.
- Implement **Red/Green TDD** loops where the local agent must first make a failing test pass before moving to the next scenario.
- Use **Scenario-as-Holdout**: Store end-to-end user stories in a local directory that the agent only sees during the validation phase, not during the implementation phase.

## Related tools / concepts
- [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)
- [Digital Twin Universe](https://factory.strongdm.ai/techniques/digital-twin-universe)
- [Qwen 2.5 Coder](../../tools/ai_knowledge/qwen.md)
- [Jules](../../tools/ai_knowledge/jules.md) (The autonomous coding agent used in this hub)

## Sources / References
- [Simon Willison: Software Factories and the Agentic Moment](https://simonwillison.net/2026/Feb/7/software-factory/)
- [StrongDM Software Factory Principles](https://factory.strongdm.ai/principles)
- [StrongDM Techniques](https://factory.strongdm.ai/techniques)

## Contribution Metadata
- Last reviewed: 2026-03-09
- Confidence: high
