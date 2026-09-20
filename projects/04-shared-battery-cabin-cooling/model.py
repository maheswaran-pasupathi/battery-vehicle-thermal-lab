from dataclasses import dataclass


@dataclass
class CoolingCase:
    ambient_c: float
    cabin_kw: float
    battery_kw: float
    cop: float
    available_cooling_kw: float


def energy_balance(case: CoolingCase):
    total_kw = case.cabin_kw + case.battery_kw
    compressor_kw = total_kw / case.cop
    condenser_kw = total_kw + compressor_kw
    return total_kw, compressor_kw, condenser_kw


def allocate_capacity(case: CoolingCase, battery_priority=True):
    available = max(case.available_cooling_kw, 0.0)

    if battery_priority:
        battery_delivered = min(case.battery_kw, available)
        remaining = available - battery_delivered
        cabin_delivered = min(case.cabin_kw, remaining)
    else:
        total = case.cabin_kw + case.battery_kw
        if total <= 0:
            return 0.0, 0.0
        fraction = min(available / total, 1.0)
        battery_delivered = case.battery_kw * fraction
        cabin_delivered = case.cabin_kw * fraction

    return battery_delivered, cabin_delivered


if __name__ == "__main__":
    case = CoolingCase(
        ambient_c=45.0,
        cabin_kw=20.0,
        battery_kw=8.0,
        cop=2.5,
        available_cooling_kw=25.0,
    )

    total, compressor, condenser = energy_balance(case)
    batt_delivered, cabin_delivered = allocate_capacity(case, battery_priority=True)

    print("Shared battery + cabin cooling — illustrative case")
    print(f"Ambient: {case.ambient_c:.1f} °C")
    print(f"Cabin demand: {case.cabin_kw:.1f} kW")
    print(f"Battery demand: {case.battery_kw:.1f} kW")
    print(f"Total cooling demand: {total:.1f} kW")
    print(f"Compressor power at COP={case.cop:.2f}: {compressor:.1f} kW")
    print(f"Condenser heat rejection: {condenser:.1f} kW")
    print()
    print(f"Available cooling capacity: {case.available_cooling_kw:.1f} kW")
    print("Battery-priority allocation:")
    print(f"  Battery delivered: {batt_delivered:.1f} kW")
    print(f"  Cabin delivered:   {cabin_delivered:.1f} kW")
    print(f"  Unmet battery load: {max(case.battery_kw-batt_delivered,0):.1f} kW")
    print(f"  Unmet cabin load:   {max(case.cabin_kw-cabin_delivered,0):.1f} kW")
