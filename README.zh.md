# AI 生成股票研究报告的 Report Audit Benchmark

本项目面向真实 AI 生成的股票研究报告开展 claim-level 证据核验、确定性评分与可审计错误分析。

FinRobot 官方报告是被审查对象，而非事实来源。上市公司公开披露材料、监管文件、投资者材料与可复核的带日期市场数据构成验证依据。

## V1 范围

V1 是 **Report Audit Benchmark**。它不依赖本地重新跑通 FinRobot，也不声称 Evidence-Gated generation workflow 已经改善报告生成质量。

| 问题 | V1 回答 |
| --- | --- |
| 审查什么？ | AI 生成股票研究报告中的可核验 claims。 |
| 审查谁？ | FinRobot 官方 5 份 equity reports：NVDA、MSFT、META、TSLA、COP。 |
| 事实依据是什么？ | 上市公司公开披露、SEC 文件、年报、业绩材料、投资者演示和可复核市场数据。 |
| 输出什么？ | report inventory、claim-level tasks、scoring rules、error inventory、benchmark mapping、audit reports。 |
| 当前阶段是什么？ | V1 审查官方报告；本地 fresh-run 只是补充样本；V2 baseline vs evidence-gated generation comparison 单独规划。 |

## 为什么做这个项目

金融报告文本流畅并不等于可靠。专业场景真正需要核验的是：

- claim 是否保留了原报告的表述和边界；
- 数字、单位、期间和计算是否正确；
- 验证来源在报告生成时点是否已经可获得；
- 报告自身是否提供足够 citation 供独立复核；
- 表述属于披露事实、计算结果、分析推断，还是需要人工复核的判断。

本项目把这些问题转化为可复用的评测资产，而不是只做主观报告质量评价。

## 被审查材料

被审查材料分为三层：

| 样本层级 | 作用 |
| --- | --- |
| Core Audit Set | 五份 FinRobot 官方报告，构成 V1 benchmark 主样本。 |
| Supplementary Fresh-Run Set | 本地生成的 FinRobot 报告，必须有运行 provenance，只用于测试协议迁移性。 |
| Planned Comparative Set | 未来 V2 的 baseline vs evidence-gated generation 输出。 |

五份 FinRobot 官方 HTML 报告存放在 `reports/source/official_examples/`：

- `reports/source/official_examples/finrobot_official_nvda.html`
- `reports/source/official_examples/finrobot_official_msft.html`
- `reports/source/official_examples/finrobot_official_meta.html`
- `reports/source/official_examples/finrobot_official_tsla.html`
- `reports/source/official_examples/finrobot_official_cop.html`

五份报告结构一致，包含 Investment Thesis、Company Overview、Financial Analysis、Valuation Analysis、Recent News & Events、Sensitivity Analysis、Key Catalysts、Technical & Advanced Analysis、Competitive Landscape 和 Financial Data。

报告页脚只有泛化来源，例如 `Company Filings, FMP, Yahoo Finance, AI4Finance Estimates`。该页脚不等同于逐条 claim citation。

如果生成本地 fresh-run 报告，产物放在 `reports/local_runs/`，并且进入补充审查前必须有 manifest。它不替代官方报告主样本，也不能用来声称 FinRobot 随时间改进或退步。

## 方法论

V1 要确保审查对象始终绑定原始报告文本：

- `report_excerpt`：完整原文片段；
- `claim_quote`：从原文直接截取的最小可核验短语；
- `normalized_claim`：仅为核验做最小规范化；
- `extraction_note`：说明任何拆分、补全或规范化理由。

Benchmark 区分三个审查维度：

- `substantive_accuracy`：内容本身是 supported、contradicted、unsupported，还是 needs human review；
- `report_level_traceability`：报告自身是否提供足够 citation 信息；
- `evaluator_assisted_verifiability`：审查者是否能用公开来源重建证据路径。

这种区分很重要：历史财务数字可能内容正确，但报告层面的引用可追溯性仍然很弱。

