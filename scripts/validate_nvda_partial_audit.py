#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "benchmark" / "report_audit_tasks.json"
CLAIMS_PATH = ROOT / "evidence" / "nvda" / "verified_claims.json"
REPORT_PATH = (
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
CASE_HTML_PATH = (
    ROOT
    / "reports"
    / "audit_outputs"
    / "official_report_audits"
    / "nvda_partial_audit_case_report.html"
)

EXPECTED_TASK_IDS = {
    "NVDA-INVOV-B01-REV-VALUES",
    "NVDA-INVOV-B02-REV-GROWTH",
    "NVDA-INVOV-B08-SGA-MARGIN",
}
EXPECTED_FORMAL_CANDIDATES = {"B01", "B02", "B08"}
EXPECTED_EXCLUDED = {"B05", "B06", "B04", "B10", "B11"}
FORBIDDEN_TEXT = [
    "NVDA report is accurate",
    "FinRobot produces accurate reports",
    "complete NVDA audit",
    "full NVDA report is accurate",
    "完整 NVDA audit 已完成",
    "FinRobot 整体可靠",
    "generation comparison 已完成",
    "enterprise controls 已实现",
    "生产控制已实现",
]


def load_json(path: Path):
    with path.open() as f:
        return json.load(f)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    tasks_data = load_json(TASKS_PATH)
    claims_data = load_json(CLAIMS_PATH)
    report = REPORT_PATH.read_text()
    html_report = HTML_PATH.read_text() if HTML_PATH.exists() else ""
    case_html_report = CASE_HTML_PATH.read_text() if CASE_HTML_PATH.exists() else ""

    formal_tasks = tasks_data["tasks"]
    formal_task_ids = {task["claim_id"] for task in formal_tasks}
    assert_true(len(formal_tasks) == 3, "formal L2 task count must be 3")
    assert_true(
        formal_task_ids == EXPECTED_TASK_IDS,
        f"formal task IDs mismatch: {sorted(formal_task_ids)}",
    )
    assert_true(
        set(tasks_data["eligible_pilot_candidates"]) == EXPECTED_FORMAL_CANDIDATES,
        "eligible pilot candidates must be B01/B02/B08",
    )

    claims = {item["candidate_id"]: item for item in claims_data["verified_claims"]}
    assert_true(EXPECTED_FORMAL_CANDIDATES <= set(claims), "missing formal candidates")
    assert_true(EXPECTED_EXCLUDED <= set(claims), "missing excluded/backlog candidates")

    l2_claims = [claims[c] for c in sorted(EXPECTED_FORMAL_CANDIDATES)]
    assert_true(
        all(item["substantive_judgment"] == "supported" for item in l2_claims),
        "all formal L2 claims must be supported",
    )
    assert_true(
        all(item["citation_traceability"] == "weak" for item in l2_claims),
        "all formal L2 claims must have weak report-level traceability",
    )
    assert_true(
        all(item["execution_level"] == "L2_semi_automated" for item in l2_claims),
        "all formal claims must be L2_semi_automated",
    )

    excluded_status = {claims[c]["review_status"] for c in EXPECTED_EXCLUDED}
    assert_true(
        excluded_status <= {"downgraded_not_formal_task", "backlog_not_formal_task"},
        f"unexpected excluded status: {excluded_status}",
    )
    assert_true(
        all(claims[c]["formal_task_id"] is None for c in EXPECTED_EXCLUDED),
        "excluded/backlog candidates must not have formal_task_id",
    )

    required_report_phrases = [
        "# NVDA Partial Audit Report — Investment Overview",
        "Status: Partial audit / in progress",
        "Coverage: Investment Overview section only",
        "Formal scored claims: 3 L2 tasks",
        "Excluded or deferred claims: 5 documented cases",
        "Not covered: full-report accuracy, cross-company results, generation comparison",
        "## 3. Eligibility Rules for Formal Scoring",
        "L2_SOURCE_CLOSURE_REQUIRED",
        "L2_DEPENDENT_METRIC_UNCLOSED",
        "B04",
        "B10",
        "B11",
        "Ambiguity Log References",
        "No additional extraction or judgment ambiguity was escalated",
    ]
    for phrase in required_report_phrases:
        assert_true(phrase in report, f"missing report phrase: {phrase}")

    for phrase in FORBIDDEN_TEXT:
        assert_true(phrase not in report, f"forbidden overclaim phrase found: {phrase}")
        if html_report:
            assert_true(phrase not in html_report, f"forbidden overclaim phrase found in HTML: {phrase}")
        if case_html_report:
            assert_true(
                phrase not in case_html_report,
                f"forbidden overclaim phrase found in case HTML: {phrase}",
            )

    if html_report:
        required_html_phrases = [
            "<title>NVDA Partial Audit Report",
            'lang="zh-CN"',
            "概览",
            "Claims 明细",
            "来源",
            "排除项",
            "校验",
            "代码映射",
            "主要功能与代码/数据映射",
            "分母限定为符合条件的 L2 tasks",
            "L2 合格集合内的实质准确率",
            "HTML 是面向人类阅读的展示层",
            "reports/audit_outputs/official_report_audits/nvda_partial_audit.md",
            "#F8F5FD",
            "#4D77A7",
            "#B2A4CF",
            "#84A7CD",
            "#FDE4E4",
            "#D4D4D4",
        ]
        for phrase in required_html_phrases:
            assert_true(phrase in html_report, f"missing HTML phrase: {phrase}")

    if case_html_report:
        required_case_html_phrases = [
            "<title>NVDA Partial Audit Case Report",
            'lang="zh-CN"',
            'data-tab-target="overview"',
            'data-tab-target="product-goal"',
            'data-tab-target="audit-results"',
            'data-tab-target="rubrics"',
            'data-tab-target="improvements"',
            'data-tab-target="implementation"',
            "Overview / 项目概览",
            "Product Goal / 服务目标",
            "Audit Results / 审查结果",
            "Rubrics &amp; Protocol / 评分与方法",
            "Improvement Plan / 待改进项",
            "Implementation / 代码与复现",
            'data-code-target="task-schema"',
            'data-code-target="verified-claim"',
            'data-code-target="validation-script"',
            "Product Requirement Statement",
            "Non-Goals / 当前不服务的目标",
            "Evaluation Dimensions",
            "L2 Eligibility Rules",
            "Scoring Execution Levels",
            "Traceability Rubric",
            "Implementation Map",
            "Proposed Evidence-Gate Rules",
            "These are audit-derived improvement requirements, not implemented production controls in v1.",
            "Eligible L2 Claims",
            "3 / 3",
            "Weak Report-Level Traceability",
            "B05",
            "B06",
            "B04",
            "B10",
            "B11",
            "nvda_partial_audit_case_report.html",
            "portfolio-facing case report / presentation layer",
        ]
        for phrase in required_case_html_phrases:
            assert_true(phrase in case_html_report, f"missing case HTML phrase: {phrase}")
        assert_true(
            'class="tab-panel active" id="tab-overview"' in case_html_report,
            "case HTML must default to Overview tab",
        )
        assert_true(
            "function activateTab" in case_html_report and "code-tab-panel active" in case_html_report,
            "case HTML must include real tab-switching behavior",
        )

    print("PASSED: NVDA partial audit validation")
    print("Validated artifacts:")
    print(f"- {TASKS_PATH.relative_to(ROOT)}")
    print(f"- {CLAIMS_PATH.relative_to(ROOT)}")
    print(f"- {REPORT_PATH.relative_to(ROOT)}")
    if html_report:
        print(f"- {HTML_PATH.relative_to(ROOT)}")
    if case_html_report:
        print(f"- {CASE_HTML_PATH.relative_to(ROOT)}")
    print("Validated metrics: L2 denominator, task IDs, supported count, traceability count, excluded-claim separation, report boundary text")


if __name__ == "__main__":
    main()
