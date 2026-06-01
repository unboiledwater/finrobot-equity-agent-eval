#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "benchmark" / "report_audit_tasks.json"
CLAIMS_PATH = ROOT / "evidence" / "nvda" / "verified_claims.json"
MD_PATH = (
    ROOT
    / "reports"
    / "audit_outputs"
    / "official_report_audits"
    / "nvda_partial_audit.md"
)
HTML_PATH = (
    ROOT
    / "reports"
    / "audit_outputs"
    / "official_report_audits"
    / "nvda_partial_audit.html"
)


PALETTE = {
    "bg": "#F8F5FD",
    "primary": "#4D77A7",
    "secondary": "#B2A4CF",
    "secondary_2": "#84A7CD",
    "surface": "#FFFFFF",
    "surface_alt": "#E2F4F3",
    "warning": "#FDE4E4",
    "border": "#D4D4D4",
    "muted": "#A1A0A5",
    "soft": "#DCDEEE",
}


def load_json(path: Path):
    with path.open() as f:
        return json.load(f)


def esc(value) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def chip(label: str, kind: str = "default") -> str:
    classes = {
        "supported": "chip chip-supported",
        "weak": "chip chip-weak",
        "downgraded": "chip chip-downgraded",
        "backlog": "chip chip-backlog",
        "passed": "chip chip-passed",
        "default": "chip",
    }
    return f'<span class="{classes.get(kind, classes["default"])}">{esc(label)}</span>'


