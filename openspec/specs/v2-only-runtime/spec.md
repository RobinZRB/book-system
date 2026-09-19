# v2-only-runtime Specification

## Purpose
The single layout the runtime resolves, with no second path. Books, chapters, guides, and concepts come from one canonical direct catalog beneath the system root, while private learning events and derived learning state come from the runtime data root; neither requires an active-stage pointer or a compatibility fallback.

## Requirements

### Requirement: Active runtime content is authoritative
The runtime SHALL resolve books, chapters, guides, and concepts from one canonical direct catalog beneath the system root. It SHALL resolve private learning events and derived learning state from the runtime data root. Neither path SHALL require `.booksys/current.json` or an active stage pointer.

#### Scenario: Declared content is located
- **WHEN** a skill locates declared book content
- **THEN** catalog resolution returns resources from the canonical direct catalog

#### Scenario: Catalog and learning commands remain usable
- **WHEN** the catalog contains valid packages
- **THEN** health checks and representative catalog and learning commands remain successful

### Requirement: Runtime uses one canonical v2 layout
The project SHALL provide one canonical direct book catalog, one learning event store, and the documented catalog and learning command surface. Runtime metadata SHALL not include active-stage selection, generic operation workspaces, receipts, required generic projections, an installation target, or a distribution build.

#### Scenario: Runtime command is invoked
- **WHEN** an operator invokes a supported runtime command
- **THEN** it resolves the canonical catalog or learning state appropriate to that command

#### Scenario: Runtime content is inspected
- **WHEN** source, runtime data, skill bundles, and operator documentation are inspected
- **THEN** active references describe the simplified canonical layout
