from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from self_improving_agent_lab.reflection import RUBRIC_KEYS


def compare_trace_scores(
    baseline_traces: Iterable[dict[str, Any]],
    memory_traces: Iterable[dict[str, Any]],
) -> dict[str, dict[str, float]]:
    baseline_by_id = _index_by_task_id(baseline_traces)
    memory_by_id = _index_by_task_id(memory_traces)
    if set(baseline_by_id) != set(memory_by_id):
        raise ValueError("Baseline and memory traces must contain the same task IDs")

    task_count = len(baseline_by_id)
    if task_count == 0:
        return {key: {"baseline": 0.0, "memory": 0.0, "delta": 0.0} for key in RUBRIC_KEYS}

    rows: dict[str, dict[str, float]] = {}
    for key in RUBRIC_KEYS:
        baseline_avg = sum(_score(trace, key) for trace in baseline_by_id.values()) / task_count
        memory_avg = sum(_score(trace, key) for trace in memory_by_id.values()) / task_count
        rows[key] = {
            "baseline": baseline_avg,
            "memory": memory_avg,
            "delta": memory_avg - baseline_avg,
        }
    return rows


def render_comparison_report(
    comparison: dict[str, dict[str, float]],
    *,
    eval_task_path: str,
    baseline_trace_path: str,
    memory_trace_path: str,
    memory_path: str,
    manual_review_path: str | None = None,
    manual_review_summary: str | None = None,
) -> str:
    improved = any(row["delta"] > 0 for row in comparison.values())
    regressed = any(row["delta"] < 0 for row in comparison.values())
    if improved and not regressed:
        conclusion = "Memory-v0 produced a rubric-level improvement on at least one metric without a score regression."
    elif regressed:
        conclusion = "Memory-v0 regressed at least one rubric metric; do not treat it as an improvement."
    else:
        conclusion = "Memory-v0 produced no rubric-score improvement; this run does not prove self-improvement."

    lines = [
        "# Baseline vs Memory-v0 Comparison",
        "",
        "Source status: local observation",
        "",
        "## Inputs",
        "",
        f"- Eval task path: `{eval_task_path}`",
        f"- Baseline trace path: `{baseline_trace_path}`",
        f"- Memory trace path: `{memory_trace_path}`",
        f"- Memory path: `{memory_path}`",
        "",
        "## Average Scores",
        "",
        "| Metric | Baseline | Memory-v0 | Delta |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key in RUBRIC_KEYS:
        row = comparison[key]
        lines.append(f"| `{key}` | {row['baseline']:.2f} | {row['memory']:.2f} | {row['delta']:.2f} |")

    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            conclusion,
            "",
        ]
    )
    if manual_review_path:
        lines.extend(
            [
                "## Manual Review",
                "",
                f"- Review path: `{manual_review_path}`",
                (
                    f"- Current review status: {manual_review_summary}"
                    if manual_review_summary
                    else "- Current review status: manual review is recorded separately."
                ),
                "",
            ]
        )

    lines.extend(
        [
            "## Interpretation Guard",
            "",
            "- A score tie is not evidence that memory helped.",
            "- Manual review is required for any claimed semantic improvement.",
            "- A rubric-score improvement is only meaningful when the changed metric reflects a real quality gap.",
            "",
        ]
    )
    return "\n".join(lines)


def write_comparison_report(report_text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report_text, encoding="utf-8")


def _index_by_task_id(traces: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for trace in traces:
        task_id = str(trace.get("task_id", ""))
        if not task_id:
            raise ValueError("Trace is missing task_id")
        indexed[task_id] = trace
    return indexed


def _score(trace: dict[str, Any], key: str) -> float:
    return float(trace.get("scores", {}).get(key, 0.0))
