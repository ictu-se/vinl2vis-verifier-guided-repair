# Controlled Verifier-Loop Run 2026-05-14

This run adds a true verifier-in-the-loop experiment path for Paper 5.

## Implementation

- Runner: `scripts/faithbench_run_verifier_loop.py`
- Smoke output: `benchmark/faithbench/outputs/verifier_loop_20260514_smoke25/`
- Smoke result: `benchmark/faithbench/results/verifier_loop_20260514_smoke25/`
- Full overnight output: `benchmark/faithbench/outputs/verifier_loop_overnight_20260514_173818/`
- Full overnight result: `benchmark/faithbench/results/verifier_loop_overnight_20260514_173818/`
- Full overnight status: `conferences/05_verifier_guided_nl2vis/reports/verifier_loop_overnight_20260514_173818_status.md`
- Overnight launcher for full runs: `scripts/run_verifier_loop_overnight.sh`

The runner implements three controlled variants:

- `vg_select_k`: generate three candidates and select the highest deterministic verifier score.
- `vg_repair_1`: select the best candidate, then run one verifier-feedback repair round.
- `vg_repair_2`: select the best candidate, then run two verifier-feedback repair rounds.

Candidate selection uses the deterministic FaithBench evaluator with rendering enabled.
The selected outputs are ordinary FaithBench JSONL records and can be evaluated by
`scripts/faithbench_evaluate_outputs.py`.

## Smoke 25 Result

Command:

```sh
python3 scripts/faithbench_run_verifier_loop.py \
  --model qwen3:4b \
  --methods vg_select_k vg_repair_1 vg_repair_2 \
  --split benchmark/faithbench/splits/smoke_25.jsonl \
  --out-dir benchmark/faithbench/outputs/verifier_loop_20260514_smoke25 \
  --k 3 \
  --timeout 240 \
  --num-predict 2048 \
  --progress-every 5
```

Evaluation:

```sh
python3 scripts/faithbench_evaluate_outputs.py \
  --outputs benchmark/faithbench/outputs/verifier_loop_20260514_smoke25 \
  --split benchmark/faithbench/splits/smoke_25.jsonl \
  --result-dir benchmark/faithbench/results/verifier_loop_20260514_smoke25 \
  --render
```

| Model | Method | n | Faithfulness | Execution | Grounding | Decision | Render ok | Unsafe plot | Unneeded clarify |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| qwen3:4b | vg_select_k | 25 | 94.433 | 96.000 | 96.533 | 100.000 | 80.0% | 0.0% | 0.0% |
| qwen3:4b | vg_repair_1 | 25 | 94.433 | 96.000 | 96.533 | 100.000 | 80.0% | 0.0% | 0.0% |
| qwen3:4b | vg_repair_2 | 25 | 94.433 | 96.000 | 96.533 | 100.000 | 80.0% | 0.0% | 0.0% |

Failure taxonomy: `{}`.

Smoke baselines already in the repository:

| Model | Method | n | Faithfulness | Execution | Grounding | Decision | Render ok |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| qwen3:4b | verifier_repair | 25 | 87.910 | 70.800 | 96.000 | 100.000 | 68.0% |
| qwen3:4b | qwen_chart_type_strict_repair | 25 | 93.533 | 92.600 | 94.933 | 100.000 | 76.0% |

## Full Overnight Result

The overnight run completed the 250-case pilot, three 1000-case settings, and
the 860-case held-out setting for `vg_select_k`. The smoke split remains the
only split where `vg_repair_1` and `vg_repair_2` were run, because multi-round
repair is substantially more expensive.

| Model | Method | n | Faithfulness | Execution | Grounding | Decision | Render ok | Unsafe plot | Unneeded clarify |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| qwen3:4b | vg_select_k pilot | 250 | 94.396 | 96.000 | 97.200 | 100.000 | 80.0% | 0.0% | 0.0% |
| qwen3:4b | vg_select_k balanced Vietnamese | 1000 | 94.173 | 96.000 | 96.433 | 100.000 | 80.0% | 0.0% | 0.0% |
| qwen3:4b | vg_select_k English explicit | 1000 | 94.028 | 99.375 | 94.290 | 100.000 | 99.0% | 0.0% | 0.0% |
| qwen3:4b | vg_select_k matched bilingual | 1000 | 93.806 | 97.895 | 96.565 | 100.000 | 96.7% | 0.0% | 0.0% |
| qwen3:4b | vg_select_k held-out Vietnamese | 860 | 91.390 | 95.349 | 97.116 | 100.000 | 76.744% | 0.0% | 0.0% |

Failure taxonomy: `{}`.

Pilot baseline already in the repository:

| Model | Method | n | Faithfulness | Execution | Grounding | Decision | Render ok |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| qwen3:4b | verifier_repair | 250 | 87.146 | 69.300 | 96.507 | 99.200 | 67.2% |

## Interpretation

The controlled `vg_select_k` path gives a stronger algorithmic claim than the
previous single-prompt `verifier_repair` run: candidate outputs are generated,
deterministically scored, and selected before final evaluation. On smoke it
also matches the one- and two-round repair variants, which suggests candidate
selection is doing most of the useful work on these cases.

The full-paper claim can now report completed `vg_select_k` controlled-loop
evidence for pilot, balanced Vietnamese, English explicit, matched bilingual,
and held-out Vietnamese splits. It should still avoid claiming that one- or
two-round verifier-feedback repair has been evaluated at full scale, because
those variants were only run on the smoke split.
