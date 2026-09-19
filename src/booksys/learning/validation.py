"""Validation rules for learning inputs and append-only event records."""

from __future__ import annotations

from datetime import datetime
import math
from typing import Any, Iterable

from ..domain.contracts import ALLOWED_RATINGS, validate_identifier

EVENT_KINDS = frozenset({"reading", "review"})
FSRS_STATES = frozenset({"New", "Learning", "Review", "Relearning"})
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
SCHEDULE_KEYS = (
    "rating",
    "desired_retention",
    "scheduler_version",
    "parameter_version",
    "due",
    "state",
    "review_datetime",
)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _timestamp(value: Any, field: str) -> list[str]:
    if not isinstance(value, str) or not value:
        return [f"{field} must be an ISO-8601 timestamp"]
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return [f"{field} must be an ISO-8601 timestamp"]
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return [f"{field} must include a timezone"]
    return []


def _identifier(value: Any, field: str) -> list[str]:
    try:
        validate_identifier(value, field)
    except ValueError as exc:
        return [str(exc)]
    return []


def _string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        return [f"{field} must be a list of strings"]
    return []


def validate_review_payload(payload: Any, *, include_schedule: bool = False) -> list[str]:
    """Validate a trainer submission or the evidence portion of a review event."""
    if not isinstance(payload, dict):
        return ["review payload must be an object"]
    errors: list[str] = []
    for key in REVIEW_KEYS:
        if key not in payload:
            errors.append(f"review payload missing: {key}")
    if errors:
        return errors
    if not isinstance(payload["question_kind"], str) or not payload["question_kind"].strip():
        errors.append("question_kind must be a non-empty string")
    level = payload["target_level"]
    if not isinstance(level, int) or isinstance(level, bool) or not 1 <= level <= 5:
        errors.append("target_level must be an integer from 1 to 5")
    for key in ("emt_expectations", "misconceptions", "emt_hits"):
        errors.extend(_string_list(payload[key], key))
    if not _is_number(payload["emt_score"]) or not 0 <= payload["emt_score"] <= 1:
        errors.append("emt_score must be a number from 0 to 1")
    if not isinstance(payload["objective_pass"], bool):
        errors.append("objective_pass must be a boolean")
    if not _is_number(payload["confidence"]) or not 0 <= payload["confidence"] <= 1:
        errors.append("confidence must be a number from 0 to 1")
    if payload["user_rating"] not in ALLOWED_RATINGS - {"again"}:
        errors.append("user_rating must be hard, good, or easy")
    if payload["objective_pass"] and not set(payload["emt_hits"]).issubset(set(payload["emt_expectations"])):
        errors.append("emt_hits must be drawn from emt_expectations")
    if include_schedule:
        errors.extend(validate_schedule(payload.get("schedule"), payload.get("final_rating"), payload.get("objective_pass"), payload.get("user_rating")))
    return errors


def validate_schedule(schedule: Any, final_rating: Any = None, objective_pass: Any = None, user_rating: Any = None) -> list[str]:
    if not isinstance(schedule, dict):
        return ["schedule must be an object"]
    errors: list[str] = []
    for key in SCHEDULE_KEYS:
        if key not in schedule:
            errors.append(f"schedule missing: {key}")
    if errors:
        return errors
    rating = schedule["rating"]
    if rating not in ALLOWED_RATINGS:
        errors.append("schedule.rating must be again, hard, good, or easy")
    if final_rating is not None and rating != final_rating:
        errors.append("schedule.rating must equal final_rating")
    if objective_pass is not None and isinstance(objective_pass, bool):
        expected = user_rating if objective_pass else "again"
        if final_rating != expected:
            errors.append("final_rating is inconsistent with objective_pass and user_rating")
    retention = schedule["desired_retention"]
    if not _is_number(retention) or not 0 < retention <= 1:
        errors.append("schedule.desired_retention must be a number greater than 0 and at most 1")
    for key in ("scheduler_version", "parameter_version"):
        if not isinstance(schedule[key], str) or not schedule[key].strip():
            errors.append(f"schedule.{key} must be a non-empty string")
    errors.extend(_timestamp(schedule["due"], "schedule.due"))
    errors.extend(_timestamp(schedule["review_datetime"], "schedule.review_datetime"))
    state = schedule["state"]
    if not isinstance(state, dict):
        errors.append("schedule.state must be an object")
    else:
        if state.get("state") not in FSRS_STATES:
            errors.append("schedule.state.state is not a supported FSRS state")
        step = state.get("step")
        if step is not None and (not isinstance(step, int) or isinstance(step, bool) or step < 0):
            errors.append("schedule.state.step must be a non-negative integer or null")
        for key in ("stability", "difficulty"):
            if state.get(key) is not None and (not _is_number(state[key]) or state[key] < 0):
                errors.append(f"schedule.state.{key} must be a non-negative number or null")
        for key in ("due", "last_review"):
            if state.get(key) is not None:
                errors.extend(_timestamp(state[key], f"schedule.state.{key}"))
    return errors


def validate_event(event: Any) -> list[str]:
    """Return all structural and kind-specific errors for one event."""
    if not isinstance(event, dict):
        return ["event must be an object"]
    required = ("schema_version", "event_id", "kind", "aggregate_id", "occurred_at", "idempotency_key", "payload")
    errors = [f"event missing: {key}" for key in required if key not in event]
    if errors:
        return errors
    if event["schema_version"] != 1:
        errors.append("schema_version must be 1")
    errors.extend(_identifier(event["event_id"], "event_id"))
    if event["kind"] not in EVENT_KINDS:
        errors.append("kind must be reading or review")
    errors.extend(_identifier(event["aggregate_id"], "aggregate_id"))
    errors.extend(_timestamp(event["occurred_at"], "occurred_at"))
    if not isinstance(event["idempotency_key"], str) or not event["idempotency_key"]:
        errors.append("idempotency_key must be a non-empty string")
    payload = event["payload"]
    if event["kind"] == "reading":
        if not isinstance(payload, dict):
            errors.append("reading payload must be an object")
        else:
            for key in ("book_id", "chapter_id"):
                errors.extend(_identifier(payload.get(key), f"payload.{key}"))
            if payload.get("chapter_id") != event["aggregate_id"]:
                errors.append("aggregate_id must equal payload.chapter_id")
    elif event["kind"] == "review":
        errors.extend(_identifier(event["aggregate_id"], "concept_id"))
        errors.extend(validate_review_payload(payload, include_schedule=False))
        if isinstance(payload, dict):
            final = payload.get("final_rating")
            if final not in ALLOWED_RATINGS:
                errors.append("final_rating must be again, hard, good, or easy")
            errors.extend(validate_schedule(payload.get("schedule"), final, payload.get("objective_pass"), payload.get("user_rating")))
    return errors


def validate_events(events: Iterable[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for event in events:
        errors.extend(validate_event(event))
    return errors
