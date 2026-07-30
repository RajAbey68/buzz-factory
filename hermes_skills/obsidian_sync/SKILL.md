---
name: obsidian-sync-skill
description: Pulls daily activity logs, agent turn history, and fleet digests from the buzz-acp gateway and appends them to Mama Obsidian Vault (second-brain/inbox/buzz-digest.md).
author: AutHarvest / Hermes / AntiGravity
version: 1.0.0
---

# Mama Obsidian Vault Sync Skill (`obsidian-sync-skill`)

This Hermes skill synchronizes activity logs, agent execution traces, and campaign/job digests from the `buzz-acp` gateway directly into the **Mama Obsidian Vault** (`~/second-brain/inbox/buzz-digest.md` and `/Users/arajiv/Documents/Obsidian Vault/Mama_Obsidian/buzz-digest.md`).

## Synchronization Architecture

```
┌─────────────────────────┐          ┌─────────────────────────┐          ┌─────────────────────────┐
│ `buzz-acp` Event Gateway│          │ Hermes Sync Script      │          │ Mama Obsidian Vault     │
│ (`devserver` Hostinger) │ ────────►│ (`scripts/obsidian_sync`) ───────►│ `~/second-brain/inbox/` │
│ Event & Activity Logs   │          │ CommonMark + YAML Front │          │ `buzz-digest.md`        │
└─────────────────────────┘          └─────────────────────────┘          └─────────────────────────┘
```

## Commands & Usage

### 1. Execute Digest Sync (Local or Remote SSH)
```bash
# Direct local/devserver execution:
python3 /Users/arajiv/buzz-implementation-plan/scripts/obsidian_sync.py

# Remote Cron Execution from devserver:
ssh devserver.hostinger "python3 ~/.hermes/skills/obsidian_sync/obsidian_sync.py"
```

### 2. Formatting & Ollama RAG Requirements
- **Standard Header Structure:** All appended entries use CommonMark headers (`## YYYY-MM-DD Digest`).
- **YAML Frontmatter:** Entries include metadata tags (`fleet`, `agent`, `status`, `timestamp`).
- **Ollama Indexing Ready:** Formatted for instant RAG indexing by local Ollama (`gemma3:4b` / `llama3.3`).

## Output Target Files
- Primary Vault: `/Users/arajiv/Documents/Obsidian Vault/Mama_Obsidian/buzz-digest.md`
- Inbox Sync: `/Users/arajiv/second-brain/inbox/buzz-digest.md`
