"""Generate a public-safe dashboard from synthetic JSON records."""
from __future__ import annotations
import argparse, html, json, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.status_engine import FuelRecord, MovementState, classify_status

def dt(value):
    return datetime.fromisoformat(value) if value else None

def build_rows(items, now):
    rows=[]
    for item in items:
        decision=classify_status(
            FuelRecord(item["tail_number"], item["ramp"], item["spot"], dt(item["request_time"])),
            MovementState(bool(item.get("flight_seen_after_request")), item.get("airborne_now"), dt(item.get("observed_at"))),
            now=now,
        )
        rows.append({**item,"status":decision.status.value,"map_visible":decision.map_visible,
                     "location_is_exact":decision.location_is_exact,"reason":decision.reason})
    return rows

def render(rows, generated_at):
    payload=json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Aircraft Location Demo</title>
<style>:root{{--bg:#eef2f7;--panel:#fff;--text:#17202a;--line:#d8dee8}}body.dark{{--bg:#111827;--panel:#1f2937;--text:#f3f4f6;--line:#374151}}*{{box-sizing:border-box}}body{{margin:0;font-family:Arial;background:var(--bg);color:var(--text)}}header{{padding:24px;background:#172b4d;color:white}}main{{max-width:1200px;margin:auto;padding:24px}}.panel,.notice{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}}.notice{{margin-bottom:16px}}.controls{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}}input,select,button{{padding:9px;border:1px solid var(--line);border-radius:7px;background:var(--panel);color:var(--text)}}.grid{{display:grid;grid-template-columns:1.3fr .7fr;gap:16px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border-bottom:1px solid var(--line);text-align:left;font-size:14px}}.Parking{{color:#147d42}}.Landed{{color:#a15c00}}.Flying{{color:#1d63c4}}.Uncertain{{color:#b42318}}.ramp{{border:1px solid var(--line);border-radius:9px;padding:10px;margin-bottom:10px}}.aircraft{{display:inline-block;margin:4px;padding:7px 9px;border-radius:7px;background:#dbeafe;color:#17375e;font-weight:bold}}.approx{{border:2px dashed #b7791f;background:#fef3c7}}@media(max-width:850px){{.grid{{grid-template-columns:1fr}}}}</style></head>
<body><header><h1>Aircraft Location Decision-Support Demo</h1><p>Synthetic records, conservative status logic, and map-visibility rules.</p></header><main><div class="notice"><b>Portfolio-only demo.</b> All aircraft, locations, and events are fictional.</div><div class="controls"><input id="search" placeholder="Search"><select id="filter"><option value="">All statuses</option><option>Parking</option><option>Landed</option><option>Flying</option><option>Uncertain</option></select><button id="theme">Toggle theme</button><button onclick="print()">Print</button></div><div class="grid"><section class="panel"><h2>Reference table</h2><table><thead><tr><th>Tail</th><th>Aircraft</th><th>Location</th><th>Status</th><th>Basis</th></tr></thead><tbody id="rows"></tbody></table></section><section class="panel"><h2>Visual map</h2><p>Parking is exact; Landed is ramp-level only.</p><div id="map"></div></section></div><p>Generated {html.escape(generated_at.isoformat(timespec="minutes"))}</p></main>
<script>const records={payload};const rows=document.getElementById('rows'),map=document.getElementById('map'),search=document.getElementById('search'),filter=document.getElementById('filter');function draw(){{const q=search.value.toLowerCase(),s=filter.value,v=records.filter(r=>(!s||r.status===s)&&JSON.stringify(r).toLowerCase().includes(q));rows.innerHTML=v.map(r=>`<tr><td>${{r.tail_number}}</td><td>${{r.aircraft}}</td><td>${{r.ramp}} / ${{r.spot}}</td><td class="${{r.status}}"><b>${{r.status}}</b></td><td title="${{r.reason}}">${{r.location_is_exact?'service location':'approximate / movement-derived'}}</td></tr>`).join('');const ramps={{}};v.filter(r=>r.map_visible).forEach(r=>(ramps[r.ramp]??=[]).push(r));map.innerHTML=Object.keys(ramps).sort().map(name=>`<div class="ramp"><b>${{name}}</b><div>${{ramps[name].map(r=>`<span class="aircraft ${{r.location_is_exact?'':'approx'}}">${{r.tail_number}} · ${{r.location_is_exact?r.spot:'ramp only'}}</span>`).join('')}}</div></div>`).join('')||'<p>No map-eligible records.</p>'}}search.oninput=draw;filter.onchange=draw;document.getElementById('theme').onclick=()=>document.body.classList.toggle('dark');draw();</script></body></html>'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,default=ROOT/'sample_data/status_scenarios.json');parser.add_argument('--output',type=Path,default=ROOT/'dashboard/Parking_Location_sample.html');parser.add_argument('--now',default='2026-07-23T15:00:00+00:00');args=parser.parse_args()
    now=datetime.fromisoformat(args.now).astimezone(timezone.utc);items=json.loads(args.input.read_text(encoding='utf-8'));args.output.write_text(render(build_rows(items,now),now),encoding='utf-8');print(f'Wrote {args.output}')
if __name__=='__main__':main()
