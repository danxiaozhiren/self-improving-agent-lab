# Article Summary Rubric

The first experiment scope is `article_summary` only. Technical-route analysis is intentionally out of scope until the summary loop has a credible evaluator.

## Score Shape

Each trace stores these deterministic first-pass scores:

```text
format_validity
source_status_grounding
mechanism_coverage
engineering_takeaway
```

Each score is `0.0`, `0.5`, or `1.0`. The rule-based evaluator is not the final judge; it is a cheap guardrail that should catch obvious failures and produce inspectable signals for reflection.

## format_validity

Scores whether the output is a real answer rather than a placeholder.

- `1.0`: The output is non-empty, not a TODO placeholder, and long enough to contain a meaningful summary.
- `0.5`: The output is non-empty and not a TODO placeholder, but too short to be a useful summary.
- `0.0`: The output is empty or starts with a TODO-style placeholder.

## source_status_grounding

Scores whether the output preserves the source-status boundary from the task input.

- `1.0`: The output explicitly mentions the expected source status, such as `paper_claims` or `author inference`.
- `0.5`: The output mentions source status generally, but does not match the expected source status.
- `0.0`: The output does not mention source status.

The goal is not just a header. Important claims in articles should still avoid presenting author inference, community implementation, or local observation as official facts.

## mechanism_coverage

Scores whether the output explains how the idea works.

- `1.0`: The output contains at least two mechanism signals, such as loop, feedback, trace, workflow, memory, tool, mechanism, or their Chinese equivalents.
- `0.5`: The output contains one mechanism signal.
- `0.0`: The output contains no mechanism signal, or the output is a placeholder.

This score is intentionally shallow. It checks whether a mechanism explanation is likely present; it does not prove the explanation is correct.

## engineering_takeaway

Scores whether the output converts the summary into an actionable engineering implication.

- `1.0`: The output contains at least two takeaway signals, such as engineering, takeaway, rule, SOP, should, next step, or their Chinese equivalents.
- `0.5`: The output contains one takeaway signal.
- `0.0`: The output contains no actionable engineering signal, or the output is a placeholder.

## Known Limits

This rubric can be fooled by keyword stuffing. A later evaluator should add examples, negative cases, and possibly a judge model. Until then, trace review should treat scores as signals, not proof.
