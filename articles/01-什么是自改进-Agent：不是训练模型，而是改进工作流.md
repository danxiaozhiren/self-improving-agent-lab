# 什么是自改进 Agent：不是训练模型，而是改进工作流

## 问题

讨论“自改进 Agent”时，最容易混在一起的两件事是：

1. 模型权重有没有被重新训练。
2. Agent 系统下一次做事有没有变好。

这篇文章先采用一个更工程化的定义：在不更新模型权重的前提下，如果系统能把一次任务的执行结果、失败原因和评估信号沉淀下来，并影响下一次任务执行，那么它就在做工作流层面的自改进。

这不是说训练不重要，而是说很多可落地的改进发生在模型之外：任务集、trace、评估器、反思记录、memory、prompt、工具协议和 SOP。

## Source Status

- Official facts: 本文暂不引用厂商官方实现细节。
- Paper claims: 当前实验任务集中使用了 Self-Refine 和 Reflexion 作为待总结对象，但本文不展开复述论文结论。
- Community implementation: 本文暂不基于第三方框架源码下结论。
- Author inference: “自改进可以先落在工作流版本上”是本文的工程判断。
- Local observation: 本仓库已经跑通了固定任务集、baseline trace 和规则型 rubric score。

## 机制解释

一个最小的自改进闭环可以拆成六步：

```text
task -> run -> trace -> evaluate -> reflect -> update workflow/memory -> rerun
```

这里真正值得观察的不是“模型说了什么”，而是每一步有没有留下可比较的证据。

`task` 需要固定，否则前后两次运行无法比较。比如同样是文章总结任务，输入字段至少要稳定包含标题、正文片段、来源状态和总结目标。

`trace` 不是普通日志。普通日志偏向排障，trace 偏向复盘和比较。它应该保存任务输入、工作流版本、关键步骤、最终输出、评分和反思字段。

`evaluate` 是自改进的刹车和仪表盘。没有评估，系统很容易把“写得更长”“看起来更像答案”误认为变好。

`reflect` 不是把整段聊天记录塞进 memory，而是把失败压缩成可复用规则。例如：“下次总结论文方法时，必须区分 paper claims 和 author inference。”

`update` 的对象也不一定是模型。更常见、更容易落地的对象是 prompt、任务拆分方式、工具调用顺序、memory note、rubric 或 SOP。

所以，本项目把“自改进”的第一层定义为：**让工作流版本可以被观察、评分、反思和比较。**

## 最小实验

当前仓库先做了一个很小的 baseline 实验，还没有接真实 LLM。

固定任务集在：

```text
experiments/tasks/article_summary_v0.jsonl
```

里面有 3 个文章总结任务：

- `summary-001`: Self-Refine
- `summary-002`: Reflexion
- `summary-003`: Agent Trace Discipline

运行命令是：

```bash
python3 experiments/run_baseline.py
```

执行链路是：

```text
experiments/tasks/article_summary_v0.jsonl
  -> load_tasks_jsonl()
  -> run_baseline()
  -> evaluate_trace()
  -> runs/baseline-v0.jsonl
```

当前 `run_baseline()` 仍然是占位实现，只返回：

```text
TODO: connect model/tool loop
```

这很刻意。第一步不是假装已经有智能，而是先把可复现任务、结构化 trace 和评分管道搭起来。

## 实验观察

本地测试结果：

```text
python3 -m pytest
9 passed
```

baseline 运行结果：

```text
python3 experiments/run_baseline.py
Wrote 3 traces to /Users/abi/Documents/project/personal/self-improving-agent-lab/runs/baseline-v0.jsonl
```

一条 trace 的核心字段包括：

```json
{
  "task_id": "summary-001",
  "workflow_version": "baseline-v0",
  "input": {
    "title": "Self-Refine",
    "source_status": "paper_claims"
  },
  "steps": [
    {"name": "receive_task"},
    {"name": "evaluate_trace"}
  ],
  "output": "TODO: connect model/tool loop",
  "scores": {
    "format_validity": 0.0,
    "has_mechanism": 1.0,
    "has_takeaway": 0.0,
    "mentions_source_status": 0.0
  },
  "reflection": ""
}
```

这个结果说明两件事。

第一，当前 baseline 明确失败：`format_validity` 是 0，说明占位输出不能算有效答案；`mentions_source_status` 是 0，说明它没有遵守来源标签要求；`has_takeaway` 是 0，说明没有给出工程启发。

第二，当前 evaluator 也暴露了一个局限：`has_mechanism` 得到 1，只是因为占位输出里出现了 `model/tool loop` 这样的关键词。这说明第一版规则评分只能作为粗筛，不能当成最终质量判断。

这正是自改进实验需要 trace 的原因：我们不仅能看到答案差，也能看到评估器哪里粗糙。

## 工程启发

第一，先固定任务集，再谈改进。没有固定任务集，任何“变好”都只是感觉。

第二，trace shape 要早定下来。后面无论接 LLM、工具调用、reflection memory 还是 judge agent，都应该继续保留 `task_id`、`workflow_version`、`input`、`steps`、`output`、`scores` 和 `reflection`。

第三，rubric 可以先粗糙，但必须可解释。当前规则型 evaluator 明显不完美，不过它能暴露 baseline 的失败，也能暴露自己的误判点。

第四，memory 应该来自失败压缩，而不是来自完整记录堆积。下一步真正有价值的不是“保存更多文本”，而是从失败 trace 中提炼可复用规则。

第五，这个项目的文章应该跟实验交替推进。代码给文章提供观察对象，文章再把观察转成下一轮实验问题。

下一轮实验可以从两个方向继续：

1. 把 baseline 从占位输出升级成一个确定性 summary formatter。
2. 改进 evaluator，让 `has_mechanism` 不再只靠单个关键词命中。

这篇文章的结论很朴素：**自改进 Agent 的第一步不是让模型变聪明，而是让系统知道自己上一次哪里做得不好。**
