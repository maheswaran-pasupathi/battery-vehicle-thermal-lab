import math
import unittest

from model import (
    CoolingCase,
    allocate_capacity,
    compressor_power_kw,
    condenser_rejection_kw,
    energy_balance,
    illustrative_capacity_from_ambient,
    illustrative_cop_from_ambient,
)


class TestSharedCooling(unittest.TestCase):
    def test_base_energy_balance(self):
        result = energy_balance(CoolingCase())
        self.assertTrue(math.isclose(result["total_cooling_kw"], 28.0))
        self.assertTrue(math.isclose(result["compressor_kw"], 11.2))
        self.assertTrue(math.isclose(result["condenser_kw"], 39.2))

    def test_battery_priority(self):
        result = allocate_capacity(20.0, 8.0, 25.0, "battery_priority")
        self.assertTrue(math.isclose(result["battery_delivered_kw"], 8.0))
        self.assertTrue(math.isclose(result["cabin_delivered_kw"], 17.0))
        self.assertTrue(math.isclose(result["cabin_unmet_kw"], 3.0))

    def test_conservation_under_capacity_limit(self):
        result = allocate_capacity(20.0, 8.0, 25.0, "proportional")
        self.assertLessEqual(result["total_delivered_kw"], 25.0 + 1e-12)

    def test_hotter_ambient_degrades_simple_map(self):
        self.assertLess(
            illustrative_cop_from_ambient(45.0),
            illustrative_cop_from_ambient(25.0),
        )
        self.assertLess(
            illustrative_capacity_from_ambient(45.0),
            illustrative_capacity_from_ambient(25.0),
        )

    def test_condenser_rejection(self):
        self.assertTrue(
            math.isclose(condenser_rejection_kw(28.0, 11.2), 39.2)
        )

    def test_invalid_cop(self):
        with self.assertRaises(ValueError):
            compressor_power_kw(10.0, 0.0)


if __name__ == "__main__":
    unittest.main()
