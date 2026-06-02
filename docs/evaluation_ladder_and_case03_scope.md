# Evaluation Ladder and Case 03 Scope — Evidence-to-Decision Chain Audit

## Why the Benchmark Must Go Beyond Report Appearance

LLM systems are naturally strong at producing financial-report-shaped text: coherent language, familiar section structures, polished conclusions, and presentation patterns that resemble analyst research.

This benchmark does not evaluate writing style or whether an output looks like a professional report. It evaluates whether the research reliability chain is auditable: facts must be traceable, derived metrics must be reproducible, assumptions must be dated and sourced, reasoning must remain bounded by evidence, and final decisions must preserve uncertainty and counter-evidence.

The current NVDA and MSFT cases establish the initial foundation at the facts and derived metrics layers. Future extensions must move deeper into modeling, research reasoning, and decision synthesis.

## Evaluation Ladder

| Level | Evaluation Target | Core Question | Current Coverage |
| --- | --- | --- | --- |
| L1 — Reported Facts | 财务数字、正式事件、期间与单位 | 报告中的事实能否回溯至 primary evidence？ | NVDA / MSFT 初步覆盖 |
| L2 — Derived Metrics | 增长率、利润率、EBITDA、CAGR 等 | 指标定义与计算输入是否闭合、可复算？ | NVDA 初步覆盖 |
| L3 — Modeling & Assumptions | DCF、peer valuation、forward multiples、预测 | 假设、时点、来源和敏感性是否可重建？ | 已识别缺口，尚未完成专门案例 |
| L4 — Research Reasoning | 竞争优势、产业判断、增长驱动、风险叙事 | 推断是否受到证据与反证约束？ | 初步触及，待扩展 |
| L5 — Decision Synthesis | 多 Agent 分歧、风险传播、最终决策 | 最终结论是否保留关键反证与不确定性？ | 拟由 Case 03 覆盖 |

## Current Cases Mapping

| Case | Artifact | Covered Levels | Status |
| --- | --- | --- | --- |
| Case 01 | FinRobot NVDA public report | L1 / L2，初步涉及 L4 boundary | Completed partial pilot audit |
| Case 02 | FinRobot MSFT public report | L1 / L2，部分 H1 escalation | Completed partial breadth validation |
| Case 03 | TradingAgents AAPL official appendix outputs | Planned L1 / L4 / L5 | Scope defined only; not yet audited |
| Deferred Candidate | AlphaEngine AppLovin public article | Potential L3 / L4 strategic-transaction scenario | Deferred; raw Agent artifact not confirmed |

## Why TradingAgents AAPL Is Selected for Case 03

TradingAgents 官方论文附录提供了 AAPL 多 Agent 示例输出。该样本包含 analyst / bull / bear / risk / fund manager 等角色链条，因此能够把当前 benchmark 从事实与派生指标核验，扩展到多 Agent 分歧、风险传播与最终决策汇总评价。

Case 03 拟新增的不是对报告外观的评价，而是对 evidence-to-decision chain 的检查：上游事实与预测是否可追溯，不同角色的分歧是否由清晰证据支撑，风险意见是否进入最终结论，以及 fund manager recommendation 是否保留关键不确定性。

目前仅确认官方附录中公开的示例输出，不声称拥有 TradingAgents 内部完整 trace、工具调用记录、私有运行日志或生产环境数据。本文件仅定义 scope，不启动审计，不抽取 claims，不进行 evidence mapping，也不产生 scoring judgment。

## Why AlphaEngine AppLovin Is Deferred

AlphaEngine / FinGPT Agent 与 Kimi 金融场景高度相关。月之暗面官方平台公开展示了 AlphaEngine 集成 Kimi K2 Thinking，用于研报、财务数据、产业链与深度报告处理，因此它适合作为后续金融 Agent 研究链条评估的相关候选方向。

但当前发现的 AppLovin 公开全文属于 Agent-assisted 且经公开发布流程编辑的文章。在无法确认原始 AlphaEngine artifact 前，本项目不将其作为正式 scored case，不审计 AppLovin，不登记 AlphaEngine evidence records，也不声称已经取得 Kimi 原始 Agent 输出、AlphaEngine 内部数据、工具或 trace。

AlphaEngine AppLovin 可保留为未来 strategic transaction / industry reasoning scenario candidate，尤其适合在后续取得可固定、可追溯的原始 Agent artifact 后，用于检验产业判断、交易叙事、建模假设与风险约束。

## Planned Research Question

Can a multi-agent financial workflow preserve a verifiable evidence-to-decision chain from upstream factual analysis and conflicting researcher views to downstream risk handling and final fund-manager recommendation?

拟检验的问题是：在多 Agent 金融决策工作流中，上游事实、看多/看空分歧与风险意见，是否能够被最终决策准确保留并追溯；还是会被压缩为缺乏证据边界的单一投资建议。
