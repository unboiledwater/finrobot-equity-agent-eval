# Report Audit Benchmark for AI-Generated Equity Research Reports

This project evaluates real AI-generated equity research reports through claim-level evidence verification, deterministic scoring, and auditable error analysis.

FinRobot reports are evaluated artifacts, not ground truth. Public company disclosures, regulatory filings, investor materials, and reproducible dated market data serve as verification sources.

## V1 Scope

V1 is a **Report Audit Benchmark**. It does not require locally rerunning FinRobot, and it does not claim that an evidence-gated generation workflow has improved report quality.

| Question | V1 answer |
| --- | --- |
| What is evaluated? | AI-generated equity research report claims. |
| Which reports? | Five official FinRobot equity reports: NVDA, MSFT, META, TSLA, and COP. |
| What is the source of truth? | Public company disclosures, SEC filings, annual reports, earnings materials, investor presentations, and reproducible market data. |
| What is produced? | Report inventory, claim-level tasks, scoring rules, error inventory, benchmark mapping, and audit reports. |
| What is current vs planned? | V1 audits official reports. Local fresh-runs are supplementary. V2 baseline vs evidence-gated generation comparison is planned separately. |

## Why This Exists

Polished financial prose is not enough for professional use. A reliable financial Agent output must be checkable:

- Does the claim preserve the original report wording and boundary?
- Is the number, unit, period, and calculation correct?
- Was the verification source available at the report date?
- Does the report itself provide enough citation detail for independent review?
- Is the statement a disclosed fact, a calculation, an inference, or a judgment requiring human review?

The project turns these questions into reusable evaluation assets instead of treating report quality as a broad subjective judgment.

## Evaluated Artifacts

The evaluated artifacts are separated into three classes:

| Artifact class | Role |
| --- | --- |
| Core Audit Set | Five official FinRobot reports used as the V1 benchmark sample. |
| Supplementary Fresh-Run Set | Locally generated FinRobot reports with run provenance, used only to test protocol portability. |
| Planned Comparative Set | Future baseline vs evidence-gated generation outputs for V2. |

The five official FinRobot HTML reports are stored under `reports/source/official_examples/`:

- `reports/source/official_examples/finrobot_official_nvda.html`
- `reports/source/official_examples/finrobot_official_msft.html`
- `reports/source/official_examples/finrobot_official_meta.html`
- `reports/source/official_examples/finrobot_official_tsla.html`
- `reports/source/official_examples/finrobot_official_cop.html`

Each report has a common section structure: Investment Thesis, Company Overview, Financial Analysis, Valuation Analysis, Recent News & Events, Sensitivity Analysis, Key Catalysts, Technical & Advanced Analysis, Competitive Landscape, and Financial Data.

The reports use generic source footers such as `Company Filings, FMP, Yahoo Finance, AI4Finance Estimates`. That footer is not treated as claim-level evidence.

Local fresh-runs, if generated, are stored under `reports/local_runs/` and must include a manifest before entering supplementary audit. They do not replace the official report sample and are not used to claim FinRobot improved or degraded over time.

## Methodology

V1 keeps the audit object tied to the original report text:

- `report_excerpt`: full original report passage.
- `claim_quote`: the smallest directly quoted verifiable phrase.
- `normalized_claim`: minimal normalization needed for verification.
- `extraction_note`: why any split, completion, or normalization was made.

The benchmark separates three review dimensions:

- `substantive_accuracy`: whether the claim is supported, contradicted, unsupported, or requires human review.
- `report_level_traceability`: whether the report itself provides enough citation detail.
- `evaluator_assisted_verifiability`: whether the evaluator can reconstruct the evidence path from public sources.

This distinction matters: a historical number can be substantively correct while still having weak report-level traceability.

## Scoring Levels

Deterministic scoring means the rule is fixed and repeatable. It does not always mean the process is fully automated.

| Level | Meaning | V1 use |
| --- | --- | --- |
| `L1_automated` | Script can directly judge structured values. | Standardized numeric fields and simple consistency checks. |
| `L2_semi_automated` | Script recomputes or compares values; reviewer confirms source and basis. | Most financial figures, percentages, margins, and multiples. |
| `L3_rule_based_manual` | Reviewer follows fixed rules and records evidence. | Period alignment, source timing, complex disclosure matching. |
| `H1_human_review` | Judgment is reviewed but excluded from deterministic accuracy. | Peer defensibility, risk materiality, overstatement, investment thesis support. |

Claims with weak or absent traceability may be excluded from L1/L2 accuracy depending on claim type. Market price, market cap, forward multiple, consensus, target price, peer comparison, and forward-looking claims require dated and reproducible sources before entering deterministic scoring.

## Single-Reviewer Boundary

V1 does not claim inter-reviewer agreement. During the single-reviewer stage, ambiguous cases are recorded in `pilot/ambiguity_log.md` for later reviewer calibration.

The ambiguity log captures segmentation, normalization, source alignment, tolerance, judgment, and scoring-level disputes. This prevents uncertain decisions from disappearing into free-form notes.

## Project Layout

```text
reports/source/official_examples/      Official FinRobot reports being audited
reports/local_runs/metadata/           Local fresh-run manifests and schemas
reports/local_runs/outputs/            Locally generated supplementary reports
reports/report_inventory.json          Source, date, section, and claim-density inventory
benchmark/taxonomy.md                  Claim scope, segmentation, judgment, and failure taxonomy
benchmark/scoring_rules.json           Scoring levels, traceability gates, and tolerance rules
benchmark/report_audit_tasks.json      V1 claim-level benchmark tasks
pilot/                                 NVDA segmentation pilot and ambiguity log
evidence/                              Primary-source maps and verified claims by ticker
reports/audit_outputs/official_report_audits/          Official report audits
reports/audit_outputs/local_run_supplementary_audits/  Supplementary fresh-run audits
planned_v2/                            Baseline vs evidence-gated generation experiment plan
```

## Current Implementation Boundary

V1 does not claim:

- local FinRobot generation is required for the audit benchmark
- local fresh-runs replace the official report core sample
- local fresh-runs prove FinRobot improved or degraded over time
- Evidence Gate has already improved generated report quality
- FinRobot internal generation traces are available
- tenant isolation, permission-scope injection, redaction, or production audit logging are implemented

Enterprise controls remain an extension design topic until executable tests are added. FMP data used in local generation is input provenance, not final verification ground truth.

## Current Artifacts

Current completed artifact status:

- NVDA partial audit status: `partial audit / in progress`.
- Coverage: `Investment Overview` section only.
- Formal scored claims: 3 L2 tasks.
- Excluded or deferred claims: 5 documented cases.
- Canonical Markdown audit artifact: `reports/audit_outputs/official_report_audits/nvda_partial_audit.md`.
- Human-readable HTML rendering: `reports/audit_outputs/official_report_audits/nvda_partial_audit.html`.
- Portfolio-facing case report / presentation layer: `reports/audit_outputs/official_report_audits/nvda_partial_audit_case_report.html`.
- Structured evidence map: `evidence/nvda/verified_claims.json`.
- Validation script: `scripts/validate_nvda_partial_audit.py`.

The current NVDA artifact does not represent a complete NVDA report audit or a full FinRobot reliability conclusion.

## V2 Planned Extension

V2 will compare baseline generation against an evidence-gated generation workflow only after the generation path is stable and outputs are saved. Until then, V2 results are not represented as completed findings.
