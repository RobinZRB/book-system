## Why

The v2 runtime prepares fast, complete evidence manifests, but its bundled book-user guidance asks for a concise response and does not require a visible investment-analysis sequence.  As a result, a capable evidence package can produce a much thinner answer than the legacy flow's Gate, red-flag investigation, and multi-dimension analysis.

## What Changes

- Add a structured, visible detailed-analysis presentation contract for investment and finance requests prepared through `user.analyze`.
- Require the analysis bundle to expose protocol-derived Gate steps, red-flag investigation results, dimensions, counter-evidence, external-fact gaps, and a traceable conclusion while preserving partial analysis.
- Preserve a concise mode for non-investment or explicitly brief requests; detailed investment analysis becomes the default when the user asks to analyse a stock, company, or investment opportunity.
- Add deterministic tests and behavioral evaluations that reject an investment answer which omits the Gate, triggered-risk disposition, or required dimension status.

## Capabilities

### New Capabilities

- `detailed-investment-analysis`: A user-facing, evidence-traceable analysis protocol that renders prepared investment context as Gate, risk investigation, multi-dimension analysis, and conclusion.

### Modified Capabilities

- `booksys-operations`: Prepared read-only analysis workspaces must carry enough structured protocol execution metadata to support detailed rendering without weakening the read-only or partial-analysis contract.
- `skill-distribution`: The book-user bundle must instruct supported harnesses to render the detailed investment-analysis contract and evaluate its completeness.

## Impact

- Affects `src/booksys/analysis_context.py`, `skills/book-user/resources/guidance.md`, tests, behavioral evaluations, and the `user.analyze` manifest schema.
- Does not alter book data, require result commits, or add network/data-provider dependencies.
