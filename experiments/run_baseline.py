from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from self_improving_agent_lab.experiment_runner import main


if __name__ == "__main__":
    default_args = [
        "--tasks",
        str(ROOT / "experiments/tasks/article_summary_v0.jsonl"),
        "--output",
        str(ROOT / "runs/baseline-v0.jsonl"),
    ]
    raise SystemExit(main(sys.argv[1:] or default_args))
