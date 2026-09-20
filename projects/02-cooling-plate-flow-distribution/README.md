# 02 Coolant flow distribution across parallel cooling plates

A pump gives a total flow, but parallel branches do not share it equally. This builds a small hydraulic network and looks at the header layout.

[Open the notebook](notebook.ipynb)

Steps: pump curve against system curve, branch flows for U-type and Z-type headers, the temperature effect of the flow spread, and balancing with orifices.

Main results for four identical branches:

- The pump operates at about 22 L/min, roughly 5.6 L/min per branch, with no header loss.
- With header losses the flow spread is 5.3% for a U-type layout and 1.5% for a Z-type layout.
- The flow spread gives a small wall temperature spread here (0.33 K against 0.10 K) because the plate is well cooled. It matters more when the margin is smaller.
- Orifices remove the spread completely and cost little total flow in this circuit.

Limits: four-branch toy network, quadratic losses, illustrative pump and header values.
