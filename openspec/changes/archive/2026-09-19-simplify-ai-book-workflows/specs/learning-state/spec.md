## ADDED Requirements

### Requirement: Narrow learning command interface
The runtime SHALL expose commands to read learning status and due work, record one chapter completion, and record one concept review. These commands SHALL accept stable declared identities, enforce their own write invariants, and hide event storage, projection rebuilding, and scheduling details from skills. An identifier SHALL carry its own scope: review takes a concept identity alone, and status reports the whole event stream rather than filtering it per book.

#### Scenario: Coach completes a chapter
- **WHEN** book-coach records completion for a declared book and chapter
- **THEN** the runtime appends one reading event and returns updated reading status

#### Scenario: Coach records a chapter a second time
- **WHEN** book-coach records completion for a chapter that already has a reading event
- **THEN** the runtime appends a further reading event rather than rejecting the request

#### Scenario: Trainer records a review
- **WHEN** book-trainer records a review for a declared concept with objective assessment data and user rating
- **THEN** the runtime appends one review event, calculates due state, and returns resulting learning status

#### Scenario: Invalid learning identity
- **WHEN** a learning command receives an undeclared or malformed identity
- **THEN** it rejects the request without changing event history

## ADDED Requirements

### Requirement: Compatible legacy takeover
After migration, coaching and training SHALL read and write only the canonical learning event store through the narrow learning interface. The interface SHALL not depend on operation workspaces, receipts, generic projections, or legacy due-state artifacts.

#### Scenario: V2 learning event stream
- **WHEN** a trainer or coach operation reads or writes learning state
- **THEN** it uses the canonical event store through the narrow learning interface

#### Scenario: Learning command reads state
- **WHEN** book-coach or book-trainer requests learning state
- **THEN** it receives state derived from the canonical event stream without an operation workspace

#### Scenario: Legacy due state is absent
- **WHEN** health checks inspect learning data after migration
- **THEN** no legacy due-state artifact is required and event validation remains successful

### Requirement: Append-only learning events
Reading and review history SHALL be stored as versioned append-only events using stable book, chapter, and concept identities and timezone-aware timestamps. A history that must be corrected SHALL gain further events; existing event bytes SHALL never be rewritten or deleted.

#### Scenario: Record reading activity
- **WHEN** book-coach records a valid chapter completion
- **THEN** one reading event is appended and only reading state is updated

#### Scenario: An earlier event is wrong
- **WHEN** a recorded reading or review no longer reflects what happened
- **THEN** the stream keeps the original bytes and mastery and due state are recomputed from the full stream

### Requirement: Preserve assessment and scheduling evidence
Each review event SHALL retain question kind, target level, fixed EMT expectations, misconceptions, EMT hits and score, objective pass/fail, confidence, the user's pre-feedback recall rating, final scheduling rating, and scheduler and parameter versions.

#### Scenario: Objective failure overrides recall rating
- **WHEN** EMT produces an objective failure even though the user selected Hard, Good, or Easy
- **THEN** the final scheduling rating is Again while the original user rating and objective evidence are retained

#### Scenario: Objective pass
- **WHEN** EMT produces an objective pass
- **THEN** the final scheduling rating uses the user's pre-feedback rating and preserves the EMT result independently

### Requirement: FSRS scheduling from recorded state
The runtime SHALL use a pinned supported FSRS implementation with configurable desired retention defaulting to `0.90`. Each review SHALL record the scheduling state FSRS produced, and the next review of the same concept SHALL resume from that recorded state so its interval grows with history. Due results SHALL be reproducible from recorded events and versioned policy while the scheduler remains internal to the learning interface.

#### Scenario: New concept review
- **WHEN** a concept receives its first valid review
- **THEN** the learning interface returns the next schedule computed by FSRS from a fresh card

#### Scenario: Subsequent review of the same concept
- **WHEN** a concept that already has a review receives another valid review
- **THEN** the schedule is computed from the state recorded on the previous review rather than from a fresh card

#### Scenario: Missing FSRS dependency
- **WHEN** a scheduling operation requires FSRS but the pinned dependency is unavailable or incompatible
- **THEN** the learning command fails explicitly and does not silently fall back to another scheduler

### Requirement: Derived learning state
Reading status, mastery state, and due work SHALL be derived on demand from authoritative events and stable package identities. No cache is required, and no skill or user-facing contract SHALL refer to a derived state file.

#### Scenario: Rebuild mastery state
- **WHEN** derived learning state is removed
- **THEN** replaying package identities and review events recreates the same mastery state and due results for the same effective date and policy

#### Scenario: Reading and mastery write isolation
- **WHEN** coach and trainer record learning data
- **THEN** coach writes only reading events and trainer writes only review events
