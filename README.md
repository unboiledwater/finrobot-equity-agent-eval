# 金融 Agent 研究结论可信度审计 Benchmark

### Public Financial Agent Output Audit Benchmark

大模型天然能够生成结构完整、语言流畅、看起来像研报的金融报告。但金融研究的可信度不取决于文本外观，而取决于一条更严格的研究链条：事实是否可核验，计算是否可复算，建模假设是否可追踪，推断是否越过证据，以及最终结论是否保留风险与反证。

本项目面向公开可获取的金融 Agent 输出，建立 claim-level、evidence-gated 的审计框架，评估 AI 生成研究内容是否具有可复核的 evidence-to-decision chain。

> 当前已完成 FinRobot 官方公开输出中的两个局部案例：NVDA 为深审 pilot case，MSFT 为轻量迁移验证案例。当前结果仅覆盖选定 claims，不代表整份报告审计完成，不代表 FinRobot 系统整体可靠性，也不代表跨系统比较已经完成。

## 快速查看

- **项目当前状态总览**：[benchmark_status_summary.md](reports/audit_outputs/benchmark_status_summary.md)
- **NVDA 深审案例**：[nvda_partial_audit.md](reports/audit_outputs/official_report_audits/nvda_partial_audit.md) / [HTML case report artifact](reports/audit_outputs/official_report_audits/nvda_partial_audit_case_report.html)
- **MSFT 轻量迁移验证摘要**：[msft_breadth_audit_summary.md](reports/audit_outputs/msft_breadth_audit_summary.md)
- **Case 03 范围设计**：[evaluation_ladder_and_case03_scope.md](docs/evaluation_ladder_and_case03_scope.md)

注：GitHub 普通文件链接通常显示 HTML 源码；上述 NVDA HTML 仅作为 case report artifact，不等同于已部署在线页面。

## 为什么不是评估“报告写得像不像”

大模型擅长模仿研究报告的语言、结构和页面呈现，因此文本流畅、格式完整或结论像分析师报告，不能证明其真正具备研究能力。

本项目关注以下问题：

| 研究链条层级 | 金融 Agent 需要经受的检查 | 当前覆盖状态 |
| --- | --- | --- |
| 历史事实 | 营收、费用、现金流、公告事项是否能够回溯至正式披露 | NVDA / MSFT 已初步覆盖 |
| 派生计算 | 增长率、利润率、EBITDA margin、CAGR 是否口径闭合并可复算 | NVDA 已暴露相关问题 |
| 建模与估值 | Forward P/E、EV/EBITDA、DCF 假设与敏感性是否绑定日期、输入与预测来源 | 当前已识别缺口，尚未形成完整建模审计案例 |
| 研究推断 | 竞争优势、增长驱动、行业格局与风险判断是否超过证据支持范围 | 当前仅初步覆盖 |
| 决策综合 | 在多 Agent 工作流中，分歧、反证和风险是否进入最终结论 | 计划由 Case 03 扩展 |

## Evidence-to-Decision Chain

```text
Primary Evidence / Dated Data
        ↓
Reported Facts
        ↓
Derived Metrics
        ↓
Modeling Assumptions & Valuation
        ↓
Research Inference and Counter-Evidence
        ↓
Final Recommendation / Decision Synthesis
```

本项目的评价原则是：上游证据或口径未闭合时，下游结论不得自动获得支持；对于预测、估值、风险判断和最终建议，必须保留来源、假设、不确定性与反方证据。

## 已完成案例

| 案例 | 当前审计范围 | 已验证内容 | 暴露出的关键问题 |
| --- | --- | --- | --- |
| **NVDA / FinRobot** | `Investment Overview` 中已映射 claims 的 partial deep pilot audit | 3 条 eligible L2 claims 中，2 条严格支持，1 条为带展示精度提示的支持；3/3 未被一手来源反驳 | 数值展示精度未说明、EBITDA 口径未闭合、估值依据缺少可追溯时点、数字事实不能自动支持经营叙事 |
| **MSFT / FinRobot** | 选定 4 条 claims 的 partial breadth validation | 2 条 L2 strictly supported，2 条进入 H1/backlog | 证明协议可迁移到第二份公开报告，同时显示前瞻或叙事主张不能强行纳入确定性评分 |

META、TSLA 与 COP 目前仅为已登记候选报告，尚未进入 claim-level 审计，不计入当前 findings。

## 当前最重要的发现

