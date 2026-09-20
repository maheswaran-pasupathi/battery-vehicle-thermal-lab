# 01 Battery heat and coolant sizing

How much heat a battery pack makes and how much coolant flow is needed to carry it away.

[Open the notebook](notebook.ipynb)

Steps: heat per cell (ohmic plus reversible), heat per pack, coolant flow from an energy balance, and the temperature rise with no cooling.

Main results for a 96s3p pack of 50 Ah cells (about 53 kWh) at 25 °C:

- Heat at 1C, 2C and 3C is about 1.15, 3.74 and 7.77 kW.
- A cold cell makes more heat for the same current: at 2C a cell at 0 °C makes 21 W against 13 W at 25 °C.
- At 2C and a 3 K coolant rise the flow needed is about 21 L/min. Halving the allowed rise doubles it.
- With no cooling, 30 minutes at 2C takes the pack to about 47 °C and 3C to about 64 °C.

Limits: lumped pack, constant coolant properties, illustrative cell values.
