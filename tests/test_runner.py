import json
from datetime import datetime

from self_improving_agent_lab.experiment_runner import run_baseline_jsonl
from self_improving_agent_lab.runner import RunTrace, Task, TraceStep, run_baseline


def test_trace_step_serializes_to_dict() -> None:
    step = TraceStep(name="tool_result", payload={"ok": True, "rows": 3})

    assert step.to_dict() == {
        "name": "tool_result",
        "payload": {"ok": True, "rows": 3},
    }


def test_run_trace_serializes_to_dict() -> None:
    trace = RunTrace(
        task_id="summary-001",
        workflow_version="baseline-v0",
        started_at="2026-06-02T00:00:00+00:00",
    )
    trace.add_step("receive_task", kind="article_summary")
    trace.output = "TODO: connect model/tool loop"
    trace.scores = {"format_validity": 0.0}
    trace.reflection = "Needs a real model loop."

    assert trace.to_dict() == {
        "task_id": "summary-001",
        "workflow_version": "baseline-v0",
        "started_at": "2026-06-02T00:00:00+00:00",
        "input": {},
        "steps": [
            {
                "name": "receive_task",
                "payload": {"kind": "article_summary"},
            }
        ],
        "output": "TODO: connect model/tool loop",
        "scores": {"format_validity": 0.0},
        "reflection": "Needs a real model loop.",
    }


def test_run_trace_serializes_to_json() -> None:
    trace = RunTrace(
        task_id="summary-001",
        workflow_version="baseline-v0",
        started_at="2026-06-02T00:00:00+00:00",
    )
    trace.add_step("receive_task", kind="article_summary")

    payload = json.loads(trace.to_json())

    assert payload["task_id"] == "summary-001"
    assert payload["input"] == {}
    assert payload["steps"] == [
        {
            "name": "receive_task",
            "payload": {"kind": "article_summary"},
        }
    ]


def test_baseline_trace_is_json_serializable() -> None:
    task = Task(
        task_id="summary-001",
        kind="article_summary",
        input={"title": "Agent loops", "url": "https://example.com/agent-loops"},
    )

    trace = run_baseline(task)
    payload = json.loads(trace.to_json())

    assert payload["task_id"] == "summary-001"
    assert payload["workflow_version"] == "baseline-v0"
    assert payload["input"] == {
        "title": "Agent loops",
        "url": "https://example.com/agent-loops",
    }
    assert payload["steps"] == [
        {
            "name": "receive_task",
            "payload": {
                "kind": "article_summary",
                "input_keys": ["title", "url"],
            },
        }
    ]
    assert payload["scores"] == {}
    datetime.fromisoformat(payload["started_at"])


def test_baseline_jsonl_runner_writes_trace_file(tmp_path) -> None:
    task_path = tmp_path / "tasks.jsonl"
    output_path = tmp_path / "runs" / "baseline-v0.jsonl"
    task_path.write_text(
        json.dumps(
            {
                "task_id": "summary-001",
                "kind": "article_summary",
                "input": {
                    "title": "Trace discipline",
                    "source_status": "author_inference",
                    "article_excerpt": "Structured traces make repeated runs comparable.",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    traces = run_baseline_jsonl(task_path, output_path)
    lines = output_path.read_text(encoding="utf-8").splitlines()

    assert len(traces) == 1
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["task_id"] == "summary-001"
    assert payload["input"]["title"] == "Trace discipline"
    assert payload["workflow_version"] == "baseline-v0"
    assert payload["scores"] == {
        "format_validity": 0.0,
        "has_mechanism": 1.0,
        "has_takeaway": 0.0,
        "mentions_source_status": 0.0,
    }
    assert payload["steps"][-1] == {
        "name": "evaluate_trace",
        "payload": {
            "rubric_keys": [
                "format_validity",
                "has_mechanism",
                "has_takeaway",
                "mentions_source_status",
            ],
        },
    }
