"""04A — Couple shared cabin/battery demand to the refrigeration cycle."""

from typing import Dict

from model import allocate_capacity
from refrigeration import RefrigerationCase, solve_cycle


def solve_shared_cycle(
    cabin_demand_kw: float,
    battery_demand_kw: float,
    available_cooling_kw: float,
    evaporating_c: float,
    condensing_c: float,
    superheat_k: float = 8.0,
    subcooling_k: float = 5.0,
    isentropic_efficiency: float = 0.70,
    ambient_c: float = 45.0,
    strategy: str = "battery_priority",
) -> Dict[str, float]:
    allocation = allocate_capacity(
        cabin_demand_kw,
        battery_demand_kw,
        available_cooling_kw,
        strategy=strategy,
    )
    delivered_kw = allocation["total_delivered_kw"]

    cycle = solve_cycle(
        RefrigerationCase(
            evaporating_c=evaporating_c,
            condensing_c=condensing_c,
            superheat_k=superheat_k,
            subcooling_k=subcooling_k,
            isentropic_efficiency=isentropic_efficiency,
            cooling_load_kw=delivered_kw,
            ambient_c=ambient_c,
        )
    )

    return {
        "cabin_demand_kw": cabin_demand_kw,
        "battery_demand_kw": battery_demand_kw,
        "available_cooling_kw": available_cooling_kw,
        **allocation,
        **cycle,
    }


if __name__ == "__main__":
    result = solve_shared_cycle(
        cabin_demand_kw=20.0,
        battery_demand_kw=8.0,
        available_cooling_kw=25.0,
        evaporating_c=5.0,
        condensing_c=55.0,
    )
    for key, value in result.items():
        if isinstance(value, float):
            print(f"{key}: {value:.3f}")
