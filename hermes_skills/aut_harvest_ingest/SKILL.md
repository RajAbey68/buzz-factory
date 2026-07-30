---
name: aut-harvest-ingest
description: Ingestion skill for AutHarvest. Runs PhantomBuster CSV imports, Gmail Indeed alert reader, and RSS discovery scripts.
author: AutHarvest / Hermes
version: 1.0.0
---

# AutHarvest Job Ingestion Skill

This Hermes skill runs job discovery and ingestion pipelines, wrapping the core parsers from `AutumnHarvest`.

## Commands & Usage

### 1. Ingest LinkedIn Jobs (PhantomBuster CSV)
```bash
python3 /Users/arajiv/AutumnHarvest/scripts/ingest_jobs.py --source phantombuster --input /path/to/linkedin_export.csv
```

### 2. Ingest Indeed Email Alerts (Gmail OAuth Reader)
```bash
python3 /Users/arajiv/AutumnHarvest/scripts/ingest_jobs.py --source gmail
```

### 3. Run Batch Ingestion Suite
```bash
python3 /Users/arajiv/AutumnHarvest/scripts/ingest_all.py
```

## Schema Integration
Parsed jobs are validated against `src/models.py` (Pydantic models) and stored in Supabase with initial status `New`.
