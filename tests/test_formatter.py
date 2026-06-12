from self_improving_agent_lab.evaluator import evaluate_article_summary_output
from self_improving_agent_lab.formatter import format_article_summary
from self_improving_agent_lab.runner import Task


def test_article_summary_formatter_preserves_source_status_and_goal() -> None:
    task = Task(
        task_id="summary-001",
        kind="article_summary",
        input={
            "title": "Trace discipline",
            "source_status": "author_inference",
            "article_excerpt": "Structured traces make repeated runs comparable.",
            "summary_goal": "Explain why traces matter before memory.",
        },
    )

    output = format_article_summary(task)

    assert "Source status: author_inference." in output
    assert "Trace discipline" in output
    assert "Structured traces make repeated runs comparable." in output
    assert "Explain why traces matter before memory." in output


def test_article_summary_formatter_exposes_input_specificity_gap() -> None:
    task = Task(
        task_id="summary-001",
        kind="article_summary",
        input={
            "title": "Trace discipline",
            "source_status": "author_inference",
            "article_excerpt": "Structured traces make repeated runs comparable.",
        },
    )

    scores = evaluate_article_summary_output(
        output=format_article_summary(task),
        source_status="author_inference",
        task_input=task.input,
    )

    assert scores == {
        "format_validity": 1.0,
        "source_status_grounding": 1.0,
        "mechanism_coverage": 1.0,
        "engineering_takeaway": 1.0,
        "input_specificity": 0.0,
    }


def test_article_summary_formatter_can_apply_memory_specificity_rule() -> None:
    task = Task(
        task_id="summary-001",
        kind="article_summary",
        input={
            "title": "Trace discipline",
            "source_status": "author_inference",
            "article_excerpt": "Structured traces make repeated runs comparable.",
        },
    )

    scores = evaluate_article_summary_output(
        output=format_article_summary(
            task,
            memory_rules=["Use input-specific evidence in the Mechanism section instead of a generic mechanism template."],
        ),
        source_status="author_inference",
        task_input=task.input,
    )

    assert scores == {
        "format_validity": 1.0,
        "source_status_grounding": 1.0,
        "mechanism_coverage": 1.0,
        "engineering_takeaway": 1.0,
        "input_specificity": 1.0,
    }
