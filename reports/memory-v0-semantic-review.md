# Memory-v0 Semantic Review

Source status: local observation

## Scope

This review checks whether the `input_specificity` rubric improvement in
`reports/baseline-vs-memory-v0.md` reflects a real quality improvement.

Reviewed artifacts:

- Baseline traces: `runs/baseline-v0-eval.jsonl`
- Memory traces: `runs/memory-v0-eval.jsonl`
- Held-out tasks: `experiments/tasks/article_summary_eval_v0.jsonl`

## Verdict

The memory-v0 improvement is narrow but semantically plausible.

Memory-v0 changed the held-out outputs from a fully generic `Mechanism` section
to a task-aware mechanism detail that connects the article excerpt to the
requested goal. That is a meaningful improvement over the baseline mechanism
template.

Treat this as validation of the narrow memory loop and evaluator change, not as
proof that a real LLM agent now writes better article summaries. The current
improvement is still deterministic and template-driven.

## Task Notes

| Task | Baseline issue | Memory-v0 change | Manual judgment |
| --- | --- | --- | --- |
| `summary-eval-001` | Mechanism uses the same generic loop/feedback/trace/memory sentence. | Adds a mechanism detail saying the excerpt shows traces preserve task inputs, actions, outputs, scores, and failure signals. | Passes the narrow specificity check; still mostly repeats the excerpt. |
| `summary-eval-002` | Mechanism does not address source-status drift. | Adds a mechanism detail connecting mixed source-status notes to wrong confidence in later reflection. | Passes the narrow specificity check; explanation is template-like but relevant. |
| `summary-eval-003` | Mechanism does not address eval leakage. | Adds a mechanism detail connecting eval-task answers in memory to unpersuasive memory-enhanced results. | Passes the narrow specificity check; this is the strongest of the three because it names the leakage mechanism directly. |

## Follow-up

- Add semantic negative fixtures where the mechanism is task-specific but wrong.
- Reduce excerpt copying by requiring a compressed mechanism explanation.
- Replace the deterministic formatter with a real LLM agent and inspect real
  failure modes.
