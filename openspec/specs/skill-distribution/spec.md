# skill-distribution Specification

## Purpose
How the four skills -- book-reader, book-user, book-coach, and book-trainer -- ship and activate. Each bundle is self-contained and loads its own guidance, and each reaches the runtime only through the supported catalog or learning interface, so no skill depends on legacy directories or pipeline scripts.

## Requirements

### Requirement: Four focused self-contained skills
Each skill SHALL load its bundled guidance and use the supported direct catalog or learning interface without requiring legacy directories or pipeline scripts. Book-reader SHALL prepare the small package format. Book-user SHALL choose relevant declared books and chapters semantically, read direct resources, and state useful source choices, evidence limits, and inference boundaries. It SHALL not require runtime keyword selection, retry rationales, generated assurance plans, or structured external-fact packages. Book-coach and book-trainer SHALL use only the narrow learning interface for state changes.

#### Scenario: Skill activation
- **WHEN** one of the four skills is activated outside the source repository
- **THEN** it can load every required bundled instruction and invoke its documented direct runtime interface

#### Scenario: Question-driven source choice
- **WHEN** book-user receives a question
- **THEN** it can inspect the catalog and choose relevant book and chapter resources without a keyword-matching retry protocol

#### Scenario: Investment research
- **WHEN** book-user needs current facts for an investment or company question
- **THEN** it researches only information material to the answer, gives source and date where available, separates facts from inference, and states material unknowns or disconfirming conditions

#### Scenario: Learning write isolation
- **WHEN** book-coach or book-trainer completes work
- **THEN** it invokes the corresponding narrow learning command and cannot write package content or the other learning stream

#### Scenario: Investment analysis orchestration
- **WHEN** book-user receives an investment or company request and research is available
- **THEN** it selects material research in light of the book framework and keeps book evidence, external evidence, counter-evidence, and inference distinct

#### Scenario: Non-investment framework analysis
- **WHEN** book-user receives a non-investment framework question
- **THEN** it applies relevant source material, alternatives, and uncertainty without forcing investment terminology

#### Scenario: Semantic book selection
- **WHEN** book-user must choose among catalog entries
- **THEN** it makes a justified semantic choice or asks the user only when the choice is genuinely ambiguous

#### Scenario: Caller-selected chapters
- **WHEN** a user names a declared chapter
- **THEN** book-user reads that chapter directly and does not substitute another chapter

#### Scenario: Offline fallback
- **WHEN** external research is unavailable
- **THEN** book-user states that limit and may provide a bounded book-only answer

#### Scenario: Skill instruction scope
- **WHEN** a skill describes an executable workflow
- **THEN** it states the semantic decisions the AI owns and the concrete direct catalog or learning command it invokes

#### Scenario: Legacy project directories are absent
- **WHEN** a skill is activated after cutover
- **THEN** all guidance and runtime references resolve through the canonical skill bundle and direct runtime interfaces

#### Scenario: Runtime path scan
- **WHEN** canonical skill documentation and bundled resources are scanned before cleanup
- **THEN** no executable instruction points to a removed operation, stage-pointer, or analysis-context path

### Requirement: Skill bundles resolve without legacy paths
Each skill bundle SHALL carry every instruction and resource it needs, and SHALL name the concrete direct runtime command it invokes. Nothing outside the bundle SHALL be required to activate it, and no bundle SHALL require an evaluation harness, a contract file, or a generated report in order to be used.

#### Scenario: Bundle is self-sufficient
- **WHEN** a skill is activated outside the source repository
- **THEN** it loads its guidance and its declared resources from the bundle alone

#### Scenario: No harness dependency
- **WHEN** a bundle's declared resources and commands are inspected
- **THEN** none of them resolves through an evaluation contract, a report file, or a removed operation path
