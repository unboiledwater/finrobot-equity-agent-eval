# Planned V2: Baseline vs Evidence-Gated Generation

V2 is not part of the completed V1 audit benchmark.

## Purpose

Compare a baseline generation workflow with an evidence-gated generation workflow after the local generation path is stable and outputs are saved.

## Boundary

Until real baseline and gated outputs exist, the project must not claim:

- Evidence Gate improved accuracy.
- Evidence Gate reduced human review cost.
- The generation harness is production-ready.

## Planned Metrics

- Substantive accuracy.
- Report-level traceability.
- Unsupported inference rate.
- Task completion rate.
- Human review modification count.

Final correctness scoring should remain rule-based or manually auditable. LLMs may assist with summaries, initial error classification, and candidate failure discovery, but not final correctness decisions.
