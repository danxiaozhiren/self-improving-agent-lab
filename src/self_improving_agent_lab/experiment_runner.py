from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

from self_improving_agent_lab.evaluator import evaluate_trace
from self_improving_agent_lab.runner import RunTrace, Task, run_baseline


def load_tasks_jsonl(path: Path) -> list[Task]:
    tasks: list[Task] = []
    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            try:
                tasks.append(Task.from_dict(payload))
            except ValueError as error:
                raise ValueError(f"{path}:{line_number}: {error}") from error
    return tasks


def write_traces_jsonl(traces: Iterable[RunTrace], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for trace in traces:
            file.write(trace.to_json())
            file.write("\n")


def run_baseline_tasks(
    tasks: Iterable[Task],
    workflow_version: str = "baseline-v0",
) -> list[RunTrace]:
    traces = [run_baseline(task, workflow_version=workflow_version) for task in tasks]
    for trace in traces:
        trace.scores = evaluate_trace(trace)
        trace.add_step("evaluate_trace", rubric_keys=sorted(trace.scores.keys()))
    return traces


def run_baseline_jsonl(
    task_path: Path,
    output_path: Path,
    workflow_version: str = "baseline-v0",
) -> list[RunTrace]:
    traces = run_baseline_tasks(
        load_tasks_jsonl(task_path),
        workflow_version=workflow_version,
    )
    write_traces_jsonl(traces, output_path)
    return traces


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the baseline workflow over JSONL tasks.")
    parser.add_argument(
        "--tasks",
        type=Path,
        default=Path("experiments/tasks/article_summary_v0.jsonl"),
        help="Path to the input task JSONL file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("runs/baseline-v0.jsonl"),
        help="Path for the output trace JSONL file.",
    )
    parser.add_argument(
        "--workflow-version",
        default="baseline-v0",
        help="Workflow version label stored in each trace.",
    )
    args = parser.parse_args(argv)

    traces = run_baseline_jsonl(args.tasks, args.output, args.workflow_version)
    print(f"Wrote {len(traces)} traces to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
