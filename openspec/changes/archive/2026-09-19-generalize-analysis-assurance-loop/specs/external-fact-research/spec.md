## MODIFIED Requirements

### Requirement: Framework-driven research plan
Before external research begins, the workflow SHALL derive a visible research
plan from the selected book protocol, applicability check, escalation triggers,
analysis dimensions, alternative explanations, and known evidence gaps. Each
requested external field SHALL identify the framework item it is intended to
assess, its purpose, source-tier preference, applicable-date rule, and quality
or uncertainty impact; research SHALL not expand into unrelated information
merely because it is available. Investment fields SHALL retain their existing
primary-source preference and source-tier rules.

#### Scenario: Valuation dimension requires current facts
- **WHEN** the selected framework marks valuation or safety margin as requiring
  external evidence
- **THEN** the research plan requests only the current price and the valuation
  inputs needed to assess that framework item, with its source preference and
  applicable date

#### Scenario: Non-investment dimension requires corroboration
- **WHEN** a selected non-investment protocol dimension identifies a
  plan-linked external claim that must be corroborated
- **THEN** the research plan records the claim's protocol link, purpose,
  preferred source class, applicable-date rule, and consequence if it remains
  unverified

#### Scenario: Red flag requires investigation
- **WHEN** an applicability check, red flag, or escalation trigger is marked for
  investigation
- **THEN** the research plan requests the targeted evidence and relevant
  alternative explanation needed to reach a disposition for that item

#### Scenario: Framework does not require a field
- **WHEN** an external fact is not linked to an applicable protocol, trigger,
  alternative explanation, or dimension
- **THEN** the research stage does not present it as required analysis evidence
