## MODIFIED Requirements

### Requirement: Full staged legacy migration
The active package catalog SHALL be v2-native after cutover and SHALL not retain v1-labelled generator modes, source markers, migration plans, or legacy identity locators. Migration provenance required to validate active packages SHALL be represented with v2-native, stable metadata.

#### Scenario: Authoritative v2 package set
- **WHEN** the active stage passes strict manifest and provenance validation
- **THEN** runtime package selection reads only its manifests and resources

#### Scenario: V1 provenance cleanup
- **WHEN** active package metadata is normalized after cutover
- **THEN** package validation remains successful and stable identities, resource digests, and package content remain unchanged
