"""Level-2 vapor-compression cycle model for Project 04.

Uses CoolProp for refrigerant properties. Default values are educational and
illustrative, not product specifications.
"""

from dataclasses import dataclass
from typing import Dict

from CoolProp.CoolProp import PropsSI


@dataclass(frozen=True)
class RefrigerationCase:
    refrigerant: str = "R134a"
    evaporating_c: float = 5.0
    condensing_c: float = 55.0
    superheat_k: float = 8.0
    subcooling_k: float = 5.0
    isentropic_efficiency: float = 0.70
    cooling_load_kw: float = 25.0
    ambient_c: float = 45.0


def _k(celsius: float) -> float:
    return celsius + 273.15


def solve_cycle(case: RefrigerationCase) -> Dict[str, float]:
    if not (0.0 < case.isentropic_efficiency <= 1.0):
        raise ValueError("isentropic_efficiency must be in (0, 1]")
    if case.condensing_c <= case.evaporating_c:
        raise ValueError("condensing temperature must exceed evaporating temperature")

    ref = case.refrigerant
    p_low = PropsSI("P", "T", _k(case.evaporating_c), "Q", 1, ref)
    p_high = PropsSI("P", "T", _k(case.condensing_c), "Q", 0, ref)

    t1 = _k(case.evaporating_c + case.superheat_k)
    h1 = PropsSI("H", "P", p_low, "T", t1, ref)
    s1 = PropsSI("S", "P", p_low, "T", t1, ref)

    h2s = PropsSI("H", "P", p_high, "S", s1, ref)
    h2 = h1 + (h2s - h1) / case.isentropic_efficiency
    t2 = PropsSI("T", "P", p_high, "H", h2, ref)

    t3 = _k(case.condensing_c - case.subcooling_k)
    h3 = PropsSI("H", "P", p_high, "T", t3, ref)
    h4 = h3

    q_evap = h1 - h4
    w_comp = h2 - h1
    q_cond = h2 - h3

    if q_evap <= 0 or w_comp <= 0:
        raise ValueError("cycle state produced non-physical specific energy terms")

    cop = q_evap / w_comp
    mdot = case.cooling_load_kw * 1000.0 / q_evap
    compressor_kw = mdot * w_comp / 1000.0
    condenser_kw = mdot * q_cond / 1000.0
    condenser_approach_k = case.condensing_c - case.ambient_c
    pressure_ratio = p_high / p_low

    return {
        "p_low_bar": p_low / 1e5,
        "p_high_bar": p_high / 1e5,
        "pressure_ratio": pressure_ratio,
        "t1_suction_c": t1 - 273.15,
        "t2_discharge_c": t2 - 273.15,
        "t3_liquid_c": t3 - 273.15,
        "superheat_k": case.superheat_k,
        "subcooling_k": case.subcooling_k,
        "condenser_approach_k": condenser_approach_k,
        "q_evap_kj_per_kg": q_evap / 1000.0,
        "w_comp_kj_per_kg": w_comp / 1000.0,
        "q_cond_kj_per_kg": q_cond / 1000.0,
        "cop": cop,
        "mass_flow_kg_s": mdot,
        "compressor_kw": compressor_kw,
        "condenser_kw": condenser_kw,
    }


if __name__ == "__main__":
    result = solve_cycle(RefrigerationCase())
    for key, value in result.items():
        print(f"{key}: {value:.3f}")
