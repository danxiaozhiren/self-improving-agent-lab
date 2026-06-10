from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from self_improving_agent_lab.evaluator import evaluate_trace
from self_improving_agent_lab.experiment_runner import load_tasks_jsonl, write_traces_jsonl
from self_improving_agent_lab.formatter import format_article_summary
from self_improving_agent_lab.runner import RunTrace, Task


def extract_memory_rules(memory_text: str) -> list[str]:
    rules: list[str] = []
    in_rules = False
    for line in memory_text.splitlines():
        stripped = line.strip()
        if stripped == "## Memory Rules":
            in_rules = True
            continue
        if in_rules and stripped.startswith("## "):
            break
        if in_rules and stripped.startswith("- "):
            rules.append(stripped[2:].strip())
    return rules


def run_memory_enhanced(
    task: Task,
    memory_text: str,
    workflow_version: str = "memory-v0",
) -> RunTrace:
    rules = extract_memory_rules(memory_text)
    trace = RunTrace.start(task, workflow_version)
    trace.add_step("receive_task", kind=task.kind, input_keys=sorted(task.input.keys()))
    trace.add_step("load_reflection_memory", rule_count=len(rules), source_status="local observation")
    if task.kind == "article_summary":
        trace.output = format_article_summary(task, memory_rules=rules)
        trace.add_step("format_article_summary", strategy="deterministic-memory-v0")
    else:
        trace.output = f"TODO: unsupported task kind {task.kind}"
    trace.scores = evaluate_trace(trace)
    trace.add_step("evaluate_trace", rubric_keys=sorted(trace.scores.keys()))
    return trace


def run_memory_enhanced_tasks(
    tasks: Iterable[Task],
    memory_text: str,
    workflow_version: str = "memory-v0",
) -> list[RunTrace]:
    return [run_memory_enhanced(task, memory_text, workflow_version=workflow_version) for task in tasks]


def run_memory_enhanced_jsonl(
    task_path: Path,
    memory_path: Path,
    output_path: Path,
    workflow_version: str = "memory-v0",
) -> list[RunTrace]:
    traces = run_memory_enhanced_tasks(
        load_tasks_jsonl(task_path),
        memory_path.read_text(encoding="utf-8"),
        workflow_version=workflow_version,
    )
    write_traces_jsonl(traces, output_path)
    return traces
