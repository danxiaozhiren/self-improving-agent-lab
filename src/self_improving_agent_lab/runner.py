from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Task:
    """A repeatable unit of work for an agent workflow."""

    task_id: str
    kind: str
    input: dict[str, Any]


@dataclass
class TraceStep:
    """One observable step in an agent run."""

    name: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class RunTrace:
    """Structured trace for comparing workflow versions."""

    task_id: str
    workflow_version: str
    started_at: str
    steps: list[TraceStep] = field(default_factory=list)
    output: str = ""
    scores: dict[str, float] = field(default_factory=dict)
    reflection: str = ""

    @classmethod
    def start(cls, task: Task, workflow_version: str) -> "RunTrace":
        return cls(
            task_id=task.task_id,
            workflow_version=workflow_version,
            started_at=datetime.now(timezone.utc).isoformat(),
        )

    def add_step(self, name: str, **payload: Any) -> None:
        self.steps.append(TraceStep(name=name, payload=payload))


def run_baseline(task: Task, workflow_version: str = "baseline-v0") -> RunTrace:
    """Run a deterministic placeholder workflow.

    This intentionally avoids any model SDK. The first implementation step is to
    replace this placeholder with a real model/tool loop while preserving trace
    shape.
    """

    trace = RunTrace.start(task, workflow_version)
    trace.add_step("receive_task", kind=task.kind, input_keys=sorted(task.input.keys()))
    trace.output = "TODO: connect model/tool loop"
    trace.scores = {"format_validity": 0.0}
    return trace