## 评分层级

Deterministic scoring 表示规则固定、结果可复核，不等于所有步骤都已经完全自动化。

| 层级 | 含义 | V1 用途 |
| --- | --- | --- |
| `L1_automated` | 脚本可直接判定结构化值。 | 标准化数字字段和简单一致性检查。 |
| `L2_semi_automated` | 脚本复算或比较，reviewer 确认来源与口径。 | 大多数财务数字、百分比、margin、multiple。 |
| `L3_rule_based_manual` | reviewer 按固定规则核验并记录证据。 | 期间对齐、来源时点、复杂披露匹配。 |
| `H1_human_review` | 保留复核判断，但不进入 deterministic accuracy。 | peer 合理性、风险重大性、推断过度、投资逻辑支撑度。 |

引用弱或缺失的 claim 是否进入 L1/L2 取决于 claim 类型。市场价格、市值、forward multiple、consensus、目标价、peer comparison 和前瞻性结论必须有带日期且可复核的来源，才能进入确定性评分。

## 单 Reviewer 边界

V1 不声称已经验证 inter-reviewer agreement。单 reviewer 阶段遇到的模糊判断会记录在 `pilot/ambiguity_log.md`，作为后续 reviewer 校准材料。

歧义日志记录 segmentation、normalization、source alignment、tolerance、judgment 和 scoring level 等争议点，避免不确定判断只停留在备注里。

## 目录结构

```text
reports/source/official_examples/      被审查的 FinRobot 官方报告
reports/local_runs/metadata/           本地 fresh-run manifest 与 schema
reports/local_runs/outputs/            本地生成的补充报告
reports/report_inventory.json          报告来源、日期、章节和候选 claim 密度
benchmark/taxonomy.md                  claim 类型、切分规则、判定标签和错误类型
benchmark/scoring_rules.json           评分层级、traceability gate 和容差规则
benchmark/report_audit_tasks.json      V1 claim-level benchmark tasks
pilot/                                 NVDA segmentation pilot 与 ambiguity log
evidence/                              按 ticker 存放一手来源映射和 verified claims
reports/audit_outputs/official_report_audits/          官方报告审查输出
reports/audit_outputs/local_run_supplementary_audits/  本地 fresh-run 补充审查输出
planned_v2/                            baseline vs evidence-gated generation 实验计划
```

## 当前实现边界

V1 不声称：

- 本地 FinRobot 生成链路是 audit benchmark 的前提；
- 本地 fresh-run 替代官方报告主样本；
- 本地 fresh-run 证明 FinRobot 随时间改进或退步；
- Evidence Gate 已经改善了生成报告质量；
- 已拿到 FinRobot 内部生成 trace；
- 已实现 tenant isolation、permission-scope injection、redaction 或 production audit logging。

Enterprise controls 只作为扩展设计，除非后续加入可运行测试。本地生成中使用的 FMP 数据只代表输入 provenance，不是最终事实标准。

## 当前产物

当前已完成的产物状态：

- NVDA partial audit 状态：`partial audit / in progress`。
- 覆盖范围：仅 `Investment Overview` 章节。
- 正式评分 claims：3 个 L2 tasks。
- 排除或待补证据 claims：5 个 documented cases。
- Canonical Markdown 审查产物：`reports/audit_outputs/official_report_audits/nvda_partial_audit.md`。
- 面向人类阅读的 HTML 展示层：`reports/audit_outputs/official_report_audits/nvda_partial_audit.html`。
- 结构化 evidence map：`evidence/nvda/verified_claims.json`。
- 校验脚本：`scripts/validate_nvda_partial_audit.py`。

当前 NVDA 产物不代表完整 NVDA 报告审查，也不代表 FinRobot 整体可靠性结论。

## V2 规划

V2 会在生成链路稳定且输出可保存之后，再比较 baseline generation 与 evidence-gated generation workflow。在真实结果产生前，V2 不作为已完成结论展示。
