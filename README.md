# Buzz Autonomous Software & Marketing Factory Agents (Hermes + Hostinger)

> **Platform:** Buzz ([buzz.xyz](https://buzz.xyz) / [github.com/block/buzz](https://github.com/block/buzz))  
> **Agent OS:** Hermes Agent OS running on Hostinger `devserver`  
> **Marketing Foundation:** SMMFactory ([SMMFactory Local Clone](file:///Users/arajiv/SMMFactory))

---

## Architecture Overview

```
                      ┌─────────────────────────────────────────┐
                      │    Buzz Workspace / Nostr Relay         │
                      │  #engineering  •  #marketing-ops  •  DMs│
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
                      └────────┬───────────────────────┬────────┘
                               │                       │
            ┌──────────────────▼─────┐       ┌─────────▼──────────────┐
            │ Software Factory Fleet │       │ Marketing Factory Fleet│
            ├────────────────────────┤       ├────────────────────────┤
            │ • @SystemArchitect     │       │ • @GrowthAnalyst       │
            │ • @FeatureDeveloper    │       │ • @SEOIntelAgent       │
            │ • @QAGatekeeper (P-3)  │       │ • @CreativeCopywriter  │
            │ • @DevOpsRelease       │       │ • @AdDeployer          │
            └────────────────────────┘       └────────────────────────┘
```

---

## Directory Structure

- `agents/`: Declarative `.yaml` manifests defining roles, channel subscriptions, system prompts, and model pins.
- `workflows/`: Declarative `.yaml` execution flows for `buzz-workflow` engine (CI/CD, daily digests, campaign launch gates).
- `hermes_skills/`: Hermes skill packages deployed to `devserver` on Hostinger.
- `config/`: ACP harness and MCP server configurations (`buzz-acp.config.json`, `mcp_servers.json`).

---

## Quick Start & Setup

### 1. Synchronize Hermes Skills to Hostinger `devserver`
Copy the Hermes skills directory to your Hermes environment on `devserver`:

```bash
scp -r hermes_skills/ user@devserver.hostinger:~/.hermes/skills/
```

### 2. Configure Environment Secrets
Ensure the following environment variables are set in your Keychain or `devserver` environment:

- `SEMRUSH_API_KEY` or `SERANKING_API_KEY`: Search intelligence API keys.
- `META_API_KEY`: Meta Marketing API access token.
- `GOOGLE_ADS_KEY`: Google Ads developer token.
- `GCP_SA_KEY`: Path to GCS service account JSON key for media storage (`gs://marketing-studio-assets`).

### 3. Connect Buzz to Relay & Test Channel Interactions

1. Open your Buzz desktop client (`buzz.xyz`).
2. Join `#engineering` or `#marketing-ops`.
3. Test a Software Factory command:
   ```text
   @SystemArchitect Add a health-check endpoint to the server
   ```
4. Test a Marketing Factory command:
   ```text
   @SEOIntelAgent Run SEO scan for campaign ko-lake-easter
   ```

---

## Four-Eyes Quality Gate (P-3 Compliance)

No campaign deployment or software PR merge can occur without passing through `@QAGatekeeper` (pinned to an independent non-Anthropic model such as `qwen-3.7-plus` or local `gemma3:4b`). Production deployments require a human signed Nostr attestation in `#marketing-ops`.
