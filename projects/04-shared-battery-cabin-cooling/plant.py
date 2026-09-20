"""04E — Integrated transient shared battery/cabin thermal plant.

The model is deliberately reduced order. It is intended for reasoning,
sensitivity studies and interview preparation, not vehicle design.
"""

from dataclasses import dataclass
from typing import Dict, List

from compressor_map import operating_point
from controls import controller
from heat_exchangers import condenser_condensing_temperature_c
from loads import BatteryInputs, CabinInputs, battery_heat_kw, cabin_cooling_load_kw
from model import allocate_capacity
from refrigeration import RefrigerationCase, solve_cycle


@dataclass(frozen=True)
class PlantCase:
    ambient_c: float = 45.0
    cabin_initial_c: float = 38.0
    battery_initial_c: float = 36.0
    cabin_thermal_mass_kj_per_k: float = 900.0
    battery_thermal_mass_kj_per_k: float = 3600.0
    battery_current_a: float = 450.0
    battery_resistance_ohm: float = 0.035
    evaporating_c: float = 5.0
    base_subcooling_k: float = 5.0
    base_superheat_k: float = 8.0
    dt_s: float = 60.0


def _solve_refrigeration_fixed_point(
    ambient_c: float,
    evaporating_c: float,
    delivered_kw: float,
    compressor_speed_ratio: float,
    fan_ratio: float,
    superheat_k: float,
    subcooling_k: float,
    condenser_ua_factor: float = 1.0,
    compressor_capacity_factor: float = 1.0,
):
    condensing_c = ambient_c + 12.0
    cycle = None
    map_pt = None

    for _ in range(8):
        trial = solve_cycle(
            RefrigerationCase(
                evaporating_c=evaporating_c,
                condensing_c=condensing_c,
                superheat_k=superheat_k,
                subcooling_k=subcooling_k,
                isentropic_efficiency=0.70,
                cooling_load_kw=max(delivered_kw, 0.1),
                ambient_c=ambient_c,
            )
        )
        map_pt = operating_point(
            trial["pressure_ratio"],
            compressor_speed_ratio,
        )
        eta = map_pt["isentropic_efficiency"]
        capacity_kw = map_pt["capacity_kw"] * compressor_capacity_factor

        actual_load = min(max(delivered_kw, 0.1), capacity_kw)
        cycle = solve_cycle(
            RefrigerationCase(
                evaporating_c=evaporating_c,
                condensing_c=condensing_c,
                superheat_k=superheat_k,
                subcooling_k=subcooling_k,
                isentropic_efficiency=eta,
                cooling_load_kw=actual_load,
                ambient_c=ambient_c,
            )
        )

        ua_scale = max(condenser_ua_factor, 0.2)
        new_condensing = condenser_condensing_temperature_c(
            cycle["condenser_kw"] / ua_scale,
            ambient_c,
            fan_ratio,
        )
        condensing_c = 0.55 * condensing_c + 0.45 * new_condensing

    return cycle, map_pt


def simulate(
    minutes: int = 60,
    case: PlantCase = PlantCase(),
    faults: Dict[str, float] | None = None,
) -> List[Dict[str, float]]:
    faults = faults or {}
    battery_c = case.battery_initial_c
    cabin_c = case.cabin_initial_c
    rows = []

    condenser_ua_factor = faults.get("condenser_ua_factor", 1.0)
    compressor_capacity_factor = faults.get("compressor_capacity_factor", 1.0)
    battery_cooling_effectiveness = faults.get("battery_cooling_effectiveness", 1.0)
    valve_battery_limit_kw = faults.get("valve_battery_limit_kw", 1e9)
    subcooling_k = faults.get("subcooling_k", case.base_subcooling_k)
    superheat_k = faults.get("superheat_k", case.base_superheat_k)

    for minute in range(minutes + 1):
        cabin_load = cabin_cooling_load_kw(
            CabinInputs(
                ambient_c=case.ambient_c,
                cabin_c=cabin_c,
                solar_kw=5.0,
                occupants=4,
                latent_kw=1.5,
            )
        )["total_kw"]

        current = case.battery_current_a if minute <= 35 else 0.65 * case.battery_current_a
        batt_load = battery_heat_kw(
            BatteryInputs(
                current_a=current,
                resistance_ohm=case.battery_resistance_ohm,
                temperature_c=battery_c,
            )
        )["total_kw"]

        command = controller(
            battery_c=battery_c,
            cabin_c=cabin_c,
            total_demand_kw=cabin_load + batt_load,
        )

        speed = min(
            command["compressor_speed_ratio"],
            faults.get("compressor_speed_limit", 1.0),
        )

        preliminary_cycle, map_pt = _solve_refrigeration_fixed_point(
            ambient_c=case.ambient_c,
            evaporating_c=case.evaporating_c,
            delivered_kw=cabin_load + batt_load,
            compressor_speed_ratio=speed,
            fan_ratio=command["fan_ratio"],
            superheat_k=superheat_k,
            subcooling_k=subcooling_k,
            condenser_ua_factor=condenser_ua_factor,
            compressor_capacity_factor=compressor_capacity_factor,
        )

        available = map_pt["capacity_kw"] * compressor_capacity_factor
        allocation = allocate_capacity(
            cabin_load,
            batt_load,
            available,
            strategy=command["strategy"],
        )

        battery_delivered = min(
            allocation["battery_delivered_kw"] * battery_cooling_effectiveness,
            valve_battery_limit_kw,
        )
        cabin_delivered = allocation["cabin_delivered_kw"]
        total_delivered = battery_delivered + cabin_delivered

        cycle, map_pt = _solve_refrigeration_fixed_point(
            ambient_c=case.ambient_c,
            evaporating_c=case.evaporating_c,
            delivered_kw=max(total_delivered, 0.1),
            compressor_speed_ratio=speed,
            fan_ratio=command["fan_ratio"],
            superheat_k=superheat_k,
            subcooling_k=subcooling_k,
            condenser_ua_factor=condenser_ua_factor,
            compressor_capacity_factor=compressor_capacity_factor,
        )

        net_cabin_kw = cabin_load - cabin_delivered
        net_batt_kw = batt_load - battery_delivered

        cabin_c += net_cabin_kw * case.dt_s / case.cabin_thermal_mass_kj_per_k
        battery_c += net_batt_kw * case.dt_s / case.battery_thermal_mass_kj_per_k

        rows.append(
            {
                "minute": float(minute),
                "cabin_c": cabin_c,
                "battery_c": battery_c,
                "cabin_load_kw": cabin_load,
                "battery_load_kw": batt_load,
                "cabin_delivered_kw": cabin_delivered,
                "battery_delivered_kw": battery_delivered,
                "compressor_speed_ratio": speed,
                "fan_ratio": command["fan_ratio"],
                "strategy_battery_priority": float(command["strategy"] == "battery_priority"),
                "available_capacity_kw": map_pt["capacity_kw"] * compressor_capacity_factor,
                **cycle,
            }
        )

    return rows


if __name__ == "__main__":
    rows = simulate()
    print(rows[-1])
