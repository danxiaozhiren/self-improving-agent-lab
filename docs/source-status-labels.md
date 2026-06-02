# Source Status Labels

Use source labels in every article and experiment note. The goal is to avoid presenting inference as confirmed implementation detail.

## Labels

### Official facts

Use for vendor docs, official blog posts, SDK documentation, product pages, and release notes.

Example:

```text
Source status: official facts
```

### Paper claims

Use for methods, experiments, and conclusions reported by a paper.

Example:

```text
Source status: paper claims
```

### Community implementation

Use for third-party repos, teaching projects, examples, or framework code that is not an official vendor implementation.

Example:

```text
Source status: community implementation
```

### Author inference

Use for synthesis, interpretation, likely architecture, or engineering judgment based on multiple sources.

Example:

```text
Source status: author inference
```

### Local observation

Use for behavior observed in this repository's experiments.

Example:

```text
Source status: local observation
```

## Article Template

```text
# Title

## Problem

## Source Status

- Official facts:
- Paper claims:
- Community implementation:
- Author inference:
- Local observation:

## Mechanism

## Minimal Experiment

## Common Misunderstandings

## Engineering Takeaways
```
