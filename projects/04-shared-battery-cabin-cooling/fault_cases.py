"""04F — Fault scenarios for the integrated thermal plant.

The faults are intentionally generic proxies. They demonstrate diagnostic
signatures, not OEM failure thresholds.
"""

from typing import Dict

from plant import PlantCase, simulate


FAULTS: Dict[str, Dict[str, float]] = {
    "baseline": {},
    "condenser_airflow_restriction": {
        "condenser_ua_factor": 0.60,
    },
    "compressor_speed_limited": {
        "compressor_speed_limit": 0.70,
    },
    "low_refrigerant_proxy": {
        "subcooling_k": 1.0,
        "superheat_k": 18.0,
        "compressor_capacity_factor": 0.80,
    },
    "battery_flow_maldistribution": {
        "battery_cooling_effectiveness": 0.65,
    },
    "battery_valve_restriction": {
        "valve_battery_limit_kw": 4.0,
    },
}


def run_fault_case(name: str, minutes: int = 60):
    if name not in FAULTS:
        raise KeyError(f"Unknown fault case: {name}")
    return simulate(
        minutes=minutes,
        case=PlantCase(),
        faults=FAULTS[name],
    )


def summarize(name: str, rows):
    peak_battery = max(r["battery_c"] for r in rows)
    peak_cabin = max(r["cabin_c"] for r in rows)
    max_high = max(r["p_high_bar"] for r in rows)
    max_superheat = max(r["superheat_k"] for r in rows)
    min_subcool = min(r["subcooling_k"] for r in rows)
    max_comp = max(r["compressor_kw"] for r in rows)

    return {
        "case": name,
        "peak_battery_c": peak_battery,
        "peak_cabin_c": peak_cabin,
        "max_high_side_bar": max_high,
        "max_superheat_k": max_superheat,
        "min_subcooling_k": min_subcool,
        "max_compressor_kw": max_comp,
    }


if __name__ == "__main__":
    for name in FAULTS:
        rows = run_fault_case(name)
        print(summarize(name, rows))
