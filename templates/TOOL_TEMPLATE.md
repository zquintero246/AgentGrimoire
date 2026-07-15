# Tool template

Copy this layout to add a new spell. One folder per tool, inside the
domain folder that fits best:

```
<domain>/
  <spell_name>/
    spell.json     # manifest (required for auto-loading)
    spell.py       # implementation (any language works; see below)
    README.md      # purpose, inputs, outputs, example, safety notes
```

## spell.json

```json
{
  "name": "<spell_name>",
  "description": "One line: what the tool does.",
  "entrypoint": "spell.py:<function_name>",
  "parameters": {
    "type": "object",
    "properties": {
      "some_input": {
        "type": "string",
        "description": "What this input means."
      }
    },
    "required": ["some_input"]
  }
}
```

- `name` must match the folder name.
- `entrypoint` is `<file>.py:<function>`, relative to the spell folder.
- `parameters` is standard JSON Schema — this is exactly what a model
  sees when deciding how to call your tool, so write the descriptions
  for a model.

## spell.py

```python
"""<spell_name> — one line: what the tool does.

Input : some_input (str)
Output: <shape of the return value>

Notes on side effects, determinism, and safety (see CONTRIBUTING §2.5).

Example:
    >>> <spell_name>("...")
    ...
"""


def <function_name>(some_input: str):
    """One-line summary."""
    ...
```

- Plain function, typed inputs, machine-readable output (dict/list/str).
- Stdlib only unless the tool's purpose demands more (justify it in the
  README).
- Raise `ValueError`/`FileNotFoundError` with **actionable messages** —
  in agent loops the error text is fed back to the model, so write it
  for a model to self-correct.

## Non-Python tools

Tools in other languages are welcome (CONTRIBUTING §2.6): document the
CLI invocation in the folder README. They won't auto-load into Python
orchestrators, but a thin `spell.py` wrapper (subprocess) makes them
loadable too.

## Checklist before the PR

- [ ] Folder name == manifest `name`
- [ ] Manifest parses and `entrypoint` resolves
- [ ] Docstring with inputs/outputs/example
- [ ] README.md in the folder
- [ ] Deterministic (or nondeterminism documented)
- [ ] No paid APIs; runs locally
- [ ] `pip install -r requirements-dev.txt && pytest` passes
