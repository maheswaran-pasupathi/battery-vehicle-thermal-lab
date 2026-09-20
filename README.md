# Battery and vehicle thermal lab

Small, reproducible studies on battery cooling and vehicle thermal management. Each one is a short notebook that goes from the physics to a plot to what it means for a design, with the assumptions and limits written down.

I work on battery cooling and vehicle thermal simulation (GT-SUITE 1D models coupled with 3D conjugate heat transfer). These notebooks are the simple versions of questions I meet in that work: how much heat, how much coolant, how the flow splits, and what a cooling strategy costs in energy.

All numbers are illustrative and generic. No employer data is used anywhere.

## Projects

| # | Project | What it answers | Result in one line |
|---|---|---|---|
| 01 | [Battery heat and coolant sizing](projects/01-battery-heat-and-coolant-sizing) | How much heat does a pack make and how much coolant flow does it need? | A 53 kWh pack makes about 3.7 kW at 2C and needs roughly 21 L/min for a 3 K rise; with no cooling it reaches 47 °C in 30 minutes |
| 02 | [Coolant flow distribution](projects/02-cooling-plate-flow-distribution) | How does flow split across parallel cooling plates and what does the header layout do? | A U-type header gives a 5.3% flow spread, a Z-type 1.5%; orifices remove the spread at a small cost in total flow |
| 03 | [Pack temperature and cooling strategy](projects/03-pack-temperature-cooling-strategy) | Radiator or chiller over a hot-day route, and what does it cost? | At 38 °C ambient the radiator peaks at 45.7 °C; a chiller held 40 °C for 0.61 kWh (1.1% of the pack) |\n| 04 | [Shared battery + cabin cooling](projects/04-shared-battery-cabin-cooling) | How do cabin and battery loads share finite refrigeration capacity? | A 20 kW cabin + 8 kW battery load needs 28 kW cooling; at COP 2.5 that is 11.2 kW compressor power and 39.2 kW condenser rejection |

## Running them

```
pip install -r requirements.txt
jupyter notebook
```

The notebooks are saved with their outputs, so they can be read on GitHub without running anything.

## What is next

- Cabin pull-down and HVAC energy\n- Add compressor/COP maps and refrigerant-state diagnostics to Project 04
- Heat pump against resistive heating in cold weather, and the effect on range
- Auxiliary energy and its share of vehicle range
- Passing values from a 3D result to a 1D model, with an energy check
- Fast-charge thermal limits and pre-conditioning

## Notes on the numbers

Cell resistance, entropic coefficient, pump curve, header losses, heat exchanger values and the route are chosen to look reasonable, not taken from a product. The notebooks show how the quantities relate. They are not design data.
