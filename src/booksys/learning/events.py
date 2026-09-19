from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator
import uuid

from ..canonical import dumps, iter_jsonl
from ..domain.contracts import ALLOWED_RATINGS, ContractError, validate_identifier
from .validation import validate_event


def finalize_rating(user_rating: str, objective_pass: bool) -> str:
    if user_rating not in ALLOWED_RATINGS - {"again"}:
        raise ContractError("user_rating must be hard, good, or easy")
    return user_rating if objective_pass else "again"


def make_event(kind: str, aggregate_id: str, payload: dict[str, Any], *, occurred_at: str | None = None, idempotency_key: str | None = None) -> dict[str, Any]:
    """Build one event envelope.

    ``idempotency_key`` is opt-in: without one the event is always new, so a
    second reading of the same chapter is recorded as a second event rather than
    being mistaken for a retry.
    """
    validate_identifier(aggregate_id, "aggregate_id")
    return {
        "schema_version": 1,
        "event_id": f"evt:{uuid.uuid4().hex[:24]}",
        "kind": kind,
        "aggregate_id": aggregate_id,
        "occurred_at": occurred_at or datetime.now(timezone.utc).isoformat(),
        "idempotency_key": idempotency_key or uuid.uuid4().hex,
        "payload": payload,
    }


def append_event(path: str | Path, event: dict[str, Any]) -> bool:
    """Append one event; return False when its idempotency key was already recorded."""
    p = Path(path)
    if p.exists():
        key = event.get("idempotency_key")
        if key and any(prior.get("idempotency_key") == key for prior in iter_jsonl(p)):
            return False
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(dumps(event) + "\n")
    return True


def iter_events(path: str | Path) -> Iterator[dict[str, Any]]:
    for _line_no, event in iter_event_records(path):
        yield event


class EventStreamError(ValueError):
    """Raised when the authoritative JSONL stream cannot be safely read."""

    def __init__(self, path: Path, line_no: int, message: str):
        self.path = path
        self.line_no = line_no
        super().__init__(f"{path}:{line_no}: {message}")


def iter_event_records(path: str | Path) -> Iterator[tuple[int, dict[str, Any]]]:
    """Yield ``(line_number, event)`` while preserving source locations."""
    source = Path(path)
    with source.open("r", encoding="utf-8", newline="") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                import json
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise EventStreamError(source, line_no, f"invalid JSON: {exc.msg}") from exc
            if not isinstance(event, dict):
                raise EventStreamError(source, line_no, "event must be an object")
            yield line_no, event


def validate_event_record(event: dict[str, Any]) -> list[str]:
    """Expose the shared event validator at the event-store boundary."""
    return validate_event(event)


def make_review_event(
    aggregate_id: str,
    *,
    question_kind: str,
    target_level: int,
    emt_expectations: list[str],
    misconceptions: list[str],
    emt_hits: list[str],
    emt_score: float,
    objective_pass: bool,
    confidence: float,
    user_rating: str,
    scheduler_version: str,
    parameter_version: str,
    occurred_at: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    final = finalize_rating(user_rating, objective_pass)
    payload = {
        "question_kind": question_kind,
        "target_level": target_level,
        "emt_expectations": list(emt_expectations),
        "misconceptions": list(misconceptions),
        "emt_hits": list(emt_hits),
        "emt_score": emt_score,
        "objective_pass": objective_pass,
        "confidence": confidence,
        "user_rating": user_rating,
        "final_rating": final,
        "scheduler_version": scheduler_version,
        "parameter_version": parameter_version,
    }
    return make_event("review", aggregate_id, payload, occurred_at=occurred_at, idempotency_key=idempotency_key)
