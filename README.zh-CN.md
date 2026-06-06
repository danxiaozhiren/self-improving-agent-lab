# self-improving-agent-lab

[English](README.md) | [中文](README.zh-CN.md)

用于学习和实验自改进 AI Agent 的笔记与小型实验仓库。

本仓库研究 Agent 系统如何在不重新训练模型权重的情况下持续改进。实践闭环是：

1. 运行一个任务。
2. 保存执行轨迹和结果。
3. 用测试、评分 rubric 或 judge agent 评估结果。
4. 反思失败原因。
5. 更新 memory、prompt、SOP 或 workflow 版本。
6. 重新运行并对比结果。

## 范围

第一个目标是搭建一个小型 research-assistant lab，并且第一阶段只做文章总结。技术路线分析先后置，等文章总结闭环具备可信 rubric、固定任务集、trace 格式和 baseline 对比之后再扩展。实现会保持足够简单，便于检查：Python、JSONL/SQLite、Markdown 笔记和可复现的任务集。

## 仓库结构

```text
articles/      基于实验和来源笔记沉淀的中文文章系列。
docs/          阅读路线、来源标签和文章提纲。
experiments/   小型可运行实验和结果日志。
src/           Agent loop 组件的最小 Python 包。
tests/         回归测试和评估夹具。
```

## 第一批里程碑

- [x] 构建固定任务集，用于文章总结。
- [x] 将每次运行保存为结构化 trace。
- [x] 将文章总结 rubric 具体化到每个分数都能解释。
- [x] 将占位 baseline 替换成确定性 summary formatter。
- [ ] 从失败案例生成 reflection notes。
- [ ] 用版本历史保存 memory notes。
- [ ] 在 held-out 文章总结任务上对比 baseline 和 memory-enhanced runs。

## 来源状态标签

写笔记时，需要清楚区分这些类别：

- Official facts：厂商文档、官方博客、API references。
- Paper claims：论文报告的方法、实验和结论。
- Community implementation：第三方仓库、教学项目或示例代码。
- Author inference：我的解释、综合判断或推理。
- Local observation：本仓库实验中观察到的行为。
