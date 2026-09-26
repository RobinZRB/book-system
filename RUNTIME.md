# Runtime

## Prerequisites

Python 3.11 or later, with the pinned `fsrs` package installed (`fsrs==6.3.2`). The pin is also recorded on every review event as `scheduler_version`, so a recorded stream states which scheduler produced it.

The runtime runs straight from the source tree; there is no build step and installing is optional. On Windows, `booksys.bat` runs `python -m booksys` with `PYTHONPATH=src`; on Linux and macOS, run `PYTHONPATH=src python3 -m booksys`. Installing the package (`pip install .`) is only needed to get the bare `booksys` command. Either way, every command reads or writes only the two areas below.

The runtime has two authoritative areas:

- `.booksys/content/books` — compact book packages. `booksys packages import` publishes one package; a published package is never rewritten.
- `.booksys/runtime/learning/events.jsonl` — append-only reading and review events.

Catalog reads are direct. Learning status and due state are rebuilt from events. Every review event records the scheduling state FSRS produced, and the next review of the same concept resumes from that state.

Use `booksys doctor` for catalog and event validation. It reports the event
stream and JSONL line for structurally valid but invalid events; `learn status`
and `learn due` fail closed when authoritative history is invalid instead of
returning a partial projection. No command repairs or rewrites the event log.

Roots resolve from `--project-root` (default: working directory), `--system-root`, and `--data-root`, or from `.booksys/config.json` with `system_root` and `data_root` keys.

The on-disk contracts for the root configuration and the learning event envelope are documented under `schemas/`. They are reference documents; the runtime does not load them.
