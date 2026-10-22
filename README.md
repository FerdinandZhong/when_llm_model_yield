# When Language Models Yield

**Answer Revision Across Science, Commonsense, and Values**

This project studies how language models revise answers after user pushback. It compares bare suggestions, generic justification, and formal wording, each with and without claimed authority. Neutral reconsideration provides an additional condition without a suggested alternative.

The study covers Gemma, Llama, Luna, and Qwen across science, commonsense, and profile-conditioned values. It distinguishes harmful yielding, factual correction, and value redirection. Reviewed correction experiments cover Llama and Luna only.

## Reproduce the principal results

The [standalone reproduction package](reproducibility/README.md) reconstructs **120 main-table rates and 352 paired contrasts**, including their bootstrap confidence intervals. It uses saved, coded outcomes. It does not call model APIs or require the original datasets.

Use Python 3.10 or newer. From the repository root:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r reproducibility/requirements.txt
python reproducibility/reproduce.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. Installing NumPy may require network access; the reproduction calculation runs offline.

The script checks its input checksum and compares computed results against the supplied reference exports. A successful run writes `reproduced_results.csv` and `reproduction_check.json` inside `reproducibility/`. A failed comparison raises an error.

## Repository contents

```text
README.md         Study overview and reproduction instructions
reproducibility/  Standalone analysis, coded inputs, and reference results
.gitignore        Local research data and manuscript exclusions
```

The standalone package is the supported entry point for reproducing the principal numerical results. Historical acquisition code, endpoint configurations, internal documentation, and figure utilities remain outside this initial release pending cleanup.

Both manuscript workspaces are excluded from Git. Local datasets, raw responses, historical campaign outputs, and build files are also excluded.

## Interpretation and coverage

Comparisons concern the implemented wording packages. They do not isolate psychological mechanisms. Value redirection measures adoption of a suggested alternative; it is not automatically an error or harmful behavior.

The package reproduces analysis of the frozen eligible cohorts. It does not independently verify initial-answer eligibility, response parsing, correction adjudication, or upstream survey provenance. It also does not regenerate every sensitivity analysis or manuscript figure.

The coded inputs contain no respondent profiles, original identifiers, question text, or raw model responses. Source identification and redistribution permissions for the original survey materials remain unresolved; those materials are excluded.

## Release status

The main repository is [when_llm_model_yield](https://github.com/FerdinandZhong/when_llm_model_yield). An anonymous reviewer copy is planned separately. No archival identifier has been assigned. This README does not grant redistribution rights for third-party materials.
