# 05 Cold-weather range: resistive heater or heat pump?

A steady-speed range model of an electric vehicle in winter. It compares a resistive heater, a heat pump, and a heat pump that also reuses powertrain waste heat, across ambient temperature and speed.

[Open the notebook](notebook.ipynb)

Steps: traction power, cabin heat demand, heat pump COP, range, gain over the resistive heater, and a sensitivity check on the two values I trust least.

Main results (60 kWh usable, 2.2 t vehicle, cabin held at 22 °C):

| Speed | Ambient | Resistive (km) | Heat pump (km) | Heat pump + waste heat (km) |
|---|---|---|---|---|
| 50 km/h | 0 °C | 353 | 451 | 457 |
| 80 km/h | 0 °C | 309 | 351 | 356 |
| 110 km/h | 0 °C | 236 | 253 | 256 |
| 50 km/h | -20 °C | 244 | 244 | 249 |

At city speed the heat pump gives back about 100 km at 0 °C; at highway speed only about 17 km, because the road load dominates. Below the -15 °C cut-out the gain is gone and only the waste-heat share is left. Varying the heat pump quality and the cabin conductance by 25% moves the gain at 0 °C and 60 km/h between about 60 and 86 km, so those two values need test data.

Limits: steady speed with no stops (so absolute ranges are long, read the differences), no cabin warm-up transient, no battery heating, no defrost, fixed capacity loss in the cold.
