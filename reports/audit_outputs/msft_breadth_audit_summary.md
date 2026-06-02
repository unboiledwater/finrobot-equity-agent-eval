# MSFT Breadth Validation Summary

Status: breadth validation partial completed  
Evaluated artifact: `finrobot_official_msft`  
Sample ID: `FR-MSFT-001`  
Coverage: `Company Overview / Investment Overview` selected claims only  
Not covered: full-report audit, cross-company score, cross-system comparison

## 1. Boundary

This artifact is a lightweight breadth-validation check for the audit protocol. It does not represent a complete MSFT report audit and does not add MSFT to any five-company aggregate score.

FinRobot report text is the evaluated artifact, not a verification source. Official Microsoft disclosures and reproducible dated sources are the verification basis.

## 2. Claim-Level Results

| Candidate | Claim scope | Claim quote | Eligibility | Judgment | Traceability | Execution |
| --- | --- | --- | --- | --- | --- | --- |
| `M01` | fact | `FY24 revenue reaching $245.1 billion` | eligible_l2 | supported | weak | L2 |
| `M02` | calculation | `up 15.7% year-over-year` | eligible_l2 | supported | weak | L2 |
| `M03` | valuation | `EV/EBITDA valuation remains at a premium (23.6x for 2025E vs. Amazon’s 15.3x)` | not_eligible_h1_pending_dated_market_source | needs_human_review | weak | H1 |
| `M04` | inference | `Azure’s continued leadership in cloud infrastructure, expansion in AI-powered productivity tools (such as Copilot)` | not_eligible_h1_reasoning_boundary | needs_human_review | weak | H1 |

## 3. Lightweight Score Summary

| Metric | Result |
| --- | --- |
| Total extracted breadth-validation claims | 4 |
| Eligible L2 claims | 2 |
| Strictly supported L2 claims | 2 |
| Supported with presentation caveat | 0 |
| Contradicted | 0 |
| H1 / backlog claims | 2 |
| Strong report-level traceability | 0 |
| Weak report-level traceability | 4 |

These results apply only to the four selected claims above. They do not represent a complete MSFT report audit.

## 4. Source Register

Primary source:

- `SRC-MSFT-FY2024-10K`: Microsoft Corporation Form 10-K for fiscal year ended June 30, 2024, published 2024-07-30, available before the FinRobot report timestamp.
- `SRC-MSFT-FY2024-IR`: Microsoft Investor Relations annual report source, available before the FinRobot report timestamp.

Source-mapped findings:

- FY2024 revenue was `$245,122 million`, which supports the report's `$245.1 billion` display.
- FY2023 revenue was `$211,915 million`; `(245,122 - 211,915) / 211,915 = 15.7%` when rounded to one decimal place.
- Microsoft Cloud revenue increased `23%` to `$137.4 billion`; Azure and other cloud services revenue increased `29%`, including `8 points` from AI services.

## 5. Excluded / H1 Cases

`M03` is not L2 eligible because forward EV/EBITDA requires a dated enterprise value, net debt or EV basis, EBITDA estimate basis, and peer-source provenance.

`M04` is not L2 eligible because the report's cloud and AI statement includes analytical leadership and growth-driver framing. Public disclosures provide contextual support for cloud and AI relevance, but not a deterministic score for the complete narrative claim.

## 6. Next Step

MSFT can be expanded only after additional primary-source mapping is completed. Until then, this file should be cited as `breadth_validation_partial_completed`, not a complete-report audit status.
