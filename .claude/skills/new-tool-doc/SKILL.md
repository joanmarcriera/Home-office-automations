---
name: new-tool-doc
description: Scaffold a new tool documentation page following the repo's catalogue conventions. Pass the tool name and category. Creates the file, populates the standard template, and adds it to mkdocs.yml nav.
disable-model-invocation: true
---

# New Tool Doc

Scaffold a new tool page for the Home-Office Automation & AI Hub catalogue.

## Usage

```
/new-tool-doc <tool-name> <category>
```

Categories: `ai_knowledge` | `frameworks` | `providers` | `agents` | `orchestration` | `infrastructure` | `benchmarking` | `development_ops`

## Steps

1. **Determine the file path** from the category:
   - `docs/tools/<category>/<tool-name>.md`

2. **Check for duplicates** — search the repo for the tool name before creating:
   ```bash
   grep -r "<tool-name>" docs/tools/ --include="*.md" -l
   ```
   If a match exists, tell the user and stop.

3. **Create the file** using this exact template:

```markdown
# <Tool Name>

## What it is
<One sentence: what the tool is.>

## What problem it solves
<One paragraph: the specific problem it addresses.>

## Where it fits in the stack
**Category**: <Category from taxonomy>

## Typical use cases
- **<Use case 1>**: <Description>
- **<Use case 2>**: <Description>

## Strengths
- **<Strength 1>**: <Description>
- **<Strength 2>**: <Description>

## Limitations
- **<Limitation 1>**: <Description>
- **<Limitation 2>**: <Description>

## When to use it
- <Scenario>

## When not to use it
- <Scenario>

## Related tools / concepts
- [<Related Tool>](<relative-path>)

## Sources / references
- [<Source title>](<URL>)
```

4. **Add to mkdocs.yml nav** — find the correct nav section for the category and insert the new entry in alphabetical order.

5. **Add to the category index** at `docs/tools/<category>/index.md` — insert a row in the Contents table.

6. **Confirm** what was created and where.
