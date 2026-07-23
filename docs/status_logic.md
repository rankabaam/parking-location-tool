# Status Logic

The public engine separates the latest recorded service location from later synthetic movement evidence.

## Decision Order

1. At or beyond 48 hours, classify the record as `Uncertain`.
2. A valid current airborne observation produces `Flying`.
3. A later detected flight inside the freshness window produces `Landed`; the old spot is no longer exact.
4. A recently confirmed `Flying` state may be retained briefly through an observation gap.
5. Otherwise, a fresh service-location record remains `Parking`.

## Visual Map

- `Parking`: shown at the recorded spot.
- `Landed`: shown at ramp level only.
- `Flying`: hidden.
- `Uncertain`: hidden.

## Limits

The demo does not determine availability, airworthiness, fuel state, dispatch authorization, or exact real-time position. It demonstrates explicit confidence handling, status precedence, and safe fallback behavior using fictional records.
