## Weekly Doc Deepening

The following docs are the shallowest in the knowledge base and need practical content.

### Target docs
<!-- GENERATED_LIST placeholder — weekly_planner.py fills this -->

### Instructions
For each doc above:
1. Read the tool's official website/GitHub from its **Sources / References** section
2. Add a `## Getting started` section after `## When not to use it` with:
   - Installation command (`pip install`, `npm install`, `docker pull`, or equivalent)
   - A minimal working example in a fenced code block (Python, CLI, or config as appropriate)
3. If the tool has a CLI, add `## CLI examples` with 2-3 common commands
4. If the tool has an API/SDK, add `## API examples` with a Python or curl snippet
5. Keep all existing content unchanged
6. Update `- Last reviewed:` in the Contribution Metadata section

### Quality checks
- Verify: `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"`
- Ensure all code examples are complete and runnable (no placeholder `...` blocks)
