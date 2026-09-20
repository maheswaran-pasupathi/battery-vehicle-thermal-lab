# 03 Pack temperature over a route: radiator or chiller

A lumped pack temperature model over a two-hour hot-day route, comparing no cooling, a radiator, and a chiller that switches on late or early.

[Open the notebook](notebook.ipynb)

Steps: model, route load, four strategies, temperature history, and the trade between temperature and cooling energy.

Main results at 38 °C ambient with a 40 °C example limit:

| Strategy | Peak (°C) | Cooling energy (kWh) |
|---|---|---|
| none | 52.7 | 0.00 |
| radiator | 45.7 | 0.21 |
| chiller, late | 40.0 | 0.61 |
| chiller, early | 38.0 | 0.79 |

The radiator cannot hold the limit because its coolant is never colder than 43 °C. The chiller can, and the energy it uses (about 1 to 1.5% of the pack) comes out of the range.

Limits: one lumped temperature, fixed COP, synthetic route, no cabin load on the chiller.
