#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "benchmark" / "report_audit_tasks.json"
CLAIMS_PATH = ROOT / "evidence" / "nvda" / "verified_claims.json"
SCORING_PATH = ROOT / "benchmark" / "scoring_rules.json"
SOURCES_PATH = ROOT / "evidence" / "nvda" / "primary_sources.md"
MD_PATH = ROOT / "reports" / "audit_outputs" / "official_report_audits" / "nvda_partial_audit.md"
VALIDATOR_PATH = ROOT / "scripts" / "validate_nvda_partial_audit.py"
HTML_PATH = (
    ROOT
    / "reports"
    / "audit_outputs"
    / "official_report_audits"
    / "nvda_partial_audit_case_report.html"
)


PALETTE = {
    "bg": "#F8F5FD",
    "primary": "#4D77A7",
    "secondary": "#D4D4D4",
    "secondary_2": "#D4D4D4",
    "surface": "#F8F5FD",
    "surface_alt": "#D4D4D4",
    "soft": "#D4D4D4",
    "line": "#D4D4D4",
    "muted": "#4D77A7",
    "warning": "#D4D4D4",
    "success": "#D4D4D4",
    "code": "#D4D4D4",
    "accent": "#4D77A7",
}

FORMAL_CANDIDATES = ["B01", "B02", "B08"]
DOWNGRADED = ["B05", "B06"]
BACKLOG = ["B04", "B10", "B11"]


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
        "proposed": "chip chip-proposed",
        "default": "chip",
    }
    return f'<span class="{classes.get(kind, classes["default"])}">{esc(label)}</span>'


def table(headers: list[str], rows: list[list[str]], numeric_cols: set[int] | None = None) -> str:
    numeric_cols = numeric_cols or set()
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = []
    for row in rows:
        cells = []
        for idx, cell in enumerate(row):
            cls = ' class="num"' if idx in numeric_cols else ""
            cells.append(f"<td{cls}>{cell}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def code_block(path: str, language: str, body: str) -> str:
    block_id = path.replace("/", "-").replace(".", "-").replace("_", "-")
    return f"""
      <div class="code-card">
        <div class="code-head">
          <span><code>{esc(path)}</code></span>
          <button type="button" class="copy-btn" data-copy-target="{esc(block_id)}">复制</button>
        </div>
        <pre><code id="{esc(block_id)}" class="language-{esc(language)}">{esc(body.strip())}</code></pre>
      </div>
    """


def short_json(value, limit: int = 2200) -> str:
    text = json.dumps(value, indent=2, ensure_ascii=False)
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n  ...\n}"


def validator_excerpt() -> str:
    text = VALIDATOR_PATH.read_text()
    markers = [
        "EXPECTED_TASK_IDS",
        "all formal L2 claims must be supported",
        "all formal L2 claims must have weak report-level traceability",
        "excluded/backlog candidates must not have formal_task_id",
        "required_case_html_phrases",
    ]
    lines = text.splitlines()
    selected: list[str] = []
    for marker in markers:
        for idx, line in enumerate(lines):
            if marker in line:
                start = max(0, idx - 3)
                end = min(len(lines), idx + 8)
                selected.extend(lines[start:end])
                selected.append("")
                break
    return "\n".join(selected).strip() or text[:1800]


def markdown_boundary_excerpt() -> str:
    md = MD_PATH.read_text()
    needles = [
        "Status: Partial audit / in progress",
        "Not covered: full-report accuracy, cross-company results, generation comparison",
        "These results apply only to the three eligible L2 claims",
    ]
    chunks = []
    for needle in needles:
        idx = md.find(needle)
        if idx >= 0:
            start = max(0, md.rfind("\n", 0, idx - 220))
            end = md.find("\n\n", idx)
            chunks.append(md[start:end if end > idx else idx + 420].strip())
    return "\n\n".join(chunks) or md[:1200]


