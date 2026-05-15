# Data Fields

This document defines the sample data fields used in the Parking Location Tool.

All examples in this repository use fictional data for demonstration purposes only.

## Field Definitions

| Field Name | Description | Example |
|---|---|---|
| `tail_number` | Aircraft registration or aircraft identifier used in the sample request | `N123AB` |
| `ramp` | Generalized parking ramp label | `Ramp A` |
| `spot` | Parking spot number within the ramp area | `4` |
| `fuel_type` | Requested fuel type | `100LL` |
| `request_time` | Time when the sample fuel request was received or recorded | `2026-05-15 07:32` |

## Example Record

```csv
tail_number,ramp,spot,fuel_type,request_time
N123AB,Ramp A,4,100LL,2026-05-15 07:32
