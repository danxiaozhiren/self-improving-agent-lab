# Experiments

This directory stores small, repeatable experiments.

## v0 Experiment: Article Summary Agent With Reflection

Question: does a reflection memory improve repeated article-summary tasks?

Scope guard: this experiment only covers `article_summary`. Technical-route analysis is a later experiment with different metrics.

### Baseline

1. Run a fixed set of article-summary tasks.
2. Save traces as JSONL.
3. Score outputs with a rubric.

Run the current deterministic baseline:

```bash
python3 experiments/run_baseline.py
```

This reads `experiments/tasks/article_summary_v0.jsonl` and writes traces to `runs/baseline-v0.jsonl`.

### Reflection Pass

1. Read failed or weak traces.
2. Generate reflection notes.
3. Store notes in a memory file.
4. Re-run the same task set with memory enabled.
5. Compare scores and failure types.

### Metrics

- Format validity.
- Source-status grounding.
- Mechanism coverage.
- Engineering takeaway.
- Repeated failure count.
- Manual review notes for high-scoring but bad outputs.

See `docs/rubric-article-summary.md` for the concrete first-pass rubric and `docs/memory-experiment-design.md` for the baseline vs memory-enhanced comparison rules.

### Trace Shape

```json
{
  "task_id": "summary-001",
  "workflow_version": "baseline-v0",
  "started_at": "2026-06-02T00:00:00+00:00",
  "input": {},
  "steps": [],
  "output": "",
  "scores": {},
  "reflection": ""
}
```
