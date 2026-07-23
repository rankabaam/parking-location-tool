from datetime import datetime, timedelta, timezone
import unittest
from src.status_engine import AircraftStatus, FuelRecord, MovementState, classify_status

NOW = datetime(2026, 7, 23, 15, 0, tzinfo=timezone.utc)

class StatusEngineTests(unittest.TestCase):
    def record(self, hours_old=1):
        return FuelRecord("N101PX", "Ramp Alpha", "A-04", NOW - timedelta(hours=hours_old))

    def test_parking(self):
        result = classify_status(self.record(), MovementState(), now=NOW)
        self.assertEqual(result.status, AircraftStatus.PARKING)
        self.assertTrue(result.map_visible)

    def test_flying(self):
        state = MovementState(True, True, NOW)
        result = classify_status(self.record(), state, now=NOW)
        self.assertEqual(result.status, AircraftStatus.FLYING)
        self.assertFalse(result.map_visible)

    def test_landed(self):
        state = MovementState(True, False, NOW)
        result = classify_status(self.record(12), state, now=NOW)
        self.assertEqual(result.status, AircraftStatus.LANDED)
        self.assertTrue(result.map_visible)
        self.assertFalse(result.location_is_exact)

    def test_stale_overrides_landed(self):
        state = MovementState(True, False, NOW)
        result = classify_status(self.record(49), state, now=NOW)
        self.assertEqual(result.status, AircraftStatus.UNCERTAIN)
        self.assertFalse(result.map_visible)

    def test_short_flying_hold(self):
        state = MovementState(last_confirmed_status=AircraftStatus.FLYING,
                              last_confirmed_time=NOW - timedelta(minutes=30))
        self.assertEqual(classify_status(self.record(), state, now=NOW).status, AircraftStatus.FLYING)

if __name__ == "__main__":
    unittest.main()