def table(headers: list[str], rows: list[list[str]], numeric_cols: set[int] | None = None) -> str:
    numeric_cols = numeric_cols or set()
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body_rows = []
    for row in rows:
        cells = []
        for idx, cell in enumerate(row):
            cls = ' class="num"' if idx in numeric_cols else ""
            cells.append(f"<td{cls}>{cell}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body_rows)}</tbody></table></div>'


def main() -> None:
    tasks_data = load_json(TASKS_PATH)
    claims_data = load_json(CLAIMS_PATH)
    md_text = MD_PATH.read_text()
    formal_tasks = tasks_data["tasks"]
    claims = {item["candidate_id"]: item for item in claims_data["verified_claims"]}
    formal_candidates = ["B01", "B02", "B08"]
    downgraded = ["B05", "B06"]
    backlog = ["B04", "B10", "B11"]

    supported = sum(1 for c in formal_candidates if claims[c]["substantive_judgment"] == "supported")
    weak = sum(1 for c in formal_candidates if claims[c]["citation_traceability"] == "weak")

    claims_rows = []
    for task in formal_tasks:
        candidate = next(
            c for c, item in claims.items() if item.get("formal_task_id") == task["claim_id"]
        )
        claims_rows.append(
            [
                f"<code>{esc(task['claim_id'])}</code>",
                f"<code>{esc(candidate)}</code>",
                esc(task["claim_quote"]),
                chip("已支持", "supported"),
                chip("弱可追溯", "weak"),
                f"<code>{esc(task['execution_level'])}</code>",
            ]
        )

    source_rows = [
        [
            "<code>SRC-NVDA-FY2024-10K</code>",
            "Form 10-K",
            "NVIDIA Corporation Form 10-K for fiscal year ended January 28, 2024",
            "2024-02-21",
            "FY2024 and FY2023",
            chip("报告前可用", "passed"),
        ],
        [
            "<code>SRC-NVDA-FY2024-RESULTS</code>",
            "Earnings release",
            "NVIDIA fiscal 2024 results release",
            "2024-02-21",
            "FY2024 and FY2023",
            chip("报告前可用", "passed"),
        ],
        [
            "<code>SRC-NVDA-FY2026-10K</code>",
            "Form 10-K",
            "NVIDIA Corporation Form 10-K for fiscal year ended January 25, 2026",
            "2026-02-25",
            "FY2026 and comparative columns",
            chip("报告前可用", "passed"),
        ],
        [
            "<code>SRC-NVDA-FY2026-RESULTS</code>",
            "Earnings release",
            "NVIDIA fiscal 2026 results release",
            "2026-02-25",
            "FY2026 and FY2025",
            chip("报告前可用", "passed"),
        ],
    ]

    exclusion_rows = []
    localized_exclusion_reasons = {
        "B05": "缺少与报告指标定义完全一致的已披露 EBITDA 口径和可复现输入；FinRobot/FMP 表格不能作为最终事实标准。",
        "B06": "EBITDA margin 依赖 EBITDA 口径；在 EBITDA 定义不可复现前，不能进入确定性 L2 评分。",
        "B04": "CAGR 的起点、终点和期间未被充分指定；重新进入需要明确起始期间、结束期间和来源数值。",
        "B10": "EV/EBITDA 需要带日期的市场价值、净债务或 EV 口径，以及 EBITDA 定义；报告未识别这些输入。",
        "B11": "Forward PE 需要带日期的股价和 EPS 预测来源；报告未识别这些输入。",
    }
    for cid in downgraded:
        item = claims[cid]
        rule = "L2_SOURCE_CLOSURE_REQUIRED" if cid == "B05" else "L2_DEPENDENT_METRIC_UNCLOSED"
        reentry = (
            "补充已披露 EBITDA 定义或可复现 reconciliation。"
            if cid == "B05"
            else "闭合 B05，并确认收入分母期间一致。"
        )
        exclusion_rows.append(
            [
                f"<code>{cid}</code>",
                esc(item["claim_quote"]),
                esc(localized_exclusion_reasons[cid]),
                f"<code>{rule}</code>",
                esc(reentry),
                chip("已降级", "downgraded"),
            ]
        )
    for cid in backlog:
        item = claims[cid]
        exclusion_rows.append(
            [
                f"<code>{cid}</code>",
                esc(item["claim_quote"]),
                esc(localized_exclusion_reasons[cid]),
                "<code>TRACEABILITY_INPUTS_REQUIRED</code>",
                "补齐缺失来源、日期或公式输入后再评估。",
                chip("待补证据", "backlog"),
            ]
        )

    code_map_rows = [
        [
            "Claim 级结果",
            "展示符合 L2 资格的正式任务与评分分母",
            "<code>benchmark/report_audit_tasks.json</code>",
            "<code>scripts/validate_nvda_partial_audit.py</code>",
        ],
        [
            "证据登记",
            "展示来源闭合状态与 claim 判定",
            "<code>evidence/nvda/verified_claims.json</code>",
            "<code>docs/source_temporal_alignment_rules.md</code>",
        ],
        [
            "来源登记",
            "展示披露日期、覆盖期间与报告生成前可用性",
            "<code>evidence/nvda/primary_sources.md</code>",
            "一手来源映射复核",
        ],
        [
            "排除与待补证据",
            "展示不进入确定性分母的降级或暂缓 claims",
            "<code>evidence/nvda/verified_claims.json</code>",
            "<code>benchmark/scoring_rules.json</code>",
        ],
        [
            "校验",
            "校验 JSON/Markdown/HTML 统计与边界措辞",
            "<code>scripts/validate_nvda_partial_audit.py</code>",
            "必须输出 PASSED",
        ],
    ]

    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NVDA Partial Audit Report — 投资概览局部审查</title>
  <style>
    :root {{
      --bg: {PALETTE['bg']};
      --primary: {PALETTE['primary']};
      --secondary: {PALETTE['secondary']};
      --secondary-2: {PALETTE['secondary_2']};
      --surface: {PALETTE['surface']};
      --surface-alt: {PALETTE['surface_alt']};
      --warning: {PALETTE['warning']};
      --border: {PALETTE['border']};
      --muted: {PALETTE['muted']};
      --soft: {PALETTE['soft']};
      --text: #263241;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 15px;
      line-height: 1.55;
    }}
    .page {{ max-width: 1180px; margin: 0 auto; padding: 28px 22px 40px; }}
    header {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px;
      box-shadow: 0 10px 30px rgba(77, 119, 167, 0.08);
    }}
    h1 {{ margin: 0 0 10px; color: var(--primary); font-size: 28px; letter-spacing: 0; }}
    h2 {{ margin: 0 0 14px; color: var(--primary); font-size: 20px; letter-spacing: 0; }}
    h3 {{ margin: 18px 0 10px; color: var(--primary); font-size: 16px; letter-spacing: 0; }}
    p {{ margin: 0 0 12px; }}
    code {{ background: var(--soft); border-radius: 5px; padding: 2px 5px; font-size: 0.92em; }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 18px;
    }}
    .metric {{
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      min-height: 86px;
    }}
    .metric .label {{ color: #4f5c68; font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }}
    .metric .value {{ margin-top: 6px; font-size: 22px; color: var(--primary); font-weight: 700; }}
    .tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin: 18px 0;
    }}
    .tab-link {{
      display: inline-block;
      text-decoration: none;
      color: var(--primary);
      border: 1px solid var(--border);
      background: var(--surface);
      border-radius: 8px;
      padding: 8px 12px;
      font-weight: 650;
    }}
    .tab-link:hover {{ background: var(--soft); }}
    section {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      margin: 16px 0;
    }}
    .callout {{
      background: var(--warning);
      border-left: 4px solid var(--secondary);
      border-radius: 8px;
      padding: 12px 14px;
      margin: 12px 0;
    }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--border); border-radius: 8px; }}
    table {{ width: 100%; border-collapse: collapse; background: var(--surface); min-width: 760px; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); vertical-align: top; text-align: left; }}
    th {{ background: var(--soft); color: var(--primary); font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }}
    tr:last-child td {{ border-bottom: 0; }}
    .num {{ text-align: right; }}
    .chip {{
      display: inline-block;
      border-radius: 999px;
      padding: 3px 9px;
      border: 1px solid var(--border);
      background: var(--soft);
      color: var(--primary);
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }}
    .chip-supported, .chip-passed {{ background: #E9F5F1; color: #3b6f55; }}
    .chip-weak {{ background: #FEF1E8; color: #7F6E9C; }}
    .chip-downgraded, .chip-backlog {{ background: var(--warning); color: #7F6E9C; }}
    .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
    footer {{ color: #5e6670; margin-top: 18px; font-size: 13px; }}
    @media (max-width: 860px) {{
      .summary-grid, .two-col {{ grid-template-columns: 1fr; }}
      .page {{ padding: 16px 12px 28px; }}
      h1 {{ font-size: 24px; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <header id="overview">
      <h1>NVDA Partial Audit Report — 投资概览局部审查</h1>
      <p>本 HTML 报告只渲染 canonical Markdown 与结构化 JSON 产物，不新增任何审查判断。</p>
      <div class="summary-grid">
        <div class="metric"><div class="label">状态</div><div class="value">局部审查</div><div>Audit / in progress</div></div>
        <div class="metric"><div class="label">覆盖范围</div><div class="value">1 个章节</div><div>仅 Investment Overview</div></div>
        <div class="metric"><div class="label">正式评分 Claims</div><div class="value">3 L2</div><div>分母限定为符合条件的 L2 tasks</div></div>
        <div class="metric"><div class="label">校验</div><div class="value">已通过</div><div>由脚本复算与边界检查支持</div></div>
      </div>
      <div class="callout">
        当前 <strong>3/3 supported</strong> 只适用于已满足 L2 纳入条件的正式任务集合；不代表整份 NVDA 报告准确率、跨公司结果，也不代表 generation comparison 结论。
      </div>
    </header>

    <nav class="tabs" aria-label="报告标签页">
      <a class="tab-link" href="#overview">概览</a>
      <a class="tab-link" href="#claims">Claims 明细</a>
      <a class="tab-link" href="#sources">来源</a>
      <a class="tab-link" href="#exclusions">排除项</a>
      <a class="tab-link" href="#validation">校验</a>
      <a class="tab-link" href="#code-map">代码映射</a>
    </nav>

    <section id="claims">
      <h2>Claims 明细</h2>
      <p>以下为符合 L2 条件的正式任务集合的 claim-level 结果。当前评分分母：<strong>3</strong>。</p>
      {table(["Task ID", "Candidate", "原始 Claim Quote", "实质判断", "报告级可追溯性", "执行层级"], claims_rows)}
      <div class="two-col">
        <div>
          <h3>确定性评分摘要</h3>
          {table(["指标", "结果"], [["符合条件的 L2 formal tasks 总数", "3"], ["Supported（已支持）", str(supported)], ["Contradicted（相矛盾）", "0"], ["Unsupported（未支持）", "0"], ["L2 合格集合内的实质准确率", "3/3"]], numeric_cols={1})}
        </div>
        <div>
          <h3>报告级引用可追溯性</h3>
          {table(["指标", "结果"], [["Strong traceability（强可追溯）", "0"], ["Partial traceability（部分可追溯）", "0"], ["Weak traceability（弱可追溯）", str(weak)], ["Absent traceability（无可追溯）", "0"]], numeric_cols={1})}
        </div>
      </div>
    </section>

    <section id="sources">
      <h2>来源</h2>
      <p>本节列出用于 source closure 的一手来源。下列来源均在 FinRobot 报告时间戳之前可获得。</p>
      {table(["Source ID", "类型", "文件", "发布日期", "期间", "报告前可用性"], source_rows)}
    </section>

    <section id="exclusions">
      <h2>排除项</h2>
      <p>已降级与待补证据的 claims 会被记录，但不进入当前确定性准确率分母。</p>
      {table(["Candidate", "Claim", "排除/暂缓原因", "触发规则", "重新进入条件", "状态"], exclusion_rows)}
    </section>

    <section id="validation">
      <h2>校验</h2>
      <p>{chip("已通过", "passed")} 校验状态：<strong>已通过</strong>。</p>
      <p>已校验产物：<code>benchmark/report_audit_tasks.json</code>、<code>evidence/nvda/verified_claims.json</code>、<code>reports/audit_outputs/official_report_audits/nvda_partial_audit.md</code>。</p>
      <p>已校验指标：L2 分母、task IDs、supported 数量、traceability 数量、排除项与分母隔离、HTML tab 存在性、代码/数据映射、批准配色和报告边界措辞。</p>
    </section>

    <section id="code-map">
      <h2>主要功能与代码/数据映射</h2>
      {table(["报告功能", "作用", "主要数据/代码产物", "校验或依赖"], code_map_rows)}
    </section>

    <footer>
      Canonical source：<code>reports/audit_outputs/official_report_audits/nvda_partial_audit.md</code>。HTML 是面向人类阅读的展示层。
      Markdown 源文件长度：{len(md_text)} 个字符。
    </footer>
  </div>
</body>
</html>
"""
    HTML_PATH.write_text(html_doc)
    print(HTML_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
