## Purpose

Provide current, auditable external facts and counter-evidence for investment
analysis so book frameworks can be applied to a verified company state rather
than to an empty external-data placeholder.

## ADDED Requirements

### Requirement: Framework-driven research plan
Before external research begins, the workflow SHALL derive a visible research
plan from the selected book protocol, Gate, red flags, analysis dimensions,
and known evidence gaps. Each requested external field SHALL identify the
framework item it is intended to assess; research SHALL not expand into
unrelated company information merely because it is available.

#### Scenario: Valuation dimension requires current facts
- **WHEN** the selected framework marks valuation or safety margin as requiring external evidence
- **THEN** the research plan requests only the current price and the valuation inputs needed to assess that framework item, with its source preference and applicable date

#### Scenario: Red flag requires investigation
- **WHEN** a Gate or red flag is marked for investigation
- **THEN** the research plan requests the targeted facts and counter-evidence needed to reach a disposition for that item

#### Scenario: Framework does not require a field
- **WHEN** a company fact is not linked to an applicable protocol, Gate, red flag, or dimension
- **THEN** the research stage does not present it as required analysis evidence

### Requirement: Structured external fact package
The system SHALL represent every acquired or caller-supplied external fact as
an immutable analysis input containing a field, value, source URL or document
identity, retrieval time, applicable date, source tier, and verification
status.  It SHALL retain missing fields, conflicting values, and stale facts
as explicit diagnostics rather than silently choosing or repairing them.

#### Scenario: Primary-source financial fact
- **WHEN** research finds an issuer, exchange, or regulator disclosure that supports a requested financial fact
- **THEN** the analysis input records the fact with primary-source provenance, retrieval time, applicable date, and a citation-ready identity

#### Scenario: Conflicting facts
- **WHEN** two valid sources provide incompatible values for the same fact and applicable date
- **THEN** the package retains both values, identifies the conflict, and prevents synthesis from presenting either as an uncontested fact

#### Scenario: Missing current data
- **WHEN** a required external fact cannot be sourced or validated
- **THEN** the package lists the missing field and reason without fabricating a replacement

### Requirement: Independent research and counter-evidence
For an investment/company request, the workflow SHALL support independent,
research-plan-driven collection of positive/current facts and counter-evidence
before synthesis. It SHALL prefer issuer, exchange, and regulator sources for
financial facts, and shall label lower-tier sources and their limitations when
they are used for market data or corroboration.

#### Scenario: Counter-evidence found
- **WHEN** independent research finds material counter-evidence relevant to an analysis dimension
- **THEN** the package links it to that dimension and preserves its provenance separately from supporting facts

#### Scenario: No counter-evidence found
- **WHEN** research completes the selected scope without material counter-evidence
- **THEN** the package reports the searched scope and states that absence is not evidence of safety

#### Scenario: Research capability unavailable
- **WHEN** the runtime cannot perform external research
- **THEN** the workflow accepts caller-supplied facts when available and otherwise produces an explicit offline/missing-data diagnostic while allowing book-only partial analysis
