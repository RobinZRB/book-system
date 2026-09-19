## MODIFIED Requirements

### Requirement: Compatibility paths are removed
The release SHALL remove rollback metadata, legacy pipeline adapters, legacy-only CLI actions, historical migration snapshots, and v1-labelled compatibility code or active runtime metadata after the active stage passes verification. OpenSpec archival history is non-runnable audit material and is excluded from this runtime cleanup.

#### Scenario: Rollback is unavailable after cutover
- **WHEN** an operator requests a removed compatibility action
- **THEN** the CLI reports that the project is v2-only and does not recreate or consult legacy state

#### Scenario: Removed command requested
- **WHEN** an operator requests a removed compatibility action
- **THEN** the CLI rejects it and does not recreate retired state

#### Scenario: V1 residue scan
- **WHEN** source, active runtime data, skill bundles, evaluation assets, and operator documentation are scanned after cleanup
- **THEN** no runnable v1 compatibility path, v1-labelled command, or active v1-labelled metadata is found
