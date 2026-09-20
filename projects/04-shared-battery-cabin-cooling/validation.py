"""04G — Validation and evidence framework.

This module intentionally separates:
1. verification / conservation checks,
2. comparison with published experimental values,
3. calibration,
4. independent validation.

Published reference used for one transparent benchmark:
Periyasamy et al. (2026), Asia-Pacific Journal of Chemical Engineering,
DOI: 10.1002/apj.70202.

The paper reports an R134a experimental COP of 3.12 at evaporating temperature
-15 °C and condensing temperature 40 °C, with experimental COP uncertainty
±0.08. This single point is a benchmark only; it is not sufficient to claim
full validation of this project model.
"""

from dataclasses import dataclass
from typing import Dict

from refrigeration import RefrigerationCase, solve_cycle


@dataclass(frozen=True)
class LiteraturePoint:
    name: str
    evaporating_c: float
    condensing_c: float
    experimental_cop: float
    uncertainty_cop: float
    source: str


R134A_2026_POINT = LiteraturePoint(
    name="R134a experimental standard-rating point",
    evaporating_c=-15.0,
    condensing_c=40.0,
    experimental_cop=3.12,
    uncertainty_cop=0.08,
    source="Periyasamy et al. 2026, DOI 10.1002/apj.70202",
)


def compare_to_literature(
    point: LiteraturePoint = R134A_2026_POINT,
    isentropic_efficiency: float = 0.70,
    superheat_k: float = 7.0,
    subcooling_k: float = 5.0,
) -> Dict[str, float]:
    result = solve_cycle(
        RefrigerationCase(
            refrigerant="R134a",
            evaporating_c=point.evaporating_c,
            condensing_c=point.condensing_c,
            superheat_k=superheat_k,
            subcooling_k=subcooling_k,
            isentropic_efficiency=isentropic_efficiency,
            cooling_load_kw=1.0,
            ambient_c=25.0,
        )
    )

    error = result["cop"] - point.experimental_cop
    error_pct = 100.0 * error / point.experimental_cop

    return {
        "predicted_cop": result["cop"],
        "experimental_cop": point.experimental_cop,
        "uncertainty_cop": point.uncertainty_cop,
        "error_cop": error,
        "error_percent": error_pct,
        "within_reported_uncertainty": float(
            abs(error) <= point.uncertainty_cop
        ),
    }


def calibrate_efficiency_to_point(
    point: LiteraturePoint = R134A_2026_POINT,
    lower: float = 0.40,
    upper: float = 0.90,
    iterations: int = 50,
) -> float:
    """Fit compressor isentropic efficiency to one point.

    This is CALIBRATION, not validation. The fitted point must not then be used
    as independent validation evidence.
    """
    for _ in range(iterations):
        eta = 0.5 * (lower + upper)
        comparison = compare_to_literature(
            point=point,
            isentropic_efficiency=eta,
        )
        if comparison["predicted_cop"] < point.experimental_cop:
            lower = eta
        else:
            upper = eta
    return 0.5 * (lower + upper)


def verification_checks() -> Dict[str, float]:
    result = solve_cycle(
        RefrigerationCase(
            evaporating_c=5.0,
            condensing_c=55.0,
            cooling_load_kw=25.0,
        )
    )
    energy_error_kw = result["condenser_kw"] - (
        25.0 + result["compressor_kw"]
    )
    return {
        "energy_balance_error_kw": energy_error_kw,
        "positive_cop": float(result["cop"] > 0.0),
        "high_pressure_above_low": float(
            result["p_high_bar"] > result["p_low_bar"]
        ),
    }


if __name__ == "__main__":
    print("Verification:", verification_checks())
    print("Benchmark before calibration:", compare_to_literature())
    fitted = calibrate_efficiency_to_point()
    print("Calibrated compressor efficiency:", fitted)
    print(
        "Calibrated-point comparison (not independent validation):",
        compare_to_literature(isentropic_efficiency=fitted),
    )
