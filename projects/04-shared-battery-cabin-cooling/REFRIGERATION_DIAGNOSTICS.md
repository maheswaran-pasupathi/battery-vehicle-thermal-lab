# Refrigeration diagnostics — Level 2

This extension replaces the fixed-COP assumption with a simple vapor-compression cycle solved from refrigerant properties using **CoolProp**.

## State definition

Default educational case:

- refrigerant: R134a
- evaporating saturation temperature: 5 °C
- condensing saturation temperature: 55 °C
- superheat: 8 K
- subcooling: 5 K
- compressor isentropic efficiency: 0.70
- delivered cooling: 25 kW
- ambient: 45 °C

The cycle calculates:

- low-side pressure,
- high-side pressure,
- pressure ratio,
- suction temperature,
- discharge temperature,
- liquid-line temperature,
- specific evaporator cooling,
- specific compressor work,
- COP,
- refrigerant mass flow,
- compressor power,
- condenser heat rejection,
- condenser approach.

## Why this matters for diagnosis

A compressor running near maximum speed does **not** prove that the thermal system is healthy.

A stronger diagnosis checks:

- suction and discharge pressure,
- evaporating and condensing saturation temperature,
- superheat,
- subcooling,
- condenser approach,
- compressor pressure ratio,
- delivered evaporator/chiller load,
- compressor electrical/mechanical work.

## Interview logic

### High superheat
Can indicate evaporator starvation, low refrigerant flow, excessive load or expansion-device limitation.

### Low subcooling
Can indicate insufficient liquid inventory at the condenser outlet or refrigerant-inventory issues.

### High condensing temperature / high pressure ratio
Raises compressor work and discharge temperature, reducing COP and available thermal margin.

### Small condenser approach margin
At very hot ambient, the condenser has little temperature headroom for rejection.

These are **learning heuristics**, not OEM diagnostic thresholds.

## Files

- `refrigeration.py` — property-based cycle solver
- `diagnostics.py` — simple educational fault-logic helper
- `test_refrigeration.py` — conservation and trend tests

## Run

```bash
pip install -r requirements.txt
cd projects/04-shared-battery-cabin-cooling
python refrigeration.py
python -m unittest test_refrigeration.py
```

## Next step

The next useful fidelity increase is to replace the fixed compressor efficiency with a **synthetic or published compressor map** and then connect the refrigeration solver back to the shared battery/cabin load-allocation model.