| 发现 | 案例依据 | 对金融 Agent Harness 的意义 |
| --- | --- | --- |
| **数字未被反驳，不等于报告已经可审计** | NVDA 的 eligible claims 在外部核验后成立，但报告自身 traceability 仍弱 | 生成层应为关键结论绑定来源文件、期间与计算依据 |
| **数值展示方式也会影响研究可复现性** | NVDA B01 存在 presentation / truncation caveat | 报告应明确数值展示精度与截断/舍入口径 |
| **派生指标不能脱离定义与 reconciliation** | NVDA B05/B06 未进入确定性评分 | EBITDA、adjusted margin 等指标应强制披露定义和输入 |
| **估值和未来判断比历史数字更需要证据门控** | NVDA backlog 与 MSFT H1/backlog | Forward valuation、增长叙事与风险判断需绑定日期来源、假设和人工复核 |
| **当前项目只是研究链条审计的起点** | NVDA/MSFT 主要覆盖事实与派生指标层 | 后续需要扩展至建模假设、反方证据与最终决策综合 |

## 数据来源边界

专业金融研究的增量价值可能来自授权数据库、合规调研、内部研究材料与独立建模；本项目当前并不声称已经接入这些非公开或授权数据环境。

在当前 output-audit 阶段：

- 对已发生的历史财务事实，以 SEC / 公司官方披露等 primary evidence 作为核验基准；
- 对估值、预测和市场敏感指标，要求可重建的日期、输入与来源；
- 对产业判断、调研观点和最终投资结论，若无法闭合证据链，则不进入确定性评分；
- 对未来企业级部署中的授权数据库、私有数据权限与合规控制，仅作为待扩展的 harness 维度，不声称已经实现。

## 下一阶段：从报告事实核验到 Evidence-to-Decision Chain Audit

当前 NVDA 与 MSFT 案例建立了 facts / derived metrics 层的初步审计协议。下一阶段拟选择官方可固定的多 Agent 金融输出样本，检查：

- 上游 Agent 使用的事实和预测是否可核验；
- Bull / Bear 等不同角色是否基于清晰证据提出分歧；
- 风险意见是否在最终结论中被保留；
- 最终决策是否遗漏反证或将不确定叙事包装成确定建议。

候选 Case 03：`TradingAgents AAPL Evidence-to-Decision Chain Audit`。该案例当前仅处于 scope-design 阶段，尚未进入正式 claim extraction、evidence mapping 或 scoring。

## 当前不声称的内容

本项目目前不声称：

- 已完成 FinRobot 五份官方报告的审计；
- 已完成 NVDA 或 MSFT 整份报告的审计；
- 已全面评价 FinRobot 系统的金融研究能力；
- 已完成跨系统对比；
- 已正式审计 TradingAgents 或 AlphaEngine 输出；
- 已评价 Agent 的隐藏 trace、工具调用过程或运行成本；
- 已接入 Bloomberg、Wind、iFinD、CSMAR 或客户私有数据库；
- 已评价基于私有调研数据的研究能力；
- 已实现生产级权限、脱敏、多租户或审计日志控制；
- 当前结果可以构成投资建议。

## 主要产物

| Artifact | Purpose |
| --- | --- |
| [reports/audit_outputs/benchmark_status_summary.md](reports/audit_outputs/benchmark_status_summary.md) | 当前项目状态与边界总览 |
| [reports/audit_outputs/official_report_audits/nvda_partial_audit.md](reports/audit_outputs/official_report_audits/nvda_partial_audit.md) | NVDA canonical audit narrative |
| [reports/audit_outputs/msft_breadth_audit_summary.md](reports/audit_outputs/msft_breadth_audit_summary.md) | MSFT lightweight breadth-validation summary |
| [evidence/nvda/verified_claims.json](evidence/nvda/verified_claims.json) | NVDA claim-level evidence records |
| [evidence/msft/verified_claims.json](evidence/msft/verified_claims.json) | MSFT claim-level evidence records |
| [benchmark/scoring_rules.json](benchmark/scoring_rules.json) | Eligibility、scoring 与 downgrade 规则 |
| [reports/audit_outputs/official_report_audits/nvda_partial_audit_case_report.html](reports/audit_outputs/official_report_audits/nvda_partial_audit_case_report.html) | NVDA HTML case report artifact；GitHub 普通文件链接通常显示 HTML 源码，不等同于已部署在线页面 |

## 说明

本项目不是投资建议，不评价 NVDA / MSFT 的投资价值；它关注的是金融 Agent 输出在专业场景中是否具备可核验、可审计、可复盘的 evidence-to-decision chain。
