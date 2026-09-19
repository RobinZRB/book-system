## MODIFIED Requirements

### Requirement: Four focused self-contained skills
Each skill SHALL load runtime guidance and protocol assets from its own `skills/` bundle and SHALL not require legacy project directories or pipeline scripts.

#### Scenario: Skill activation
- **WHEN** one of the four skills is activated outside the source repository
- **THEN** it can load every required bundled instruction without following a path into a sibling project directory

#### Scenario: Investment analysis orchestration
- **WHEN** book-user receives an investment/company request and external research is available
- **THEN** it derives a visible plan from the selected framework, obtains only plan-linked structured research inputs before synthesis, and keeps book evidence, supporting external facts, counter-evidence, and inferences distinct in the final answer

#### Scenario: Offline fallback
- **WHEN** external research is unavailable
- **THEN** book-user discloses the unavailable fields and may continue with validated caller-supplied facts and book-only partial analysis

#### Scenario: Skill instruction scope
- **WHEN** a skill describes an executable workflow
- **THEN** it states when to trigger, the semantic decisions the AI owns, and the concrete `booksys` operation to invoke without duplicating storage layouts or projection procedures

#### Scenario: Legacy project directories are absent
- **WHEN** a skill is activated after v2 cutover
- **THEN** all guidance, protocol, and runtime references resolve inside the canonical skill bundle and v2 runtime

#### Scenario: Runtime path scan
- **WHEN** canonical skill documentation and configuration are scanned before cleanup
- **THEN** no executable instruction points to a removed top-level skill, data, or pipeline directory
