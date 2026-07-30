---
name: smmfactory-seo
description: Run SEMrush or SE Ranking competitive SEO & PPC intelligence scans for target domains and campaigns.
author: SMMFactory / Hermes
version: 1.0.0
---

# SEMrush / SE Ranking SEO & PPC Intelligence Skill

This Hermes skill runs search-side competitive intelligence scans for target campaigns using a provider-neutral adapter (`SEMrush` or `SE Ranking`).

## Commands & Usage

### 1. Execute SEO Scan
Run the SEO scanner against a specific campaign slug or domain:

```bash
# Using SEMrush API:
SEMRUSH_API_KEY="$SEMRUSH_API_KEY" node /Users/arajiv/SMMFactory/scripts/seo-scan.mjs --provider semrush --campaign <slug>

# Using SE Ranking API:
SERANKING_API_KEY="$SERANKING_API_KEY" node /Users/arajiv/SMMFactory/scripts/seo-scan.mjs --provider seranking --campaign <slug>
```

### 2. Output Schema (`seo_intel.json`)
The scan outputs a canonical JSON file to `campaigns/<slug>/research/seo_intel.json`:

```json
{
  "provider": "semrush | seranking",
  "domain": "example.com",
  "timestamp": "2026-07-30T16:00:00Z",
  "metrics": {
    "authority_score": 45,
    "organic_traffic": 12500,
    "paid_traffic": 3200,
    "organic_keywords": 890,
    "paid_keywords": 120
  },
  "organic_competitors": [],
  "keyword_gap": [],
  "top_ppc_keywords": []
}
```

## Security & Credentials
- Credentials MUST be passed via environment variables (`SEMRUSH_API_KEY` or `SERANKING_API_KEY`).
- Never log raw API tokens in output logs.
