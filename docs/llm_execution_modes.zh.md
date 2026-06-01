# LLM 执行模式

本项目对 FinRobot 和披露材料 Agent Eval 采用分层 LLM 执行策略。

## 为什么需要分层

FinRobot 报告质量高度依赖 LLM 生成的文本章节。禁用 LLM 会丢掉最重要的被测能力之一。

但 benchmark 也必须可复现、可控、可审计。一次报告可能调用多次 LLM，thinking 模型会产生明显的延迟长尾。因此 harness 将连通性测试、正式报告生成和 deterministic scoring 分开。

## 模式

| 模式 | 用途 | Kimi 配置 | 理由 |
|---|---|---|---|
| Smoke test | 验证 API key、base URL 和模型名 | `thinking: disabled`，`temperature=0.6`，较小 `max_tokens` | 快、成本低，不评估报告质量。 |
| 正式报告生成 | 生成 FinRobot 研究报告文本章节 | `thinking: enabled`，`temperature=1.0`，`max_tokens=8192` | 保留 Kimi K2.6 推理能力，同时控制长尾延迟。 |
| Benchmark scoring | 按 deterministic rubric 打分 | 默认不用 LLM | 保持评分可复现、可审计。 |
| 专家复核 | 可选质性评审 | 可用 LLM，但需要人工确认 | 可辅助判断金融写作质量，但不能替代确定性检查。 |

## 观察到的行为

在 NVDA 运行中，Kimi thinking mode 成功生成了报告章节，但部分章节延迟较长。一次批量运行在 `major_takeaways` 处卡住；将该章节单独重试并把 `max_tokens` 设为 8192 后成功完成。

`news_summary.txt` 被有意写成数据可用性说明，因为当前 FMP 套餐限制了 news endpoint。相比编造新闻催化剂，这种处理更适合评测项目。

## Harness 发现

- 某个估值段落引用的 2027 EBITDA 数字与生成的 CSV 表格不一致。
- 上游 FinRobot 的 FMP legacy endpoint 对新 API key 失效。
- 部分上游错误日志包含完整 FMP URL 和 API key，需要日志脱敏。
- EV/EBITDA peer 数据和 news 数据缺失应在报告和评测输出中披露。

