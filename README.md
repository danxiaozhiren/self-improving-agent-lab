# self-improving-agent-lab

[English](README.md) | [中文](README.zh-CN.md)

Learning notes and small experiments for self-improving AI agents.

This repository studies how agent systems can improve without retraining model weights. The practical loop is:

1. Run a task.
2. Save the trace and result.
3. Evaluate the result with tests, rubrics, or a judge agent.
4. Reflect on failures.
5. Update memory, prompts, SOPs, or workflow versions.
6. Re-run and compare.

## Scope

The first target is a small research-assistant lab for article summarization only. Technical-route analysis is intentionally postponed until the article-summary loop has a credible rubric, fixed task set, trace format, and baseline comparison. The implementation will stay simple enough to inspect: Python, JSONL/SQLite, Markdown notes, and reproducible task sets.

## Repository Layout

```text
articles/      Chinese article series based on experiments and source notes.
docs/          Reading roadmap, source labels, and article outlines.
experiments/   Small runnable experiments and result logs.
src/           Minimal Python package for agent-loop components.
tests/         Regression tests and evaluation fixtures.
```

## First Milestones

- [x] Build a fixed task set for article summary.
- [x] Save each run as a structured trace.
- [x] Make the article-summary rubric concrete enough to explain each score.
- [x] Replace the placeholder baseline with a deterministic summary formatter.
- [x] Generate a train-only reflection memory artifact.
- [x] Store memory notes with version history.
- [ ] Generate reflection notes from actual low-score failure cases.
- [x] Compare baseline vs memory-enhanced runs on held-out article-summary tasks.
- [ ] Produce a memory-enhanced run with a defensible held-out improvement.

## Source Status Labels

When writing notes, separate these categories clearly:

- Official facts: vendor docs, official blog posts, API references.
- Paper claims: methods and results reported by papers.
- Community implementation: third-party repos or teaching projects.
- Author inference: my interpretation or synthesis.
- Local observation: behavior observed in this repo's experiments.
