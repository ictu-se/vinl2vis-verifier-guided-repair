# Verifier-Guided Repair Table Summary

## Main Before/After

| Setting | n | Base faith. | Final faith. | Delta | Base render | Final render |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| VI balanced | 1000 | 90.225 | 94.210 | 3.985 | 80.0 | 79.6 |
| EN explicit | 1000 | 83.630 | 93.870 | 10.240 | 74.5 | 97.8 |
| Matched EN/VI | 1000 | 91.587 | 94.650 | 3.063 | 90.9 | 97.4 |
| Held-out VI 4B | 860 | 90.226 | 94.880 | 4.654 | 75.116 | 76.279 |
| Held-out VI 8B | 860 | 91.562 | 95.260 | 3.698 | 74.767 | 76.279 |

## Paired Outcomes

| Setting | Improved | Unchanged | Degraded | Mean delta | Median delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| VI balanced | 642 | 310 | 48 | 3.985 | 2.900 |
| EN explicit | 714 | 211 | 75 | 10.240 | 8.700 |
| Matched EN/VI | 392 | 545 | 63 | 3.063 | 0.000 |
| Held-out VI 4B | 421 | 385 | 54 | 4.654 | 3.700 |
| Held-out VI 8B | 390 | 420 | 50 | 3.698 | 0.700 |

## Final Strict-Transform Audit

| Setting | Faithfulness | Failure taxonomy |
| --- | ---: | --- |
| balanced 1000 stricttransform v1 | 94.210 | filter 6; sort 3 |
| English 1000 stricttransform v2 | 93.870 | filter 4; sort 1 |
| matched bilingual 1000 stricttransform v1 | 94.650 | filter 5; aggregation 2 |
| held-out 4B stricttransform v1 | 94.880 | filter 8; sort 6 |
| held-out 8B stricttransform v1 | 95.260 | filter 7; sort 2 |
