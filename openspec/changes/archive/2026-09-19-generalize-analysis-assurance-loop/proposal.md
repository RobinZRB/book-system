## Why

The current detailed analysis contract is investment-specific: its manifest
contains fixed financial risk and valuation dimensions, and non-investment
requests normally receive only concise guidance. This prevents a management,
psychology, technical, or historical book from providing the same auditable
distinction among framework evidence, current evidence, alternative
explanations, uncertainty, and inference.

The system needs one domain-neutral assurance loop that lets each book supply
the analytical lens without treating every analysis as an investment decision
or inventing domain facts.

## What Changes

- Add a generic framework-analysis assurance contract to every `user.analyze`
  workspace, with an applicability check, evidence plan and quality records,
  protocol-derived dimensions, explicit alternative explanations, and
  uncertainty/coverage diagnostics.
- Let callers optionally supply a decision contract and evidence items for any
  domain. Preserve their provenance, freshness, conflicts, and uncertainty;
  do not require external research for interpretive or book-only questions.
- Replace the investment-only presentation outline in book-user guidance with
  a universal visible loop. Make detailed rendering request-aware, while
  retaining a light path for straightforward explanatory and narrative-book
  questions.
- Keep the investment protocol and external-fact package backward compatible:
  investment red flags, source tiers, and current-fact research become a
  domain adapter layered on the generic contract rather than being removed.
- Add deterministic and behavioral coverage for non-investment decision,
  diagnostic, and interpretive analyses, including alternative explanations,
  missing evidence, and no-applicability cases.

## Capabilities

### New Capabilities

- `framework-analysis-assurance`: A domain-neutral, evidence-to-conclusion
  analysis loop that selected book protocols can populate without hard-coded
  investment dimensions.

### Modified Capabilities

- `booksys-operations`: `user.analyze` workspaces expose the generic
  assurance plan and accept optional domain-neutral decision and evidence
  inputs while preserving the current investment fields.
- `detailed-investment-analysis`: Investment presentation remains detailed and
  retains its existing disclosures as a specialization of the generic loop.
- `external-fact-research`: The research-plan contract becomes
  domain-neutral and supports evidence-quality and uncertainty records without
  relaxing its investment source-tier rules.
- `skill-distribution`: Book-user guidance selects the universal or light
  presentation path and clearly separates book evidence, external evidence,
  and inference in every domain.

## Impact

Primary changes affect `src/booksys/analysis_context.py`, the book-user
guidance and bundled protocols, associated analysis-context tests and
behavioral evaluations, plus the listed OpenSpec specifications. The public
`user.analyze` manifest gains additive fields; existing investment clients and
their field names remain supported. No package data, learning state, or
network provider is added.
