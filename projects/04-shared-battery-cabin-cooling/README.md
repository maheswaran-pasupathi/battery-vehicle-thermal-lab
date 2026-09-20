# 04 Shared battery + cabin cooling capacity

A compact reduced-order study of an EV thermal-management problem: the **cabin evaporator** and **battery chiller** share finite refrigeration capacity, especially during hot-ambient stationary fast charging.

This is deliberately a small public engineering model. It starts from conservation of energy before adding compressor maps, refrigerant properties or a full 1D plant.

All numbers are illustrative and generic. No employer or product data is used.

## Engineering questions

1. How much combined cooling is requested by cabin and battery?
2. How much compressor electrical power does that imply?
3. How much heat must the condenser reject?
4. What changes as ambient temperature rises?
5. What happens when demand exceeds available refrigeration capacity?
6. How does battery-priority allocation affect cabin comfort?
7. Which missing physics should be added at the next fidelity level?

## Level 0 — base energy balance

Illustrative base case:

- ambient = 45 °C
- cabin demand = 20 kW
- battery chiller demand = 8 kW
- COP = 2.5
- available refrigeration capacity = 25 kW

Demand:

```text
Q_total = Q_cabin + Q_battery
        = 20 + 8
        = 28 kW
```

Compressor power:

```text
COP = Q_cooling / W_compressor

W_compressor = 28 / 2.5
             = 11.2 kW
```

Condenser rejection:

```text
Q_condenser = Q_cooling + W_compressor
            = 28 + 11.2
            = 39.2 kW
```

So **compressor electrical power is not the cooling load**, and condenser rejection is larger than the useful cooling load.

## Level 1 — finite capacity and load allocation

The base case requests 28 kW while only 25 kW is available.

With a simple battery-priority strategy:

- battery receives its requested 8 kW,
- cabin receives 17 kW,
- cabin has 3 kW unmet demand.

Three simple strategies are implemented:

- `battery_priority`
- `cabin_priority`
- `proportional`

These are control-policy examples, not a production controller.

## Level 1 — ambient sensitivity

The model includes **illustrative**, deliberately simple ambient-dependent COP and available-capacity functions.

They are not refrigerant-property calculations or compressor maps.

The purpose is to reproduce the correct engineering tendency:

```text
ambient temperature rises
        ↓
condenser heat rejection becomes harder
        ↓
COP and/or available cooling capacity can fall
        ↓
shared cabin + battery margin shrinks
```

The notebook sweeps ambient temperature and shows when the combined demand crosses the available-capacity envelope.

## Level 2 preview — transient stationary fast charge

A synthetic 60-minute scenario is included:

- stationary vehicle,
- hot ambient,
- initially high cabin pull-down load,
- high battery thermal demand during fast charge,
- finite shared cooling capacity.

This makes the allocation problem visible over time rather than at one operating point.

## Files

- [notebook.ipynb](notebook.ipynb) — worked study with plots and engineering interpretation
- [model.py](model.py) — reusable model functions
- [test_model.py](test_model.py) — basic physics/logic checks

## Run

From the repository root:

```bash
pip install -r requirements.txt
python projects/04-shared-battery-cabin-cooling/model.py
jupyter notebook
```

## What this model can diagnose

At this fidelity it can distinguish:

- requested cooling load,
- available refrigeration capacity,
- compressor electrical power,
- condenser heat rejection,
- cabin/battery allocation,
- unmet load,
- sensitivity to hot ambient.

It **cannot** yet diagnose whether a real vehicle problem is caused by:

- refrigerant charge,
- compressor-map limitation,
- high-side pressure,
- low-side pressure,
- superheat,
- subcooling,
- condenser air-side degradation,
- expansion-device behavior,
- local battery coolant maldistribution,
- local TIM/contact resistance.

Those require the next model layer or measurements.

## Next fidelity layer

Project 04 should grow in this order:

1. replace illustrative COP/capacity trends with compressor-map data;
2. add condensing and evaporating temperatures;
3. add high-/low-side saturation state reasoning;
4. add superheat and subcooling;
5. add condenser approach temperature;
6. calculate cabin sensible + latent load;
7. calculate battery heat from current, resistance and temperature;
8. add transient coolant/battery thermal mass;
9. add battery/cabin control allocation;
10. correlate against a published refrigeration/HVAC dataset.

## Interview connection

This project supports one important diagnostic rule:

> **High compressor speed or high compressor power does not prove the refrigeration system is performing correctly.**

The engineering check is:

```text
Load -> Sink -> Flow -> Capacity -> Distribution -> Control -> Fault/degradation
```

For the refrigeration side, delivered cooling and operating state must eventually be checked using pressure, temperature, compressor-envelope and heat-exchanger evidence.

## Limitations

- educational reduced-order model;
- illustrative data;
- simple ambient trends, not compressor maps;
- no refrigerant-property package;
- no humidity/latent cabin model yet;
- no battery thermal capacitance in the current control calculation;
- no product-specific validation.

The purpose is to build the system reasoning cleanly before increasing fidelity.
