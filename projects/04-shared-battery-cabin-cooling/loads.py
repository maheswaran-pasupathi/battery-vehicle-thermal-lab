"""04D — Cabin and battery thermal-load models."""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class CabinInputs:
    ambient_c: float = 45.0
    cabin_c: float = 30.0
    ua_kw_per_k: float = 0.55
    solar_kw: float = 5.0
    occupants: int = 4
    occupant_sensible_kw_each: float = 0.10
    ventilation_kw: float = 1.5
    latent_kw: float = 1.5


@dataclass(frozen=True)
class BatteryInputs:
    current_a: float = 450.0
    resistance_ohm: float = 0.035
    temperature_c: float = 35.0
    reversible_coeff_v_per_k: float = 0.0


def cabin_cooling_load_kw(inp: CabinInputs) -> Dict[str, float]:
    envelope = max(inp.ambient_c - inp.cabin_c, 0.0) * inp.ua_kw_per_k
    occupants = inp.occupants * inp.occupant_sensible_kw_each
    sensible = envelope + inp.solar_kw + occupants + inp.ventilation_kw
    total = sensible + max(inp.latent_kw, 0.0)
    return {
        "envelope_kw": envelope,
        "solar_kw": inp.solar_kw,
        "occupants_kw": occupants,
        "ventilation_kw": inp.ventilation_kw,
        "latent_kw": inp.latent_kw,
        "sensible_kw": sensible,
        "total_kw": total,
    }


def battery_heat_kw(inp: BatteryInputs) -> Dict[str, float]:
    ohmic_w = inp.current_a**2 * inp.resistance_ohm
    reversible_w = (
        inp.current_a
        * (inp.temperature_c + 273.15)
        * inp.reversible_coeff_v_per_k
    )
    total_w = ohmic_w + reversible_w
    return {
        "ohmic_kw": ohmic_w / 1000.0,
        "reversible_kw": reversible_w / 1000.0,
        "total_kw": total_w / 1000.0,
    }


if __name__ == "__main__":
    print(cabin_cooling_load_kw(CabinInputs()))
    print(battery_heat_kw(BatteryInputs()))
