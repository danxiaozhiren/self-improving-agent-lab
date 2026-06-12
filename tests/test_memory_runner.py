import pytest

from self_improving_agent_lab.comparison import compare_trace_scores, render_comparison_report
from self_improving_agent_lab.memory_runner import extract_memory_rules, run_memory_enhanced
from self_improving_agent_lab.runner import Task


MEMORY_TEXT = """# Article Summary Reflection Memory v0

Source status: local observation

## Memory Rules

- Keep the four required sections: Source status, Summary, Mechanism, and Engineering takeaway.
- Preserve the task input source status exactly; do not upgrade inference or paper claims into official facts.
- Use input-specific evidence in the Mechanism section instead of a generic mechanism template.

## Leakage Guard

- Do not add eval task titles, excerpts, final answers, or task IDs to this memory.
"""


def test_extract_memory_rules() -> None:
    assert extract_memory_rules(MEMORY_TEXT) == [
        "Keep the four required sections: Source status, Summary, Mechanism, and Engineering takeaway.",
        "Preserve the task input source status exactly; do not upgrade inference or paper claims into official facts.",
        "Use input-specific evidence in the Mechanism section instead of a generic mechanism template.",
    ]


def test_memory_enhanced_trace_records_memory_step_and_scores() -> None:
    task = Task(
        task_id="summary-eval-001",
        kind="article_summary",
        input={
            "title": "Agent Trace Discipline",
            "source_status": "author_inference",
            "article_excerpt": "Structured traces make repeated runs comparable.",
            "summary_goal": "Explain why trace discipline matters.",
        },
    )

    trace = run_memory_enhanced(task, MEMORY_TEXT)
    payload = trace.to_dict()

    assert payload["workflow_version"] == "memory-v0"
    assert payload["steps"][1] == {
        "name": "load_reflection_memory",
        "payload": {"rule_count": 3, "source_status": "local observation"},
    }
    assert payload["steps"][2] == {
        "name": "format_article_summary",
        "payload": {"strategy": "deterministic-memory-v0"},
    }
    assert "Memory rule applied:" in payload["output"]
    assert payload["scores"] == {
        "format_validity": 1.0,
        "source_status_grounding": 1.0,
        "mechanism_coverage": 1.0,
        "engineering_takeaway": 1.0,
        "input_specificity": 1.0,
    }


def test_comparison_report_does_not_claim_improvement_for_score_tie() -> None:
    baseline = [
        {
            "task_id": "summary-eval-001",
            "scores": {
                "format_validity": 1.0,
                "source_status_grounding": 1.0,
                "mechanism_coverage": 1.0,
                "engineering_takeaway": 1.0,
                "input_specificity": 0.0,
            },
        }
    ]
    memory = [
        {
            "task_id": "summary-eval-001",
            "scores": {
                "format_validity": 1.0,
                "source_status_grounding": 1.0,
                "mechanism_coverage": 1.0,
                "engineering_takeaway": 1.0,
                "input_specificity": 0.0,
            },
        }
    ]

    comparison = compare_trace_scores(baseline, memory)
    report = render_comparison_report(
        comparison,
        eval_task_path="experiments/tasks/article_summary_eval_v0.jsonl",
        baseline_trace_path="runs/baseline-v0-eval.jsonl",
        memory_trace_path="runs/memory-v0-eval.jsonl",
        memory_path="memories/article-summary-reflection-v0.md",
    )

    assert comparison["format_validity"]["delta"] == 0.0
    assert "does not prove self-improvement" in report


def test_comparison_report_can_link_manual_review() -> None:
    comparison = {
        "format_validity": {"baseline": 1.0, "memory": 1.0, "delta": 0.0},
        "source_status_grounding": {"baseline": 1.0, "memory": 1.0, "delta": 0.0},
        "mechanism_coverage": {"baseline": 1.0, "memory": 1.0, "delta": 0.0},
        "engineering_takeaway": {"baseline": 1.0, "memory": 1.0, "delta": 0.0},
        "input_specificity": {"baseline": 0.0, "memory": 1.0, "delta": 1.0},
    }

    report = render_comparison_report(
        comparison,
        eval_task_path="experiments/tasks/article_summary_eval_v0.jsonl",
        baseline_trace_path="runs/baseline-v0-eval.jsonl",
        memory_trace_path="runs/memory-v0-eval.jsonl",
        memory_path="memories/article-summary-reflection-v0.md",
        manual_review_path="reports/memory-v0-semantic-review.md",
        manual_review_summary="directional improvement only.",
    )

    assert "## Manual Review" in report
    assert "`reports/memory-v0-semantic-review.md`" in report
    assert "directional improvement only" in report


def test_comparison_requires_same_task_ids() -> None:
    with pytest.raises(ValueError, match="same task IDs"):
        compare_trace_scores(
            [{"task_id": "baseline-only", "scores": {}}],
            [{"task_id": "memory-only", "scores": {}}],
        )
