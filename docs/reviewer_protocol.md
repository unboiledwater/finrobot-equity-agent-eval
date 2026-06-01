# Reviewer Protocol

## Objective

Review FinRobot official reports as evaluated artifacts. Do not treat them as ground truth.

## Claim Extraction

1. Select the original report passage as `report_excerpt`.
2. Quote the smallest verifiable phrase as `claim_quote`.
3. Use `normalized_claim` only when necessary for verification.
4. Explain every split or normalization in `extraction_note`.
5. Do not strengthen narrative language into a stronger factual claim.

## Judgment

Score `substantive_judgment` separately from `citation_traceability`.

A claim can be substantively supported while still having weak report-level traceability. That condition should be recorded, not collapsed into a factual error.

## Execution Levels

Use `L1` or `L2` only when inputs, period, and source basis are sufficiently reproducible. Use `L3` for fixed-rule manual checks. Use `H1` for peer, risk, materiality, and inference-boundary judgments.

## Ambiguity Logging

Record ambiguous decisions in `pilot/ambiguity_log.md`. Do not use a single-reviewer pilot to claim inter-reviewer agreement.
