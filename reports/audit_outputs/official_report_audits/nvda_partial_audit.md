# NVDA Partial Audit Report — Investment Overview

Status: Partial audit / in progress  
Coverage: Investment Overview section only  
Formal scored claims: 3 L2 tasks  
Excluded or deferred claims: 5 documented cases  
Not covered: full-report accuracy, cross-company results, generation comparison

## 1. Audit Scope and Current Boundary

This artifact audits selected claims from the `Investment Overview` section of `finrobot_official_nvda`.

The denominator for deterministic scoring is limited to claims that satisfy the L2 eligibility rules in this report. The current `3/3 supported` result applies only to the three eligible L2 formal tasks listed below. It does not represent the accuracy or traceability of the complete NVDA report.

## 2. Evaluated Artifact and Source Register

Evaluated report:

- Report ID: `finrobot_official_nvda`
- Source file: `reports/source/official_examples/finrobot_official_nvda.html`
- Report timestamp: `2026-03-22 19:48`
- Audited section: `Company Overview / Investment Overview`

Primary sources used:

- `SRC-NVDA-FY2024-10K`: NVIDIA Form 10-K for fiscal year ended January 28, 2024, published 2024-02-21.
- `SRC-NVDA-FY2024-RESULTS`: NVIDIA fiscal 2024 results release, published 2024-02-21.
- `SRC-NVDA-FY2026-10K`: NVIDIA Form 10-K for fiscal year ended January 25, 2026, published 2026-02-25.
- `SRC-NVDA-FY2026-RESULTS`: NVIDIA fiscal 2026 results release, published 2026-02-25.

All listed sources were available before the FinRobot report timestamp.

## 3. Eligibility Rules for Formal Scoring

| L2 eligibility rule | Requirement |
| --- | --- |
| Claim type | Claim must be an independently verifiable numeric fact or reproducible calculation. |
| Original boundary | `claim_quote` must trace back to the report text without substantive rewriting. |
| Source closure | A primary source and evidence excerpt must be identified. |
| Temporal alignment | Verification source must be available before the report timestamp, with period and version status recorded. |
| Scoring method | Claim must map to a predefined deterministic rule and be marked `L2_semi_automated`. |
| Exclusion condition | Claims requiring additional metric-definition inference, missing source inputs, or missing valuation-date inputs cannot enter L2. |

## 4. Claim-Level Results: Eligible L2 Formal Tasks

| Task ID | Candidate | Claim quote | Substantive judgment | Report-level traceability | Execution |
| --- | --- | --- | --- | --- | --- |
| `NVDA-INVOV-B01-REV-VALUES` | `B01` | `revenue surging from $26.9 billion in FY2023 to $60.9 billion in FY2024` | supported | weak | L2 |
| `NVDA-INVOV-B02-REV-GROWTH` | `B02` | `representing a 125.9% year-over-year increase` | supported | weak | L2 |
| `NVDA-INVOV-B08-SGA-MARGIN` | `B08` | `SG&A as a percentage of revenue declining from 9% in FY2023 to just 2.1% in FY2026` | supported | weak | L2 |

## 5. Deterministic Score Summary

| Metric | Result |
| --- | --- |
| Total eligible L2 formal tasks | 3 |
| Supported | 3 |
| Contradicted | 0 |
| Unsupported | 0 |
| Substantive accuracy within eligible L2 set | 3/3 |

These results apply only to the three eligible L2 claims currently mapped from the `Investment Overview` section.

## 6. Report-Level Citation Traceability Summary

| Metric | Result |
| --- | --- |
| Strong traceability | 0 |
| Partial traceability | 0 |
| Weak traceability | 3 |
| Absent traceability | 0 |

The three L2 claims are substantively supported after evaluator-assisted source mapping, but the FinRobot report itself provides only a generic source footer and does not identify the exact filing, period, or calculation basis.

## 7. Rule-Based Downgrade Cases

Claims Excluded from Deterministic Scoring Due to Unclosed Primary-Source Verification.

| Candidate | Claim | Exclusion reason | Rule triggered | Re-entry condition |
| --- | --- | --- | --- | --- |
| `B05` | FY2024 EBITDA of `$35.6B` | EBITDA is not directly reported as a GAAP line item in the mapped primary source, and no reproducible EBITDA definition has been recorded. | `L2_SOURCE_CLOSURE_REQUIRED` | Add a disclosed EBITDA definition or a reproducible reconciliation with all inputs. |
| `B06` | FY2023/FY2024 EBITDA margin of `22.2%` and `58.4%` | EBITDA margin depends on the EBITDA definition from `B05`; without that definition, the numerator is not closed. | `L2_DEPENDENT_METRIC_UNCLOSED` | Close `B05` and verify the revenue denominator period alignment. |

These claims are documented in `verified_claims.json` as `downgraded_not_formal_task` and are not included in the deterministic accuracy denominator.

## 8. Traceability / Backlog Claims

| Candidate | Claim | Missing inputs | Current status |
| --- | --- | --- | --- |
| `B04` | `68.3% CAGR through FY2027` | Start period, endpoint, and source values for the CAGR calculation are not sufficiently specified. | `backlog_not_formal_task` |
| `B10` | EV/EBITDA of `43.5x` in FY2024 and `31.4x` in FY2026 | Dated market value, net debt or enterprise value basis, and EBITDA basis are missing. | `backlog_not_formal_task` |
| `B11` | FY2026E PE ratio of `37.7x` | Dated share price source and EPS estimate source are missing. | `backlog_not_formal_task` |

These claims may be revisited only after the missing inputs are mapped. They are not included in the deterministic accuracy denominator.

## 9. Ambiguity Log References

Existing ambiguity references:

- `AMB-NVDA-001`: CAGR period and endpoint ambiguity for `B04`.
- `AMB-NVDA-003`: EV/EBITDA valuation basis and source-alignment issue for `B10`.

No additional extraction or judgment ambiguity was escalated in this partial audit iteration. This section is retained for future protocol calibration and reviewer-agreement validation.

## 10. Validation Check

Validation script:

- `scripts/validate_nvda_partial_audit.py`

Validated artifacts:

- `benchmark/report_audit_tasks.json`
- `evidence/nvda/verified_claims.json`
- `reports/audit_outputs/official_report_audits/nvda_partial_audit.md`

Expected validation:

- L2 denominator: 3
- Formal task IDs: `NVDA-INVOV-B01-REV-VALUES`, `NVDA-INVOV-B02-REV-GROWTH`, `NVDA-INVOV-B08-SGA-MARGIN`
- Supported L2 claims: 3
- Weak traceability among L2 claims: 3
- Excluded/deferred candidates separated from denominator: `B05`, `B06`, `B04`, `B10`, `B11`

## 11. Next Claims To Map

Next NVDA work should focus on one of the following:

- resolve `B04` only if the CAGR start/end period and source values can be specified;
- map valuation inputs for `B10` or `B11` only if dated market price, estimate basis, and formula inputs are available;
- keep EBITDA-related claims excluded until a reproducible EBITDA definition is recorded.
