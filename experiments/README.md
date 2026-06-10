# Experiments

This directory stores small, repeatable experiments.

## v0 Experiment: Article Summary Agent With Reflection

Question: does a reflection memory improve repeated article-summary tasks?

Scope guard: this experiment only covers `article_summary`. Technical-route analysis is a later experiment with different metrics.

### Baseline

1. Run a fixed held-out set of article-summary tasks.
2. Save traces as JSONL.
3. Score outputs with a rubric.

Run the current deterministic baseline:

```bash
python3 experiments/run_baseline.py
```

This reads `experiments/tasks/article_summary_eval_v0.jsonl` and writes traces to `runs/baseline-v0-eval.jsonl`.

### Task Split

- `experiments/tasks/article_summary_train_v0.jsonl`: tasks that may be inspected when generating reflection notes or memory rules.
- `experiments/tasks/article_summary_eval_v0.jsonl`: held-out tasks for baseline vs memory-enhanced comparison.
- `experiments/tasks/article_summary_v0.jsonl`: initial smoke set kept for simple runner checks.

The train and eval task IDs and titles should stay disjoint. Memory notes must not copy eval task facts or final answers.

### Reflection Pass

1. Read failed or weak traces.
2. Generate reflection notes.
3. Store notes in a memory file.
4. Re-run the same task set with memory enabled.
5. Compare scores and failure types.

Generate the first train-only reflection memory:

```bash
python3 experiments/generate_reflection_memory.py
```

This reads `experiments/tasks/article_summary_train_v0.jsonl`, writes train traces to `runs/baseline-v0-train.jsonl`, and writes versioned memory notes to `memories/article-summary-reflection-v0.md`.

Run the memory-enhanced eval comparison:

```bash
python3 experiments/run_memory_enhanced.py
```

This writes `runs/memory-v0-eval.jsonl` and `reports/baseline-vs-memory-v0.md`. The report must be read as a comparison result, not as proof of improvement.

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
