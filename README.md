# AgentGrimoire  
A collaborative spellbook of modular, open-source tools for AI agents — built for developers who want full control over their agent architecture, without relying on paid APIs or proprietary ecosystems.

---

## Overview

AgentGrimoire is an expanding collection of lightweight, modular tools designed for building AI agents in local-first and fully open environments. The goal is simple: provide a community-driven ecosystem of reusable components that developers can combine to create their own agent systems.

This repository also serves as the foundation for a future open-source ADK alternative. Think of AgentGrimoire as the low-level toolkit that will eventually power an open, extensible, developer-focused agent framework.

AgentGrimoire focuses on:

- Local-first, API-independent workflows  
- Transparency and readability  
- Minimal dependencies  
- Small, focused, well-documented tools  
- Cross-language flexibility  
- Community-driven design and contributions  

Use it alongside local LLMs, custom orchestrators, multi-agent systems, or your own ADK-style architectures.

---

## Purpose

AgentGrimoire exists for developers who want full control over their agent stack.  
No vendor lock-in, no required cloud infrastructure, and no black-box abstractions.

You can use this repository to:

- Build custom agent pipelines  
- Compose multi-agent systems using modular tools  
- Support entirely local inference setups  
- Develop your own open-source ADK-like framework  
- Share practical utilities that solve real agent-related problems  

The project stays intentionally minimalist. Its strength comes from community contributions.

---

## Repository Structure

The repository is organized into domain-based folders; each tool (a
**spell**) lives in its own folder with a manifest, an implementation,
and a short README:

```
<domain>/
  <spell_name>/
    spell.json     # manifest: name, description, entrypoint, JSON Schema
    spell.py       # implementation (stdlib-only unless justified)
    README.md      # purpose, inputs, outputs, example, safety notes
```

Tools can be implemented in any language. What matters is that they remain:

- Minimal  
- Modular  
- Easy to integrate  
- Well-documented  
- Runnable locally  

Every tool should feel like a small, focused utility that an agent can call directly.

---

## The Spellbook

| Spell | Domain | What it does |
|---|---|---|
| `word_count` | `text/` | Words, characters, and lines of a text |
| `regex_extract` | `text/` | Every match of a regex, capped |
| `calculate` | `math/` | Safe arithmetic (AST whitelist, never `eval`) |
| `read_text` | `files/` | Read a local text file, size-capped |
| `list_directory` | `files/` | Directory entries with type and size |
| `current_datetime` | `system/` | The current date/time (models can't guess it) |
| `http_fetch` | `network/` | GET a public URL, size/time-capped, SSRF-guarded |

Every spell is validated in CI: manifests are checked, the whole tree is
loaded, and each tool is executed against sample inputs.

---

## Tool Format

Each tool ships three files (see
[templates/TOOL_TEMPLATE.md](./templates/TOOL_TEMPLATE.md) for the full
skeleton):

- **`spell.json`** — the manifest: `name` (matches the folder),
  `description`, `entrypoint` (`spell.py:function`), and `parameters` as
  standard JSON Schema. This is what a model reads to decide how to call
  the tool — write the descriptions for a model.
- **The implementation** — a plain function with typed inputs and
  machine-readable output. Errors must carry actionable messages: in
  agent loops the error text is fed back to the model so it can
  self-correct.
- **A folder README** — purpose, inputs/outputs, example, safety notes.

The design philosophy mirrors the Unix style: small components, composed into larger systems.

---

## Using the Grimoire from an orchestrator

The manifest convention is orchestrator-agnostic JSON. With
[sanctum-engine](https://github.com/zquintero246/sanctum-engine) the whole
tree loads in one line:

```python
import asyncio
from sanctum import Tome, summon
from sanctum.oracle.ollama import OllamaOracle   # or any local backend

tome = Tome.load_from_directory("path/to/AgentGrimoire")
entity = summon(OllamaOracle(arcana="qwen2.5:7b"), tome)

result = asyncio.run(entity.ainvoke({"messages": [
    {"role": "user", "content": "What is (2 + 3) * sqrt(16)? Use a tool."},
]}))
print(result["messages"][-1]["content"])
```

Every `spell.py` is also a self-contained module with zero framework
imports — copy the file straight into your project, or load it by path
with `importlib` if you prefer to vendor nothing.

To validate the collection locally:

```sh
pip install -r requirements-dev.txt
pytest
```

---

## Contribution Guidelines

Detailed rules are provided here:

**[CONTRIBUTING.md](./CONTRIBUTING.md)**

Summary:

- Write clear and readable code  
- Keep tools small and single-purpose  
- Minimize dependencies  
- Document everything  
- Ensure tools run locally without paid APIs  
- Maintain the folder structure and naming conventions  

High-quality community contributions are encouraged and appreciated.

---

## Examples

The quickest full example is in
[Using the Grimoire from an orchestrator](#using-the-grimoire-from-an-orchestrator)
above; every spell folder also carries its own README with a runnable
snippet. For a complete multi-agent pipeline consuming this repository's
conventions, see the
[sanctum-engine examples](https://github.com/zquintero246/sanctum-engine/tree/main/examples).

---

## Contributors

<a href="https://github.com/zquintero246/AgentGrimoire/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=zquintero246/AgentGrimoire&max=200" alt="Contributors" />
</a>

---

## Visual

![ascii-animation](https://github.com/user-attachments/assets/23680558-fd58-4d66-b28f-1cc65c28fc77)


## License

MIT License. See the LICENSE file for details.

