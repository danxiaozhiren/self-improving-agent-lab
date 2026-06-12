# Memory Experiment Design

The first memory experiment should answer a narrow question:

```text
Do reflection notes improve article-summary outputs on held-out tasks?
```

## Scope

Only `article_summary` tasks are included in the first loop. Technical-route analysis is postponed because it needs different metrics and stronger factual checking.

## Dataset Split

Use two task sets:

- `experiments/tasks/article_summary_train_v0.jsonl`: the agent may inspect failed traces and generate memory notes from these tasks.
- `experiments/tasks/article_summary_eval_v0.jsonl`: the agent must not use task-specific answers from these tasks when writing memory.

Memory-enhanced runs are only credible when compared on the same held-out `eval` task set.

The older `experiments/tasks/article_summary_v0.jsonl` file is a smoke set, not the memory-experiment split.

## Memory Rules

Allowed memory content:

- Reusable writing rules.
- Source-status discipline.
- Common failure patterns.
- Rubric-specific improvement hints.
- Workflow or prompt constraints.

Forbidden memory content:

- Final answers for a specific eval task.
- Article-specific facts copied from eval inputs.
- Hard-coded task IDs.
- Any rule that depends on knowing the held-out answer.

## First Memory Artifact

The first generated memory file is:

```text
memories/article-summary-reflection-v0.md
```

Generate it with:

```bash
python3 experiments/generate_reflection_memory.py
```

The script runs baseline only on `experiments/tasks/article_summary_train_v0.jsonl`, stores intermediate train traces under `runs/`, and writes only aggregate scores plus reusable rules into the memory file.

## Memory-Enhanced Comparison

Run the first comparison with:

```bash
python3 experiments/run_memory_enhanced.py
```

The script runs both baseline and `memory-v0` on the held-out eval split, then writes:

```text
reports/baseline-vs-memory-v0.md
```

If the report shows no score delta, treat that as "no demonstrated improvement", even though the pipeline executed successfully. If the report shows a rubric delta, treat it as rubric-level evidence only until a manual semantic review checks whether the changed text is genuinely better.

The first manual semantic review is recorded in:

```text
reports/memory-v0-semantic-review.md
```

Its current outcome is deliberately conservative: memory-v0 now produces a
task-specific mechanism detail that passes the stricter review, but the
improvement is still deterministic and template-driven.

## Comparison Metrics

Compare baseline and memory-enhanced runs with:

- Average rubric score per metric.
- Repeated failure count.
- Source-status violation count.
- Manual review notes for high-scoring but bad outputs.

## Minimum Evidence Bar

A memory experiment is not convincing unless it shows:

1. The exact train/eval task split.
2. The memory notes generated from train traces.
3. Baseline and memory-enhanced traces on the same eval tasks.
4. Metric differences plus at least one manual review note.
