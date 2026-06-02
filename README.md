# 金融 Agent 生成报告可信度审计 Benchmark

### Public Financial Agent Output Audit Benchmark

本项目评估公开金融 Agent 生成的投研报告是否真正可信、可复核：财务数字是否准确，派生指标是否有明确口径，估值结论是否绑定时点来源，以及分析叙事是否越过证据边界。

当前已完成两份 FinRobot 官方公开报告中选定 claims 的审计：**NVDA** 为深审 pilot case，**MSFT** 为轻量迁移验证案例。

> 当前结果只覆盖两份公开报告中的选定 claims，不代表整份报告审计完成，不代表 FinRobot 系统整体表现，也不代表跨系统比较已经完成。

## 快速查看

- **NVDA 深审案例 HTML artifact**：[nvda_partial_audit_case_report.html](reports/audit_outputs/official_report_audits/nvda_partial_audit_case_report.html)
  注：GitHub 普通文件链接通常显示 HTML 源码，不等同于已部署在线页面。
- **项目当前状态总览**：[benchmark_status_summary.md](reports/audit_outputs/benchmark_status_summary.md)
- **MSFT 轻量迁移验证摘要**：[msft_breadth_audit_summary.md](reports/audit_outputs/msft_breadth_audit_summary.md)

## 项目在检查什么问题

金融 Agent 的高风险错误，往往不是“写得不像研报”，而是：

| 风险 | 典型表现 | 本项目的处理方式 |
| --- | --- | --- |
| 数字看起来正确，但证据链不可追踪 | 报告写出营收或费用率，却没有对应 filing、期间与计算依据 | 将 claim 映射至 SEC / 公司官方披露 |
| 派生指标口径未闭合 | EBITDA、EBITDA margin 或 CAGR 没有定义与复算输入 | 证据不足时降级，不进入确定性评分 |
| 估值指标缺少时点依据 | Forward P/E 或 EV/EBITDA 没有价格日期、预测来源或分母定义 | 转入待补证据或人工复核 |
| 数字事实被扩张为商业判断 | 某项费用率下降被直接表述为完整经营逻辑成立 | 分离 factual claim 与 inference |

## 已完成案例

| 案例 | 审计范围 | 当前发现 | 产物 |
| --- | --- | --- | --- |
| **NVDA / FinRobot** | `Investment Overview` 中已完成证据映射的 claims；partial deep pilot audit | 3 条可进入规则判断的 claims 中，2 条得到严格支持，1 条因展示精度/截断口径问题标记为带提示支持；另有 2 条派生指标 claims 被降级、3 条进入 backlog | [HTML artifact](reports/audit_outputs/official_report_audits/nvda_partial_audit_case_report.html) / [Canonical audit](reports/audit_outputs/official_report_audits/nvda_partial_audit.md) / [Evidence records](evidence/nvda/verified_claims.json) |
| **MSFT / FinRobot** | 选定 4 条 claims；partial breadth validation | 2 条可按规则确认，2 条因来源或判断基础不足进入 H1/backlog；用于验证审计协议能够迁移至第二份公开报告 | [Summary](reports/audit_outputs/msft_breadth_audit_summary.md) / [Evidence records](evidence/msft/verified_claims.json) |

已登记但尚未进入 claim-level 审计的候选报告：**META、TSLA、COP**。它们不计入当前 findings，也不构成“五份报告均已审计”。

## 当前最重要的发现

| 发现 | 来自案例 | 对金融 Agent Harness 的意义 |
| --- | --- | --- |
| **数字没有被反驳，不等于报告已经可审计** | NVDA 的可评分 claims 均缺少强 claim-level traceability | 生成层应绑定来源文件、期间与计算依据 |
| **数值展示精度本身也会影响可复现性** | NVDA B01 只能在截断展示口径下接受，不能视为普通四舍五入 | 报告应声明 rounding / truncation 规则 |
| **派生指标必须披露定义** | NVDA B05/B06 的 EBITDA 与 EBITDA margin 无法闭合口径 | Non-GAAP 或 derived metrics 应强制附 definition / reconciliation |
| **估值与叙事 claims 不能被强行纳入确定性评分** | NVDA backlog 与 MSFT H1/backlog | Forward valuation 与业务判断需要带日期来源或人工复核 |

## 审计流程

公开金融 Agent 报告 → 抽取可以单独核验的 claims → 映射 SEC / 公司官方披露等一手来源 → 按规则判断严格支持、带提示支持、降级或转人工复核 → 汇总可转化为金融 Agent Harness 约束的失效模式

| 术语 | 含义 |
| --- | --- |
| Claim | 从 Agent 报告中抽取、可单独核验的一项主张 |
| Strictly Supported | 来源、期间、口径与规则均闭合，可按确定性规则确认 |
| Supported with Presentation Caveat | 核心数值未被反驳，但展示精度或截断方式未被报告说明 |
| Downgraded / Backlog | 证据、指标定义或时点依据尚未闭合，不进入确定性结论 |
| H1 Review | 涉及叙事、估值合理性或风险判断，需要人工复核 |

## 当前边界

本项目目前不声称：

- 已完成 FinRobot 五份官方报告的审计；
- 已完成 NVDA 或 MSFT 整份报告的审计；
- 已经评价 FinRobot 系统整体可靠性；
- 已完成跨系统 comparison；
- 已纳入 AlphaEngine、TradingAgents、FinRpt 等外部系统；
- 已评价 Agent trace、工具调用或多 Agent 协作过程；
- 已实现生产级权限、脱敏、多租户或审计控制。

## 已登记候选样本

| Sample | System | Current Status | Possible Future Purpose |
| --- | --- | --- | --- |
| META | FinRobot | Inventory only | 科技平台 / AI 投入叙事迁移测试 |
| TSLA | FinRobot | Inventory only | 高估值与 reasoning-boundary 测试 |
| COP | FinRobot | Inventory only | 能源行业 sector-transfer 测试 |

未来还可在完成样本准入核验后，引入其他公开金融 Agent 输出，用于扩展产业链研究、战略交易叙事或多 Agent 决策汇总的评测；当前这些方向尚未纳入正式 benchmark。

## 主要产物

| Artifact | Purpose |
| --- | --- |
| [reports/audit_outputs/benchmark_status_summary.md](reports/audit_outputs/benchmark_status_summary.md) | 当前项目状态与边界总览 |
| [reports/audit_outputs/official_report_audits/nvda_partial_audit.md](reports/audit_outputs/official_report_audits/nvda_partial_audit.md) | NVDA canonical audit narrative |
| [reports/audit_outputs/msft_breadth_audit_summary.md](reports/audit_outputs/msft_breadth_audit_summary.md) | MSFT lightweight breadth-validation summary |
| [evidence/nvda/verified_claims.json](evidence/nvda/verified_claims.json) | NVDA claim-level evidence records |
| [evidence/msft/verified_claims.json](evidence/msft/verified_claims.json) | MSFT claim-level evidence records |
| [benchmark/scoring_rules.json](benchmark/scoring_rules.json) | Eligibility、scoring 与 downgrade 规则 |

## 说明

本项目不是投资建议，不评价 NVDA / MSFT 的投资价值；它关注的是金融 Agent 输出在专业场景中是否具备可核验、可审计、可复盘的证据链。
