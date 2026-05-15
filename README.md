# ViNL2Vis Verifier-Guided Repair

This repository contains code and paper-facing evidence tables for verifier-guided repair of decision-aware natural-language-to-visualization (NL2Vis) artifacts.

The release is intentionally code-focused. It does not include manuscript LaTeX, PDFs, submission packages, or author-identifying paper material.

## Contents

- `src/vinl2vis_verifier/`: modular Python package.
- `data/tables/`: released CSV tables used for manuscript-facing results.
- `reports/`: reproducibility and run-summary notes with no manuscript source files.
- `examples/`: example commands for rerunning audits on local benchmark artifacts.
- `scripts/`: thin command-line wrappers.

## What The Code Does

The package supports three reproducibility tasks:

1. Validate internal consistency of released result tables.
2. Generate a compact Markdown summary from the released result tables.
3. Run a strict transformation audit over NL2Vis output JSONL files, checking whether explicit filter, sort, and aggregation commitments appear in the produced Vega-Lite specification.

The strict audit is deterministic. It does not call an LLM or VLM.

## Installation

Use Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e .
```

For development checks:

```bash
python3 -m pip install -r requirements-dev.txt
```

## Quick Validation

From the repository root:

```bash
vinl2vis-verifier validate-tables --tables data/tables
vinl2vis-verifier summarize --tables data/tables --out reports/TABLE_SUMMARY.md
```

Equivalent wrapper:

```bash
PYTHONPATH=src python scripts/validate_release.py validate-tables --tables data/tables
```

Expected validation output:

```text
OK: validated tables in data/tables
```

## Strict Transformation Audit

To audit one generated-output JSONL file:

```bash
vinl2vis-verifier strict-audit \
  --name heldout_4b_stricttransform_v1 \
  --split /path/to/benchmark/faithbench/splits/heldout_860_v1.jsonl \
  --outputs /path/to/benchmark/faithbench/outputs/heldout860_qwen3_4b_stricttransform_v1/qwen3_4b__stricttransform_v1__n860.jsonl \
  --out results/heldout_4b_strict_audit.csv
```

The split file must contain `sample_id` and an `intent` object. The output file must contain matching `sample_id` values and a response object with `vega_lite_spec`, `spec`, or `chart_spec`.

## Released Tables

The repository includes the following CSV tables:

- `main_before_after_results.csv`
- `paired_sample_delta_summary.csv`
- `strict_transform_flags_before_repair.csv`
- `strict_transform_results_after_repair.csv`
- `english_repair_chain_failure_reduction.csv`
- `watchdog_stop_cases.csv`
- `verifier_guided_repair_ledger.csv`

These tables are intended to be small, inspectable evidence artifacts. Full generated model outputs and benchmark data should be distributed separately through the dataset release or supplementary artifact channel.

## Reproducibility Notes

The repository is designed for double-blind review and lightweight verification:

- No manuscript source is included.
- No generated paper PDF is included.
- No private author metadata is required to run the table checks.
- Large model outputs are referenced by path conventions but are not bundled here.

## License

MIT License.
