from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Task:
    """A repeatable unit of work for an agent workflow."""

    task_id: str
    kind: str
    input: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Task":
        missing_keys = {"task_id", "kind", "input"} - payload.keys()
        if missing_keys:
            missing = ", ".join(sorted(missing_keys))
            raise ValueError(f"Task payload is missing required keys: {missing}")
        if not isinstance(payload["input"], dict):
            raise ValueError("Task input must be a JSON object")
        return cls(
            task_id=str(payload["task_id"]),
            kind=str(payload["kind"]),
            input=dict(payload["input"]),
        )


@dataclass
class TraceStep:
    """One observable step in an agent run."""

    name: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "payload": dict(self.payload),
        }


@dataclass
class RunTrace:
    """Structured trace for comparing workflow versions."""

    task_id: str
    workflow_version: str
    started_at: str
    input: dict[str, Any] = field(default_factory=dict)
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
            input=dict(task.input),
        )

    def add_step(self, name: str, **payload: Any) -> None:
        self.steps.append(TraceStep(name=name, payload=payload))

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "workflow_version": self.workflow_version,
            "started_at": self.started_at,
            "input": dict(self.input),
            "steps": [step.to_dict() for step in self.steps],
            "output": self.output,
            "scores": dict(self.scores),
            "reflection": self.reflection,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)


def run_baseline(task: Task, workflow_version: str = "baseline-v0") -> RunTrace:
    """Run a deterministic placeholder workflow.

    This intentionally avoids any model SDK. The first implementation step is to
    replace this placeholder with a real model/tool loop while preserving trace
    shape.
    """

    trace = RunTrace.start(task, workflow_version)
    trace.add_step("receive_task", kind=task.kind, input_keys=sorted(task.input.keys()))
    trace.output = "TODO: connect model/tool loop"
    return trace
