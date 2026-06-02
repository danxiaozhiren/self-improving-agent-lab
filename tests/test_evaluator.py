from self_improving_agent_lab.evaluator import evaluate_article_summary_output, evaluate_trace
from self_improving_agent_lab.runner import RunTrace


def test_placeholder_output_scores_low() -> None:
    scores = evaluate_article_summary_output(
        output="TODO: connect model/tool loop",
        source_status="paper_claims",
    )

    assert scores == {
        "format_validity": 0.0,
        "mentions_source_status": 0.0,
        "has_mechanism": 1.0,
        "has_takeaway": 0.0,
    }


def test_output_scores_when_it_mentions_required_signals() -> None:
    scores = evaluate_article_summary_output(
        output=(
            "Source status: paper_claims. The mechanism is a feedback loop. "
            "Engineering takeaway: preserve trace data before changing memory."
        ),
        source_status="paper_claims",
    )

    assert scores == {
        "format_validity": 1.0,
        "mentions_source_status": 1.0,
        "has_mechanism": 1.0,
        "has_takeaway": 1.0,
    }


def test_evaluate_trace_uses_trace_input_source_status() -> None:
    trace = RunTrace(
        task_id="summary-001",
        workflow_version="baseline-v0",
        started_at="2026-06-02T00:00:00+00:00",
        input={"source_status": "author_inference"},
        output="Source status: author inference. The trace makes the workflow observable.",
    )

    scores = evaluate_trace(trace)

    assert scores["format_validity"] == 1.0
    assert scores["mentions_source_status"] == 1.0
    assert scores["has_mechanism"] == 1.0


def test_missing_source_status_only_affects_source_status_score() -> None:
    trace = RunTrace(
        task_id="summary-001",
        workflow_version="baseline-v0",
        started_at="2026-06-02T00:00:00+00:00",
        output="The mechanism is a workflow loop. Engineering takeaway: preserve trace data.",
    )

    scores = evaluate_trace(trace)

    assert scores["format_validity"] == 1.0
    assert scores["mentions_source_status"] == 0.0
    assert scores["has_mechanism"] == 1.0
    assert scores["has_takeaway"] == 1.0
