# 04 Shared battery + cabin cooling capacity

A small first-principles model for a hot-ambient EV case where the **cabin evaporator** and **battery chiller** share the same refrigeration system.

The objective is not to reproduce a specific vehicle. It is to answer four practical questions:

1. What is the combined cooling load?
2. What compressor electrical power is required for a given COP?
3. How much heat must the condenser reject?
4. If refrigeration capacity is limited, how much cooling can be allocated to the battery and cabin?

All inputs are illustrative and generic.

## Base case

- Ambient: 45 °C
- Cabin cooling demand: 20 kW
- Battery chiller demand: 8 kW
- Cooling COP: 2.5
- Available refrigeration capacity: 25 kW

For the unconstrained demand:

- Total cooling demand = 28 kW
- Compressor electrical power = 11.2 kW
- Condenser heat rejection = 39.2 kW

Because only 25 kW of cooling capacity is available in this illustrative case, the model demonstrates a simple battery-priority allocation strategy.

## Engineering logic

```text
Cabin load ----                > shared refrigeration system -> compressor -> condenser -> ambient
Battery chiller/
```

Core equations:

```text
Q_total = Q_cabin + Q_battery
COP = Q_total / W_compressor
Q_condenser = Q_total + W_compressor
```

This project deliberately separates:

- **cooling load** from **compressor electrical power**,
- **total capacity** from **load allocation**,
- **refrigeration limitation** from **local battery flow/distribution problems**.

## Run

```bash
python model.py
```

The script prints the base-case energy balance and a battery-priority capacity allocation.

## Next fidelity steps

Later versions can add:

- COP as a function of ambient and evaporating temperature,
- compressor map / operating envelope,
- condenser approach temperature,
- refrigerant high- and low-side states,
- cabin sensible + latent load,
- battery heat generation from current and resistance,
- transient fast-charge thermal load,
- control logic for battery/cabin priority,
- coupling to the existing pack-temperature project.

## Limits

This is a Level-0/Level-1 educational model:
- fixed COP,
- no refrigerant property model,
- no compressor map,
- no transient thermal capacitance,
- no product-specific data.

Its purpose is to establish the energy balance and system-level reasoning before adding refrigerant-cycle fidelity.
