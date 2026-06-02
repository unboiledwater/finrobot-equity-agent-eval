# Public Financial Agent Output Audit Benchmark — Current Status Summary

## 1. Scope Statement

This benchmark evaluates the reliability of publicly available financial-agent outputs through claim-level evidence mapping and controlled judgment rules. It evaluates output quality; it does not deploy, rerun, or regenerate a financial Agent.

Current formal evidence-mapped findings are limited to selected claims from two FinRobot official public reports: NVDA as a partial deep pilot case and MSFT as a partial breadth-validation case. META, TSLA, and COP remain registered inventory-only candidates and are not included in current scored findings.

This summary does not constitute a complete FinRobot system evaluation and does not constitute a cross-system comparison.

## 2. Evaluated Artifact Status

| Sample ID | System | Company | Current Role | Audit Status | Current Coverage |
| --- | --- | --- | --- | --- | --- |
| FR-NVDA-001 | FinRobot | Nvidia | Partial deep pilot case | partial_audit_completed | Selected claims from Investment Overview only |
| FR-MSFT-001 | FinRobot | Microsoft | Partial breadth validation case | breadth_validation_partial_completed | Selected claims only |
| FR-META-001 | FinRobot | Meta | Registered candidate | inventory_only | Not audited |
| FR-TSLA-001 | FinRobot | Tesla | Reasoning-boundary candidate | inventory_only | Not audited |
| FR-COP-001 | FinRobot | ConocoPhillips | Sector-transfer candidate | inventory_only | Not audited |

## 3. Formal Findings Currently Available

| Sample | Audit Depth | Audited Claims | L2 Strictly Supported | Supported with Presentation Caveat | H1 / Backlog / Downgraded | Boundary |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| NVDA | Partial deep pilot audit | 8 | 2 | 1 | 5 | Not a full-report audit |
| MSFT | Partial breadth validation | 4 | 2 | 0 | 2 | Selected claims only |

NVDA currently shows `3/3 not contradicted` within the eligible L2 set: 2 strictly supported claims and 1 claim supported with a display-precision caveat. MSFT currently has 2 strictly supported L2 claims and 2 H1 / backlog claims. These counts are derived from the current canonical claim records and are not system-level accuracy rates.

## 4. Validated Failure Types So Far

| Failure Type | Observed In | Evidence Status | Product / Harness Implication |
| --- | --- | --- | --- |
| Weak claim-level traceability | NVDA B01/B02/B05/B06/B08/B04/B10/B11; MSFT M01/M02/M03/M04 | Validated | Historical financial claims should bind source document, period and evidence path. |
| Undisclosed display precision or truncation convention | NVDA B01 | Validated | Numeric presentation requires explicit precision / truncation treatment. |
| Derived metric definition not closed | NVDA B05/B06 | Validated | EBITDA and dependent margins require definition or reconciliation before deterministic scoring. |
| Forward valuation lacks reproducible dated inputs | NVDA B10/B11; MSFT M03 | Validated / Backlog | Forward multiples require as-of date, price basis and forecast provenance. |
| Narrative claim requires reasoning-boundary review | MSFT M04 | Validated / H1 | Numeric or contextual support must not automatically validate business inference. |

## 5. What This Benchmark Currently Demonstrates

- Claim-level audit protocol has been applied to one deep pilot case and one lightweight breadth-validation case.
- The framework separates strict factual support from presentation caveats, traceability weakness and human-review escalation.
- Derived metrics and forward-looking valuation claims are prevented from entering deterministic scoring when their evidence basis is not closed.
- The current results demonstrate early protocol transferability within FinRobot official public outputs.
- No current result establishes full-report reliability or cross-system generalization.

## Explicit Non-Claims

This summary does not claim that:

- all five FinRobot reports have been audited;
- the complete NVDA or MSFT reports have been audited;
- FinRobot as a system has been comprehensively evaluated;
- cross-system comparison has been completed;
- AlphaEngine, TradingAgents, FinRpt or any other external system has been formally included;
- agent traces, tool-use behavior or multi-agent coordination have been evaluated;
- production-grade enterprise controls have been implemented.

## 7. Next Candidate Expansion

| Candidate Direction | Candidate Artifact | Purpose | Current Status |
| --- | --- | --- | --- |
| Kimi-adjacent financial report output | AlphaEngine / FinGPT Agent public report, subject to source confirmation | Extend to industry-chain or strategic-transaction narrative audit | Not yet admitted |
| Multi-agent synthesis output | TradingAgents public AAPL outputs, subject to artifact confirmation | Extend to disagreement and decision-synthesis audit | Not yet admitted |
| Additional FinRobot sector case | TSLA or COP | Optional later sector / reasoning-boundary transfer check | Inventory only |

The candidate directions above are future candidates only. They are not included in the formal benchmark in this summary, and no evidence records or tasks are added for them in this iteration.
