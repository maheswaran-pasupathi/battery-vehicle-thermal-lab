import unittest

from compressor_map import operating_point
from fault_cases import FAULTS, run_fault_case
from heat_exchangers import (
    cabin_evaporator_capacity_kw,
    chiller_capacity_kw,
    condenser_condensing_temperature_c,
)
from loads import BatteryInputs, CabinInputs, battery_heat_kw, cabin_cooling_load_kw
from validation import verification_checks


class TestStages04ATo04G(unittest.TestCase):
    def test_compressor_capacity_increases_with_speed(self):
        low = operating_point(3.0, 0.5)
        high = operating_point(3.0, 1.0)
        self.assertGreater(high["capacity_kw"], low["capacity_kw"])

    def test_condenser_restriction_increases_condensing_temperature(self):
        normal = condenser_condensing_temperature_c(30.0, 40.0, 1.0)
        low_fan = condenser_condensing_temperature_c(30.0, 40.0, 0.5)
        self.assertGreater(low_fan, normal)

    def test_positive_loads(self):
        self.assertGreater(cabin_cooling_load_kw(CabinInputs())["total_kw"], 0.0)
        self.assertGreater(battery_heat_kw(BatteryInputs())["total_kw"], 0.0)

    def test_heat_exchanger_capacity_trends(self):
        self.assertGreater(chiller_capacity_kw(35.0, 5.0), 0.0)
        self.assertGreater(cabin_evaporator_capacity_kw(30.0, 5.0), 0.0)

    def test_fault_registry(self):
        self.assertIn("condenser_airflow_restriction", FAULTS)
        rows = run_fault_case("compressor_speed_limited", minutes=2)
        self.assertEqual(len(rows), 3)

    def test_energy_verification(self):
        check = verification_checks()
        self.assertAlmostEqual(check["energy_balance_error_kw"], 0.0, places=6)
        self.assertEqual(check["positive_cop"], 1.0)
        self.assertEqual(check["high_pressure_above_low"], 1.0)


if __name__ == "__main__":
    unittest.main()
