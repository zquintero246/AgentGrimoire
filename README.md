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

The repository is organized into domain-based folders. Each directory groups tools by their purpose within agent workflows.

Examples:

- `text/` — text formatting, rewriting, parsing, summarization  
- `search/` — lightweight scrapers, local search utilities, safe fetchers  
- `files/` — file operations, conversion utilities, metadata processors  
- `system/` — shell-level helpers, OS utilities, environment tools  
- `llm/` — helpers for local inference or model utilities  
- `network/` — minimal HTTP request helpers  

Tools can be implemented in any language. What matters is that they remain:

- Minimal  
- Modular  
- Easy to integrate  
- Well-documented  
- Runnable locally  

Every tool should feel like a small, focused utility that an agent can call directly.

---

## Tool Format

Each tool must include:

- A clear explanation of its purpose  
- Usage examples or instructions  
- Input and output details  
- Notes on behavior or safety (if applicable)  
- Minimal external dependencies  

The design philosophy mirrors the Unix style: small components, composed into larger systems.

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

## Examples (Work in Progress)

If you want an early example, feel free to open an issue.

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

