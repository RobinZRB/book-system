## Why

The project has completed its v2 cutover.  Active code, data, and user-facing guidance should describe the supported v2 runtime directly, rather than retaining retired-version terminology and negative compatibility checks outside OpenSpec history.

## What Changes

- **BREAKING** Remove non-OpenSpec references, tests, and health-check rules that name retired v1 compatibility surfaces or the former baseline command.
- Retain positive validation of the active v2 pointer, strict packages, runtime roots, skills, and supported command surface.
- Rewrite affected active specifications as positive v2 contracts; archived OpenSpec history remains unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `v2-only-runtime`: define the authoritative v2 runtime using positive operational requirements.
- `booksys-operations`: define the supported command interface and root resolution without retired-version terminology.

## Impact

Updates `check_all.py`, runtime tests, operator documentation, skill guidance, and the two active specifications.  No package format, runtime-data location, or supported command is added.
