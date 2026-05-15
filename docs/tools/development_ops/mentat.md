# Mentat

## What it is
Mentat is an open-source AI coding assistant that operates directly from your command line. Unlike many other AI tools, Mentat coordinates edits across multiple files and locations simultaneously, leveraging the full context of your project without requiring manual copy-pasting.

## What problem it solves
It reduces the friction of applying complex, multi-file changes and refactors. By understanding the codebase context and providing a terminal-native workflow, Mentat helps developers execute broad architectural changes or repetitive editing tasks with high precision and minimal manual effort.

## Where it fits in the stack
**Development & Ops / AI Coding Assistant**. It serves as a terminal-based alternative to IDE-integrated AI tools, offering more direct control over multi-file edit coordination.

## Typical use cases
- **Multi-file Refactoring**: Renaming classes or functions and updating all references across the project.
- **Feature Implementation**: Scaffolding new features that require changes in logic, tests, and configuration files.
- **Codebase Navigation**: Asking questions about how different parts of the project interact.
- **Automated Bug Fixing**: Providing instructions to fix a bug and letting Mentat identify and edit the relevant files.

## Getting started

### Installation
Mentat requires Python 3.10 or higher. It is recommended to use a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mentat-ai
```

### Configuration
Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

### Basic Usage
Run Mentat within your git project directory:

```bash
# Start Mentat with specific files in context
mentat path/to/file1.py path/to/file2.py

# Start Mentat with a whole directory
mentat src/
```

Once inside the Mentat REPL, you can provide instructions in natural language.

## Strengths
- **Multi-file Coordination**: Exceptional at managing edits that span across several files.
- **Context Awareness**: Automatically respects `.gitignore` and includes project context by default.
- **Terminal-Native**: Fits perfectly into workflows for developers who prefer the command line.
- **Fine-grained Control**: Allows users to specify exactly which files should be in context.

## Limitations
- **External API Dependency**: Primarily relies on OpenAI's models (GPT-4), requiring an active API key and internet connection.
- **Context Limits**: Large projects can still hit LLM token limits if too many files are included at once.
- **Community Size**: Smaller ecosystem compared to established tools like GitHub Copilot or Aider.

## When to use it
- When performing refactors that affect multiple files.
- When you want to remain in the terminal but need AI help with complex code changes.
- When you need to provide a lot of local context to the AI without manual copy-pasting.

## When not to use it
- For simple, single-file completions where an IDE extension like Copilot might be faster.
- If you prefer a GUI-based interaction for AI assistance.
- In environments without reliable internet access or where proprietary code cannot be sent to external APIs.

## Related tools / concepts
- [Aider](aider.md): A similar terminal-based AI pair programming tool.
- [Plandex](plandex.md): An AI coding engine designed for complex tasks.
- [Claude Code](claude-code.md): Anthropic's official terminal-based coding assistant.
- [Cursor](cursor.md): An AI-native code editor.
- [Windsurf](windsurf.md): An agentic IDE by Codeium.
- [Continue](continue_dev.md): An open-source AI extension for VS Code and JetBrains.
- [Codeium](codeium.md): A suite of AI-powered development tools.

## Sources / references
- [Official GitHub Repository](https://github.com/AbanteAI/mentat)
- [Mentat Website](https://mentat.ai/)
- [Mentat Documentation](https://mentat.codes/)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
