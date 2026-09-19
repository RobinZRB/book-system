## Purpose

Provide auditable reading and mastery state from append-only events, with objective assessment evidence separated from scheduling and with a compatible transition from legacy due dates to FSRS.

## ADDED Requirements

### Requirement: Append-only learning events
Reading and review history SHALL be stored as versioned append-only events using stable book, chapter, and concept identities and timezone-aware timestamps. Corrections SHALL append superseding events and SHALL not rewrite historical events.

#### Scenario: Record reading activity
- **WHEN** `book-coach` commits a valid reading activity
- **THEN** one idempotent reading event is appended and only reading projections are updated

#### Scenario: Correct a review event
- **WHEN** an accepted review result must be corrected
- **THEN** a new event references and supersedes the prior event while the prior bytes remain unchanged

### Requirement: Preserve assessment and scheduling evidence
Each new review event SHALL retain the question kind and target level, fixed EMT expectations, misconceptions, EMT hits and score, objective pass/fail, confidence, the user's pre-feedback recall rating, the final scheduling rating, and scheduler and parameter versions.

#### Scenario: Objective failure overrides recall rating
- **WHEN** EMT produces an objective failure even though the user selected Hard, Good, or Easy
- **THEN** the final scheduling rating is Again while both the original user rating and objective evidence remain recorded

#### Scenario: Objective pass
- **WHEN** EMT produces an objective pass
- **THEN** the final scheduling rating uses the user's pre-feedback Hard, Good, or Easy rating and preserves the EMT result independently

### Requirement: FSRS scheduling for new reviews
The system SHALL use a pinned supported FSRS implementation for new scheduling decisions with configurable desired retention defaulting to `0.90`. Scheduler state and due projections SHALL be reproducible from recorded events and versioned scheduling policy.

#### Scenario: New concept review
- **WHEN** a concept without legacy schedule state receives its first valid review
- **THEN** FSRS computes its next schedule using the recorded final rating and current versioned policy

#### Scenario: Missing FSRS dependency
- **WHEN** a scheduling operation requires FSRS but the pinned dependency is unavailable or incompatible
- **THEN** commit fails explicitly and does not silently fall back to another scheduler

### Requirement: Compatible legacy takeover
Legacy concepts SHALL retain their existing due dates and legacy state until their next real review. Historical binary pass/fail records SHALL not be fabricated into Hard or Easy ratings. On the next real review, the concept SHALL begin FSRS scheduling from that observed event while legacy evidence remains auditable.

#### Scenario: Legacy concept before next review
- **WHEN** a migrated legacy concept has not yet received a new review
- **THEN** its pre-migration due date remains observable and no inferred FSRS rating is created

#### Scenario: Legacy concept takeover
- **WHEN** a migrated legacy concept receives its next real review
- **THEN** the system records the complete new event, starts FSRS scheduling for subsequent reviews, and preserves the legacy due and state as migration evidence

### Requirement: Deterministic learning projections
Review logs, mastery maps, due queues, calibration alerts, reading plans, and preparation views SHALL be projections derived from authoritative events and package identities. Removing or corrupting a projection SHALL not lose learning history.

#### Scenario: Rebuild mastery state
- **WHEN** mastery projections are removed
- **THEN** replaying package identities and review events recreates the same mastery levels, alerts, and active schedules for the same effective date and scheduler policy

#### Scenario: Reading and mastery write isolation
- **WHEN** coach and trainer operations commit data
- **THEN** coach operations append only reading events and trainer operations append only review events

