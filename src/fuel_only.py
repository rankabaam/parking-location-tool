"""Independent, synthetic Fuel Request-only parking board demo.

No Outlook, ADS-B, FR24, email access or real aircraft data is used.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path


@dataclass(frozen=True)
class FuelEntry:
    aircraft: str
    area: str
    position: str
    requested_at: datetime


def parse_time(value: str) -> datetime:
    timestamp = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("Timestamp must include a timezone")
    return timestamp.astimezone(timezone.utc)


def load_latest(path: Path, *, now: datetime) -> list[FuelEntry]:
    required = {"aircraft", "area", "position", "requested_at"}
    latest: dict[str, FuelEntry] = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Missing required CSV headers")
        for number, row in enumerate(reader, start=2):
            try:
                item = FuelEntry(
                    aircraft=row["aircraft"].strip(),
                    area=row["area"].strip(),
                    position=row["position"].strip(),
                    requested_at=parse_time(row["requested_at"]),
                )
                if not all((item.aircraft, item.area, item.position)):
                    raise ValueError("Blank required value")
                if item.requested_at > now:
                    raise ValueError("Future timestamp")
            except (TypeError, AttributeError, ValueError) as exc:
                raise ValueError(f"Invalid record at line {number}: {exc}") from exc
            old = latest.get(item.aircraft)
            if old is None or item.requested_at >= old.requested_at:
                latest[item.aircraft] = item
    return sorted(latest.values(), key=lambda r: r.aircraft)


def status(record: FuelEntry, *, now: datetime) -> str:
    age = now - record.requested_at
    if age < timedelta(0):
        raise ValueError("Future record timestamp")
    if age >= timedelta(hours=48):
        return "Uncertain"
    if age >= timedelta(hours=24):
        return "Review"
    if age >= timedelta(hours=12):
        return "Aging"
    return "Recent"


def is_map_visible(record: FuelEntry, *, now: datetime) -> bool:
    return status(record, now=now) != "Uncertain"


def render(entries: list[FuelEntry], *, now: datetime) -> str:
    cards = []
    pins = []
    for item in entries:
        label = status(item, now=now)
        age = round((now - item.requested_at).total_seconds() / 3600, 1)
        cards.append(
            "<tr data-search='" + escape((item.aircraft + " " + item.area + " " + item.position).lower(), quote=True) +
            "'><td>" + escape(item.aircraft) + "</td><td>" + escape(item.area) +
            "</td><td>" + escape(item.position) + "</td><td>" +
            escape(item.requested_at.strftime("%Y-%m-%d %H:%M UTC")) + "</td><td>" +
            str(age) + "h</td><td><span class='pill " + label.lower() + "'>" +
            label + "</span></td></tr>"
        )
        if is_map_visible(item, now=now):
            pins.append("<li><strong>" + escape(item.aircraft) + "</strong> — " +
                        escape(item.area) + " / " + escape(item.position) + "</li>")
    content = "\n".join(cards)
    areas = "\n".join(pins) or "<li>No locations within the visual freshness window.</li>"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="30">
<title>Fuel Request-only Location Board — Synthetic Demo</title>
<style>
body{{font:15px system-ui,sans-serif;margin:auto;max-width:1100px;padding:24px;line-height:1.5;background:#f4f7fb;color:#15283b}}
header,.panel{{background:white;border:1px solid #d7e1eb;border-radius:12px;padding:18px;margin:16px 0}}
h1{{margin:0}}.note{{color:#40566b}}table{{border-collapse:collapse;width:100%}}
th,td{{border-bottom:1px solid #dae3ec;text-align:left;padding:10px}}tr:hover{{background:#f1f8ff}}
input{{width:100%;max-width:360px;padding:9px;margin-bottom:12px}}.scroll{{overflow-x:auto}}
.pill{{padding:4px 8px;border-radius:7px;background:#e2f2e7}}.aging{{background:#fff4c9}}
.review{{background:#ffdfb2}}.uncertain{{background:#f5dce1}}
li{{margin:7px 0}}@media(max-width:600px){{body{{padding:10px}}th,td{{padding:5px}}}}
</style></head><body><header><h1>Fuel Request-only Location Board</h1>
<p class="note">Synthetic portfolio demonstration · ADS-B / flight inference disabled · as of {escape(now.strftime("%Y-%m-%d %H:%M UTC"))}</p>
<p>Color bands: recent &lt;12h; aging 12–24h; review 24–48h; uncertain ≥48h.</p>
</header><section class="panel"><h2>Records</h2><input aria-label="Filter aircraft records" id="q" placeholder="Search invented aircraft or location">
<div class="scroll"><table><thead><tr><th>Aircraft</th><th>Area</th><th>Position</th><th>Last request</th><th>Age</th><th>Status</th></tr></thead>
<tbody>{content}</tbody></table></div></section><section class="panel"><h2>Visual location list (recent only)</h2>
<p class="note">A recent service record is a last-reported location, not proof of current aircraft position.</p>
<ul>{areas}</ul></section>
<script>document.getElementById('q').addEventListener('input',e=>{{const q=e.target.value.toLowerCase();
document.querySelectorAll('tbody tr').forEach(tr=>tr.hidden=!tr.dataset.search.includes(q));}})</script>
</body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("sample_data/fuel_only_sample.csv"))
    parser.add_argument("--output", type=Path, default=Path("dashboard/Fuel_Only_sample.html"))
    parser.add_argument("--as-of", help="ISO date-time including timezone, e.g. 2026-08-15T12:00:00Z")
    args = parser.parse_args()
    now = parse_time(args.as_of) if args.as_of else datetime.now(timezone.utc)
    records = load_latest(args.input, now=now)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(records, now=now), encoding="utf-8")
    print(f"Wrote {args.output} ({len(records)} fictional aircraft)")


if __name__ == "__main__":
    main()
