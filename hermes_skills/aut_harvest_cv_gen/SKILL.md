---
name: aut-harvest-cv-gen
description: Generates fact-grounded tailored .docx CVs and cover letters from candidate experience in ruvector.db.
author: AutHarvest / Hermes
version: 1.0.0
---

# Fact-Grounded CV & Cover Letter Generation Skill

This Hermes skill generates tailored `.docx` CVs and cover letters customized for shortlisted jobs, strictly grounded against verified career data (`ruvector.db`).

## Commands & Usage

### 1. Generate Tailored CV
```bash
python3 /Users/arajiv/AutumnHarvest/scripts/run_generation.py --job_id <UUID> --output_dir /Users/arajiv/AutumnHarvest/outputs
```

### 2. Fact-Grounding Provenance Audit
Before saving the document, the skill verifies:
- Every job title and employment date exists in `ruvector.db`.
- No metric or achievement percentage is fabricated.
- ATS keywords are matched naturally without keyword-stuffing flags.

## Output Assets
- Tailored CV: `/Users/arajiv/AutumnHarvest/outputs/CV_Rajiv_<Company>_<Date>.docx`
- Cover Letter: `/Users/arajiv/AutumnHarvest/outputs/CL_Rajiv_<Company>_<Date>.docx`
