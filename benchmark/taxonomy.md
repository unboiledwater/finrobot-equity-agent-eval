# Report Audit Taxonomy

This taxonomy defines how claims are extracted and judged in V1.

## Claim Scope

- `fact`: A disclosed historical fact or directly reported figure.
- `calculation`: A value derived from disclosed or market inputs.
- `valuation`: A valuation multiple, range, market-cap statement, or forward estimate.
- `comparison`: A peer, industry, or cross-period comparison.
- `inference`: An analytical conclusion that goes beyond the source text.
- `risk_disclosure`: A risk statement, materiality judgment, or downside scenario.

## Segmentation Rules

1. Preserve the original `report_excerpt`.
2. Use `claim_quote` for the smallest directly quoted verifiable phrase.
3. Use `normalized_claim` only for minimal verification normalization.
4. Record every split, completion, or normalization in `extraction_note`.
5. Do not convert narrative language into a stronger factual claim.
6. Split compound sentences into separate tasks only when each claim can be independently verified.

## Claim Atomicity

- `atomic`: One verifiable claim.
- `composite`: Multiple claims that must be split or marked as not directly scorable.
- `narrative`: Framing or analysis that should not be forced into numeric verification.

## Judgment Labels

- `supported`: The claim is substantively supported by temporally aligned evidence.
- `contradicted`: The claim conflicts with temporally aligned evidence or reproducible calculation.
- `unsupported`: The claim lacks adequate basis for its stated certainty.
- `needs_human_review`: The claim requires materiality, comparability, or analytical judgment and is excluded from deterministic accuracy.

## Traceability Labels

- `strong`: Report identifies source, date or period, and enough detail to reproduce the claim.
- `partial`: Report identifies a source family but misses some date, period, or calculation detail.
- `weak`: Report gives only generic source attribution; evaluator can reconstruct evidence externally.
- `absent`: No usable source trail is provided.
- `not_applicable`: Citation is not applicable to the claim type.

## Failure Types

- `numeric_error`
- `unit_error`
- `period_mismatch`
- `calculation_error`
- `source_missing`
- `source_timing_mismatch`
- `citation_traceability_weak`
- `valuation_basis_missing`
- `peer_defensibility_issue`
- `overstated_inference`
- `risk_materiality_review`
- `section_inconsistency`
