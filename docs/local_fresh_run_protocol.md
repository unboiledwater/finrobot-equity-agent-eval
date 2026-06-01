# Local Fresh-Run Protocol

Local FinRobot fresh-runs are supplementary report artifacts. They do not replace the official FinRobot report sample used in V1.

## Purpose

Use timestamped local outputs to test whether the same claim-level audit protocol works on newly generated reports. Local runs also prepare future V2 controlled generation comparison.

V1 must not claim that local fresh-runs prove FinRobot improved or degraded over time. Official examples and local runs may differ by code version, model, prompt, data provider response, peer set, and market timing.

## Required Provenance

Every local report must have a manifest before entering supplementary audit. The manifest records:

- run id, ticker, company name, and generation timestamp
- FinRobot repository, release, and commit
- generation mode, model provider, and model name
- financial data provider and data retrieval timestamp
- peer tickers
- output file paths and hashes
- known limitations

FMP data is treated as generation input provenance, not final verification ground truth. Local report claims remain subject to primary-source verification.

## Directory Boundary

```text
reports/local_runs/metadata/   run manifests and manifest schema
reports/local_runs/outputs/    generated reports and intermediate non-sensitive outputs
```

Do not store local fresh-run outputs in `reports/source/official_examples/`.

## Safety Controls

- Run in an isolated virtual environment or container.
- Use least-privilege API keys.
- Do not mount unrelated personal directories.
- Run only the equity report generation path.
- Redact API keys, request URLs, config files, and sensitive logs before committing artifacts.

## First Targets

The first local fresh-run target is NVDA. COP may be added after NVDA. V1 should not expand to companies outside the official five-report sample.

## Entry Into Supplementary Audit

A local fresh-run may enter supplementary audit only when:

1. the generated report is saved;
2. the run manifest is complete;
3. sensitive data has been removed;
4. the report is audited with the same claim-level protocol used for official reports.
