---
name: smmfactory-ad-deployer
description: Drafts Meta Advantage+ and Google Performance Max ad campaigns, submitting campaign summaries for human and P-3 Four-Eyes review before production launch.
author: SMMFactory / Hermes
version: 1.0.0
---

# Meta & Google Ads Campaign Deployer Skill

This Hermes skill configures multi-platform paid media campaign drafts (Meta Advantage+, Google Performance Max, ChatGPT Recommendation Cards) and manages reporting integrations.

## Execution Rules

### 1. Build Draft Campaigns
- Inject `ad_sets.json` (Pomelli visuals) and `ai_analysis.json` copy variants.
- Construct Meta Advantage+ ad set hierarchy (Broad targeting + interest hooks).
- Construct Google Performance Max asset groups for target geo-locations.
- Create tracking Google Sheet using `gws` integration.

### 2. Four-Eyes Gate Verification (P-3 & Human Signoff)
Before turning campaigns to `ACTIVE` status:
- Generate `Campaign_Summary.md` in the campaign folder.
- Execute non-Anthropic review check (e.g. via local `gemma3:4b` or `qwen-3.7-plus`).
- Post summary + staging preview links to Buzz `#marketing-ops` Nostr channel.
- Wait for human owner Nostr attestation before changing status to active.

## Credentials
- `META_API_KEY`: Meta Marketing API Access Token.
- `GOOGLE_ADS_KEY`: Google Ads API Developer Token & Credentials.
- `GCP_SA_KEY`: Google Cloud Service Account for GCS media upload (`gs://marketing-studio-assets`).
