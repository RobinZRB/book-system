## Purpose

Make prepared investment and finance analysis understandable and auditable by
requiring a visible, evidence-linked reasoning sequence rather than a bare
summary of selected chapters.

## ADDED Requirements

### Requirement: Detailed investment analysis presentation
For a stock, company, or investment-opportunity request, the book-user
workflow SHALL present a detailed analysis by default.  The presentation SHALL
contain a pre-analysis Gate, a red-flag investigation, a multi-dimension
analysis, an explicit counter-view or its absence, missing external facts, and
a traceable conclusion.  It SHALL distinguish book evidence, external facts,
and inferences.

#### Scenario: Evidence is available for an investment request
- **WHEN** prepared context has matched evidence for a stock, company, or investment opportunity
- **THEN** the answer presents the Gate, every applicable risk disposition, each protocol dimension with its execution state, evidence citations, and a conclusion linked to those findings

#### Scenario: Evidence is only partial
- **WHEN** a prepared investment analysis reports unmatched protocol sections or unverified external facts
- **THEN** the answer still presents all matched Gate, risk, and dimension findings, labels only the unsupported items as unassessed, and lists the specific missing facts without fabricating conclusions

#### Scenario: No opposing evidence is found
- **WHEN** the prepared evidence package contains no counter-evidence for a conclusion
- **THEN** the answer states that no counter-evidence was found in the selected scope and does not represent absence as proof

### Requirement: Concise presentation remains available
The book-user workflow SHALL retain concise presentation for non-investment
requests and for an investment request that explicitly asks for a brief scan.
Concise presentation SHALL retain the conclusion, evidence provenance, and
missing-evidence disclosure.

#### Scenario: User asks for a brief investment scan
- **WHEN** the request explicitly asks for a quick or concise assessment
- **THEN** the answer may compress the detailed sections while retaining Gate disposition, material red flags, conclusion, citations, and missing facts
