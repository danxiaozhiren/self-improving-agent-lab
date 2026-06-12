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
    input_evidence = _input_evidence_clause(title, article_excerpt, summary_goal_sentence, memory_rules)
    memory_rule = f" Memory rule applied: {memory_rules[0]}" if memory_rules else ""

    return "\n".join(
        [
            f"Source status: {source_status}.",
            f"Summary: {title} - {mechanism_basis}",
            (
                "Mechanism: The useful part for this workflow is to identify the loop, "
                f"feedback, trace, and memory signals that can be compared across runs.{input_evidence}"
            ),
            (
                "Engineering takeaway: the next step should preserve a clear rule for "
                f"source labels while answering the task goal: {summary_goal_sentence}.{memory_rule}"
            ),
        ]
    )


def _input_evidence_clause(
    title: str,
    article_excerpt: str,
    summary_goal: str,
    memory_rules: Sequence[str],
) -> str:
    if not any("input-specific evidence" in rule.lower() for rule in memory_rules):
        return ""
    evidence = _sentence_fragment(article_excerpt) or "the provided article excerpt contains the key evidence"
    goal = _sentence_fragment(summary_goal) or "the requested summary goal"
    return (
        f" Mechanism detail for {title}: the excerpt shows that {_lower_first(evidence)}. "
        f"This supports the goal by connecting the article-specific claim to {_lower_first(goal)}."
    )


def _sentence_fragment(text: str) -> str:
    return text.strip().rstrip(".。")


def _lower_first(text: str) -> str:
    if not text:
        return text
    return text[:1].lower() + text[1:]
