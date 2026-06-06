from __future__ import annotations

from self_improving_agent_lab.runner import RunTrace


RUBRIC_KEYS = (
    "format_validity",
    "source_status_grounding",
    "mechanism_coverage",
    "engineering_takeaway",
)

MIN_MEANINGFUL_OUTPUT_CHARS = 80

MECHANISM_SIGNALS = (
    "mechanism",
    "loop",
    "feedback",
    "trace",
    "workflow",
    "memory",
    "tool",
    "机制",
    "闭环",
    "反馈",
    "轨迹",
    "工作流",
    "记忆",
    "工具",
)

TAKEAWAY_SIGNALS = (
    "takeaway",
    "engineering",
    "rule",
    "sop",
    "should",
    "next step",
    "actionable",
    "启发",
    "工程",
    "规则",
    "结论",
    "下一步",
    "应该",
)


def evaluate_trace(trace: RunTrace) -> dict[str, float]:
    """Score a trace with a deterministic first-pass rubric."""

    return evaluate_article_summary_output(
        output=trace.output,
        source_status=str(trace.input.get("source_status", "")),
    )


def evaluate_article_summary_output(output: str, source_status: str) -> dict[str, float]:
    normalized = output.strip().lower()
    expected_source = source_status.strip().lower()
    is_placeholder = _is_placeholder(normalized)

    return {
        "format_validity": _score_format_validity(normalized),
        "source_status_grounding": _score_source_status(normalized, expected_source, is_placeholder),
        "mechanism_coverage": _score_signal_coverage(normalized, MECHANISM_SIGNALS, is_placeholder),
        "engineering_takeaway": _score_signal_coverage(normalized, TAKEAWAY_SIGNALS, is_placeholder),
    }


def _score_format_validity(normalized_output: str) -> float:
    if _is_placeholder(normalized_output):
        return 0.0
    if len(normalized_output) < MIN_MEANINGFUL_OUTPUT_CHARS:
        return 0.5
    return 1.0


def _score_source_status(
    normalized_output: str,
    expected_source: str,
    is_placeholder: bool,
) -> float:
    if is_placeholder:
        return 0.0
    source_variants = set()
    if expected_source:
        source_variants = {
            expected_source,
            expected_source.replace("_", " "),
            expected_source.replace("_", "-"),
        }
    if source_variants and any(variant in normalized_output for variant in source_variants):
        return 1.0
    if any(
        marker in normalized_output
        for marker in ("source status", "source-status", "source_status", "来源状态", "来源标签")
    ):
        return 0.5
    return 0.0


def _score_signal_coverage(
    normalized_output: str,
    signals: tuple[str, ...],
    is_placeholder: bool,
) -> float:
    if is_placeholder:
        return 0.0
    hits = {signal for signal in signals if signal in normalized_output}
    if len(hits) >= 2:
        return 1.0
    if len(hits) == 1:
        return 0.5
    return 0.0


def _is_placeholder(normalized_output: str) -> bool:
    if not normalized_output:
        return True
    return normalized_output.startswith(("todo:", "todo："))
