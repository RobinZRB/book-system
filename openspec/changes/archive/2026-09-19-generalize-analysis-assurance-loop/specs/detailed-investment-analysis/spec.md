## MODIFIED Requirements

### Requirement: Detailed investment analysis presentation
For a stock, company, or investment-opportunity request, the book-user
workflow SHALL present a detailed analysis by default. The presentation SHALL
render the domain-neutral assurance loop and its investment adapter: an
applicability and decision-context check, pre-analysis Gate, red-flag
investigation, multi-dimension analysis, explicit counter-view or its absence,
evidence quality and missing external facts, a traceable conditional
conclusion, and applicable review triggers. It SHALL distinguish book evidence,
external facts, and inferences.

#### Scenario: Evidence is available for an investment request
- **WHEN** prepared context has matched evidence for a stock, company, or
  investment opportunity
- **THEN** the answer presents the Gate, every applicable risk disposition,
  each protocol dimension with its execution state, evidence citations,
  alternative-explanation state, and a conclusion linked to those findings

#### Scenario: Evidence is only partial
- **WHEN** a prepared investment analysis reports unmatched protocol sections
  or unverified external facts
- **THEN** the answer still presents all matched Gate, risk, and dimension
  findings, labels only the unsupported items as unassessed, lists the
  specific missing facts, and conditions the conclusion without fabricating
  findings

#### Scenario: No opposing evidence is found
- **WHEN** the prepared evidence package contains no counter-evidence for a
  conclusion
- **THEN** the answer states the searched scope and whether alternatives were
  searched, and does not represent absence as proof
