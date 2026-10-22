# Standalone analysis reproduction

This folder reproduces 120 main-table rates and 352 common-cohort paired contrasts from coded revision outcomes. It includes target-adoption and answer-switching contrasts with 95% bootstrap confidence intervals.

## Run

Use Python 3.10 or newer with NumPy 2.2.6. From this folder:

```sh
python -m pip install -r requirements.txt
python reproduce.py
```

The calculation needs no network access, model API, or files outside this folder. Do not use Python's `-O` option: verification uses assertions.

## Files

| File | Purpose |
| --- | --- |
| `reproduce.py` | Recompute rates, paired contrasts, and intervals; check reference results |
| `requirements.txt` | Pinned NumPy dependency |
| `analysis_inputs.npz` | Coded outcomes and anonymous cluster indices |
| `analysis_inputs.json` | Group definitions, dimensions, and input checksum |
| `standardized_rates.csv` | Reference main-table rates |
| `within_model_contrasts.csv` | Reference paired contrasts |

The script writes `reproduced_results.csv` and `reproduction_check.json`. Both are generated outputs and are ignored by Git. A checksum or numerical mismatch raises an error.

## Calculation

The inputs cover 16 model, task, and setting groups. Outcome codes are −1 for invalid, 0 for retention, 1 for target adoption, and 2 for another revision. The common-valid cohort includes histories with valid responses in every condition of the corresponding group.

The calculation retains assigned clusters, including clusters with no common-valid history. Anonymous cluster indices preserve the original sorted order. Resampling uses 2,000 draws and seed 20260926. Paired comparisons retain the shared history and cluster structure. Estimates and interval bounds must match the reference exports within an absolute tolerance of 1e-8.

```text
Coded outcomes + cluster indices
              |
              v
     Common-valid cohorts
              |
              v
 Rates + paired bootstrap contrasts
              |
              v
 Check against reference CSV files
              |
              v
 Results CSV + verification JSON
```

## Scope and limits

The package reproduces analysis of frozen eligible cohorts. It does not independently authenticate initial eligibility, original parsing, correction adjudication, or upstream survey provenance. It does not reproduce every condition-valid sensitivity, the separate contemporary Qwen analysis, or manuscript figures.

Inputs contain no respondent profiles, original identifiers, question text, raw model responses, credentials, or endpoint URLs. Original survey materials are excluded because their provenance and redistribution permissions remain unresolved.

The six computational files were copied byte-for-byte from the local manuscript supplement. The original records remain unchanged. No archival identifier has been assigned.
