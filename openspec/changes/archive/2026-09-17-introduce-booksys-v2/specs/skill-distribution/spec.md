## Purpose

Deliver four focused, self-contained AI skills that share one deterministic runtime, install safely beside other skills, exclude private data by default, and remain behaviorally testable across supported harnesses.

## ADDED Requirements

### Requirement: Four focused self-contained skills
The distribution SHALL retain separate `book-reader`, `book-user`, `book-coach`, and `book-trainer` skills. Each bundle SHALL contain its required instructions and referenced resources using skill-root-relative paths, and SHALL delegate deterministic storage and scheduling work to `booksys`.

#### Scenario: Skill activation
- **WHEN** one of the four skills is activated outside the source repository
- **THEN** it can load every required bundled instruction without following a path into a sibling project directory

#### Scenario: Skill instruction scope
- **WHEN** a skill describes an executable workflow
- **THEN** it states when to trigger, the semantic decisions the AI owns, and the concrete `booksys` operation to invoke without duplicating storage layouts or projection procedures

### Requirement: Per-skill installation
The installer SHALL install each book skill independently into `.agents/skills` and `.workbuddy/skills` at project or user scope. It SHALL coexist with unrelated real directories and skills and SHALL never replace an entire harness skill root.

#### Scenario: Coexist with OpenSpec
- **WHEN** `.agents/skills` already contains OpenSpec-managed skill directories
- **THEN** installing the four book skills preserves every existing unrelated entry and adds only the four requested skill entries

#### Scenario: Existing real directory collision
- **WHEN** a target skill path is a real directory not managed by this installer
- **THEN** installation stops for that target with a collision diagnostic and does not delete or overwrite it

### Requirement: Cross-platform installation behavior
The installer SHALL use individual Windows junctions where supported, individual symbolic links on other supported platforms, and copying only after an explicit request. It SHALL record enough installation metadata to diagnose stale or misdirected installations.

#### Scenario: Correct existing link
- **WHEN** an installed skill link already points to the current validated bundle
- **THEN** installation reports it as current and performs no write

#### Scenario: Stale managed link
- **WHEN** an installer-managed skill link points to an old bundle
- **THEN** installation may replace only that verified link and SHALL preserve the target bundle and sibling skills

### Requirement: Private data excluded from distribution
Default source and release distributions SHALL exclude raw book texts, formal user book instances, reading events, review events, learner projections, machine-specific anchors, and local operation workspaces.

#### Scenario: Default release build
- **WHEN** a release bundle is generated without explicit private-data options
- **THEN** it contains code, schemas, templates, self-contained skills, and sanitized fixtures only, together with a manifest of included content

### Requirement: Skill behavior evaluation gates
Each skill SHALL have representative behavioral evaluations that compare the changed skill against its accepted baseline. Releases SHALL treat fabrication, spoiler leakage, unauthorized writes, premature quiz feedback, mutable EMT expectations, and unsupported claims as zero-tolerance failures.

#### Scenario: Hard constraint regression
- **WHEN** a candidate skill violates any zero-tolerance behavior in an evaluation
- **THEN** the release gate fails even if mechanical unit tests pass

#### Scenario: Quality comparison
- **WHEN** hard constraints pass
- **THEN** the evaluation reports task success, traceability, context usage, latency, and blind quality comparison without requiring every soft metric to improve

### Requirement: Supported harness scope
The core project SHALL declare `.agents` and `.workbuddy` as its supported harness targets. Generated `.claude` and `.opencode` integrations SHALL not be maintained as core distribution artifacts.

#### Scenario: Unsupported harness requested
- **WHEN** a user requests installation to an unsupported harness
- **THEN** the installer reports the supported targets and does not create guessed paths

