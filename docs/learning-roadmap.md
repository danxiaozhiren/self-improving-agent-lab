# Learning Roadmap

## Phase 1: Minimal Agent Loop

Goal: understand an agent as a loop, not a single prompt.

First experiment scope: article summary only. Technical-route analysis should wait until the summary loop has stable tasks, trace shape, and evaluator behavior.

Read and build:

- Minimal loop: model call, tool request, tool execution, tool result, next model call.
- Trace format: task input, steps, tool calls, result, final answer, errors.
- Failure modes: missing context, bad tool choice, weak stopping condition, invalid output format.

Article idea: Agent is a runtime loop, not just prompt engineering.

## Phase 2: Self-Feedback and Reflection

Goal: understand test-time improvement.

References:

- Self-Refine: iterative refinement with self-feedback.
- Reflexion: verbal reinforcement through reflection notes.

Build:

- Baseline task runner.
- Feedback generator.
- Reflection note format.
- Second-run comparison.

Article idea: What does an agent actually learn when it cannot update model weights?

## Phase 3: Memory and Dreaming

Goal: treat memory as a managed asset, not chat history.

References:

- Voyager: skill library and long-term exploration memory.
- Claude Dreaming: session-based memory refinement.
- Long-term memory surveys for agent systems.

Build:

- Memory store.
- Memory versioning.
- Dreaming job: merge duplicate notes, drop stale notes, extract reusable rules.

Article idea: Memory is not transcript storage; it is distilled operational experience.

## Phase 4: Evaluation

Goal: make improvement measurable.

References:

- Agent-as-a-Judge.
- LLM-as-judge practices.
- OpenAI agent evals and tracing docs.

Build:

- Rubric evaluator.
- Rule-based checks.
- Judge-agent comparison.
- Score history by workflow version.

Article idea: No eval, no self-improvement.

## Phase 5: Multi-Agent SOP

Goal: separate collaboration structure from agent count.

References:

- MetaGPT.
- AutoGen, CrewAI, and LangGraph as framework comparisons.

Build:

- Researcher agent.
- Critic/evaluator agent.
- Editor agent.
- Shared artifacts and handoff rules.

Article idea: Multi-agent value comes from roles, handoffs, and intermediate artifacts.

## Phase 6: Workflow Optimization

Goal: optimize prompts and workflows as versioned systems.

References:

- DSPy.
- GPTSwarm.
- AFlow.
- AlphaEvolve as a frontier reference.

Build:

- Prompt/workflow version registry.
- Score comparison table.
- Simple prompt search or rule mutation.

Article idea: The unit of optimization is the workflow, not only the prompt.
