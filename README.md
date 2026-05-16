# Parking Location Tool

A practical aviation dispatch workflow concept for tracking aircraft parking locations from fuel request information.

## Overview

The Parking Location Tool is a small operational support project designed to help dispatchers quickly identify aircraft parking locations based on fuel request information.

The project demonstrates how parking-related information can be extracted, structured, and displayed in a simple dashboard format for faster lookup during dispatch operations.

## Problem

In a busy dispatch environment, aircraft parking information can be scattered across fuel request emails, verbal communication, and dispatcher notes.

This can create friction when dispatchers, pilots, or maintenance personnel need to quickly confirm where an aircraft is parked.

## Solution

This project demonstrates a workflow that:

- Reads sample fuel request information
- Extracts key parking-related fields
- Organizes aircraft tail number, ramp, spot, fuel type, and request time
- Displays the information in a simple dashboard-style format
- Supports faster lookup and cleaner dispatcher handoff

## Repository Contents

| Path | Description |
|---|---|
| `sample_data/sample_fuel_requests.csv` | Fictional structured fuel request sample data |
| `sample_data/sample_email_bodies.txt` | Fictional sample email bodies used to show field extraction |
| `docs/workflow.md` | General workflow explanation |
| `docs/data_fields.md` | Data field definitions |
| `dashboard/Parking_Location_sample.html` | Static sample dashboard using fictional data |
| `vba/SampleFuelRequestParser.bas` | Sanitized VBA demo showing basic field extraction from fictional fuel request text |

## Sample Workflow

```text
Fuel Request Email
        ↓
Data Extraction
        ↓
Structured Table
        ↓
Dashboard View
        ↓
Dispatcher Lookup
