# Baseline vs Memory-v0 Comparison

Source status: local observation

## Inputs

- Eval task path: `experiments/tasks/article_summary_eval_v0.jsonl`
- Baseline trace path: `runs/baseline-v0-eval.jsonl`
- Memory trace path: `runs/memory-v0-eval.jsonl`
- Memory path: `memories/article-summary-reflection-v0.md`

## Average Scores

| Metric | Baseline | Memory-v0 | Delta |
| --- | ---: | ---: | ---: |
| `format_validity` | 1.00 | 1.00 | 0.00 |
| `source_status_grounding` | 1.00 | 1.00 | 0.00 |
| `mechanism_coverage` | 1.00 | 1.00 | 0.00 |
| `engineering_takeaway` | 1.00 | 1.00 | 0.00 |

## Conclusion

Memory-v0 produced no rubric-score improvement; this run does not prove self-improvement.

## Interpretation Guard

- A score tie is not evidence that memory helped.
- This report compares aggregate rubric scores only; manual review is still required.
- The memory file is preservation-oriented because no low-score train failures were observed.
