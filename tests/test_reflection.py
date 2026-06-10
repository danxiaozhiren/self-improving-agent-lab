from self_improving_agent_lab.experiment_runner import load_tasks_jsonl, run_baseline_tasks
from self_improving_agent_lab.reflection import generate_reflection_memory

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRAIN_TASK_PATH = PROJECT_ROOT / "experiments/tasks/article_summary_train_v0.jsonl"
EVAL_TASK_PATH = PROJECT_ROOT / "experiments/tasks/article_summary_eval_v0.jsonl"


def test_reflection_memory_uses_train_aggregate_without_eval_leakage() -> None:
    train_tasks = load_tasks_jsonl(TRAIN_TASK_PATH)
    eval_tasks = load_tasks_jsonl(EVAL_TASK_PATH)
    train_traces = [trace.to_dict() for trace in run_baseline_tasks(train_tasks)]

    memory_text = generate_reflection_memory(
        train_traces,
        train_task_path="experiments/tasks/article_summary_train_v0.jsonl",
        trace_path="runs/baseline-v0-train.jsonl",
    )

    assert "Source status: local observation" in memory_text
    assert "Trace count: 3" in memory_text
    assert "`format_validity`: 1.00" in memory_text
    assert "No low-score train failures were observed" in memory_text
    assert "Task titles, excerpts, and final answers are intentionally omitted." in memory_text

    for task in train_tasks + eval_tasks:
        assert task.task_id not in memory_text
        assert str(task.input["title"]) not in memory_text
        assert str(task.input["article_excerpt"]) not in memory_text


def test_reflection_memory_records_low_score_metrics_without_task_ids() -> None:
    memory_text = generate_reflection_memory(
        [
            {
                "task_id": "summary-train-999",
                "scores": {
                    "format_validity": 1.0,
                    "source_status_grounding": 0.5,
                    "mechanism_coverage": 0.0,
                    "engineering_takeaway": 1.0,
                },
            }
        ],
        train_task_path="experiments/tasks/article_summary_train_v0.jsonl",
        trace_path="runs/baseline-v0-train.jsonl",
    )

    assert "`source_status_grounding` was below 1.0 in 1 train trace(s)." in memory_text
    assert "`mechanism_coverage` was below 1.0 in 1 train trace(s)." in memory_text
    assert "summary-train-999" not in memory_text
