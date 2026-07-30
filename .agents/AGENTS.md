# Project Rules — TDD BMAD & Asimov-AI Governance Framework

## 1. TDD BMAD Methodology (Behavioral Model-Driven Agentic Development)
All agent software development in `buzz-factory` MUST follow strict TDD BMAD principles:
- **Behavioral Modeling (BMAD):** Every feature or agent workflow MUST begin with a formal behavioral specification defining state transitions, schema contracts, and failure boundaries (`@SystemArchitect`).
- **Test-Driven Development (TDD):** `@FeatureDeveloper` MUST write failing automated unit tests *before* writing production implementation code. No feature PR may be submitted without accompanying test suites.
- **Verification Gate:** `@QAGatekeeper` runs tests in an isolated workspace, verifying 100% pass rates and schema compliance before merge approval.

## 2. Asimov-AI Governance Method (Safety, Ethics & Self-Correction)
All 3 agent fleets (**Software**, **Marketing**, **AutHarvest**) operate under the Asimov-AI Method:
- **First Law (System Safety & Non-Harm):** Self-healing watchdogs (`gateway_heartbeat.py`) enforce rate-limited process restarts (max 5/day). PII transport MUST use NIP-17 Gift-Wrap (`kind: 1059`) encryption.
- **Second Law (Human Intent & Ethical Bounds):** Agents stage actions but NEVER auto-submit. Humans retain absolute decision authority via 1-click Nostr action cards (`📌 Pocket` vs `⚡ Launch`). CV generation MUST enforce zero-hallucination provenance against `ruvector.db`.
- **Third Law (Self-Preservation & Auditability):** All agent turns, campaign outputs, and architectural diffs MUST persistently sync to the **Mama Obsidian Vault** (`~/second-brain/inbox/buzz-digest.md`) formatted for local Ollama RAG.

## 3. LiteLLM & Gateway Proxy Rules
- All gateway and model routing configuration MUST use verified OpenRouter or local Ollama endpoints (`gemma3:4b` / `qwen-3.7-plus`), preventing broken provider paths.
