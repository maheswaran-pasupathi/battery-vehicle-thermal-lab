"""Simple rule-based learning diagnostics for Project 04.

These are educational heuristics, not service procedures or OEM thresholds.
"""


def diagnose_state(
    superheat_k: float,
    subcooling_k: float,
    condenser_approach_k: float,
    pressure_ratio: float,
):
    notes = []

    if superheat_k > 15:
        notes.append(
            "High superheat: check evaporator starvation, low refrigerant flow, or excessive load."
        )
    elif superheat_k < 2:
        notes.append(
            "Very low superheat: check overfeeding / liquid-return risk and expansion control."
        )
    else:
        notes.append("Superheat is in the educational nominal band.")

    if subcooling_k < 2:
        notes.append(
            "Low subcooling: check refrigerant inventory, condenser completion, or flash gas risk."
        )
    elif subcooling_k > 12:
        notes.append(
            "High subcooling: check excess liquid inventory or restricted downstream flow."
        )
    else:
        notes.append("Subcooling is in the educational nominal band.")

    if condenser_approach_k < 5:
        notes.append(
            "Small condenser approach margin: heat rejection is likely difficult at this ambient."
        )
    else:
        notes.append("Condenser approach has some thermal margin.")

    if pressure_ratio > 5:
        notes.append(
            "High pressure ratio: compressor work and discharge temperature can become limiting."
        )

    return notes
