# Article Summary Rubric

The first experiment scope is `article_summary` only. Technical-route analysis is intentionally out of scope until the summary loop has a credible evaluator.

## Score Shape

Each trace stores these deterministic first-pass scores:

```text
format_validity
source_status_grounding
mechanism_coverage
engineering_takeaway
input_specificity
```

Each score is `0.0`, `0.5`, or `1.0`. The rule-based evaluator is not the final judge; it is a cheap guardrail that should catch obvious failures and produce inspectable signals for reflection.

## Required Output Sections

The first-pass evaluator expects these sections:

```text
Source status: ...
Summary: ...
Mechanism: ...
Engineering takeaway: ...
```

Keyword stuffing outside the required sections should not earn mechanism or takeaway credit.

## format_validity

Scores whether the output is a real answer rather than a placeholder.

- `1.0`: The output is non-empty, not a TODO placeholder, long enough to contain a meaningful summary, and includes all required sections with non-trivial content.
- `0.5`: The output is non-empty and not a TODO placeholder, but too short or missing one or more required sections.
- `0.0`: The output is empty or starts with a TODO-style placeholder.

## source_status_grounding

Scores whether the output preserves the source-status boundary from the task input.

- `1.0`: The output explicitly mentions the expected source status, such as `paper_claims` or `author inference`.
- `0.5`: The `Source status` section exists, but does not match the expected source status.
- `0.0`: The output does not include a `Source status` section.

The goal is not just a header. Important claims in articles should still avoid presenting author inference, community implementation, or local observation as official facts.

## mechanism_coverage

Scores whether the output explains how the idea works.

- `1.0`: The `Mechanism` section contains at least two mechanism signals, such as loop, feedback, trace, workflow, memory, tool, mechanism, or their Chinese equivalents.
- `0.5`: The `Mechanism` section contains one mechanism signal.
- `0.0`: The `Mechanism` section is missing, contains no mechanism signal, or the output is a placeholder.

This score is intentionally shallow. It checks whether a mechanism explanation is likely present; it does not prove the explanation is correct.

## engineering_takeaway

Scores whether the output converts the summary into an actionable engineering implication.

- `1.0`: The `Engineering takeaway` section contains at least two takeaway signals, such as engineering, takeaway, rule, SOP, should, next step, or their Chinese equivalents.
- `0.5`: The `Engineering takeaway` section contains one takeaway signal.
- `0.0`: The `Engineering takeaway` section is missing, contains no actionable engineering signal, or the output is a placeholder.

## input_specificity

Scores whether the `Mechanism` section uses task-specific evidence instead of only a generic mechanism template.

- `1.0`: The `Mechanism` section mentions task-specific evidence and connects it with a mechanism claim using words such as because, shows, supports, connects, or enables.
- `0.5`: The `Mechanism` section mentions the title or meaningful input terms, but only as isolated evidence or without a mechanism link.
- `0.0`: The `Mechanism` section is generic, missing, or only uses common workflow words.

Common workflow words such as trace, memory, workflow, feedback, and mechanism do not count as task-specific evidence.

## Fixture Cases

The evaluator is tested with `tests/fixtures/article_summary_eval_cases.jsonl`.

Current fixture coverage:

- good summary: all scores are `1.0`.
- TODO placeholder: all scores are `0.0`.
- keyword stuffing without sections: format gets only `0.5`, mechanism and takeaway stay `0.0`.
- wrong source status: source grounding gets only `0.5`.
- missing mechanism section: mechanism coverage is `0.0`.
- missing engineering takeaway section: engineering takeaway is `0.0`.
- thin sections: section-specific scores can receive `0.5`.
- input-specific mechanism: specificity depends on task input terms appearing in the `Mechanism` section.
- isolated keyword list: input-specific keywords receive only partial specificity credit without a mechanism link.

## Known Limits

This rubric now blocks the most obvious keyword-stuffing case and prevents isolated input keywords from receiving full `input_specificity`. It can still be fooled by polished shallow text or a task-specific but wrong mechanism explanation. A later evaluator should add stronger semantic examples, negative cases, and possibly a judge model. Until then, trace review should treat scores as signals, not proof.
