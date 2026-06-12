# Article Summary Reflection Memory v0

Source status: local observation

## Scope

This memory is generated only from the article-summary train split.

- Train task path: `experiments/tasks/article_summary_train_v0.jsonl`
- Train trace path: `runs/baseline-v0-train.jsonl`
- Trace count: 3
- Eval task content: not inspected and not copied into this memory.
- Task titles, excerpts, and final answers are intentionally omitted.

## Aggregate Scores

- `format_validity`: 1.00
- `source_status_grounding`: 1.00
- `mechanism_coverage`: 1.00
- `engineering_takeaway`: 1.00
- `input_specificity`: 0.33

## Observed Failures

- `input_specificity` was below 1.0 in 3 train trace(s).

## Memory Rules

- Keep the four required sections: Source status, Summary, Mechanism, and Engineering takeaway.
- Preserve the task input source status exactly; do not upgrade inference or paper claims into official facts.
- Put mechanism evidence in the Mechanism section, not as loose keywords elsewhere.
- Make the Engineering takeaway actionable by naming a next step, rule, or workflow constraint.
- Use input-specific evidence in the Mechanism section instead of a generic mechanism template.

## Leakage Guard

- Do not add eval task titles, excerpts, final answers, or task IDs to this memory.
- Reuse only general writing and workflow rules derived from train traces.
- Compare future memory-enhanced runs only on the held-out eval split.
