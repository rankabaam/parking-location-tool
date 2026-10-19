import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.fuel_only import FuelEntry, is_map_visible, load_latest, parse_time, render, status

NOW = datetime(2026, 8, 15, 12, tzinfo=timezone.utc)


class FuelOnlyTests(unittest.TestCase):
    def record(self, age):
        return FuelEntry("DEMO-001", "Area A", "Spot A", NOW - age)

    def test_color_boundaries(self):
        for hours, expected in ((0, "Recent"), (12, "Aging"), (24, "Review"), (48, "Uncertain")):
            self.assertEqual(status(self.record(timedelta(hours=hours)), now=NOW), expected)

    def test_map_freshness(self):
        self.assertTrue(is_map_visible(self.record(timedelta(hours=47)), now=NOW))
        self.assertFalse(is_map_visible(self.record(timedelta(hours=49)), now=NOW))

    def test_latest_duplicate_wins(self):
        csv_text = ("aircraft,area,position,requested_at\n"
                    "FAKE-1,Alpha,Old,2026-08-14T08:00:00Z\n"
                    "FAKE-1,Bravo,New,2026-08-15T08:00:00Z\n")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.csv"
            path.write_text(csv_text, encoding="utf-8")
            records = load_latest(path, now=NOW)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].position, "New")

    def test_escaping(self):
        record = FuelEntry("<script>alert(1)</script>", "Area A", "Spot", NOW)
        page = render([record], now=NOW)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_future_and_missing_tz_rejected(self):
        with self.assertRaises(ValueError):
            parse_time("2026-08-15T12:00:00")
        with self.assertRaises(ValueError):
            status(FuelEntry("X", "A", "B", NOW + timedelta(minutes=1)), now=NOW)

    def test_bad_csv_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text("aircraft,area,position,requested_at\nA,A,B,2026-08-20T00:00:00Z\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_latest(path, now=NOW)


if __name__ == "__main__":
    unittest.main()
