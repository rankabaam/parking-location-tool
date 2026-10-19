# Fuel Request-only Mode — Portfolio Update (October 2026)

The public demo originally showed a simulated four-state ADS-B-assisted model (`Parking`, `Landed`, `Flying`, `Uncertain`). That earlier experiment remains available under `src/status_engine.py` for comparison.

**The later operational design decision was to remove ADS-B / external flight-status checks.** An independent, non-operational sample of that simpler approach is now available in `src/fuel_only.py`.

## Demonstrated workflow

1. Import only fictional service-request location records from a local CSV.
2. Keep the latest record per invented aircraft identifier.
3. Classify information age: under 12h, 12–24h, 24–48h, or 48h and older.
4. Show locations newer than 48h in an offline visual location list.
5. Mark older records `Uncertain` and exclude them from that list.
6. The HTML refreshes itself every 30 seconds; source CSV ingestion requires regenerating the page.

This app **does not** infer aircraft movement or whether a plane has departed. That distinction is deliberate: a recent service request is not a verified live location.

## Run

```bash
python -m src.fuel_only --as-of 2026-08-15T12:00:00Z
python -m unittest discover -s tests -v
```

Open `dashboard/Fuel_Only_sample.html`. For real-time timestamps, omit `--as-of` and supply new fictional test entries. Do not use this as a dispatch, safety, or tracking authority.

## Portfolio and privacy boundaries

The reference records, location names, age bands in this sample, and aircraft IDs are fictional or generic. This demo does not collect emails, interface with Outlook, read live Excel books, access ADS-B/FR24, or contain employer-specific settings or code.
