"""Shared battery + cabin cooling model.

Educational reduced-order model only. All default values are illustrative and
must not be interpreted as product specifications.
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class CoolingCase:
    ambient_c: float = 45.0
    cabin_kw: float = 20.0
    battery_kw: float = 8.0
    cop: float = 2.5
    available_cooling_kw: float = 25.0


def total_cooling_demand(cabin_kw: float, battery_kw: float) -> float:
    return max(cabin_kw, 0.0) + max(battery_kw, 0.0)


def compressor_power_kw(cooling_kw: float, cop: float) -> float:
    if cop <= 0:
        raise ValueError("COP must be > 0")
    return max(cooling_kw, 0.0) / cop


def condenser_rejection_kw(cooling_kw: float, compressor_kw: float) -> float:
    return max(cooling_kw, 0.0) + max(compressor_kw, 0.0)


def illustrative_cop_from_ambient(ambient_c: float) -> float:
    """Simple illustrative degradation curve, not a compressor map."""
    return max(1.6, 3.2 - 0.04 * (ambient_c - 25.0))


def illustrative_capacity_from_ambient(ambient_c: float) -> float:
    """Simple illustrative refrigeration-capacity trend, not product data."""
    return max(15.0, 32.0 - 0.35 * (ambient_c - 25.0))


def energy_balance(case: CoolingCase) -> Dict[str, float]:
    total_kw = total_cooling_demand(case.cabin_kw, case.battery_kw)
    compressor_kw = compressor_power_kw(total_kw, case.cop)
    condenser_kw = condenser_rejection_kw(total_kw, compressor_kw)
    return {
        "total_cooling_kw": total_kw,
        "compressor_kw": compressor_kw,
        "condenser_kw": condenser_kw,
    }


def allocate_capacity(
    cabin_demand_kw: float,
    battery_demand_kw: float,
    available_kw: float,
    strategy: str = "battery_priority",
) -> Dict[str, float]:
    cabin = max(cabin_demand_kw, 0.0)
    battery = max(battery_demand_kw, 0.0)
    available = max(available_kw, 0.0)
    total = cabin + battery

    if strategy == "battery_priority":
        battery_delivered = min(battery, available)
        cabin_delivered = min(cabin, max(available - battery_delivered, 0.0))
    elif strategy == "cabin_priority":
        cabin_delivered = min(cabin, available)
        battery_delivered = min(battery, max(available - cabin_delivered, 0.0))
    elif strategy == "proportional":
        fraction = 0.0 if total <= 0 else min(available / total, 1.0)
        cabin_delivered = cabin * fraction
        battery_delivered = battery * fraction
    else:
        raise ValueError(
            "strategy must be 'battery_priority', 'cabin_priority', or 'proportional'"
        )

    return {
        "battery_delivered_kw": battery_delivered,
        "cabin_delivered_kw": cabin_delivered,
        "battery_unmet_kw": max(battery - battery_delivered, 0.0),
        "cabin_unmet_kw": max(cabin - cabin_delivered, 0.0),
        "total_delivered_kw": battery_delivered + cabin_delivered,
    }


def ambient_sweep(
    ambients_c: Iterable[float],
    cabin_kw: float = 20.0,
    battery_kw: float = 8.0,
    strategy: str = "battery_priority",
) -> List[Dict[str, float]]:
    rows = []
    for ambient_c in ambients_c:
        cop = illustrative_cop_from_ambient(ambient_c)
        capacity_kw = illustrative_capacity_from_ambient(ambient_c)
        allocation = allocate_capacity(
            cabin_kw, battery_kw, capacity_kw, strategy=strategy
        )
        delivered_kw = allocation["total_delivered_kw"]
        comp_kw = compressor_power_kw(delivered_kw, cop)
        rows.append(
            {
                "ambient_c": float(ambient_c),
                "cop": cop,
                "available_capacity_kw": capacity_kw,
                "demand_kw": cabin_kw + battery_kw,
                "delivered_kw": delivered_kw,
                "compressor_kw": comp_kw,
                "condenser_kw": condenser_rejection_kw(delivered_kw, comp_kw),
                **allocation,
            }
        )
    return rows


def transient_scenario(
    minutes: Iterable[float],
    ambient_c: float = 45.0,
    strategy: str = "battery_priority",
) -> List[Dict[str, float]]:
    """Illustrative stationary fast-charge + occupied-cabin scenario.

    Cabin demand decays as pull-down completes.
    Battery demand rises during the high-current charging phase and then falls.
    """
    cop = illustrative_cop_from_ambient(ambient_c)
    capacity_kw = illustrative_capacity_from_ambient(ambient_c)
    rows = []

    for minute in minutes:
        minute = float(minute)

        cabin_kw = 22.0 - 7.0 * min(minute / 30.0, 1.0)

        if minute <= 10.0:
            battery_kw = 5.0 + 0.3 * minute
        elif minute <= 35.0:
            battery_kw = 8.0
        else:
            battery_kw = max(4.0, 8.0 - 0.16 * (minute - 35.0))

        allocation = allocate_capacity(
            cabin_kw, battery_kw, capacity_kw, strategy=strategy
        )
        delivered_kw = allocation["total_delivered_kw"]
        comp_kw = compressor_power_kw(delivered_kw, cop)

        rows.append(
            {
                "minute": minute,
                "ambient_c": ambient_c,
                "cabin_demand_kw": cabin_kw,
                "battery_demand_kw": battery_kw,
                "available_capacity_kw": capacity_kw,
                "cop": cop,
                "compressor_kw": comp_kw,
                "condenser_kw": condenser_rejection_kw(delivered_kw, comp_kw),
                **allocation,
            }
        )
    return rows


def _print_base_case() -> None:
    case = CoolingCase()
    balance = energy_balance(case)
    allocation = allocate_capacity(
        case.cabin_kw,
        case.battery_kw,
        case.available_cooling_kw,
        strategy="battery_priority",
    )

    print("Shared battery + cabin cooling — illustrative base case")
    print(f"Ambient: {case.ambient_c:.1f} °C")
    print(f"Cabin demand: {case.cabin_kw:.1f} kW")
    print(f"Battery demand: {case.battery_kw:.1f} kW")
    print(f"Total cooling demand: {balance['total_cooling_kw']:.1f} kW")
    print(f"Compressor power at COP={case.cop:.2f}: {balance['compressor_kw']:.1f} kW")
    print(f"Condenser heat rejection: {balance['condenser_kw']:.1f} kW")
    print(f"Available cooling capacity: {case.available_cooling_kw:.1f} kW")
    print("Battery-priority allocation:")
    print(f"  Battery delivered: {allocation['battery_delivered_kw']:.1f} kW")
    print(f"  Cabin delivered:   {allocation['cabin_delivered_kw']:.1f} kW")
    print(f"  Unmet battery load: {allocation['battery_unmet_kw']:.1f} kW")
    print(f"  Unmet cabin load:   {allocation['cabin_unmet_kw']:.1f} kW")


if __name__ == "__main__":
    _print_base_case()
