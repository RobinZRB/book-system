## MODIFIED Requirements

### Requirement: Provide read-only health checks
The system SHALL provide a `doctor` operation that validates direct catalog integrity, declared source, guide, and concept resources, and learning-event integrity without changing files. For every malformed learning event, its diagnostics SHALL identify the event stream and event line when available, and describe the violated envelope, payload, identity, timestamp, or scheduling invariant. It SHALL not require analysis workspaces, receipts, generic projections, an installation target, or an adapter probe.

#### Scenario: Invalid declared resource
- **WHEN** a book declaration names a missing required resource
- **THEN** `doctor` returns failure identifying the book and resource without changing files

#### Scenario: Invalid learning event
- **WHEN** an event violates a learning invariant
- **THEN** `doctor` reports the affected event stream and event line without repairing it

#### Scenario: Missing scheduler dependency at use time
- **WHEN** a review is requested but the pinned scheduler dependency is unavailable or incompatible
- **THEN** the review command fails explicitly and writes nothing
