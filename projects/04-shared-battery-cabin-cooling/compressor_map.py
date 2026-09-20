"""04B — Synthetic compressor map / operating-envelope model.

This is intentionally generic. It demonstrates interpolation logic and map
limits without claiming any real compressor performance.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class CompressorMap:
    nominal_capacity_kw: float = 30.0
    nominal_power_kw: float = 10.0
    max_pressure_ratio: float = 6.0
    max_discharge_c: float = 120.0


def operating_point(
    pressure_ratio: float,
    speed_ratio: float,
    map_data: CompressorMap = CompressorMap(),
) -> Dict[str, float]:
    speed = min(max(speed_ratio, 0.2), 1.0)
    pr = max(pressure_ratio, 1.01)

    pr_penalty = max(0.25, 1.0 - 0.055 * (pr - 3.0) ** 2)
    efficiency = max(
        0.45,
        min(0.78, 0.72 - 0.045 * (pr - 3.0) ** 2 - 0.08 * (speed - 0.8) ** 2),
    )

    capacity_kw = map_data.nominal_capacity_kw * speed * pr_penalty
    shaft_power_kw = (
        map_data.nominal_power_kw
        * speed
        * (0.72 / efficiency)
        * (1.0 + 0.12 * (pr - 3.0))
    )

    inside_envelope = pr <= map_data.max_pressure_ratio and 0.2 <= speed <= 1.0

    return {
        "speed_ratio": speed,
        "pressure_ratio": pr,
        "isentropic_efficiency": efficiency,
        "capacity_kw": max(capacity_kw, 0.0),
        "map_power_kw": max(shaft_power_kw, 0.0),
        "inside_envelope": float(inside_envelope),
    }


if __name__ == "__main__":
    for speed in (0.5, 0.75, 1.0):
        print(speed, operating_point(4.0, speed))
