# LLM Execution Modes

This project uses a layered LLM execution strategy for FinRobot and disclosure-material agent evaluation.

## Why Layering Is Needed

FinRobot report quality depends heavily on LLM-generated text sections. Disabling LLM output would remove one of the most important capabilities being evaluated.

Benchmark runs also need to be reproducible, bounded, and auditable. A single report may call the LLM several times, and thinking models can create long latency tails. The harness therefore separates connectivity checks, formal report generation, and deterministic scoring.

## Modes

| Mode | Use case | Kimi configuration | Rationale |
|---|---|---|---|
| Smoke test | Verify API key, base URL, and model name | `thinking: disabled`, `temperature=0.6`, small `max_tokens` | Fast and low cost. Does not assess report quality. |
| Formal report generation | Generate FinRobot research report text sections | `thinking: enabled`, `temperature=1.0`, `max_tokens=8192` | Preserves Kimi K2.6's reasoning strength while bounding latency. |
| Benchmark scoring | Score output against deterministic rubric | No LLM by default | Keeps scores reproducible and audit-friendly. |
| Expert review | Optional qualitative review | LLM optional, human override required | Useful for nuanced finance writing, but should not replace deterministic checks. |

## Observed Behavior

In the NVDA run, Kimi thinking mode successfully generated report sections, but some sections had long latency. One batch run stalled on `major_takeaways`; retrying that section alone with `max_tokens=8192` completed successfully.

The `news_summary.txt` section was intentionally filled with a data-availability note because the FMP news endpoint is restricted for the current API plan. This is preferable to fabricating news-driven catalysts.

## Harness Findings

- One valuation paragraph referenced a 2027 EBITDA figure inconsistent with the generated CSV table.
- FMP legacy endpoints in upstream FinRobot fail for new API keys.
- Some upstream error logs include full FMP URLs with API keys, requiring log redaction.
- Missing EV/EBITDA peer data and restricted news data should be disclosed in the report and evaluation output.

