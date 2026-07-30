# Implementation Plan — AutHarvest: Human-in-the-Loop Job Hunter & Application Staging in Buzz

> **Target Platform:** Buzz ([buzz.xyz](https://buzz.xyz) / [github.com/block/buzz](https://github.com/block/buzz))  
> **Source Base:** [AutumnHarvest Repository](file:///Users/arajiv/AutumnHarvest) (`ingest_jobs.py`, `job_scorer.py`, `cv_generator.py`, `daily_summary.py`)  
> **Agent OS:** **Hermes Agent OS** running on **`devserver` (Hostinger)**  
> **Architecture Core:** Multi-agent autonomous discovery, fact-grounded CV tailoring, NIP-44 encrypted Nostr channel notifications, and Human-in-the-Loop decision gating ("Pocket" vs "Action/Apply").

---

## 0. Philosophy & Core Architecture: Human-in-the-Loop Assist

**AutHarvest** is **not** an ungated auto-submission bot. It is an **autonomous agent force multiplier** designed to find candidate roles, evaluate match scores against your target criteria, and generate tailored `.docx`/PDF resumes—leaving you in complete control to:
1. **Browse & Filter:** Review matched job opportunities in your `#job-hunter` Buzz channel.
2. **Pocket or Act:** Decide whether to pocket a role for later, dismiss it, or trigger 1-click application staging.
3. **5-Second Assist:** Open your authenticated browser with pre-filled fields and tailored CV attached for instant final review and submission.

```
                      ┌─────────────────────────────────────────┐
                      │    Buzz Workspace / Nostr Relay         │
                      │   #job-hunter  •  #career-ops  •  DMs   │
                      └────────────────────┬────────────────────┘
                                           │ Nostr WebSocket (NIP-44 Encrypted)
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │    Buzz Agent Gateway & `buzz-acp`      │
                      └────────────────────┬────────────────────┘
                                           │ Remote / Local API
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │     HERMES AGENT OS (`devserver`)       │
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

---

## 1. Candidate Target Profile Rules

All incoming job postings are evaluated against your core target profile:
- **Target Roles:** Senior AI Governance, Solutions Architect, Enterprise Architect, Technical Lead.
- **Compensation Threshold:** $\ge £80\text{K}$ Permanent or $\ge £600/\text{day}$ Contract.
- **Geographic Scope:** Remote / UK / EU.
- **Shortlist Bar:** Match score $\ge 4.0 / 5.0$.

---

## 2. Security, Fact-Grounding & Mama Obsidian Rules

1. **Mama Obsidian Vault Persistence (Project Constraint):** All agent factories (**Software Factory**, **SMMFactory**, **AutHarvest**) MUST automatically log structured Markdown summaries to the **Mama Obsidian Vault** (`/Users/arajiv/Documents/Obsidian Vault/Mama_Obsidian/` / `/Users/arajiv/second-brain/`).
2. **Ollama-Obsidian Compatibility:** Markdown documents MUST strictly format headers, YAML frontmatter, and bullet lists for local Ollama (`gemma3:4b` / `llama3.3`) RAG indexing and reasoning.
3. **Fact-Grounded CV Synthesis:** The `@CVTailor` agent uses your verified career history database (`ruvector.db`) as an **immutable ground truth**. It enforces a strict diff/provenance check—preventing fabricated titles, fake metrics, or unverified achievements.
4. **NIP-44 Encrypted Channel Cards:** All job summary cards and CV download links are encrypted using **NIP-44 pairwise encryption** sent directly to your private Nostr pubkey.
5. **LiteLLM Proxy Alignment:** Ensure proxy settings route through verified OpenRouter or local Ollama endpoints rather than deprecated/broken provider paths.

---

## 3. Directory & File Structure in `buzz-factory`

```
buzz-factory/
├── .agents/
│   └── AGENTS.md                   # Mama Obsidian & Ollama project rules
├── .agy/
│   └── instructions.md             # AntiGravity project instructions
├── agents/
│   ├── software_factory/
│   ├── marketing_factory/
│   └── aut_harvest/
│       ├── job_scanner.yaml        # Discovers jobs from PhantomBuster/Gmail/APIs
│       ├── match_scorer.yaml       # AI Scoring against £80K+/£600+day criteria
│       ├── cv_tailor.yaml          # Generates tailored .docx / PDF resumes (Fact-grounded)
│       └── apply_assistant.yaml    # Application dossier & 1-click launcher
├── hermes_skills/
│   ├── aut_harvest_ingest/         # Ingestion skill wrapping AutumnHarvest scripts
│   ├── aut_harvest_cv_gen/         # Tailored CV generator skill (python-docx + diff check)
│   ├── aut_harvest_assist/         # Application dossier & browser pre-fill assistant
│   └── aut_harvest_nip44/          # Encrypted Nostr event notification skill
├── workflows/
│   ├── aut_harvest_morning_routine.yaml # Daily Cron (07:00 UTC): Scan -> Score -> Digest -> Obsidian Sync
│   └── aut_harvest_stage_application.yaml # Reactive: Score >= 4.0 -> Tailor CV -> Stage Card
├── config/
│   └── aut_harvest_profile.json    # Target profile rules, skills matrix, resume paths
└── README.md
```

---

## 4. Verification & Testing Plan

### Automated Tests
1. **Mama Obsidian Vault Sync Test:** Verify job digests, software release notes, and marketing reports write cleanly to `/Users/arajiv/Documents/Obsidian Vault/Mama_Obsidian/`.
2. **Fact-Grounding Audit:** Run `aut_harvest_cv_gen` and verify zero hallucinations against `ruvector.db`.
3. **NIP-44 Crypto Test:** Verify Nostr event payload encrypts and decrypts cleanly using candidate pubkey.

### Manual Verification
1. **Obsidian Vault Inspection:** Open Obsidian and confirm `Mama_Obsidian/` receives structured Markdown notes parseable by local Ollama.
2. **Buzz Channel Interaction:** Issue `@JobScanner run scan` in `#job-hunter` inside Buzz client (`buzz.xyz`).
