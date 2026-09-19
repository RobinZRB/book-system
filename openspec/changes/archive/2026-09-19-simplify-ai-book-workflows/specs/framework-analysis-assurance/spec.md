## ADDED Requirements

### Requirement: Domain-neutral assurance plan
For every framework-based book analysis, book-user guidance SHALL require the AI to assess whether the selected framework applies, distinguish source material from external facts and inference, state material limits or alternatives, and bound its conclusion by relevant uncertainty. The runtime SHALL not generate a universal assurance plan or prescribe domain dimensions.

#### Scenario: Management framework analysis
- **WHEN** a selected management book is used to analyse an organisational decision
- **THEN** book-user applies the book's relevant framework in its own terms, discloses material limits, and does not add unrelated domain fields

#### Scenario: Narrative or explanatory question
- **WHEN** a request asks for interpretation or explanation
- **THEN** book-user gives a proportionate source-grounded answer and states material inference or limitations without a mandatory decision template

### Requirement: Applicability and decision contract
Book-user SHALL respect an explicit user decision context when supplied and SHALL not invent an action recommendation, risk tolerance, or threshold. It SHALL explain material applicability boundaries in prose when they affect the answer; the runtime SHALL not validate or serialize a decision contract.

#### Scenario: Explicit decision contract
- **WHEN** a user supplies constraints or a decision threshold
- **THEN** book-user uses those constraints when applying the framework and does not replace them with invented ones

#### Scenario: Framework has an applicability boundary
- **WHEN** source material identifies a boundary that the question does not satisfy
- **THEN** book-user identifies the boundary and does not present the framework as a complete answer

### Requirement: Cross-cutting challenge and uncertainty records
Book-user SHALL not treat an absent fact or unsearched alternative as support for a conclusion. It SHALL retain material conflicts and disclose relevant unknowns, but it SHALL decide the appropriate research scope from the question and source material rather than consume a runtime state machine.

#### Scenario: Alternative explanation is not searched
- **WHEN** an alternative explanation is material but has not been researched
- **THEN** book-user states that limitation rather than asserting no alternative exists

#### Scenario: Evidence conflicts across sources
- **WHEN** supplied or researched evidence contains incompatible material claims
- **THEN** book-user labels the affected conclusion as contested or unresolved

### Requirement: Conditional conclusion and review contract
Book-user SHALL separate book evidence, external evidence, and inference in a material decision or diagnostic answer. It SHALL state scope, assumptions, material uncertainty, and disconfirming conditions where they affect the conclusion. Observable review triggers are included when useful to the user's decision, not as a runtime-required field.

#### Scenario: Decision conclusion with an unresolved gap
- **WHEN** a decision-oriented analysis has a material evidence gap
- **THEN** book-user gives a conditional, deferred, or otherwise bounded conclusion instead of a definitive recommendation

#### Scenario: Review trigger exists
- **WHEN** an observable condition would materially challenge the conclusion
- **THEN** book-user identifies that condition as a review trigger
