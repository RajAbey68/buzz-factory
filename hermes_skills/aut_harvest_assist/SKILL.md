---
name: aut-harvest-assist
description: Builds Application Dossiers and 1-click launcher URIs to pre-fill candidate data in local browser sessions.
author: AutHarvest / Hermes
version: 1.0.0
---

# AutHarvest Application Dossier & Browser Assist Skill

This Hermes skill constructs structured Application Dossiers and 1-click browser helper links for human-in-the-loop application filling.

## Application Dossier Structure
```json
{
  "job_id": "<UUID>",
  "company": "Target Company",
  "role": "Senior AI Governance Architect",
  "dossier": {
    "full_name": "Rajiv Abeysinghe",
    "notice_period": "30 days / Immediate",
    "salary_expectation": "£85,000 / £650 per day",
    "work_authorization": "UK Citizen / Full Right to Work",
    "elevator_pitch": "27-year Enterprise & AI Solutions Architect specializing in AI Governance...",
    "cv_path": "/Users/arajiv/AutumnHarvest/outputs/CV_Rajiv_TargetCompany.docx"
  },
  "launcher_uri": "autharvest://apply?job_id=<UUID>&cv_path=..."
}
```

## Execution Flow
1. Assemble applicant answers from `aut_harvest_profile.json`.
2. Generate launcher link.
3. Attach to NIP-44 encrypted Nostr action card.
