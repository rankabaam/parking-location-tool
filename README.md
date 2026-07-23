# Parking Location Tool

A sanitized aviation-operations portfolio project that turns synthetic service-location records and movement signals into a searchable aircraft-location decision-support dashboard.

## Portfolio Demo

This repository now includes a runnable, standard-library Python demo rather than only a static mockup.

```bash
python scripts/generate_demo_dashboard.py
python -m unittest discover -s tests
```

Open `dashboard/Parking_Location_sample.html` after generation.

The demo uses fictional aircraft, invented ramp names, synthetic timestamps, and simulated movement states. It does not connect to email, spreadsheets, employer systems, or live aircraft-tracking services.

## What the Project Demonstrates

- Parsing and normalizing semi-structured operational records
- Combining service-location history with later movement signals
- Applying conservative status precedence when data becomes incomplete or stale
- Separating table visibility from visual-map eligibility
- Distinguishing exact service locations from approximate post-flight ramp placement
- Generating a searchable, printable, dark/light HTML dashboard
- Protecting behavior with regression tests

## Generalized Status Model

| Status | Public demo rule | Visual map |
|---|---|---|
| `Parking` | A fresh service-location record exists and no later flight is detected | Shown at the recorded spot |
| `Landed` | A post-request flight occurred within the freshness window and the aircraft is no longer treated as airborne | Shown approximately within the last known ramp |
| `Flying` | A current or briefly retained movement state indicates airborne | Hidden |
| `Uncertain` | The service-location record reached the stale threshold | Hidden |

Rule precedence is intentionally conservative:

1. Stale record → `Uncertain`
2. Current airborne observation → `Flying`
3. Post-request flight within the freshness window → `Landed`
4. Otherwise → `Parking`

## Architecture

```text
Synthetic service-location records
              ↓
Field normalization
              ↓
Synthetic movement-state input
              ↓
Pure status engine
              ↓
Map-visibility and confidence decision
              ↓
Generated HTML table + ramp view
              ↓
Unit-test regression checks
```

## Repository Contents

| Path | Description |
|---|---|
| `src/status_engine.py` | Pure, reusable status-classification logic |
| `scripts/generate_demo_dashboard.py` | Generates the public HTML dashboard |
| `sample_data/status_scenarios.json` | Fictional records covering all four statuses |
| `dashboard/Parking_Location_sample.html` | Generated searchable table and visual ramp view |
| `tests/test_status_engine.py` | Regression tests for status precedence and visibility |
| `docs/status_logic.md` | Decision rules, assumptions, and limitations |
| `vba/SampleFuelRequestParser.bas` | Earlier sanitized field-extraction example |
| `CHANGELOG.md` | Portfolio development history |

## Safety and Scope

This is a **situational-awareness and software-design demonstration**, not an official tracking, dispatch, release, maintenance, or airworthiness source.

The public repository excludes:

- Employer names and internal procedures
- Real aircraft records or ramp layouts
- Employee names and contact information
- Internal file paths, email folders, or system menus
- Credentials, API keys, and production configuration
- Production ADS-B integration and operational thresholds beyond generalized examples

## Current Status

The public demo is independently runnable and testable. The production implementation contains additional integration, recovery, scheduling, and validation behavior that is intentionally not published.
