# Source and Temporal Alignment Rules

V1 verifies FinRobot report claims against sources that were available at or before the report date.

## Allowed Verification Sources

- Company annual reports and 10-K filings.
- Quarterly reports and 10-Q filings.
- Earnings releases.
- Investor presentations.
- SEC filings.
- Publicly reproducible market data with an explicit date.

The evaluator does not infer or reconstruct inaccessible proprietary data sources.

## Temporal Rules

1. Do not use later data to contradict a report unless the task explicitly tests hindsight or revision mismatch.
2. Record the report generation timestamp when available.
3. Record publication date and as-of period for every verification source.
4. Mark whether the source was available before the report date.
5. Mark restated or preliminary data explicitly.

## Market Data Rules

Market price, market cap, forward multiple, consensus, and target-price claims require a dated reproducible source. If the report does not disclose the date or source and no public dated source can be reconstructed, the claim moves to `H1_human_review`.
