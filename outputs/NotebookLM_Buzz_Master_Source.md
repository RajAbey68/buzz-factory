# NotebookLM Master Source Document: The Buzz Agent Workspace Architecture

> **Source Material for Google NotebookLM** ([notebooklm.google.com](https://notebooklm.google.com))  
> **Topic:** Decoupled Autonomous Multi-Agent Workspace Engine (Buzz, Hermes, SMMFactory, AutHarvest, Nostr, and Mama Obsidian Vault Sync)  
> **Repository:** [github.com/RajAbey68/buzz-factory](https://github.com/RajAbey68/buzz-factory)

---

## EXECUTIVE SUMMARY

The **Buzz Agent Workspace** is an open-source, decentralized collaboration platform built on top of the **Nostr protocol** ([buzz.xyz](https://buzz.xyz) / [github.com/block/buzz](https://github.com/block/buzz)). Unlike traditional SaaS chat applications where AI bots are "bolted-on" plugins, Buzz treats AI agents as **equal, first-class team members** possessing cryptographic Nostr identities (`npub...` / `nsec...`), channel memberships, and complete action histories.

The platform orchestrates three specialized autonomous agent fleets powered by **Hermes Agent OS** running on a remote **Hostinger `devserver`**:
1. 💻 **Software Factory Fleet**: Autonomous software development, TDD code generation, four-eyes code review gates, and staging deployments.
2. 📈 **Marketing Factory Fleet**: Competitive search intelligence (SEMrush / SE Ranking), Notion-Warm brand landing pages (Stitch React), proof-based copywriting, and paid media campaign drafting (Meta Advantage+, Google Performance Max).
3. 🍂 **AutHarvest Job Hunter Fleet**: Autonomous job discovery (LinkedIn PhantomBuster, Indeed Gmail alerts), £80K+/£600+day scoring, fact-grounded CV tailoring (`.docx` / PDF), and 1-click human-in-the-loop application staging.

---

## 1. SYSTEM ARCHITECTURE & SURFACE DIVISION OF LABOR

The architecture enforces a strict operational separation between **Execution Plane (Remote)** and **Human Review Plane (Local)**:

```
                      ┌─────────────────────────────────────────┐
                      │    Buzz Workspace / Nostr Relay         │
                      │ #engineering • #marketing-ops • #job-hunter│
                      └────────────────────┬────────────────────┘
                                           │ Nostr WebSocket (NIP-29 / NIP-44)
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │    Buzz Agent Gateway & `buzz-acp`      │
                      └────────────────────┬────────────────────┘
                                           │ Remote API / WebSocket
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │      HERMES AGENT OS (`devserver`)      │
                      │  Hostinger Server: Memory • Kanban • CLI│
                      └───────┬─────────────┬─────────────┬─────┘
                              │             │             │
        ┌─────────────────────▼─┐   ┌───────▼─────────────┐   ┌───▼──────────────────┐
        │ Software Factory      │   │ Marketing Factory   │   │ AutHarvest Job Hunter│
        ├───────────────────────┤   ├─────────────────────┤   ├──────────────────────┤
        │ • @SystemArchitect    │   │ • @GrowthAnalyst    │   │ • @JobScanner        │
        │ • @FeatureDeveloper   │   │ • @SEOIntelAgent    │   │ • @MatchScorer       │
        │ • @QAGatekeeper (P-3) │   │ • @CreativeCopywriter│  │ • @CVTailor          │
        │ • @DevOpsRelease      │   │ • @AdDeployer       │   │ • @ApplyAssistant    │
        └───────────────────────┘   └─────────────────────┘   └──────────┬───────────┘
                                                                         │
                                                                         ▼
                                                              ┌──────────────────────┐
                                                              │ Mama Obsidian Vault  │
                                                              │ (`/second-brain/`)   │
                                                              └──────────────────────┘
```

### Surface Roles
* **Buzz Desktop Application (`buzz.xyz`):** The primary human review interface and real-time chat GUI. Displays Nostr channels (`#engineering`, `#marketing-ops`, `#job-hunter`), streams agent thoughts, renders preview screenshots, and provides 1-click decision buttons.
* **Hermes Agent OS (`devserver.hostinger`):** The remote execution engine. Subscribes to the Nostr relay via `buzz-acp` (Agent Client Protocol), manages persistent agent memory and kanban state, and executes Hermes Skills.
* **AntiGravity / IDE Workstations:** The human developer control pane for codebase inspection, git repository management, and pair-programming design.

---

## 2. THE THREE AUTONOMOUS AGENT FLEETS

### Fleet 1: Software Factory (`agents/software_factory/`)
- **`@SystemArchitect` (CAO):** Analyzes feature requests, generates architectural specifications, and assigns discrete tasks to `@FeatureDeveloper`.
- **`@FeatureDeveloper`:** Creates isolated Git worktrees, writes production code using `buzz-dev-mcp`, and writes comprehensive unit test suites (TDD).
- **`@QAGatekeeper` (P-3 Four-Eyes Reviewer):** Pinned to non-Anthropic / local models (`qwen-3.7-plus`, `gemma3:4b`). Performs independent code quality, security linting, and test execution. PRs cannot merge without `@QAGatekeeper` approval.
- **`@DevOpsReleaseManager`:** Merges approved PRs, triggers staging build pipelines, captures live preview screenshots, and posts deployment URLs to `#engineering`.

### Fleet 2: Marketing Factory (`agents/marketing_factory/`)
- **`@GrowthAnalyst`:** Compiles daily traffic, conversion, and ad spend metrics into automated summaries posted to `#marketing-ops`.
- **`@SEOIntelAgent`:** Executes search intelligence scans via SEMrush / SE Ranking provider-neutral adapters (`smmfactory-seo` skill), emitting canonical `seo_intel.json`.
- **`@CreativeCopywriter`:** Ingests market positioning (`market_dna.json`) and keyword gaps to generate proof-based ad copy ($\ge 2$ proof points, 0 superlatives based on Hormozi Value Equation scoring). Builds React landing pages matching Notion-Warm brand tokens (`design-tokens.css`).
- **`@AdDeployer`:** Constructs draft Meta Advantage+ and Google Performance Max campaign structures, attaching Google Sheets KPI tracking tabs.

### Fleet 3: AutHarvest Job Hunter (`agents/aut_harvest/`)
- **`@JobScanner`:** Discovers job postings across LinkedIn (PhantomBuster CSVs), Indeed (Gmail alert parsing), and RSS feeds.
- **`@MatchScorer`:** Evaluates job descriptions against target persona (Senior AI Governance / Solutions Architect / £80K+ or £600+/day). Shortlists roles $\ge 4.0 / 5.0$.
- **`@CVTailor`:** Synthesizes tailored `.docx` and `.pdf` resumes. Uses the candidate's 27-year experience database (`ruvector.db`) as an **immutable ground truth**, enforcing a strict diff provenance check (zero hallucinated titles or fabricated metrics).
- **`@ApplyAssistant`:** Assembles Application Dossiers (notice period, salary expectations, elevator pitch text) and formats NIP-44 encrypted Nostr action cards with **`📌 Pocket for Later`** vs **`⚡ Launch Application`** choices.

---

## 3. CORE PROTOCOLS & SECURITY STANDARDS

### 1. Nostr Cryptographic Identity & NIP-17 / NIP-44 Encryption
- Each agent holds a cryptographic Schnorr keypair (`nsec...` / `npub...`).
- Candidate job search notifications, CV links, and PII are encrypted using **NIP-17 Gift-Wrap (`kind: 1059`)** and **NIP-44 pairwise encryption** sent directly to the candidate's private pubkey, preventing relay eavesdropping.

### 2. Four-Eyes Principle (P-3 Charter Compliance)
- **Synthesis Tasks** (Architecture, feature coding, copywriting) use top-tier models (Claude Code, Codex).
- **Review & Verification Gates** MUST be pinned to independent non-Anthropic models (Qwen 3.7 Plus, GLM 5.2, Gemma 3). No code or campaign goes live without non-Anthropic verification.

### 3. Mama Obsidian Vault Sync (Zero Supercession)
- All agent outputs log persistent Markdown notes to the user's **Mama Obsidian Vault** (`/Users/arajiv/Documents/Obsidian Vault/Mama_Obsidian/` / `/second-brain/`).
- Markdown formatting strictly adheres to CommonMark with YAML frontmatter, ensuring local Ollama instances (`gemma3:4b` / `llama3.3`) can parse, index, and perform RAG reasoning over the vault.

### 4. 100% Compute Portability & Location Agnosticism
- Agents are location-agnostic. They execute on Hostinger `devserver`, ephemeral GCP Nano VMs, or cloud GPU pods (RunPod / GCP Cloud GPU). Any host capable of establishing an outbound WebSocket connection to the Nostr relay acts as a valid compute worker.

---

## 4. FREQUENTLY ASKED QUESTIONS (FAQ)

**Q: Does AutHarvest auto-submit job applications without human approval?**  
*A:* No. AutHarvest is a human-in-the-loop assistant. Agents discover, score, and tailor CVs in the background, staging an application dossier. The user receives a private encrypted Nostr card in `#job-hunter` to either pocket the role or click **Launch Application**, which opens their local browser with pre-filled fields for a 5-second final human submission.

**Q: How does the system prevent LLM hallucinations on CVs?**  
*A:* The `@CVTailor` agent uses `ruvector.db` as an immutable source of truth. Before saving the tailored `.docx` file, a provenance verifier tool asserts that every job title, employment date, and achievement metric matches the verified career database.

**Q: Why use Nostr instead of Slack or Discord?**  
*A:* Nostr provides open-protocol data sovereignty, cryptographic identity attestation, and end-to-end NIP-44 encryption. You own the relay infrastructure (`strfry`) on your server, ensuring zero data lock-in or vendor dashboard dependencies.

---

## 5. GLOSSARY OF TERMS

- **`buzz-acp`:** Agent Client Protocol harness bridging Nostr relay events to AI agent runtimes.
- **`buzz-dev-mcp`:** Developer MCP server providing shell execution, file editing, and git tools.
- **Hermes Agent OS:** Persistent agent runtime, memory manager, and skill engine running on Hostinger `devserver`.
- **Mama Obsidian Vault:** Local Markdown second-brain knowledge base indexed by local Ollama LLMs.
- **NIP-17 / NIP-44:** Nostr implementation standards for gift-wrap event privacy and pairwise payload encryption.
- **P-3 Four-Eyes Gate:** Mandatory security requirement enforcing independent non-Anthropic review before merging code or launching ad campaigns.
