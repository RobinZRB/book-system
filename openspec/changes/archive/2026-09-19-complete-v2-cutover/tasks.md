## 1. V2 runtime roots

- [x] 1.1 Add active-stage and runtime-root resolution with no compatibility fallback; add focused tests for missing/valid pointers.
- [x] 1.2 Make analysis selection and evidence loading read v2 manifests/resources from the active stage.
- [x] 1.3 Route operation guidance, learning events, and projections through canonical v2/skills roots.
- [x] 1.4 Add a strict v2 package importer that atomically publishes a prepared package into the active stage.

## 2. Remove compatibility surface

- [x] 2.1 Remove rollback and legacy-only CLI actions and adapter imports while preserving normal v2 commands.
- [x] 2.2 Move/canonicalize required guidance and protocol assets under `skills/`; update configs and references.
- [x] 2.2a Rewrite canonical skill instructions/configuration so all active paths use v2 roots and bundled assets.
- [x] 2.3 Update tests and documentation for v2-only behavior.

## 3. Cutover and cleanup

- [x] 3.1 Verify active-stage package/provenance parity and representative user/coach/trainer operations.
- [x] 3.2 Delete legacy data, historical migration snapshots, rollback metadata, operation history, and legacy pipeline directories.
- [x] 3.3 Run the full test, health, schema, and reference scans; record clean v2-only evidence.
