# Project Rules — Mama Obsidian Vault Sync & Ollama Local Inference

## 1. Mama Obsidian Vault Persistence Rule
All agent factories (**Software Factory**, **SMMFactory**, **AutHarvest**) MUST maintain persistent, bidirectionally readable Markdown sync to the **Mama Obsidian Vault** (`/Users/arajiv/Documents/Obsidian Vault` / `/Users/arajiv/second-brain`).

- **Formatting Requirement:** All agent logs, campaign summaries, job match digests, and architectural decisions MUST be written in strict, clean CommonMark Markdown with YAML frontmatter.
- **Ollama RAG Compatibility:** Markdown structures MUST use standard section headers (`#`, `##`), clean bulleting, and explicit metadata keys so local Ollama instances (`gemma3:4b` / `llama3.3`) can index, search, and perform local RAG reasoning over the vault.
- **Zero Supercession:** Vault sync is a mandatory **Project Constraint** integrated into factory workflows (`workflows/*.yaml`), never a separate or optional manual step.

## 2. LiteLLM Proxy Routing Rule
- If any proxy routing configuration is required for `agy` or LiteLLM endpoints on port 4000, ensure base URL routing uses verified OpenRouter or local Ollama endpoints rather than deprecated/broken provider paths.
