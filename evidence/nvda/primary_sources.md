# NVDA Primary Sources

## Report Under Audit

- `report_id`: `finrobot_official_nvda`
- `source_file`: `reports/source/official_examples/finrobot_official_nvda.html`
- `report_generated`: `2026-03-22 19:48`
- `audited_section`: `Company Overview / Investment Overview`

## Primary Sources Used

### SRC-NVDA-FY2024-10K

- Document type: Form 10-K / Annual Report
- Document title: NVIDIA Corporation Form 10-K for fiscal year ended January 28, 2024
- Publication date: 2024-02-21
- As-of period: Fiscal years ended January 28, 2024 and January 29, 2023
- Available before report date: true
- Source priority: primary
- URL: https://fintel.io/doc/sec-nvidia-corp-1045810-10k-2024-february-21-19774-1729

Evidence excerpts:

- Results of operations table: revenue was `$60,922 million` for year ended January 28, 2024 and `$26,974 million` for year ended January 29, 2023.
- Same table reports total revenue change of `$33,948 million` and `126%`.
- Common-size income statement reports sales, general and administrative expense as `4.4%` of revenue for fiscal 2024 and `9.1%` for fiscal 2023.

### SRC-NVDA-FY2024-RESULTS

- Document type: Earnings release
- Document title: NVIDIA Announces Financial Results for Fourth Quarter and Fiscal 2024
- Publication date: 2024-02-21
- As-of period: Fiscal 2024 and fiscal 2023
- Available before report date: true
- Source priority: primary
- URL: https://investor.nvidia.com/news/press-release-details/2024/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2024/

Evidence excerpts:

- Fiscal 2024 summary reports GAAP revenue of `$60,922 million` for FY24 and `$26,974 million` for FY23, up `126%`.
- The release states fiscal 2024 revenue was up 126% to `$60.9 billion`.

### SRC-NVDA-FY2026-10K

- Document type: Form 10-K / Annual Report
- Document title: NVIDIA Corporation Form 10-K for fiscal year ended January 25, 2026
- Publication date: 2026-02-25
- As-of period: Fiscal years ended January 25, 2026, January 26, 2025, and January 28, 2024
- Available before report date: true
- Source priority: primary
- URL: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm

Evidence excerpts:

- Consolidated statements of income report revenue of `$215,938 million` for year ended January 25, 2026.
- The same statement reports sales, general and administrative expense of `$4,579 million` for year ended January 25, 2026.

### SRC-NVDA-FY2026-RESULTS

- Document type: Earnings release exhibit
- Document title: NVIDIA Announces Financial Results for Fourth Quarter and Fiscal 2026
- Publication date: 2026-02-25
- As-of period: Fiscal 2026 and fiscal 2025
- Available before report date: true
- Source priority: primary
- URL: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26pr.htm

Evidence excerpts:

- Fiscal 2026 summary reports revenue of `$215,938 million` for FY26 and `$130,497 million` for FY25, up `65%`.

## Source Boundary Notes

- FMP and FinRobot report tables are not treated as final verification ground truth.
- EBITDA is not directly reported as a GAAP line item in the mapped primary sources above. EBITDA-related pilot claims are therefore not promoted to L2 formal tasks unless a reproducible EBITDA definition and source inputs are added later.
- The official FinRobot report provides only a generic footer for source attribution, so report-level traceability is weak even when a claim is substantively supported by primary sources.
