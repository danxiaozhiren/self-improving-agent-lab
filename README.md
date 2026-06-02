# self-improving-agent-lab

Learning notes and small experiments for self-improving AI agents.

This repository studies how agent systems can improve without retraining model weights. The practical loop is:

1. Run a task.
2. Save the trace and result.
3. Evaluate the result with tests, rubrics, or a judge agent.
4. Reflect on failures.
5. Update memory, prompts, SOPs, or workflow versions.
6. Re-run and compare.

## Scope

The first target is a small research-assistant lab for article summarization and technical-route analysis. It will keep the implementation simple enough to inspect: Python, JSONL/SQLite, Markdown notes, and reproducible task sets.

## Repository Layout

```text
docs/          Reading roadmap, source labels, and article outlines.
experiments/   Small runnable experiments and result logs.
src/           Minimal Python package for agent-loop components.
tests/         Regression tests and evaluation fixtures.
```

## First Milestones

- [ ] Build a fixed task set for article summary and importance judgment.
- [ ] Save each run as a structured trace.
- [ ] Add a rubric-based evaluator.
- [ ] Generate reflection notes from failed cases.
- [ ] Store memory notes with version history.
- [ ] Compare baseline vs memory-enhanced runs.

## Source Status Labels

When writing notes, separate these categories clearly:

- Official facts: vendor docs, official blog posts, API references.
- Paper claims: methods and results reported by papers.
- Community implementation: third-party repos or teaching projects.
- Author inference: my interpretation or synthesis.
- Local observation: behavior observed in this repo's experiments.
