# Custom Agents (SSH + LLM Loop)

## What it is
A "Custom Agent" is a lightweight Python script or automation (e.g., n8n) that implements a basic loop: Prompt LLM -> Receive Command -> Execute via SSH -> Return Output to LLM.

## What problem it solves
Provides a tailored, minimal orchestration layer for specific infrastructure tasks without the overhead or complexity of full agent platforms. It allows for precise control over the security and execution plane.

## Where it fits in the stack
**Agent / Orchestration Layer**. It is the logic that coordinates the LLM (Reasoning) and the target machine (Execution via SSH).

## Architecture overview
```text
[ LLM (Reasoning) ] <-----> [ Custom Python Script (Controller) ] <-----> [ Target Server (SSH) ]
                                      |
                                      +--> [ Approval Loop (Human) ]
```

## Typical workflows
- **Server Maintenance**: "Check disk space on all nodes and clear logs if above 90%."
- **Configuration Updates**: "Update the nginx config on the proxy server and reload the service."
- **Diagnostics**: "Analyze why the service on the Raspberry Pi is failing to start."

## Strengths
- **Simplicity**: Easy to understand and modify.
- **Security**: You control exactly which commands are allowed and how SSH is handled.
- **Portability**: Can run as a small script anywhere.
- **Transparency**: Every step of the loop is visible and can be logged easily.

## Limitations
- **Manual Work**: Requires writing and maintaining the controller script.
- **Context Management**: Needs manual handling of history and state (unlike Aider or OpenHands).
- **Tooling**: Lacks the advanced "repo map" or "browser" tools of larger frameworks.

## When to use it
- For specific, repetitive infrastructure tasks.
- When you need a high degree of security (e.g., manual approval for every command).
- For lightweight automation on resource-constrained devices.

## When not to use it
- For general software engineering or coding tasks (use Aider/OpenHands).
- When the task requires complex reasoning across hundreds of files.

## Security considerations
- **SSH Key Safety**: The script needs access to SSH keys; protect these with extreme care.
- **Command Injection**: Ensure the LLM output is parsed safely before being executed.
- **Least Privilege**: The SSH user should only have the permissions necessary for the task.

## Links to related pages
- [SSH Execution Patterns](../../architecture/ssh_execution_patterns.md)
- [Raspberry Pi Kiosk Automation](../../playbooks/raspberry-pi-kiosk-automation.md)
- [OpenAI](../ai_knowledge/openai.md)

## Sources / References

- [Reference](https://github.com/joanmarcriera/Home-office-automations)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
