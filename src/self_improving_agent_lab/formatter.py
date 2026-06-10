from __future__ import annotations

from collections.abc import Sequence

from self_improving_agent_lab.runner import Task


def format_article_summary(task: Task, memory_rules: Sequence[str] = ()) -> str:
    title = str(task.input.get("title", "Untitled article")).strip()
    source_status = str(task.input.get("source_status", "unknown")).strip()
    article_excerpt = str(task.input.get("article_excerpt", "")).strip()
    summary_goal = str(task.input.get("summary_goal", "Summarize the mechanism and engineering implication.")).strip()

    mechanism_basis = article_excerpt or "No article excerpt was provided."
    summary_goal_sentence = summary_goal.rstrip(".。")
    memory_rule = f" Memory rule applied: {memory_rules[0]}" if memory_rules else ""

    return "\n".join(
        [
            f"Source status: {source_status}.",
            f"Summary: {title} - {mechanism_basis}",
            (
                "Mechanism: The useful part for this workflow is to identify the loop, "
                "feedback, trace, and memory signals that can be compared across runs."
            ),
            (
                "Engineering takeaway: the next step should preserve a clear rule for "
                f"source labels while answering the task goal: {summary_goal_sentence}.{memory_rule}"
            ),
        ]
    )
