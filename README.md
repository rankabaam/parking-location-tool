# Parking Location Tool

A sanitized aviation-operations portfolio project demonstrating how semi-structured operational messages can be converted into a practical aircraft-location decision-support dashboard.

## Overview

This project originated from a recurring dispatch problem: parking information can become fragmented across fuel-service requests, recent movement data, verbal updates, and shift notes. The portfolio version uses fictional aircraft, generalized locations, and synthetic timestamps while preserving the underlying workflow design.

## What the Project Demonstrates

- Parsing semi-structured messages into normalized records
- Combining request history with recent movement signals
- Applying conservative status rules when location confidence is limited
- Presenting operationally useful information through a searchable dashboard and visual map
- Designing fallbacks for partial, delayed, or unavailable data
- Maintaining clear documentation, regression checks, and acceptance criteria

## Generalized Status Model

| Status | Portfolio definition |
|---|---|
| `Parking` | A recent service-location record exists and no later movement is detected |
| `Landed` | A later flight appears to have ended, but no newer service-location record is available |
| `Flying` | Recent movement data indicates the aircraft is airborne |
| `Uncertain` | Available information is stale, incomplete, or insufficient to confirm the current location |

The production workflow uses additional safeguards and operational context that are intentionally excluded from this public repository.

## Architecture

```text
Sanitized request source
        ↓
Field extraction and normalization
        ↓
Optional recent-movement lookup
        ↓
Status and confidence rules
        ↓
Structured table
        ↓
Searchable dashboard / visual map
        ↓
Dispatcher decision support
```

## Repository Contents

| Path | Description |
|---|---|
| `sample_data/` | Fictional request records and sample message bodies |
| `docs/workflow.md` | Generalized workflow explanation |
| `docs/data_fields.md` | Public sample field definitions |
| `dashboard/Parking_Location_sample.html` | Static dashboard using fictional data |
| `vba/SampleFuelRequestParser.bas` | Sanitized VBA field-extraction demonstration |
| `CHANGELOG.md` | Portfolio-level development history |

## Privacy and Scope

This repository does **not** contain employer documents, real aircraft records, employee names, internal system paths, credentials, operational maps, or confidential procedures. It is a generalized portfolio representation of the engineering and workflow-design concepts.

## Current Portfolio Direction

Planned public-safe improvements include:

- A richer fictional status engine
- Synthetic movement events and confidence scoring
- A visual map using invented ramp labels
- Automated regression examples for status-priority rules
- Expanded documentation for failure modes and operational safeguards
