from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any


RUBRIC_KEYS = (
    "format_validity",
    "source_status_grounding",
    "mechanism_coverage",
    "engineering_takeaway",
)


def load_trace_dicts_jsonl(path: Path) -> list[dict[str, Any]]:
    traces: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            if not isinstance(payload, dict):
                raise ValueError(f"{path}:{line_number}: trace payload must be a JSON object")
            traces.append(payload)
    return traces


def write_reflection_memory(memory_text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(memory_text, encoding="utf-8")


def generate_reflection_memory(
    traces: Iterable[dict[str, Any]],
    *,
    train_task_path: str,
    trace_path: str,
) -> str:
    trace_list = list(traces)
    averages = _average_scores(trace_list)
    low_score_counts = _low_score_counts(trace_list)
    low_score_total = sum(low_score_counts.values())

    lines = [
        "# Article Summary Reflection Memory v0",
        "",
        "Source status: local observation",
        "",
        "## Scope",
        "",
        "This memory is generated only from the article-summary train split.",
        "",
        f"- Train task path: `{train_task_path}`",
        f"- Train trace path: `{trace_path}`",
        f"- Trace count: {len(trace_list)}",
        "- Eval task content: not inspected and not copied into this memory.",
        "- Task titles, excerpts, and final answers are intentionally omitted.",
        "",
        "## Aggregate Scores",
        "",
    ]

    for key in RUBRIC_KEYS:
        lines.append(f"- `{key}`: {_format_score(averages.get(key, 0.0))}")

    lines.extend(
        [
            "",
            "## Observed Failures",
            "",
        ]
    )

    if low_score_total == 0:
        lines.append("- No low-score train failures were observed in this run.")
        lines.append("- Treat the rules below as preservation rules, not evidence of a memory improvement.")
    else:
        for key in RUBRIC_KEYS:
            count = low_score_counts.get(key, 0)
            if count:
                lines.append(f"- `{key}` was below 1.0 in {count} train trace(s).")

    lines.extend(
        [
            "",
            "## Memory Rules",
            "",
        ]
    )
    for rule in _memory_rules_for_scores(low_score_counts):
        lines.append(f"- {rule}")

    lines.extend(
        [
            "",
            "## Leakage Guard",
            "",
            "- Do not add eval task titles, excerpts, final answers, or task IDs to this memory.",
            "- Reuse only general writing and workflow rules derived from train traces.",
            "- Compare future memory-enhanced runs only on the held-out eval split.",
            "",
        ]
    )
    return "\n".join(lines)


def _average_scores(traces: list[dict[str, Any]]) -> dict[str, float]:
    if not traces:
        return {key: 0.0 for key in RUBRIC_KEYS}
    totals = {key: 0.0 for key in RUBRIC_KEYS}
    for trace in traces:
        scores = trace.get("scores", {})
        for key in RUBRIC_KEYS:
            totals[key] += float(scores.get(key, 0.0))
    return {key: totals[key] / len(traces) for key in RUBRIC_KEYS}


def _low_score_counts(traces: list[dict[str, Any]]) -> dict[str, int]:
    counts = {key: 0 for key in RUBRIC_KEYS}
    for trace in traces:
        scores = trace.get("scores", {})
        for key in RUBRIC_KEYS:
            if float(scores.get(key, 0.0)) < 1.0:
                counts[key] += 1
    return counts


def _memory_rules_for_scores(low_score_counts: dict[str, int]) -> list[str]:
    rules = [
        "Keep the four required sections: Source status, Summary, Mechanism, and Engineering takeaway.",
        "Preserve the task input source status exactly; do not upgrade inference or paper claims into official facts.",
        "Put mechanism evidence in the Mechanism section, not as loose keywords elsewhere.",
        "Make the Engineering takeaway actionable by naming a next step, rule, or workflow constraint.",
    ]
    if low_score_counts.get("source_status_grounding", 0):
        rules.append("When source grounding fails, repair the Source status section before changing the summary prose.")
    if low_score_counts.get("mechanism_coverage", 0):
        rules.append("When mechanism coverage fails, explain the loop, feedback, trace, workflow, or memory relationship directly.")
    if low_score_counts.get("engineering_takeaway", 0):
        rules.append("When takeaway coverage fails, add a concrete next step instead of a generic conclusion.")
    return rules


def _format_score(value: float) -> str:
    return f"{value:.2f}"
