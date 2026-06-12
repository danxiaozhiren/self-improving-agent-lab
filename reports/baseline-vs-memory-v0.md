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
| `input_specificity` | 0.00 | 1.00 | 1.00 |

## Conclusion

Memory-v0 produced a rubric-level improvement on at least one metric without a score regression.

## Manual Review

- Review path: `reports/memory-v0-semantic-review.md`
- Current review status: task-specific mechanism improvement passes the stricter review, with residual risk from deterministic template reuse.

## Interpretation Guard

- A score tie is not evidence that memory helped.
- Manual review is required for any claimed semantic improvement.
- A rubric-score improvement is only meaningful when the changed metric reflects a real quality gap.
