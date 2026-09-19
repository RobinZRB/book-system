## Context

The current runtime already uses the active-stage pointer and canonical roots.  A small set of tests, health-check code, active documentation, and specifications still describes the completed transition through retired-version terminology.

## Goals / Non-Goals

**Goals:**

- Make non-OpenSpec runtime-facing material describe and verify the active v2 system positively.
- Keep coverage for the active pointer, strict package validation, runtime roots, bundled skill resources, and supported commands.

**Non-Goals:**

- Change package schemas, data locations, supported operations, or OpenSpec archive material.
- Add migration or compatibility behavior.

## Decisions

- Replace retired-surface assertions with positive contract tests.  Tests will assert valid active-stage resolution and enumerate the supported command surface instead of attempting former inputs.  This keeps observable v2 behavior covered without preserving old names in executable tests.
- Replace the residue scanner with a positive runtime-reference check.  The health check will validate that skills use local bundled resources and that the active pointer identifies v2, while strict `doctor` validates the package catalog.  A text blacklist would itself retain retired terminology.
- Rewrite active documentation and specifications to name canonical roots and supported operations.  Archived OpenSpec material is intentionally excluded because it records prior decisions.

Alternatives considered: retaining a blacklist of retired identifiers would catch reintroductions, but conflicts with the requested v2-only source vocabulary.  Retaining rejection tests would preserve old command names in executable code, so positive help-surface coverage is used instead.

## Risks / Trade-offs

- [A retired identifier could be reintroduced without a text blacklist] → Positive tests and the small CLI parser surface continue to cover supported behavior; future changes are reviewed against the v2-only specifications.
- [Documentation wording drifts from the parser] → The health check runs runtime tests and strict `doctor` on every full verification.

## Migration Plan

1. Update active specifications and non-OpenSpec source, tests, skill guidance, and documentation.
2. Run the full test suite, `check_all.py`, strict `doctor`, and a scoped non-OpenSpec vocabulary scan.
3. Archive the change after review if all checks pass.
