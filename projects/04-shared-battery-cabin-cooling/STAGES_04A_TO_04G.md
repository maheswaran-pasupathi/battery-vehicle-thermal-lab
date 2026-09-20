# Project 04 — Fidelity roadmap implemented through 04G

The project is deliberately structured as one reusable model rather than seven disconnected demos.

## 04A — Shared load + refrigeration integration

**File:** `shared_cycle.py`

Connects:

```text
Cabin load + battery load
        ↓
finite shared capacity
        ↓
allocation strategy
        ↓
property-based vapor-compression cycle
        ↓
compressor power + condenser rejection + refrigerant state
```

The fixed-COP load calculation and the CoolProp refrigeration cycle are now one calculation chain.

---

## 04B — Compressor map and operating envelope

**File:** `compressor_map.py`

Adds a generic synthetic map with:

- speed ratio,
- pressure ratio,
- isentropic efficiency,
- available capacity,
- shaft-power proxy,
- operating-envelope flag.

The numbers are intentionally illustrative. The purpose is to teach why **95% compressor speed is not the same as 95% useful cooling capacity**.

Next replacement path: published or manufacturer compressor-map data.

---

## 04C — Condenser, cabin evaporator and battery chiller

**File:** `heat_exchangers.py`

Reduced-order UA/approach models are included for:

- condenser,
- cabin evaporator,
- battery chiller.

This introduces an explicit ambient heat-rejection limitation.

A condenser-airflow reduction now raises the condensing temperature required to reject the same heat.

---

## 04D — Physical cabin and battery heat loads

**File:** `loads.py`

### Cabin load
Includes:

- ambient/envelope sensible load,
- solar load,
- occupants,
- ventilation,
- latent-load term.

### Battery load
Starts with:

```text
Q_ohmic = I²R
Q_rev = I T dOCV/dT
```

The reversible term defaults to zero unless a justified coefficient is supplied.

The important change is that battery cooling demand can now originate from electrical loading rather than being an arbitrary fixed 8 kW.

---

## 04E — Transient plant + controls

**Files:** `controls.py`, `plant.py`

The model now integrates:

- cabin thermal state,
- battery thermal state,
- battery current/heat,
- shared refrigeration,
- compressor speed command,
- fan command,
- capacity allocation,
- condenser heat rejection,
- cycle pressure/COP,
- battery-priority switching.

This is still a reduced-order plant, not a GT-SUITE replacement.

Its purpose is to expose the same causal logic used in a 1D vehicle thermal model.

---

## 04F — Fault diagnosis

**File:** `fault_cases.py`

Implemented generic fault proxies:

1. baseline,
2. condenser airflow restriction,
3. compressor speed limitation,
4. low-refrigerant proxy,
5. battery-flow maldistribution,
6. battery-valve restriction.

Each case can be compared using:

- battery temperature,
- cabin temperature,
- high-side pressure,
- superheat,
- subcooling,
- compressor power,
- available/delivered cooling.

### Diagnostic intent

The model is designed around:

```text
Load
 -> Sink
 -> Flow
 -> Capacity
 -> Distribution
 -> Control
 -> Fault/degradation
```

It intentionally prevents the conclusion "compressor at maximum = HVAC healthy."

---

## 04G — Verification, calibration and validation framework

**File:** `validation.py`

Three layers are explicitly separated.

### Verification

Checks:

- refrigeration energy balance,
- positive COP,
- high-side pressure > low-side pressure,
- trend tests.

### Published benchmark comparison

One open experimental benchmark is included:

**Periyasamy et al. (2026), Asia-Pacific Journal of Chemical Engineering**  
DOI: https://doi.org/10.1002/apj.70202

The publication reports for R134a at an evaporating temperature of **−15 °C** and condensing temperature of **40 °C**:

- experimental COP = **3.12**
- reported COP uncertainty = **±0.08**

Project 04 compares its simple cycle model against that point.

### Calibration

The script can fit compressor isentropic efficiency to the benchmark.

This is explicitly labelled **calibration**.

The same fitted point is **not** then counted as validation.

### Current validation status

Project 04 is **not claimed to be fully experimentally validated**.

A defensible statement is:

> The cycle implementation is verified by conservation and trend checks, and one literature point is used as a transparent benchmark/calibration exercise. Full validation requires multiple independent operating points with the relevant boundary conditions and measured quantities.

That distinction is intentional and should also be used in interviews.

---

# Running the complete sequence

From the project folder:

```bash
python shared_cycle.py
python compressor_map.py
python refrigeration.py
python plant.py
python fault_cases.py
python validation.py

python -m unittest test_model.py
python -m unittest test_refrigeration.py
python -m unittest test_stages.py
```

# Remaining step after 04G

The next major fidelity level is **04H — 1D ↔ 3D coupling**:

- 1D → 3D: coolant inlet temperature, flow/pressure BC, heat load, fluid properties;
- 3D → 1D: Δp map, UA/Rth/HTC map, maldistribution penalty and validity range.

That should connect Project 04 with the cooling-plate/CHT projects rather than creating another isolated model.
