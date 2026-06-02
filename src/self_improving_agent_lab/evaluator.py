from __future__ import annotations

from self_improving_agent_lab.runner import RunTrace


RUBRIC_KEYS = (
    "format_validity",
    "mentions_source_status",
    "has_mechanism",
    "has_takeaway",
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

    return {
        "format_validity": _score_format_validity(normalized),
        "mentions_source_status": _score_source_status(normalized, expected_source),
        "has_mechanism": _score_keyword_presence(
            normalized,
            ("mechanism", "loop", "feedback", "trace", "workflow", "memory", "tool", "机制", "闭环", "反馈", "轨迹"),
        ),
        "has_takeaway": _score_keyword_presence(
            normalized,
            ("takeaway", "engineering", "rule", "sop", "should", "启发", "规则", "结论", "下一步"),
        ),
    }


def _score_format_validity(normalized_output: str) -> float:
    if not normalized_output:
        return 0.0
    if normalized_output.startswith("todo:"):
        return 0.0
    return 1.0


def _score_source_status(normalized_output: str, expected_source: str) -> float:
    if not expected_source:
        return 0.0
    source_variants = {
        expected_source,
        expected_source.replace("_", " "),
        expected_source.replace("_", "-"),
    }
    return 1.0 if any(variant in normalized_output for variant in source_variants) else 0.0


def _score_keyword_presence(normalized_output: str, keywords: tuple[str, ...]) -> float:
    return 1.0 if any(keyword in normalized_output for keyword in keywords) else 0.0