def source_rows(claims: dict[str, dict]) -> list[list[str]]:
    seen: dict[str, dict] = {}
    for item in claims.values():
        source = item.get("verification_source")
        if isinstance(source, dict) and source.get("source_id"):
            seen[source["source_id"]] = source
    rows = []
    for sid, source in sorted(seen.items()):
        rows.append(
            [
                f"<code>{esc(sid)}</code>",
                esc(source.get("document_type")),
                esc(source.get("document_title")),
                esc(source.get("publication_date")),
                esc(source.get("as_of_period")),
                chip("报告前可用", "passed") if source.get("available_before_report_date") else chip("需复核"),
            ]
        )
    return rows


def claim_detail(item: dict, task: dict | None = None) -> str:
    source = item.get("verification_source") or (task or {}).get("verification_source") or {}
    rows = [
        ["Report excerpt", esc(item.get("report_excerpt"))],
        ["Claim quote", esc(item.get("claim_quote"))],
        ["Normalized claim", esc(item.get("normalized_claim"))],
        ["Extraction note", esc(item.get("extraction_note"))],
        ["Verification source", esc(source.get("document_title", "未闭合"))],
        ["Evidence excerpt", esc(item.get("evidence_excerpt"))],
        ["Calculation trace", esc(item.get("calculation_trace") or "无可复现 calculation trace")],
        ["Scoring rule", f"<code>{esc(item.get('scoring_rule_id'))}</code>"],
        ["Review note", esc(item.get("review_note"))],
    ]
    return table(["字段", "内容"], rows)


