# MSFT Primary Sources

## Report Under Audit

- `report_id`: `finrobot_official_msft`
- `sample_id`: `FR-MSFT-001`
- `source_file`: `reports/source/official_examples/finrobot_official_msft.html`
- `report_generated`: `2026-03-22 20:05`
- `audited_section`: `Company Overview / Investment Overview`
- `audit_status`: `breadth_validation_partial_completed`

## Primary Sources Used

### SRC-MSFT-FY2024-10K

- Source Provider: SEC EDGAR
- Document type: Form 10-K / Annual Report
- Document title: Microsoft Corporation Form 10-K for fiscal year ended June 30, 2024
- Publication date: 2024-07-30
- As-of period: Fiscal years ended June 30, 2024 and June 30, 2023
- Available before report date: true
- Source priority: primary
- URL: https://www.sec.gov/Archives/edgar/data/789019/000095017024087843/msft-20240630.htm

Evidence excerpts:

- Consolidated statements of income report revenue of `$245,122 million` for fiscal 2024 and `$211,915 million` for fiscal 2023.
- Management discussion reports total revenue increased by `$33.2 billion` or `16%`, driven by growth in Productivity and Business Processes, Intelligent Cloud, and More Personal Computing.
- Microsoft Cloud revenue increased `23%` to `$137.4 billion`.
- Azure and other cloud services revenue increased `29%`, including `8 points` from AI services.

### SRC-MSFT-FY2024-IR

- Source Provider: Microsoft Investor Relations
- Document type: Annual report landing page / investor relations source
- Document title: Microsoft 2024 Annual Report
- Publication date: 2024-07-30
- As-of period: Fiscal 2024
- Available before report date: true
- Source priority: primary
- URL: https://www.microsoft.com/en-us/investor/annual-reports

Evidence excerpts:

- Microsoft investor relations hosts the annual report package used as a public-company disclosure source.

## Source Boundary Notes

- FinRobot report text is the evaluated artifact, not a verification source.
- Generic report footer text such as `Company Filings, FMP, Yahoo Finance, AI4Finance Estimates` is not treated as claim-level evidence.
- Forward valuation claims require dated market data, estimate provenance, and calculation basis before entering deterministic scoring.
- AI, cloud, and competitive-leadership narrative claims are recorded as boundary-review items unless a claim is narrowed to a source-mapped factual statement.
