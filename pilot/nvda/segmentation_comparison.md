# NVDA Segmentation Comparison

## Pilot Scope

- Source: `finrobot_official_nvda`
- Section: `Company Overview / Investment Overview`
- Goal: compare intuitive extraction with rule-based extraction before creating formal benchmark tasks.

## Round A Findings

Round A produced 8 broad candidate claims. It was fast, but several candidates were not safe for formal scoring:

- revenue values and growth percentage were bundled into one claim;
- forward estimates were mixed with CAGR calculation and vague consensus sourcing;
- historical margins were mixed with FY2027 projections;
- one extraction strengthened the report's wording from "operational leverage is evident" into "proving operational leverage";
- valuation multiples lacked dated source basis but initially appeared numeric and scorable.

## Round B Findings

Round B produced 12 more precise candidate claims by preserving quote boundaries and separating fact, calculation, valuation, comparison, and inference.

Eligible for formal task draft:

- `B01`: FY2023/FY2024 revenue values.
- `B02`: FY2024 YoY revenue growth calculation.
- `B05`: FY2024 EBITDA value.
- `B06`: FY2023/FY2024 EBITDA margin values.
- `B08`: FY2023/FY2026 SG&A margin values, subject to source-period verification.

Needs ambiguity resolution before task entry:

- `B04`: "68.3% CAGR through FY2027" conflicts with quoted FY2025/FY2026 endpoints.

Human review or backlog:

- `B03`, `B10`, `B11`: forward estimates or valuation multiples require dated reproducible source basis.
- `B07`, `B09`, `B12`: causal, peer, or forward-looking inference claims should not enter deterministic accuracy.

## Rule Changes Confirmed

The pilot confirms these rules are necessary:

1. Do not let a single sentence become one composite benchmark task.
2. Separate historical facts from forward estimates.
3. Separate numeric facts from analytical justification.
4. Route valuation multiples without dated source basis to H1 or backlog.
5. Log ambiguous calculation periods before creating formal benchmark tasks.

## Next Step

Create formal NVDA tasks from `B01`, `B02`, `B05`, `B06`, and possibly `B08` after primary-source mapping. Keep `B04` in ambiguity review until the CAGR period is resolved.
