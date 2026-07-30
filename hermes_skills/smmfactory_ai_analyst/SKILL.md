---
name: smmfactory-ai-analyst
description: Ingest market DNA and competitive ad scans to perform SWOT analysis, Hormozi Value Equation scoring, and proof-based ad copy validation.
author: SMMFactory / Hermes
version: 1.0.0
---

# AI Intelligence Analyst Skill (Hormozi Scoring & Copy Validation)

This Hermes skill synthesizes raw competitor intelligence (`competitor_intel.json`) and brand positioning (`market_dna.json`) to create actionable strategy and validated ad copy variants.

## Execution Rules

### 1. Ingest Data & Run Analysis
```bash
node /Users/arajiv/SMMFactory/scripts/ai-intelligence-analyst.mjs --campaign <slug>
```

### 2. Strategic Transformations
- **SWOT Matrix:** Generates Strengths, Weaknesses, Opportunities, and Threats for top 3 competitors.
- **Hormozi Value Equation Scoring:** Scores ad hooks on a scale of 1-10:
  $$\text{Value} = \frac{\text{Dream Outcome} \times \text{Perceived Likelihood of Achievement}}{\text{Time Delay} \times \text{Effort \& Sacrifice}}$$
- **Proof-Based Ad Copy Validation (Strict Gates):**
  - Requires **$\ge 2$ verifiable proof points** per copy variant.
  - Enforces **0 superlatives** (strictly required for ad network compliance).
- **ChatGPT Recommendation Cards:** Drafts placement cards targeted for high-intent conversational placements ($60 CPM target).

## Output File
Generates `campaigns/<slug>/research/ai_analysis.json`.
