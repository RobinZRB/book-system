## MODIFIED Requirements

### Requirement: Compatible legacy takeover
After the v2-only cutover, migrated legacy review events and due state SHALL be retained as v2 migration evidence, but runtime scheduling SHALL read the v2 event stream and SHALL not depend on legacy `mastery/` files or takeover adapters.

#### Scenario: V2 learning event stream
- **WHEN** a trainer or coach operation reads or writes learning state
- **THEN** it uses the v2 event store and projections under the runtime root