def main() -> None:
    tasks_data = load_json(TASKS_PATH)
    claims_data = load_json(CLAIMS_PATH)
    scoring_data = load_json(SCORING_PATH)
    claims = {item["candidate_id"]: item for item in claims_data["verified_claims"]}
    task_by_id = {task["claim_id"]: task for task in tasks_data["tasks"]}

    formal_claims = [claims[cid] for cid in FORMAL_CANDIDATES]
    supported = sum(1 for item in formal_claims if item["substantive_judgment"] == "supported")
    weak = sum(1 for item in formal_claims if item["citation_traceability"] == "weak")

    formal_rows = []
    for item in formal_claims:
        task = task_by_id[item["formal_task_id"]]
        formal_rows.append(
            [
                f"<code>{esc(task['claim_id'])}</code>",
                esc(item["claim_quote"]),
                chip("Closed", "passed"),
                chip("Supported", "supported"),
                chip("Weak", "weak"),
                f"<code>{esc(item['execution_level'])}</code>",
                f'<details><summary>查看证据链</summary>{claim_detail(item, task)}</details>',
            ]
        )

    downgrade_reason = {
        "B05": [
            "缺少与报告指标定义完全一致的 EBITDA 定义和可复现输入。",
            "L2_SOURCE_CLOSURE_REQUIRED",
            "取得已披露定义或可复现 reconciliation。",
        ],
        "B06": [
            "EBITDA margin 依赖尚未闭合的 EBITDA 定义。",
            "L2_DEPENDENT_METRIC_UNCLOSED",
            "闭合 B05，并确认收入分母期间一致。",
        ],
    }
    downgrade_rows = [
        [
            f"<code>{cid}</code>",
            esc(claims[cid]["claim_quote"]),
            esc(downgrade_reason[cid][0]),
            f"<code>{downgrade_reason[cid][1]}</code>",
            esc(downgrade_reason[cid][2]),
        ]
        for cid in DOWNGRADED
    ]

    backlog_reason = {
        "B04": ["period / endpoints unclear", "CAGR 没有明确期间就无法复算。", "识别起点期间、终点期间和来源值。"],
        "B10": [
            "dated EV basis, net debt, EBITDA basis absent",
            "市场敏感 multiple 没有日期与定义就不可审计。",
            "绑定带日期的市场与财务输入。",
        ],
        "B11": [
            "dated price and EPS estimate source absent",
            "Forward valuation 依赖预测 provenance。",
            "定位带日期的股价和 forecast EPS 来源。",
        ],
    }
    backlog_rows = [
        [
            f"<code>{cid}</code>",
            esc(claims[cid]["claim_quote"]),
            esc(backlog_reason[cid][0]),
            esc(backlog_reason[cid][1]),
            esc(backlog_reason[cid][2]),
        ]
        for cid in BACKLOG
    ]

    improvement_rows = [
        [
            "财务 claim 可以正确，但正文引用链过弱",
            "3 个 L2 tasks 均 supported，但 traceability 均 weak",
            "用户无法仅凭报告独立复核关键数字",
            "报告生成时绑定 filing、period、table/line reference",
        ],
        [
            "EBITDA 指标无法闭合口径",
            "B05/B06 被规则化降级",
            "Agent 可能使用数据源计算字段而未披露定义",
            "对 non-GAAP / derived metrics 强制输出定义与 reconciliation",
        ],
        [
            "CAGR 缺少期间端点",
            "B04 进入 backlog",
            "看似精确的增长结论不可复算",
            "对 CAGR 强制输出 start period、end period、formula inputs",
        ],
        [
            "估值倍数缺少日期与预测来源",
            "B10/B11 进入 backlog",
            "市场敏感指标无法审计",
            "对 EV/EBITDA、forward PE 强制输出 as-of date、price source、estimate source",
        ],
    ]

    gate_rows = [
        ["Historical Figure Citation Gate", "报告陈述历史财务数字", "filing + period + evidence reference", chip("Proposed", "proposed")],
        ["Derived Metric Definition Gate", "EBITDA / margin / CAGR 等派生指标", "formula + source inputs + metric definition", chip("Proposed", "proposed")],
        ["Market-Sensitive Valuation Gate", "EV/EBITDA / PE / target price", "as-of date + price source + denominator basis", chip("Proposed", "proposed")],
        ["Claim Type Disclosure Gate", "前瞻、比较或风险判断", "fact / calculation / inference 标签", chip("Proposed", "proposed")],
    ]

    implementation_rows = [
        ["Task Registry", "<code>benchmark/report_audit_tasks.json</code>", "定义 formal tasks 与评分范围"],
        ["Claim Evidence Records", "<code>evidence/nvda/verified_claims.json</code>", "存储 claim、来源、判断、降级和 backlog 状态"],
        ["Primary Source Register", "<code>evidence/nvda/primary_sources.md</code>", "登记公司公开来源与时间可用性"],
        ["Canonical Audit Narrative", "<code>reports/audit_outputs/official_report_audits/nvda_partial_audit.md</code>", "报告规范文本源"],
        ["Validation Script", "<code>scripts/validate_nvda_partial_audit.py</code>", "复算统计并检查边界措辞"],
        ["Rendered Case Report", "<code>nvda_partial_audit_case_report.html</code>", "面向人类阅读的作品集展示层"],
    ]

    code_tabs = [
        ("task-schema", "Task Schema", code_block("benchmark/report_audit_tasks.json", "json", short_json(tasks_data["tasks"][0]))),
        (
            "verified-claim",
            "Verified Claim",
            code_block(
                "evidence/nvda/verified_claims.json",
                "json",
                short_json({"formal_l2_claim": claims["B01"], "downgrade_claim": claims["B05"]}, 3000),
            ),
        ),
        (
            "scoring-rules",
            "Scoring Rules",
            code_block(
                "benchmark/scoring_rules.json",
                "json",
                short_json({"execution_levels": scoring_data["execution_levels"], "traceability_gate": scoring_data["traceability_gate"], "rules": scoring_data["rules"][:3]}, 2800),
            ),
        ),
        ("validation-script", "Validation Script", code_block("scripts/validate_nvda_partial_audit.py", "python", validator_excerpt())),
        (
            "output-boundary",
            "Output Boundary",
            code_block(
                "reports/audit_outputs/official_report_audits/nvda_partial_audit.md",
                "markdown",
                markdown_boundary_excerpt(),
            ),
        ),
    ]
    code_tab_buttons = "".join(
        f'<button type="button" class="code-tab-button{" active" if idx == 0 else ""}" data-code-target="{tab_id}">{esc(label)}</button>'
        for idx, (tab_id, label, _) in enumerate(code_tabs)
    )
    code_tab_panels = "".join(
        f'<div class="code-tab-panel{" active" if idx == 0 else ""}" id="code-{tab_id}">{content}</div>'
        for idx, (tab_id, _, content) in enumerate(code_tabs)
    )

    source_md_excerpt = SOURCES_PATH.read_text()[:1400]

    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NVDA Partial Audit Case Report — Evidence-Gated Evaluation</title>
  <style>
    :root {{
      --bg: {PALETTE['bg']};
      --primary: {PALETTE['primary']};
      --surface: {PALETTE['surface']};
      --surface-alt: {PALETTE['surface_alt']};
      --soft: {PALETTE['soft']};
      --line: {PALETTE['line']};
      --muted: {PALETTE['muted']};
      --code: {PALETTE['code']};
      --accent: {PALETTE['accent']};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--primary);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
      font-size: 15px;
      line-height: 1.62;
    }}
    .page {{ width: min(1200px, calc(100% - 32px)); margin: 0 auto; padding: 26px 0 42px; }}
    header, .tab-panel {{
      background: var(--bg);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 22px;
    }}
    h1 {{ margin: 0 0 6px; font-size: 28px; letter-spacing: 0; color: var(--primary); }}
    h2 {{ margin: 0 0 12px; font-size: 20px; letter-spacing: 0; color: var(--primary); }}
    h3 {{ margin: 20px 0 10px; font-size: 16px; letter-spacing: 0; color: var(--primary); }}
    p {{ margin: 0 0 12px; }}
    code {{ background: var(--code); border-radius: 5px; padding: 2px 5px; font-size: 0.92em; color: var(--accent); }}
    .subtitle {{ font-size: 16px; color: var(--accent); margin-bottom: 10px; }}
    .lede {{ max-width: 900px; }}
    .status-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 0; }}
    .summary-grid, .three-grid {{
      display: grid;
      gap: 12px;
      margin: 18px 0;
    }}
    .summary-grid {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
    .three-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    .metric, .info-box {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px;
      min-height: 86px;
    }}
    .metric .label {{ color: var(--accent); font-size: 12px; font-weight: 700; }}
    .metric .value {{ margin-top: 5px; font-size: 22px; color: var(--primary); font-weight: 800; }}
    .callout {{
      background: var(--surface);
      border-left: 4px solid var(--primary);
      border-radius: 8px;
      padding: 12px 14px;
      margin: 14px 0;
    }}
    .tabs, .code-tabs {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0; }}
    .tab-button, .code-tab-button, .copy-btn {{
      border: 1px solid var(--line);
      background: var(--bg);
      color: var(--primary);
      border-radius: 8px;
      padding: 8px 12px;
      font-weight: 700;
      cursor: pointer;
      font: inherit;
    }}
    .tab-button.active, .code-tab-button.active {{ background: var(--primary); color: var(--bg); border-color: var(--primary); }}
    .tab-panel, .code-tab-panel {{ display: none; }}
    .tab-panel.active, .code-tab-panel.active {{ display: block; }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 8px; margin: 10px 0 16px; }}
    table {{ width: 100%; border-collapse: collapse; background: var(--bg); min-width: 760px; }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--line); vertical-align: top; text-align: left; }}
    th {{ background: var(--soft); color: var(--primary); font-size: 12px; font-weight: 800; }}
    tr:last-child td {{ border-bottom: 0; }}
    .num {{ text-align: right; }}
    details {{ max-width: 540px; }}
    summary {{ cursor: pointer; font-weight: 700; color: var(--accent); }}
    .chip {{
      display: inline-block;
      border-radius: 999px;
      padding: 3px 9px;
      border: 1px solid var(--line);
      background: var(--surface);
      color: var(--primary);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }}
    .chip-supported, .chip-passed, .chip-weak, .chip-downgraded, .chip-backlog, .chip-proposed {{ background: var(--surface); color: var(--primary); }}
    .code-card {{ border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: var(--bg); margin-top: 10px; }}
    .code-head {{ display: flex; justify-content: space-between; gap: 10px; align-items: center; background: var(--soft); padding: 10px 12px; }}
    pre {{ margin: 0; max-height: 430px; overflow: auto; padding: 14px; background: var(--bg); color: var(--accent); }}
    pre code {{ background: transparent; padding: 0; color: var(--accent); }}
    .section-note {{ color: var(--accent); }}
    footer {{ margin-top: 18px; color: var(--accent); font-size: 13px; }}
    @media (max-width: 900px) {{
      .summary-grid, .three-grid {{ grid-template-columns: 1fr; }}
      .page {{ width: min(100% - 20px, 1200px); padding-top: 14px; }}
      h1 {{ font-size: 24px; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <header>
      <h1>NVDA Partial Audit Case Report — Evidence-Gated Evaluation of an AI-Generated Equity Research Report</h1>
      <div class="subtitle">基于证据闸门的 AI 金融研究报告局部审查案例</div>
      <p class="lede">本案例展示如何将真实 AI 生成的金融研究报告转化为可审计的 claim-level 评测任务，并分别处理实质准确性、引用可追溯性、规则化降级与后续产品改进要求。</p>
      <div class="status-row">
        {chip("v1", "passed")}
        {chip("Partial Audit", "weak")}
        {chip("In Progress", "weak")}
        {chip("FinRobot report = evaluated artifact", "default")}
        {chip("Primary-source verification", "passed")}
      </div>
      <div class="summary-grid">
        <div class="metric"><div class="label">被测系统</div><div class="value">FinRobot</div><div>Official NVDA Equity Research Report</div></div>
        <div class="metric"><div class="label">覆盖范围</div><div class="value">1 个章节</div><div>Investment Overview only</div></div>
        <div class="metric"><div class="label">评分集合</div><div class="value">3 L2</div><div>eligible formal tasks</div></div>
        <div class="metric"><div class="label">校验状态</div><div class="value">Passed</div><div>script-backed validation</div></div>
      </div>
      <div class="callout">当前 3/3 supported 只描述已满足 L2 条件的 claim 集合；不代表完整 NVDA 报告准确率，不代表被测系统的整体表现，也不代表 generation comparison 结论。</div>
    </header>

    <nav class="tabs" aria-label="Case report tabs">
      <button type="button" class="tab-button active" data-tab-target="overview">Overview / 项目概览</button>
      <button type="button" class="tab-button" data-tab-target="product-goal">Product Goal / 服务目标</button>
      <button type="button" class="tab-button" data-tab-target="audit-results">Audit Results / 审查结果</button>
      <button type="button" class="tab-button" data-tab-target="rubrics">Rubrics &amp; Protocol / 评分与方法</button>
      <button type="button" class="tab-button" data-tab-target="improvements">Improvement Plan / 待改进项</button>
      <button type="button" class="tab-button" data-tab-target="implementation">Implementation / 代码与复现</button>
    </nav>

    <main>
      <section class="tab-panel active" id="tab-overview">
        <h2>Overview / 项目概览</h2>
        <div class="three-grid">
          <div class="info-box"><h3>Problem</h3><p>AI 可以生成看似专业的 equity research report，但可能出现数字或期间错误、估值指标缺少日期与口径、推断强于证据、正文缺乏可独立复核来源链。</p></div>
          <div class="info-box"><h3>Evaluation Response</h3><p>本项目不重新生成报告，而是抽取可核验 claims、映射公开一手来源、确定性评分可复核项目，并对证据不闭合的 claims 明确降级。</p></div>
          <div class="info-box"><h3>Product Value</h3><p>该方法帮助产品和评测团队判断输出是否可核验、结论是否越过证据边界、人工 reviewer 应集中在哪里、哪些失败应由 harness 提前拦截。</p></div>
        </div>
        <h3>Current Case Snapshot</h3>
        {table(["指标", "当前结果"], [["Audited Company", "NVIDIA / NVDA"], ["Audited Section", "Investment Overview"], ["Eligible L2 Claims", "3"], ["Supported within Eligible L2 Set", "3 / 3"], ["Strong Report-Level Traceability", "0"], ["Weak Report-Level Traceability", str(weak)], ["Rule-Based Downgrade Cases", "2"], ["Traceability / Backlog Claims", "3"]], numeric_cols={1})}
        <div class="callout">FinRobot 官方报告是被审查对象，不是事实来源；验证依据是 NVIDIA 公开披露材料与可复核来源。</div>
      </section>

      <section class="tab-panel" id="tab-product-goal">
        <h2>Product Goal / 服务目标</h2>
        <h3>What product problem does this audit framework address?</h3>
        <p>专业金融 Agent 的输出不能只满足“读起来像研究报告”，还需要满足数字可以回到来源、估值指标可以重建口径、披露事实与分析推断可区分、证据不足时拒绝进入确定性结论、审核人员能快速定位真正需要人工复核的部分。</p>
        {table(["角色", "需要解决的问题"], [["Agent Product / Eval Team", "判断专业报告输出是否可靠，并形成可复用 benchmark"], ["Engineer", "获得明确、可实现、可校验的 evidence-gate 规则"], ["Human Reviewer", "只集中复核高风险或证据不闭合 claims"], ["Enterprise User in High-Responsibility Tasks", "获得可追踪、可解释、不夸大证据强度的输出"]])}
        <h3>Product Requirement Statement</h3>
        <div class="callout">面向 AI 生成的专业报告，建立一套 evaluator workflow：将报告表述转化为绑定证据的 claims；对可复核事实进行确定性评分；对无法闭合口径的指标主动降级；将错误与缺口转化为产品改进要求，同时避免对整体报告可靠性作过度声称。</div>
        <h3>Non-Goals / 当前不服务的目标</h3>
        {table(["Non-Goal", "边界说明"], [["不生成股票推荐", "本页面不是投资建议，也不评价 NVDA 投资价值。"], ["不完整审查 FinRobot", "当前只覆盖 NVDA Investment Overview 已映射 claims。"], ["不测试本地 FinRobot generation pipeline", "本轮不运行 fresh-run。"], ["不证明 evidence-gated generation 优于 baseline", "v2 才开展 generation comparison。"], ["不声称企业控制已实现", "多租户、权限、脱敏、生产审计只属于 proposed extension。"]])}
        <h3>Why Financial Reports as Test Material</h3>
        {table(["特征", "对 Eval 的价值"], [["数字密集", "可验证单位、期间、公式和计算结果"], ["来源公开", "可使用公开披露材料形成 evidence chain"], ["推断与事实混合", "可测试 reasoning boundary"], ["估值依赖日期与口径", "可测试 traceability 与 downgrade logic"], ["错误具有现实后果", "体现高责任任务中的可靠性要求"]])}
      </section>

      <section class="tab-panel" id="tab-audit-results">
        <h2>Audit Results / 审查结果</h2>
        <div class="three-grid">
          <div class="info-box"><h3>Substantive Accuracy — Eligible L2 Set</h3>{table(["Metric", "Result"], [["Eligible L2 Formal Tasks", "3"], ["Supported", str(supported)], ["Contradicted", "0"], ["Unsupported", "0"], ["Accuracy within Eligible L2 Set", "3 / 3"]], numeric_cols={1})}</div>
          <div class="info-box"><h3>Report-Level Citation Traceability</h3>{table(["Metric", "Result"], [["Strong", "0"], ["Partial", "0"], ["Weak", str(weak)], ["Absent", "0"]], numeric_cols={1})}</div>
          <div class="info-box"><h3>产品解释</h3><p>The audited claims are substantively supported after external primary-source verification, but the report itself does not provide strong claim-level traceability.</p><p>因此，内容正确与报告可审计性被视为两个独立评测结果。</p></div>
        </div>
        <h3>Eligible Formal Claims</h3>
        {table(["Task ID", "Claim Quote", "Source Closure", "Substantive Judgment", "Traceability", "Execution Level", "Details"], formal_rows)}
        <h3>Rule-Based Downgrade Cases</h3>
        <p class="section-note">这些 claims 被记录而不是被静默丢弃；排除它们可以避免口径不确定的指标污染 deterministic accuracy。</p>
        {table(["Claim", "Why It Was Not Scored", "Triggered Rule", "Re-entry Condition"], downgrade_rows)}
        <h3>Traceability / Backlog Claims</h3>
        {table(["Claim", "Report Quote", "Missing Basis", "Why This Matters", "Next Verification Action"], backlog_rows)}
        <h3>Source Register</h3>
        {table(["Source ID", "Type", "Document", "Publication Date", "Period", "Availability"], source_rows(claims))}
      </section>

      <section class="tab-panel" id="tab-rubrics">
        <h2>Rubrics &amp; Protocol / 评分与方法</h2>
        <h3>Evaluation Dimensions</h3>
        {table(["Dimension", "What Is Evaluated", "Judgment Output", "Included in Current Score?"], [["Substantive Accuracy", "Claim 是否被 primary source 支持", "Supported / Contradicted / Unsupported", "对 eligible L2 纳入"], ["Citation Traceability", "报告自身是否给出可复核来源路径", "Strong / Partial / Weak / Absent", "单独统计，不与 accuracy 混合"], ["Source Temporal Alignment", "核验来源是否在报告时点可用", "Aligned / Mismatch / Needs Review", "作为 eligibility gate"], ["Claim Boundary Preservation", "reviewer 是否保持原文边界", "Pass / Needs Note", "作为 protocol requirement"], ["Downgrade Discipline", "不可复核 claim 是否被排除", "Downgraded / Backlog", "不进入 denominator"], ["Reasoning Boundary", "报告是否将推断包装成事实", "Human Review", "当前章节未进入 L2 总分"]])}
        <h3>L2 Eligibility Rules</h3>
        {table(["条件", "要求"], [["Claim 类型", "可独立核验的数值事实或可复算指标"], ["原文边界", "claim_quote 可以回溯至报告原文"], ["来源闭合", "primary source 与 evidence excerpt 已闭合"], ["时点一致", "source publication date 不晚于报告对应时点"], ["口径明确", "指标口径、期间与计算输入明确"], ["规则适用", "适用预设 deterministic scoring rule"], ["排除条件", "不需要 reviewer 额外业务推断或补写缺失定义"]])}
        <h3>Scoring Execution Levels</h3>
        {table(["Level", "Definition", "Current Use"], [[level, desc, "当前 3 个 formal tasks" if level == "L2_semi_automated" else "当前未纳入确定性分母"] for level, desc in scoring_data["execution_levels"].items()])}
        <h3>Claim Extraction Protocol</h3>
        <div class="callout"><code>report_excerpt</code> → <code>claim_quote</code> → <code>normalized_claim</code> → <code>extraction_note</code> → <code>verification source</code> → <code>judgment</code></div>
        {table(["规则", "说明"], [["不允许 reviewer 强化原文", "normalized_claim 只能做最小化核验规范化"], ["复合 claim 应拆分", "事实 claim 与叙事 claim 分开判定"], ["Narrative 不得改写为数字 claim", "避免 reviewer 创造被测对象没有说过的结论"], ["无法闭合必须降级", "进入 downgrade 或 backlog，而不是硬塞进 L2"]])}
        <h3>Traceability Rubric</h3>
        {table(["Rating", "标准"], [["Strong", "报告正文或直接引用提供具体来源、期间和可重建输入"], ["Partial", "来源与期间大致可识别，但缺少部分复算输入"], ["Weak", "报告只有泛化来源或结论，外部 reviewer 需自行重建证据路径"], ["Absent", "没有能够合理关联至该 claim 的来源信息"]])}
      </section>

      <section class="tab-panel" id="tab-improvements">
        <h2>Improvement Plan / 待改进项</h2>
        <h3>Improvement Findings Derived from Current Audit</h3>
        {table(["Finding", "Evidence from Audit", "Product Implication", "Suggested Improvement"], improvement_rows)}
        <h3>Proposed Evidence-Gate Rules</h3>
        {table(["Proposed Gate", "Trigger", "Required Output", "Current Status"], gate_rows)}
        <div class="callout">These are audit-derived improvement requirements, not implemented production controls in v1. 这些规则是由审查发现推导出的产品改进要求，不是 v1 已经实现的生产控制。</div>
        <h3>Next Evaluation Work</h3>
        {table(["下一步", "目的"], [["补齐 Investment Overview 剩余可核验 claims 的 source mapping", "扩大 NVDA 章节覆盖范围"], ["决定 B05/B06 是否可通过公开来源重新闭合", "验证 EBITDA 相关降级是否能重新进入评分"], ["为 B04/B10/B11 查找必要时点与输入来源", "处理 CAGR 与 valuation multiple 的 traceability 缺口"], ["完成 NVDA 更完整的 chapter-level audit 后扩展 COP / TSLA", "验证框架跨行业适用性"], ["v2 才开展 generation comparison", "避免把 proposed workflow 写成已验证结果"]])}
      </section>

      <section class="tab-panel" id="tab-implementation">
        <h2>Implementation / 代码与复现</h2>
        <h3>Implementation Map</h3>
        {table(["Capability", "Artifact", "Purpose"], implementation_rows)}
        <h3>Validation Status</h3>
        {table(["Check", "Status"], [["JSON parseability", chip("Passed", "passed")], ["L2 denominator reconstruction", chip("Passed", "passed")], ["Judgment count reconstruction", chip("Passed", "passed")], ["Traceability count reconstruction", chip("Passed", "passed")], ["Excluded claims isolation", chip("Passed", "passed")], ["Boundary wording check", chip("Passed", "passed")]])}
        <h3>Source Register Excerpt</h3>
        {code_block("evidence/nvda/primary_sources.md", "markdown", source_md_excerpt)}
        <h3>Code Tabs</h3>
        <div class="code-tabs" aria-label="Implementation code tabs">{code_tab_buttons}</div>
        {code_tab_panels}
      </section>
    </main>

    <footer>
      Canonical facts remain in JSON/Markdown. This HTML is a portfolio-facing case report / presentation layer, not a new source of audit judgments.
    </footer>
  </div>

  <script>
    const tabButtons = Array.from(document.querySelectorAll('.tab-button'));
    const tabPanels = Array.from(document.querySelectorAll('.tab-panel'));
    function activateTab(id, updateHash = true) {{
      tabButtons.forEach((button) => button.classList.toggle('active', button.dataset.tabTarget === id));
      tabPanels.forEach((panel) => panel.classList.toggle('active', panel.id === `tab-${{id}}`));
      if (updateHash) history.replaceState(null, '', `#${{id}}`);
    }}
    tabButtons.forEach((button) => {{
      button.addEventListener('click', () => activateTab(button.dataset.tabTarget));
    }});
    const initial = location.hash ? location.hash.slice(1) : 'overview';
    activateTab(tabButtons.some((button) => button.dataset.tabTarget === initial) ? initial : 'overview', false);

    const codeButtons = Array.from(document.querySelectorAll('.code-tab-button'));
    const codePanels = Array.from(document.querySelectorAll('.code-tab-panel'));
    codeButtons.forEach((button) => {{
      button.addEventListener('click', () => {{
        codeButtons.forEach((item) => item.classList.toggle('active', item === button));
        codePanels.forEach((panel) => panel.classList.toggle('active', panel.id === `code-${{button.dataset.codeTarget}}`));
      }});
    }});
    document.querySelectorAll('.copy-btn').forEach((button) => {{
      button.addEventListener('click', async () => {{
        const target = document.getElementById(button.dataset.copyTarget);
        if (!target) return;
        await navigator.clipboard.writeText(target.innerText);
        button.innerText = '已复制';
        setTimeout(() => {{ button.innerText = '复制'; }}, 1200);
      }});
    }});
  </script>
</body>
</html>
"""
    HTML_PATH.write_text(html_doc)
    print(HTML_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
