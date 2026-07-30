# Buzz Autonomous Agent Factory (`buzz-factory`)

> **Platform:** Buzz ([buzz.xyz](https://buzz.xyz) / [github.com/block/buzz](https://github.com/block/buzz))  
> **Agent OS:** Hermes Agent OS running on Hostinger `devserver`  
> **Repository:** [github.com/RajAbey68/buzz-factory](https://github.com/RajAbey68/buzz-factory)

---

## Workspace Architecture

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
        └───────────────────────┘   └─────────────────────┘   └──────────────────────┘
```

---

## Agent Fleets

### 1. 💻 Software Factory (`agents/software_factory/`)
- `@SystemArchitect`: Task decomposition and CAO routing.
- `@FeatureDeveloper`: Git feature branch & TDD code builder (`buzz-dev-mcp`).
- `@QAGatekeeper`: P-3 Four-Eyes non-Anthropic review gatekeeper (`qwen-3.7-plus` / `gemma3:4b`).
- `@DevOpsReleaseManager`: Staging build deployments and screenshot previews.

### 2. 📈 Marketing Factory (`agents/marketing_factory/`)
- `@GrowthAnalyst`: Daily growth metrics & performance digests.
- `@SEOIntelAgent`: SEMrush / SE Ranking competitive search intelligence.
- `@CreativeCopywriter`: Notion-Warm brand copy & Stitch React landing pages.
- `@AdDeployer`: Meta Advantage+ & Google Performance Max campaign builder.

### 3. 🍂 AutHarvest Job Hunter (`agents/aut_harvest/`)
- `@JobScanner`: Automated discovery (LinkedIn PhantomBuster, Indeed Gmail alerts, RSS).
- `@MatchScorer`: AI match scoring against target persona (Senior AI Governance / Solutions Architect / £80K+ or £600+/day).
- `@CVTailor`: Fact-grounded `.docx` CV & Cover Letter synthesis (zero hallucination against `ruvector.db`).
- `@ApplyAssistant`: Application Dossiers, NIP-44 encrypted Nostr action cards, and 1-click browser helper links.

---

## Synchronizing Skills to Hostinger `devserver`

```bash
scp -r hermes_skills/ user@devserver.hostinger:~/.hermes/skills/
```

---

## Operating Instructions & Verification

1. **Software Task:** `@SystemArchitect create a new API endpoint` in `#engineering`.
2. **Marketing Task:** `@SEOIntelAgent run scan for ko-lake-easter` in `#marketing-ops`.
3. **Job Search Task:** `@JobScanner run scan` in `#job-hunter`.
