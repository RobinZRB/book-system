"""Small public learning interface used by coach and trainer skills."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from ..catalog import locate_chapter, locate_concept
from ..config import RootConfig
from ..domain.contracts import validate_identifier
from ..paths import runtime_root
from .events import append_event, iter_event_records, make_event, make_review_event
from .reducers import reduce_mastery, reduce_reading
from .scheduler import FSRSAdapter
from .validation import validate_event, validate_review_payload

REVIEW_KEYS = (
    "question_kind",
    "target_level",
    "emt_expectations",
    "misconceptions",
    "emt_hits",
    "emt_score",
    "objective_pass",
    "confidence",
    "user_rating",
)


def _event_path(roots: RootConfig) -> Path:
    return runtime_root(roots) / "learning" / "events.jsonl"


def _events(roots: RootConfig) -> list[dict[str, Any]]:
    path = _event_path(roots)
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line_no, event in iter_event_records(path):
        errors = validate_event(event)
        if errors:
            raise ValueError(f"{path}:{line_no}: " + "; ".join(errors))
        events.append(event)
    return events


def _with_idempotency_key(events: Iterable[dict[str, Any]], key: str | None) -> dict[str, Any] | None:
    if not key:
        return None
    return next((event for event in events if event.get("idempotency_key") == key), None)


def _of_kind(events: Iterable[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
    return [event for event in events if event.get("kind") == kind]


def _previous_state(events: Iterable[dict[str, Any]], concept_id: str) -> dict[str, Any] | None:
    state = None
    for event in events:
        if event.get("aggregate_id") == concept_id:
            state = (event.get("payload") or {}).get("schedule", {}).get("state") or state
    return state


def status(roots: RootConfig) -> dict[str, Any]:
    """Return reading and mastery state rebuilt from the whole event stream."""
    events = _events(roots)
    return {
        "reading": reduce_reading(_of_kind(events, "reading")),
        "mastery": reduce_mastery(_of_kind(events, "review")),
    }


def complete_chapter(
    roots: RootConfig, book_id: str, chapter_id: str, *, idempotency_key: str | None = None,
) -> dict[str, Any]:
    """Append one reading event for a declared chapter."""
    located = locate_chapter(roots, book_id, chapter_id)
    prior = _with_idempotency_key(_events(roots), idempotency_key)
    if prior:
        return {"event": prior, "status": status(roots), "recorded": False}
    event = make_event(
        "reading", located["chapter_id"], {"book_id": located["book_id"], "chapter_id": located["chapter_id"]},
        idempotency_key=idempotency_key,
    )
    errors = validate_event(event)
    if errors:
        raise ValueError("generated reading event is invalid: " + "; ".join(errors))
    append_event(_event_path(roots), event)
    return {"event": event, "status": status(roots), "recorded": True}


def review_concept(
    roots: RootConfig, concept_id: str, payload: dict[str, Any], *, idempotency_key: str | None = None,
) -> dict[str, Any]:
    """Append one review event for a declared concept and schedule its next review."""
    validate_identifier(concept_id, "concept_id")
    located = locate_concept(roots, concept_id)
    events = _events(roots)
    prior = _with_idempotency_key(events, idempotency_key)
    if prior:
        return {
            "event": prior,
            "status": status(roots),
            "schedule": (prior.get("payload") or {}).get("schedule"),
            "chapter_id": located["chapter_id"],
            "recorded": False,
        }
    missing = sorted(set(REVIEW_KEYS) - payload.keys())
    if missing:
        raise ValueError("review payload missing: " + ", ".join(missing))
    errors = validate_review_payload(payload)
    if errors:
        raise ValueError("invalid review payload: " + "; ".join(errors))
    scheduler = FSRSAdapter()
    event = make_review_event(
        concept_id,
        scheduler_version=scheduler.policy.scheduler_version,
        parameter_version=scheduler.policy.parameter_version,
        **{key: payload[key] for key in REVIEW_KEYS},
        idempotency_key=idempotency_key,
    )
    schedule = scheduler.schedule(rating=event["payload"]["final_rating"], state=_previous_state(events, concept_id))
    event["payload"]["schedule"] = schedule
    errors = validate_event(event)
    if errors:
        raise ValueError("generated review event is invalid: " + "; ".join(errors))
    append_event(_event_path(roots), event)
    return {"event": event, "status": status(roots), "schedule": schedule, "chapter_id": located["chapter_id"], "recorded": True}


def due(roots: RootConfig) -> list[dict[str, Any]]:
    """Return the concepts whose latest review is already due."""
    now = datetime.now(timezone.utc)
    latest: dict[str, str | None] = {}
    for event in _of_kind(_events(roots), "review"):
        latest[event["aggregate_id"]] = (event.get("payload") or {}).get("schedule", {}).get("due")
    return [
        {"concept_id": concept_id, "due": due_at}
        for concept_id, due_at in sorted(latest.items())
        if due_at and datetime.fromisoformat(due_at) <= now
    ]
