## Context

See `proposal.md` for motivation. `user.analyze` currently creates one
`analysis_plan` from selected evidence and section states. Its Gate, risk
definitions, dimensions, default detailed mode, and research fields are
hard-coded around investment; other protocols receive only the generic
selection and evidence inventory. The book-user guidance similarly makes the
investment outline its only detailed presentation contract.

The runtime must remain deterministic and read-only. It already preserves
selection reasons, matched/unmatched protocol sections, source identity,
freshness, conflicts, and missing external investment facts. Existing callers
and investment behavioral tests consume the current `analysis_plan` fields.

## Goals / Non-Goals

**Goals:**

- Add a generic, testable assurance model without changing existing investment
  manifest fields or source-tier behavior.
- Let selected protocol sections, rather than a fixed category taxonomy,
  provide the default dimensions for non-investment analysis.
- Make evidence quality, alternatives, gaps, and applicability explicit even
  when no external research is available or appropriate.
- Keep light explanatory and narrative analysis proportionate.

**Non-Goals:**

- Generate a final answer, score a book, or make a recommendation in the
  deterministic runtime.
- Require external research, a decision contract, monitoring, or quantitative
  methods for every book question.
- Redesign package profiles or force every protocol to expose identical
  dimensions, risk triggers, or evidence sources.
- Replace investment-specific external-fact validation with a weaker generic
  schema.

## Decisions

### Add an additive `assurance` object inside `analysis_plan`

Retain the manifest schema version and all current top-level `analysis_plan`
keys. Add `analysis_plan.assurance` with a versioned, stable shape:

```json
{
  "analysis_kind": "interpretive|diagnostic|decision_support",
  "sequence": ["decision_contract", "applicability", "evidence_quality", "dimensions", "challenge", "uncertainty", "conclusion_trace", "review"],
  "decision_contract": {"status": "provided|unspecified", "value": {}},
  "applicability": {"status": "applicable|partly_applicable|unassessed", "reasons": []},
  "evidence_quality": [],
  "dimensions": [],
  "challenges": {"escalations": [], "alternatives": [], "gaps": [], "conflicts": []},
  "conclusion_requirements": [],
  "review": {"status": "not_required|unassessed|configured", "triggers": []}
}
```

The representation uses explicit states rather than verdicts. This lets
non-investment consumers use one contract while old investment consumers keep
reading `sequence`, `gate`, `red_flags`, `dimensions`, `counter_evidence`, and
`missing_external_facts`. A separate top-level plan would be clearer in
isolation, but nesting avoids two unrelated planning APIs and provides a
natural migration path.

### Use protocol-section state as the generic dimension source

Build generic dimensions from selected books' `protocol_sections`, preserving
the protocol section identity, title, matched/unmatched status, evidence
count, and contributing book. Deduplicate stable identities across books but
do not merge their evidence. A protocol can later enrich these dimensions with
metadata; absent such metadata, the runtime uses the section inventory rather
than guessing a domain taxonomy.

Investment-specific dimensions remain unchanged and are cross-linked to the
generic records. Copying the existing fixed dimensions to every category was
rejected because it would leak financial semantics into unrelated books;
parsing arbitrary prose headings to infer risks was rejected because it would
make preparation nondeterministic.

### Accept separate generic evidence and decision inputs

Add optional request fields:

- `decision_contract`: a JSON object retained as caller input after bounded
  structural validation; absent fields stay unspecified.
- `analysis_evidence`: a list of generic evidence records. Each record carries
  an identifier or field, value/claim, framework links, source identity,
  retrieval and applicable dates when available, source class, and verification
  state. Missing provenance remains a diagnostic, not an error repair.
- `review_triggers`: an optional list of observable invalidation or review
  conditions linked to a framework item.

Normalize generic evidence into an `analysis_evidence_package` with records
and diagnostics. Keep `external_fact_package` unchanged, and expose its facts
as linked records in the generic evidence-quality view rather than converting
or overwriting them. Reusing `external_facts` for every type of evidence was
rejected because its financial field and source-tier semantics are already a
compatibility contract.

### Make the universal presentation a guidance contract, with a light route

Guidance will render the assurance sequence for framework application,
diagnosis, and decision-support requests. A pure interpretation or a
narrative-book question can use a light route: applicability, relevant text
evidence, interpretation/inference label, alternatives or limits if material,
and bounded conclusion. The guidance will treat alternatives, escalation
signals, and gaps as cross-cutting records, not as a serial checklist after
the analysis.

An explicit decision contract selects decision-support behavior. Otherwise
the plan chooses an interpretive route for static/narrative protocols and a
diagnostic route for applicable analytical protocols. Investment's current
detailed default remains an explicit adapter override. Making every question
detailed was rejected because it harms ordinary book use and adds empty fields.

### Generalize research planning without prescribing research execution

The deterministic runtime derives generic plan-linked evidence requirements
only when a selected protocol, decision contract, escalation item, or caller
request names them. Each requirement records why it matters and the effect of
missing it. Source class is descriptive for generic evidence; investment
retains its strict `primary`, `secondary`, and `unverified_caller` rules.

No network fetcher is introduced. Guidance continues to orchestrate research
outside preparation and reinjects validated inputs. This preserves current
read-only, offline, and latency guarantees.

## Risks / Trade-offs

- [Some protocols have broad or weak section names] → preserve their source
  identity and allow `unassessed`; do not invent fine-grained dimensions.
- [The additive plan can duplicate investment state] → cross-link records and
  retain legacy fields until a separately approved major-version migration.
- [Generic evidence becomes an unbounded fact dump] → require framework links
  for plan-required evidence and label unlinked caller evidence as contextual,
  not required support.
- [Automatic analysis-kind routing misclassifies an edge case] → accept an
  explicit caller override and expose the resolved kind in the manifest.
- [More records affect preparation latency] → derive only compact metadata
  from existing inventories and keep the existing warm-run regression budget.

## Migration Plan

1. Add the generic request normalizers and additive assurance/evidence package
   to `user.analyze`, retaining all current output fields.
2. Route generic dimensions from protocol-section states; adapt investment
   records into the generic view without altering their legacy values.
3. Update bundled guidance and protocol templates to consume the assurance
   object and render the light route when appropriate.
4. Add deterministic, integration, and behavioral tests for generic requests;
   run the existing investment suite to verify compatibility.
5. Release the additive manifest. Roll back by ignoring the new fields in
   guidance; no package data or persisted learning state requires migration.
