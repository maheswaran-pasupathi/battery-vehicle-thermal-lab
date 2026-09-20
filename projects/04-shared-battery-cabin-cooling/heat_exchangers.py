"""04C — Reduced-order condenser, cabin evaporator and battery chiller."""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Condenser:
    ua_kw_per_k: float = 1.8
    minimum_approach_k: float = 5.0


@dataclass(frozen=True)
class Chiller:
    ua_kw_per_k: float = 1.1
    minimum_approach_k: float = 3.0


@dataclass(frozen=True)
class CabinEvaporator:
    ua_kw_per_k: float = 1.4
    minimum_approach_k: float = 5.0


def condenser_condensing_temperature_c(
    q_reject_kw: float,
    ambient_c: float,
    fan_ratio: float = 1.0,
    condenser: Condenser = Condenser(),
) -> float:
    effective_ua = condenser.ua_kw_per_k * max(fan_ratio, 0.15)
    approach = max(condenser.minimum_approach_k, q_reject_kw / effective_ua)
    return ambient_c + approach


def chiller_capacity_kw(
    coolant_in_c: float,
    evaporating_c: float,
    chiller: Chiller = Chiller(),
) -> float:
    delta_t = max(
        coolant_in_c - evaporating_c - chiller.minimum_approach_k,
        0.0,
    )
    return chiller.ua_kw_per_k * delta_t


def cabin_evaporator_capacity_kw(
    cabin_air_in_c: float,
    evaporating_c: float,
    evaporator: CabinEvaporator = CabinEvaporator(),
) -> float:
    delta_t = max(
        cabin_air_in_c - evaporating_c - evaporator.minimum_approach_k,
        0.0,
    )
    return evaporator.ua_kw_per_k * delta_t


def exchanger_summary(
    q_reject_kw: float,
    ambient_c: float,
    fan_ratio: float,
    coolant_in_c: float,
    cabin_air_in_c: float,
    evaporating_c: float,
) -> Dict[str, float]:
    return {
        "condensing_c": condenser_condensing_temperature_c(
            q_reject_kw, ambient_c, fan_ratio
        ),
        "chiller_capacity_kw": chiller_capacity_kw(coolant_in_c, evaporating_c),
        "cabin_evap_capacity_kw": cabin_evaporator_capacity_kw(
            cabin_air_in_c, evaporating_c
        ),
    }
