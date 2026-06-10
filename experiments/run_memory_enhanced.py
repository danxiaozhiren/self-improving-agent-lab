from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from self_improving_agent_lab.comparison import (
    compare_trace_scores,
    render_comparison_report,
    write_comparison_report,
)
from self_improving_agent_lab.experiment_runner import run_baseline_jsonl
from self_improving_agent_lab.memory_runner import run_memory_enhanced_jsonl
from self_improving_agent_lab.reflection import load_trace_dicts_jsonl


EVAL_TASK_PATH = ROOT / "experiments/tasks/article_summary_eval_v0.jsonl"
MEMORY_PATH = ROOT / "memories/article-summary-reflection-v0.md"
BASELINE_TRACE_PATH = ROOT / "runs/baseline-v0-eval.jsonl"
MEMORY_TRACE_PATH = ROOT / "runs/memory-v0-eval.jsonl"
REPORT_PATH = ROOT / "reports/baseline-vs-memory-v0.md"


def main() -> int:
    run_baseline_jsonl(EVAL_TASK_PATH, BASELINE_TRACE_PATH)
    run_memory_enhanced_jsonl(EVAL_TASK_PATH, MEMORY_PATH, MEMORY_TRACE_PATH)
    comparison = compare_trace_scores(
        load_trace_dicts_jsonl(BASELINE_TRACE_PATH),
        load_trace_dicts_jsonl(MEMORY_TRACE_PATH),
    )
    report_text = render_comparison_report(
        comparison,
        eval_task_path=str(EVAL_TASK_PATH.relative_to(ROOT)),
        baseline_trace_path=str(BASELINE_TRACE_PATH.relative_to(ROOT)),
        memory_trace_path=str(MEMORY_TRACE_PATH.relative_to(ROOT)),
        memory_path=str(MEMORY_PATH.relative_to(ROOT)),
    )
    write_comparison_report(report_text, REPORT_PATH)
    print(f"Wrote comparison report to {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
