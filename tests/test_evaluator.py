import json
from pathlib import Path

from self_improving_agent_lab.evaluator import evaluate_article_summary_output, evaluate_trace
from self_improving_agent_lab.runner import RunTrace


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "article_summary_eval_cases.jsonl"


def test_placeholder_output_scores_low() -> None:
    scores = evaluate_article_summary_output(
        output="TODO: connect model/tool loop",
        source_status="paper_claims",
    )

    assert scores == {
        "format_validity": 0.0,
        "source_status_grounding": 0.0,
        "mechanism_coverage": 0.0,
        "engineering_takeaway": 0.0,
    }


def test_output_scores_when_it_mentions_required_signals() -> None:
    scores = evaluate_article_summary_output(
        output=(
            "Source status: paper_claims.\n"
            "Summary: The article describes a feedback workflow with trace evidence.\n"
            "Mechanism: The mechanism is a feedback loop that preserves trace data.\n"
            "Engineering takeaway: the next step should preserve a rule before changing memory."
        ),
        source_status="paper_claims",
    )

    assert scores == {
        "format_validity": 1.0,
        "source_status_grounding": 1.0,
        "mechanism_coverage": 1.0,
        "engineering_takeaway": 1.0,
    }


def test_output_gets_partial_credit_for_generic_source_status() -> None:
    scores = evaluate_article_summary_output(
        output=(
            "Source status: source label is present but not specific enough.\n"
            "Summary: The article describes a feedback workflow with trace evidence.\n"
            "Mechanism: The mechanism is a workflow loop.\n"
            "Engineering takeaway: preserve trace rules for the next step."
        ),
        source_status="paper_claims",
    )

    assert scores["source_status_grounding"] == 0.5


def test_evaluate_trace_uses_trace_input_source_status() -> None:
    trace = RunTrace(
        task_id="summary-001",
        workflow_version="baseline-v0",
        started_at="2026-06-02T00:00:00+00:00",
        input={"source_status": "author_inference"},
        output=(
            "Source status: author inference.\n"
            "Summary: The trace makes the workflow observable.\n"
            "Mechanism: The mechanism uses trace and workflow comparison.\n"
            "Engineering takeaway: keep a rule for source labels."
        ),
    )

    scores = evaluate_trace(trace)

    assert scores["format_validity"] == 1.0
    assert scores["source_status_grounding"] == 1.0
    assert scores["mechanism_coverage"] == 1.0


def test_missing_source_status_gets_partial_credit_for_generic_source_note() -> None:
    trace = RunTrace(
        task_id="summary-001",
        workflow_version="baseline-v0",
        started_at="2026-06-02T00:00:00+00:00",
        output=(
            "Source status: source label unavailable.\n"
            "Summary: The article describes repeated trace comparison.\n"
            "Mechanism: The mechanism is a workflow loop.\n"
            "Engineering takeaway: the next step should preserve trace data as a rule."
        ),
    )

    scores = evaluate_trace(trace)

    assert scores["format_validity"] == 1.0
    assert scores["source_status_grounding"] == 0.5
    assert scores["mechanism_coverage"] == 1.0
    assert scores["engineering_takeaway"] == 1.0


def test_article_summary_evaluator_fixture_cases() -> None:
    with FIXTURE_PATH.open(encoding="utf-8") as file:
        cases = [json.loads(line) for line in file if line.strip()]

    assert cases
    for case in cases:
        scores = evaluate_article_summary_output(
            output=case["output"],
            source_status=case["source_status"],
        )

        assert scores == case["expected_scores"], case["case_id"]
