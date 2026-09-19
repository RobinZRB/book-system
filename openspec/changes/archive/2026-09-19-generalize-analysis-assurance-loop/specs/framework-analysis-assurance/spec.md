## Purpose

Provide every framework-based book analysis with a domain-neutral, auditable
path from a user question and selected book evidence to a bounded conclusion,
without imposing investment terminology or an action recommendation.

## ADDED Requirements

### Requirement: Domain-neutral assurance plan
For every `user.analyze` workspace with one or more selected books, the system
SHALL expose an additive assurance plan. The plan SHALL record the request's
analysis mode, framework applicability state, evidence coverage and quality,
protocol-derived dimensions, alternative-explanation state, uncertainty
diagnostics, conclusion requirements, and review state. It SHALL preserve the
selected book's terminology and SHALL NOT substitute fixed investment
dimensions for a non-investment protocol.

#### Scenario: Management framework analysis
- **WHEN** a selected management book is used to analyse an organisational
  decision
- **THEN** the plan exposes the book's applicable protocol dimensions and the
  evidence, alternatives, and uncertainty states without valuation or
  financial-risk fields being required

#### Scenario: Narrative or explanatory question
- **WHEN** a request asks for interpretation or explanation rather than a
  diagnosis or decision
- **THEN** the plan marks the decision and review stages as not required while
  retaining applicability, book-evidence, inference, and limitation records

### Requirement: Applicability and decision contract
The request MAY contain an explicit decision contract identifying the question,
subject, intended use, time horizon, constraints, and decision threshold. The
system SHALL preserve supplied contract fields verbatim and SHALL mark absent
fields as unspecified; it SHALL NOT invent a decision, a risk tolerance, or an
action recommendation. The assurance plan SHALL report whether the selected
framework is applicable, partly applicable, or unassessed and why.

#### Scenario: Explicit decision contract
- **WHEN** a caller supplies a valid decision contract for a framework-based
  analysis
- **THEN** the workspace records it separately from book evidence and links
  relevant dimensions and evidence gaps to its stated question and constraints

#### Scenario: Framework has an applicability boundary
- **WHEN** selected protocol evidence identifies a population, context, or
  use-case boundary that the request does not satisfy
- **THEN** the plan reports `partly_applicable` or `not_applicable`, identifies
  the boundary, and does not present the framework as a complete answer

### Requirement: Cross-cutting challenge and uncertainty records
The assurance plan SHALL represent material risks or escalation triggers,
alternative explanations or counter-evidence, and evidence gaps or conflicts
as cross-cutting records linked to one or more dimensions. These records SHALL
remain visible through synthesis and SHALL distinguish not searched, not found
within scope, conflicting, unverified, and unavailable states. Absence of an
alternative or a fact SHALL NOT be represented as support for a conclusion.

#### Scenario: Alternative explanation is not searched
- **WHEN** a selected analysis scope contains no completed alternative-
  explanation research
- **THEN** the plan reports that the alternative was not searched rather than
  reporting that no alternative exists

#### Scenario: Evidence conflicts across sources
- **WHEN** supplied or acquired evidence contains incompatible values or
  claims relevant to the same dimension
- **THEN** the plan retains the conflict and requires the conclusion to label
  the affected assertion as contested or unresolved

### Requirement: Conditional conclusion and review contract
The assurance plan SHALL require a conclusion to distinguish book evidence,
external or caller evidence, and inference; state its scope, assumptions,
material uncertainty, and disconfirming conditions; and avoid an unsupported
pass/fail or action recommendation. For decision or diagnostic requests, the
plan SHALL also expose any supplied or protocol-derived validation or review
triggers. Interpretive requests MAY state that monitoring is not applicable.

#### Scenario: Decision conclusion with an unresolved gap
- **WHEN** a decision-oriented analysis has a material missing evidence item
- **THEN** the conclusion requirements identify the gap and require a
  conditional, deferred, or otherwise bounded conclusion instead of a
  definitive recommendation

#### Scenario: Review trigger exists
- **WHEN** a protocol or caller identifies an observable condition that would
  challenge the analysis
- **THEN** the plan includes that condition as a review trigger linked to the
  affected assumption or dimension
