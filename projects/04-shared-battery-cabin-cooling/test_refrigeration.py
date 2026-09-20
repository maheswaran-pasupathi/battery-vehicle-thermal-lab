import unittest

from refrigeration import RefrigerationCase, solve_cycle


class TestRefrigerationCycle(unittest.TestCase):
    def test_energy_balance(self):
        result = solve_cycle(RefrigerationCase())
        self.assertGreater(result["cop"], 1.0)
        self.assertGreater(result["compressor_kw"], 0.0)
        self.assertAlmostEqual(
            result["condenser_kw"],
            25.0 + result["compressor_kw"],
            places=2,
        )

    def test_hotter_condensing_temp_reduces_cop(self):
        low = solve_cycle(RefrigerationCase(condensing_c=45.0))
        high = solve_cycle(RefrigerationCase(condensing_c=60.0))
        self.assertLess(high["cop"], low["cop"])

    def test_more_superheat_changes_state(self):
        a = solve_cycle(RefrigerationCase(superheat_k=5.0))
        b = solve_cycle(RefrigerationCase(superheat_k=15.0))
        self.assertNotEqual(a["t1_suction_c"], b["t1_suction_c"])


if __name__ == "__main__":
    unittest.main()
