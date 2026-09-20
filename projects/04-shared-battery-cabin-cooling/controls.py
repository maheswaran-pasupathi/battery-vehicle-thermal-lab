"""04E — Simple supervisory controls for the shared thermal plant."""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ControlTargets:
    battery_target_c: float = 35.0
    cabin_target_c: float = 24.0


def controller(
    battery_c: float,
    cabin_c: float,
    total_demand_kw: float,
    targets: ControlTargets = ControlTargets(),
) -> Dict[str, float]:
    batt_error = max(battery_c - targets.battery_target_c, 0.0)
    cabin_error = max(cabin_c - targets.cabin_target_c, 0.0)

    compressor_speed = min(
        1.0,
        max(0.35, 0.45 + 0.03 * batt_error + 0.015 * cabin_error + 0.01 * total_demand_kw),
    )
    fan_ratio = min(1.0, max(0.35, 0.45 + 0.04 * batt_error + 0.02 * total_demand_kw))

    strategy = "battery_priority" if battery_c >= 40.0 else "proportional"

    return {
        "compressor_speed_ratio": compressor_speed,
        "fan_ratio": fan_ratio,
        "strategy": strategy,
    }
