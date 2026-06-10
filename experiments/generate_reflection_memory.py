from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from self_improving_agent_lab.experiment_runner import run_baseline_jsonl
from self_improving_agent_lab.reflection import (
    generate_reflection_memory,
    load_trace_dicts_jsonl,
    write_reflection_memory,
)


TRAIN_TASK_PATH = ROOT / "experiments/tasks/article_summary_train_v0.jsonl"
TRAIN_TRACE_PATH = ROOT / "runs/baseline-v0-train.jsonl"
MEMORY_OUTPUT_PATH = ROOT / "memories/article-summary-reflection-v0.md"


def main() -> int:
    run_baseline_jsonl(TRAIN_TASK_PATH, TRAIN_TRACE_PATH)
    memory_text = generate_reflection_memory(
        load_trace_dicts_jsonl(TRAIN_TRACE_PATH),
        train_task_path=str(TRAIN_TASK_PATH.relative_to(ROOT)),
        trace_path=str(TRAIN_TRACE_PATH.relative_to(ROOT)),
    )
    write_reflection_memory(memory_text, MEMORY_OUTPUT_PATH)
    print(f"Wrote reflection memory to {MEMORY_OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
