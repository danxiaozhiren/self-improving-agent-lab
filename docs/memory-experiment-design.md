# Memory Experiment Design

The first memory experiment should answer a narrow question:

```text
Do reflection notes improve article-summary outputs on held-out tasks?
```

## Scope

Only `article_summary` tasks are included in the first loop. Technical-route analysis is postponed because it needs different metrics and stronger factual checking.

## Dataset Split

Use two task sets:

- `train` tasks: the agent may inspect failed traces and generate memory notes from these tasks.
- `eval` tasks: the agent must not use task-specific answers from these tasks when writing memory.

Memory-enhanced runs are only credible when compared on the same held-out `eval` task set.

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
