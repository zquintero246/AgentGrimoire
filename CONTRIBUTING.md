# Contributing to AgentGrimoire

AgentGrimoire is a collaborative, community-driven collection of modular tools for AI agents.  
Contributions of any size are welcome, as long as they follow the design principles described below.

This document explains:

1. How to contribute  
2. The required conventions and design patterns for each tool  
3. The standards we follow for agent-focused development  
4. How to structure files, documentation, and examples  

The goal is to keep this repository clean, consistent, and easy to extend.

---

# 1. Contribution Process

## 1.1. Before Submitting

- Make sure your tool is **minimal**, **modular**, and **locally runnable**.  
- Verify that it does **not depend on paid APIs** or any closed ecosystem.  
- Read the design guidelines (Section 2) to ensure your tool follows agent-focused best practices.  
- Check whether a similar tool already exists in the repository.  
- If your contribution is significant or introduces a new domain folder, consider opening an issue first.

## 1.2. Fork, Branch, Commit

1. Fork the repository  
2. Create a descriptive branch name  
3. Write clean and readable code  
4. Include documentation and examples (required)  
5. Add tests if applicable  
6. Submit a pull request with a clear explanation of your tool and its purpose

## 1.3. Review Process

Maintainers will check:

- Code clarity  
- Correctness and safety  
- Consistency with tool conventions  
- Dependency minimalism  
- Documentation completeness  

We encourage iterative improvement instead of rejecting contributions outright.

---

# 2. Tool Conventions and Design Guidelines

AgentGrimoire follows the agent-tooling principles described in Google's agent tool design paper, adapted for fully open-source and local-first environments.

The goal is for every tool to be:

- **Discoverable**  
- **Predictable**  
- **Composable**  
- **Safe**  
- **Deterministic whenever possible**  
- **Transparent in inputs, outputs, and side-effects**  
- **Simple enough for an agent (or dev) to understand at a glance**

Below are the required conventions for every tool.

---

## 2.1. Tool Structure

Each tool must include:

1. **Top-level documentation block**  
   - What the tool does  
   - Its inputs and outputs  
   - Intended use cases  
   - Any assumptions or constraints  
   - Notes about determinism or safety if relevant

2. **A minimal, focused implementation**  
   - One tool should do one thing well  
   - Complex functionality should be broken into smaller tools

3. **A usage example**  
   - Show exactly how an agent or developer would call this tool  
   - Keep examples minimal and executable

4. **A clear and stable interface**  
   - Tools should expose a simple function, executable, or CLI entrypoint  
   - Inputs must be explicitly defined  
   - Outputs must be consistent and machine-readable where applicable

---

## 2.2. Inputs and Outputs

Tools must follow these conventions:

- Inputs should be **strictly typed** or clearly defined  
- Outputs must be **consistent, predictable**, and easy for an agent to parse  
- Avoid ambiguous output formats  
- Where possible, return machine-readable structures (JSON, clean text, YAML, etc.)  
- If the tool has side effects (file writes, network calls, OS operations), they must be documented clearly

Tools should never:

- Guess missing input  
- Infer behavior implicitly  
- Change format depending on situation  
- Produce non-deterministic output unless documented

---

## 2.3. Modularity and Composability

Each tool must be usable in isolation.

A tool should not:

- Depend on other tools in the repo unless explicitly stated  
- Require a large runtime environment  
- Bring in heavy frameworks or unnecessary libraries  

A tool should:

- Accept well-defined input  
- Perform a narrow operation  
- Output a clear result that other tools or agents can chain

Think of each tool as a Unix-style utility, just adapted for AI agent workflows.

---

## 2.4. Naming and Folder Structure

- Place your tool in the domain folder that best fits (e.g., `text/`, `search/`, `files/`, `network/`, etc.)  
- If a new domain is needed, keep the name simple and descriptive  
- Filenames should reflect the exact purpose of the tool  
  - Good: `text_cleaner.py`  
  - Good: `fetch_url.go`  
  - Bad: `utility.py` or `misc.go`

---

## 2.5. Determinism and Safety

Based on best practices for agent tool design:

Tools should be deterministic unless the purpose of the tool requires nondeterminism (for example, random generation).

If nondeterminism exists:

- Document it clearly  
- Provide a way to disable or control it when possible

Tools should avoid:

- Implicit side effects  
- External calls that cannot be controlled (cloud APIs, trackers, analytics)  
- Hidden state  

Since this repo is local-first, tools should never rely on online services unless the tool’s entire purpose is to perform a local-safe network request.

---

## 2.6. Cross-Language Flexibility

Tools can be implemented in any programming language.

Your tool is acceptable as long as it:

- Is minimal and modular  
- Runs locally  
- Has no proprietary dependencies  
- Includes clear instructions for running it  

This repository is intentionally polyglot, as long as conventions are respected.

---

# 3. Documentation Requirements

Every tool must include:

- A clear description  
- A short code example or CLI usage example  
- Notes on input/output behavior  
- Setup instructions if necessary  
- Limitations or known edge cases  
- Safety notes (if applicable)

Documentation must appear:

1. In the tool file itself (top-level comment or docstring)  
2. Optionally in a small README within the tool’s folder if the tool is complex  

---

# 4. Testing and Validation

Not every tool needs a full test suite, but tools should at least:

- Contain self-contained logic that can be manually tested  
- Provide a reproducible example  
- Handle invalid or unexpected input gracefully  

If you include tests:

- Use lightweight testing frameworks  
- Avoid heavy dependencies or environment setups  

---

# 5. Licensing

By contributing, you agree that your code will be released under the repository's license.  
Ensure that your contributions are original and do not include proprietary or copyrighted code.

---

# 6. Community Principles

AgentGrimoire is open-source by design and community-first in practice.

We value:

- Transparency  
- Accessibility  
- Simplicity  
- Freedom from vendor lock-in  
- Tooling that empowers developers, not platforms  

Our long-term goal is to support a future open-source ADK-style framework built entirely on community-driven, local-first tools.

Your contributions help shape that foundation.

---

# 7. Additional Reading and External Resources

These documents provide deeper insight into tool design for agent ecosystems:

### Agent Tools and Interoperability  
https://www.kaggle.com/whitepaper-agent-tools-and-interoperability-with-mcp  

Covers tool architecture, interoperability, safety considerations, and agent-tool communication standards.

### Google ADK — Custom Tool Documentation  
https://google.github.io/adk-docs/tools-custom/function-tools/  

Google’s official guidelines for designing function-based tools.  
While focused on their ADK stack, most design advice applies directly to local-first tools as well.

These resources strongly inform the conventions used in AgentGrimoire.

---

Thank you for contributing to AgentGrimoire.

