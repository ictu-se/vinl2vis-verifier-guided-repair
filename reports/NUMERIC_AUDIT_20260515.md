# Numeric Audit 2026-05-15

This report records consistency checks over the released verifier-guided repair evidence tables and controlled-loop summaries.

## Checked Sources

- `data/tables/main_before_after_results.csv`
- `data/tables/paired_sample_delta_summary.csv`
- `data/tables/english_repair_chain_failure_reduction.csv`
- `data/tables/strict_transform_flags_before_repair.csv`
- `data/tables/strict_transform_results_after_repair.csv`
- `data/tables/watchdog_stop_cases.csv`
- `data/tables/verifier_guided_repair_ledger.csv`
- Controlled verifier-loop summaries from the corresponding full-run artifacts.

## Findings

- Released CSV tables pass internal arithmetic checks.
- Before/after faithfulness deltas match final-minus-baseline values.
- Paired outcome counts sum to the paired sample size in every setting.
- Strict-transform before-repair flag totals match the sum of missing filter, sort, and aggregation flags.
- Controlled verifier-loop rows match the full-run summaries:
  - smoke 25 `vg_select_k`, `vg_repair_1`, and `vg_repair_2`: 94.433 faithfulness, 96.000 execution, 96.533 grounding, 100.000 decision, 80.0 render success.
  - pilot 250 `vg_select_k`: 94.396 faithfulness, 96.000 execution, 97.200 grounding, 100.000 decision, 80.0 render success.
  - balanced 1000 `vg_select_k`: 94.173 faithfulness, 96.000 execution, 96.433 grounding, 100.000 decision, 80.0 render success.
  - English 1000 `vg_select_k`: 94.028 faithfulness, 99.375 execution, 94.290 grounding, 100.000 decision, 99.0 render success.
  - matched 1000 `vg_select_k`: 93.806 faithfulness, 97.895 execution, 96.565 grounding, 100.000 decision, 96.7 render success.
  - held-out 860 `vg_select_k`: 91.390 faithfulness, 95.349 execution, 97.116 grounding, 100.000 decision, 76.7 render success.

## Validation Command

```bash
PYTHONPATH=src python3 -m vinl2vis_verifier.cli validate-tables --tables data/tables
```

Expected output:

```text
OK: validated tables in data/tables
```

## Conclusion

The released numeric tables are internally consistent with the available verifier-guided repair evidence package.
