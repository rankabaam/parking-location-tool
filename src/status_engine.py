"""Public-safe aircraft location status engine using synthetic records only."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional

class AircraftStatus(str, Enum):
    PARKING = "Parking"
    LANDED = "Landed"
    FLYING = "Flying"
    UNCERTAIN = "Uncertain"

@dataclass(frozen=True)
class FuelRecord:
    tail_number: str
    ramp: str
    spot: str
    request_time: datetime

@dataclass(frozen=True)
class MovementState:
    flight_seen_after_request: bool = False
    airborne_now: Optional[bool] = None
    observed_at: Optional[datetime] = None
    last_confirmed_status: Optional[AircraftStatus] = None
    last_confirmed_time: Optional[datetime] = None

@dataclass(frozen=True)
class StatusDecision:
    status: AircraftStatus
    map_visible: bool
    reason: str
    location_is_exact: bool

def _utc(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)

def classify_status(record: FuelRecord, movement: MovementState, *, now: Optional[datetime] = None,
                    stale_after: timedelta = timedelta(hours=48),
                    flying_hold: timedelta = timedelta(minutes=60)) -> StatusDecision:
    """Apply conservative precedence: stale, airborne, later flight, flying hold, parking."""
    current = _utc(now or datetime.now(timezone.utc))
    request = _utc(record.request_time)
    if current - request >= stale_after:
        return StatusDecision(AircraftStatus.UNCERTAIN, False, "Service-location record is stale.", False)
    observed_after = movement.observed_at is not None and _utc(movement.observed_at) >= request
    if observed_after and movement.airborne_now is True:
        return StatusDecision(AircraftStatus.FLYING, False, "Recent movement evidence indicates airborne.", False)
    if movement.flight_seen_after_request:
        return StatusDecision(AircraftStatus.LANDED, True, "A later flight was detected within the freshness window.", False)
    if (movement.last_confirmed_status == AircraftStatus.FLYING and movement.last_confirmed_time is not None
            and current - _utc(movement.last_confirmed_time) <= flying_hold):
        return StatusDecision(AircraftStatus.FLYING, False, "Recent Flying state retained through a short data gap.", False)
    return StatusDecision(AircraftStatus.PARKING, True, "Fresh service-location record with no later flight.", True)
