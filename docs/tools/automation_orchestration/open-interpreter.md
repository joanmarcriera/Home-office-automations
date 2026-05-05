# Open Interpreter

## What it is
Open Interpreter is an open-source tool that lets LLMs run code (Python, JavaScript, Shell, and more) locally on your computer. It provides a natural language interface to your computer's capabilities, essentially acting as a locally-running, more powerful version of OpenAI's Code Interpreter (Advanced Data Analysis).

## What problem it solves
It solves the "walled garden" problem of hosted LLM code execution. While ChatGPT can write and run code in a sandbox, Open Interpreter runs on *your* machine, meaning it has access to your files, your internet connection, and your local tools, allowing it to perform real tasks like editing videos, searching your emails, or automating complex local workflows.

## Where it fits in the stack
**Category**: Automation & Orchestration / Agentic Execution

## Typical use cases
- **File Management**: "Find all large PDFs in my Downloads and move them to a new folder called Archive."
- **Data Analysis**: "Read this CSV, create a bar chart of the sales by region, and save it as a PNG."
- **System Automation**: "Set my computer to dark mode and open my three most frequent apps."
- **Web Scraping**: "Go to this website, find the top 5 news articles, and summarize them into a text file."

## Strengths
- **Local Execution**: Complete privacy and full access to local resources.
- **Multi-language Support**: Can run Python, Bash, JavaScript, and more.
- **Interactive**: Allows for human-in-the-loop confirmation before running potentially dangerous commands.
- **Flexible Models**: Can be used with hosted models (GPT-4) or local models (via Ollama or LM Studio).

## Limitations
- **Security Risk**: Running LLM-generated code locally is inherently risky. Always use the `--save_and_run` or interactive mode to review code.
- **Hardware Dependency**: Local performance depends on your computer's specs when running local models.

## Getting started

### Installation
```bash
pip install open-interpreter
```

### Basic Usage
```bash
interpreter
```
Then simply type your request in plain English.

## CLI examples
```bash
# Start an interactive interpreter session
interpreter

# Run a task in "fast" mode using a cheaper model
interpreter --fast

# Execute a specific request directly from the terminal
interpreter --task "Summarize the latest system logs"
```

## API examples
```python
from interpreter import interpreter

# Simple chat interface
interpreter.chat("What are the 5 largest files in my home directory?")

# Stream the output for real-time display
for chunk in interpreter.chat("Convert all .webp files in this folder to .png", display=False, stream=True):
    print(chunk)

# Configure the model and settings programmatically
interpreter.offline = True # Force local execution
interpreter.llm.model = "ollama/llama3"
```

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [Claude Code](../development_ops/claude-code.md)
- [Aider](../development_ops/aider.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Goose](goose.md)
- [Cline](../agents/cline.md)

## Sources / references
- [Open Interpreter Website](https://openinterpreter.com/)
- [Open Interpreter GitHub](https://github.com/OpenInterpreter/open-interpreter)

## Contribution Metadata
- Last reviewed: 2026-05-22
- Confidence: high
