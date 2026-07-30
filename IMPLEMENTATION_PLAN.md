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
                      └───────┬─────────────────────────┬───────┘
                              │                         │
            ┌─────────────────▼──────┐       ┌──────────▼──────────────┐
            │ AutHarvest Agent Fleet │       │ AutHarvest Hermes Skills│
            ├────────────────────────┤       ├─────────────────────────┤
            │ • @JobScanner          │       │ • `aut-harvest-ingest`  │
            │ • @MatchScorer         │       │ • `aut-harvest-cv-gen`  │
            │ • @CVTailor            │       │ • `aut-harvest-assist`  │
            │ • @ApplyAssistant      │       │ • `aut-harvest-nip44`   │
            └───────────┬────────────┘       └──────────┬──────────────┘
                        │                               │
                        ▼                               ▼
            ┌────────────────────────┐       ┌─────────────────────────┐
            │ Local Browser Assist   │       │ Supabase Job DB & GCS   │
            │ (autharvest:// launcher│       │ (`ruvector.db`, `.docx`)│
            └────────────────────────┘       └─────────────────────────┘
```

---

## 1. Candidate Target Profile Rules

All incoming job postings are evaluated against your core target profile:
- **Target Roles:** Senior AI Governance, Solutions Architect, Enterprise Architect, Technical Lead.
- **Compensation Threshold:** $\ge £80\text{K}$ Permanent or $\ge £600/\text{day}$ Contract.
- **Geographic Scope:** Remote / UK / EU.
- **Shortlist Bar:** Match score $\ge 4.0 / 5.0$.

---

## 2. Security & Fact-Grounding Safeguards

1. **Fact-Grounded CV Synthesis (Zero Hallucination):** The `@CVTailor` agent uses your verified career history database (`ruvector.db`) as an **immutable ground truth**. It enforces a strict diff/provenance check—preventing fabricated titles, fake metrics, or unverified achievements.
2. **NIP-44 Encrypted Channel Cards:** All job summary cards and CV download links are encrypted using **NIP-44 pairwise encryption** sent directly to your private Nostr pubkey. No PII or job search activity is exposed on public relays.
3. **No Unsafe Auto-Submissions:** Applications are staged into pre-filled form dossiers. Submission requires your explicit click in your authenticated local browser—completely avoiding anti-bot blocks, Cloudflare CAPTCHAs, or ToS violations.

---

## 3. Directory & File Structure in `buzz-factory`

```
buzz-factory/
├── agents/
│   └── aut_harvest/
│       ├── job_scanner.yaml        # Discovers jobs from PhantomBuster/Gmail/APIs
│       ├── match_scorer.yaml       # AI Scoring against £80K+/£600+day criteria
│       ├── cv_tailor.yaml          # Generates tailored .docx / PDF resumes (Fact-grounded)
│       └── apply_assistant.yaml    # Application dossier & 1-click launcher
├── hermes_skills/
│   ├── aut_harvest_ingest/         # Ingestion skill wrapping AutumnHarvest scripts
│   │   └── SKILL.md
│   ├── aut_harvest_cv_gen/         # Tailored CV generator skill (python-docx + diff check)
│   │   └── SKILL.md
│   ├── aut_harvest_assist/         # Application dossier & browser pre-fill assistant
│   │   └── SKILL.md
│   └── aut_harvest_nip44/          # Encrypted Nostr event notification skill
│       └── SKILL.md
├── workflows/
│   ├── aut_harvest_morning_routine.yaml # Daily Cron (07:00 UTC): Scan -> Score -> Digest
│   └── aut_harvest_stage_application.yaml # Reactive: Score >= 4.0 -> Tailor CV -> Stage Card
├── config/
│   └── aut_harvest_profile.json    # Target profile rules, skills matrix, resume paths
└── README.md
```

---

## 4. Agent & Workflow Component Specifications

### [Component 1] AutHarvest Agent Fleet (`agents/aut_harvest/`)

#### [NEW] [job_scanner.yaml](file:///Users/arajiv/buzz-implementation-plan/agents/aut_harvest/job_scanner.yaml)
- **Role:** Autonomous Job Discovery Agent (`@JobScanner`).
- **Function:** Ingests jobs from LinkedIn PhantomBuster CSVs, Gmail Indeed alerts, and RSS feeds into Supabase.

#### [NEW] [match_scorer.yaml](file:///Users/arajiv/buzz-implementation-plan/agents/aut_harvest/match_scorer.yaml)
- **Role:** AI Job Scorer & Filter Agent (`@MatchScorer`).
- **Function:** Evaluates job descriptions against 27-year career experience matrix, calculates match score (0–5.0), and shortlists roles scoring $\ge 4.0$.

#### [NEW] [cv_tailor.yaml](file:///Users/arajiv/buzz-implementation-plan/agents/aut_harvest/cv_tailor.yaml)
- **Role:** Fact-Grounded CV & Cover Letter Synthesis Agent (`@CVTailor`).
- **Function:** Generates tailored `.docx` and `.pdf` resumes highlighting matching experience, key achievements, and keywords for shortlisted jobs—verifying all claims against `ruvector.db`.

#### [NEW] [apply_assistant.yaml](file:///Users/arajiv/buzz-implementation-plan/agents/aut_harvest/apply_assistant.yaml)
- **Role:** Staging & Application Assistant (`@ApplyAssistant`).
- **Function:** Assembles application dossiers (salary expectation, notice period, pitch text) and formats NIP-44 encrypted Nostr action cards with "Pocket" and "Launch Application" options.

---

### [Component 2] Hermes Skills (`hermes_skills/`)

#### [NEW] [SKILL.md (aut_harvest_ingest)](file:///Users/arajiv/buzz-implementation-plan/hermes_skills/aut_harvest_ingest/SKILL.md)
- Ingests raw job alerts from PhantomBuster LinkedIn CSVs and Indeed email digests.

#### [NEW] [SKILL.md (aut_harvest_cv_gen)](file:///Users/arajiv/buzz-implementation-plan/hermes_skills/aut_harvest_cv_gen/SKILL.md)
- Generates tailored `.docx` files using `python-docx`, verifying zero hallucinated metrics or fabricated job titles.

#### [NEW] [SKILL.md (aut_harvest_assist)](file:///Users/arajiv/buzz-implementation-plan/hermes_skills/aut_harvest_assist/SKILL.md)
- Builds 1-click launcher links (`autharvest://apply?...`) for pre-filling local browser form fields.

#### [NEW] [SKILL.md (aut_harvest_nip44)](file:///Users/arajiv/buzz-implementation-plan/hermes_skills/aut_harvest_nip44/SKILL.md)
- Encrypts job summary cards using NIP-44 pairwise crypto before sending to Nostr relays.

---

## 5. Verification & Testing Plan

### Automated Tests
1. **Ingestion & Scoring Test:** Run `aut_harvest_ingest` against test job payload; verify jobs score cleanly.
2. **Fact-Grounding Audit:** Run `aut_harvest_cv_gen` and verify zero hallucinations against `ruvector.db`.
3. **NIP-44 Crypto Test:** Verify Nostr event payload encrypts and decrypts cleanly using candidate pubkey.

### Manual Verification
1. **Buzz Channel Interaction:** Issue `@JobScanner run scan` in `#job-hunter` inside Buzz client (`buzz.xyz`).
2. **Pocket / Action Verification:** Click "Pocket" or "Launch Application" in Buzz and verify tailored CV and pre-filled application dossier open smoothly.
