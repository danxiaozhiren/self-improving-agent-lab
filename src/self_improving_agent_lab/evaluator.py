from __future__ import annotations

from dataclasses import dataclass

from self_improving_agent_lab.runner import RunTrace


RUBRIC_KEYS = (
    "format_validity",
    "source_status_grounding",
    "mechanism_coverage",
    "engineering_takeaway",
)

MIN_MEANINGFUL_OUTPUT_CHARS = 80
MIN_SECTION_CHARS = 20

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


@dataclass(frozen=True)
class SummarySections:
    source_status: str = ""
    summary: str = ""
    mechanism: str = ""
    engineering_takeaway: str = ""


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
    sections = _parse_summary_sections(output)

    return {
        "format_validity": _score_format_validity(normalized, sections),
        "source_status_grounding": _score_source_status(sections.source_status, expected_source, is_placeholder),
        "mechanism_coverage": _score_section_signal_coverage(sections.mechanism, MECHANISM_SIGNALS, is_placeholder),
        "engineering_takeaway": _score_section_signal_coverage(
            sections.engineering_takeaway,
            TAKEAWAY_SIGNALS,
            is_placeholder,
        ),
    }


def _parse_summary_sections(output: str) -> SummarySections:
    section_values: dict[str, list[str]] = {
        "source_status": [],
        "summary": [],
        "mechanism": [],
        "engineering_takeaway": [],
    }
    current_section = ""
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        section_name, section_value = _split_section_line(line)
        if section_name:
            current_section = section_name
            if section_value:
                section_values[current_section].append(section_value)
            continue
        if current_section:
            section_values[current_section].append(line)

    return SummarySections(
        source_status=" ".join(section_values["source_status"]).strip(),
        summary=" ".join(section_values["summary"]).strip(),
        mechanism=" ".join(section_values["mechanism"]).strip(),
        engineering_takeaway=" ".join(section_values["engineering_takeaway"]).strip(),
    )


def _split_section_line(line: str) -> tuple[str, str]:
    lower_line = line.lower()
    section_prefixes = {
        "source_status": ("source status:", "source-status:", "source_status:", "来源状态：", "来源状态:"),
        "summary": ("summary:", "摘要：", "摘要:"),
        "mechanism": ("mechanism:", "机制：", "机制:"),
        "engineering_takeaway": (
            "engineering takeaway:",
            "engineering takeaways:",
            "工程启发：",
            "工程启发:",
        ),
    }
    for section_name, prefixes in section_prefixes.items():
        for prefix in prefixes:
            if lower_line.startswith(prefix):
                return section_name, line[len(prefix) :].strip()
    return "", ""


def _score_format_validity(normalized_output: str, sections: SummarySections) -> float:
    if _is_placeholder(normalized_output):
        return 0.0
    present_sections = sum(
        bool(value)
        for value in (
            sections.source_status,
            sections.summary,
            sections.mechanism,
            sections.engineering_takeaway,
        )
    )
    if len(normalized_output) < MIN_MEANINGFUL_OUTPUT_CHARS or present_sections < 4:
        return 0.5
    if any(
        len(value) < MIN_SECTION_CHARS
        for value in (sections.summary, sections.mechanism, sections.engineering_takeaway)
    ):
        return 0.5
    return 1.0


def _score_source_status(
    source_status_section: str,
    expected_source: str,
    is_placeholder: bool,
) -> float:
    if is_placeholder:
        return 0.0
    normalized_section = source_status_section.strip().lower()
    if not normalized_section:
        return 0.0
    source_variants = set()
    if expected_source:
        source_variants = {
            expected_source,
            expected_source.replace("_", " "),
            expected_source.replace("_", "-"),
        }
    if source_variants and any(variant in normalized_section for variant in source_variants):
        return 1.0
    return 0.5


def _score_section_signal_coverage(
    section_content: str,
    signals: tuple[str, ...],
    is_placeholder: bool,
) -> float:
    if is_placeholder:
        return 0.0
    normalized_section = section_content.strip().lower()
    if not normalized_section:
        return 0.0
    hits = {signal for signal in signals if signal in normalized_section}
    if len(hits) >= 2:
        return 1.0
    if len(hits) == 1:
        return 0.5
    return 0.0


def _is_placeholder(normalized_output: str) -> bool:
    if not normalized_output:
        return True
    return normalized_output.startswith(("todo:", "todo："))
