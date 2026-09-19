## MODIFIED Requirements

### Requirement: Compatible legacy takeover
After the v2-only cutover, runtime scheduling SHALL read the v2 event stream and projections only. The active runtime data SHALL not retain a legacy due-state artifact or takeover metadata.

#### Scenario: V2 learning event stream
- **WHEN** a trainer or coach operation reads or writes learning state
- **THEN** it uses the v2 event store and projections under the runtime root

#### Scenario: Legacy due state is absent
- **WHEN** strict health checks inspect active learning data after cleanup
- **THEN** no legacy due-state artifact is present and v2 event/projection validation remains successful
