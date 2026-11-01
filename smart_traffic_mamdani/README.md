# 🚦 Smart Traffic Light Control System Using Mamdani Fuzzy Logic

A Python-based traffic-light simulation that recommends a green-light duration from traffic density and waiting time using a **Mamdani Fuzzy Inference System (FIS)**.

## Project specifications

- **Inputs:** Vehicles waiting (0–30), waiting time (0–120 seconds)
- **Output:** Green-light duration (5–60 seconds)
- **Inference:** Mamdani
- **Membership functions:** Triangular and shoulder functions
- **AND operator:** Minimum
- **Implication:** Minimum (clipping)
- **Aggregation:** Maximum
- **Defuzzification:** Centroid / center of gravity
- **Interface:** Streamlit | **Language:** Python
- **Hardware:** Not required

## Project overview

Fixed-time traffic signals do not adapt green duration to changing traffic conditions. This project demonstrates a fuzzy-logic controller for one simulated traffic approach. It uses the number of vehicles waiting and their waiting time to estimate a green-light duration.

> This is an educational simulation, not a certified road-traffic controller.

## Fuzzy logic concepts used

1. **Fuzzy sets:** represent categories such as Low, Medium and High.
2. **Linguistic variables:** describe traffic density and waiting time with human-readable labels.
3. **Membership functions:** map crisp inputs to degrees between 0 and 1.
4. **Fuzzification:** calculate each input's membership degrees.
5. **IF–THEN rules:** encode the traffic-control logic.
6. **Fuzzy AND:** combine antecedents using the minimum operator.
7. **Mamdani implication:** clip each output set at its rule firing strength using minimum.
8. **Aggregation:** combine all rule outputs using maximum.
9. **Defuzzification:** convert the aggregated fuzzy output to a crisp duration using the centroid method.

## Input and output membership functions

### Traffic density (0–30 vehicles)

| Fuzzy set | Triangle parameters (a,b,c) |
|---|---|
| Low | (0, 0, 12) |
| Medium | (6, 15, 24) |
| High | (18, 30, 30) |

### Waiting time (0–120 seconds)

| Fuzzy set | Triangle parameters (a,b,c) |
|---|---|
| Short | (0, 0, 40) |
| Medium | (20, 60, 100) |
| Long | (80, 120, 120) |

### Output: green-light duration (5–60 seconds)

| Fuzzy set | Triangle parameters (a,b,c) |
|---|---|
| Short | (5, 5, 25) |
| Medium | (15, 32.5, 50) |
| Long | (40, 60, 60) |

Repeated endpoints create left/right shoulder membership functions. These are illustrative project parameters, not traffic-engineering standards.

## Mamdani rule base

The nine rules are the 3 × 3 combinations of input categories.

| Traffic density | Waiting time | Green duration |
|---|---|---|
| Low | Short | Short |
| Low | Medium | Short |
| Low | Long | Medium |
| Medium | Short | Short |
| Medium | Medium | Medium |
| Medium | Long | Long |
| High | Short | Medium |
| High | Medium | Long |
| High | Long | Long |

Example: **IF** traffic is High **AND** waiting time is Long **THEN** green duration is Long.

## Mamdani inference calculations

### 1. Rule firing strength

For an AND rule:

\[
\alpha_i = \min(\mu_{\text{traffic}}, \mu_{\text{waiting}})
\]

### 2. Implication

Clip the consequent membership function by its firing strength:

\[
\mu_i'(z) = \min(\alpha_i,\mu_{B_i}(z))
\]

### 3. Aggregation

Combine all rule outputs using maximum:

\[
\mu_{\mathrm{agg}}(z)=\max_i \mu_i'(z)
\]

### 4. Centroid defuzzification

Calculate the crisp green duration:

\[
z^*=\frac{\int z\,\mu_{\mathrm{agg}}(z)\,dz}
{\int \mu_{\mathrm{agg}}(z)\,dz}
\]

The implementation approximates the integrals numerically over a fine output range.

## Workflow

1. User enters vehicles waiting and waiting time.
2. The app validates the inputs.
3. Fuzzification calculates membership degrees.
4. The nine rules are evaluated using the minimum AND operator.
5. Mamdani implication clips the output sets.
6. Maximum aggregation combines the rule outputs.
7. Centroid defuzzification calculates the green duration.
8. Streamlit displays the result, fired rules and graphs.

## Project structure

```text
smart_traffic_mamdani/
├── app.py
├── membership.py
├── mamdani.py
├── visualizations.py
├── test_cases.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and execution (Windows PowerShell)

Open the terminal in the folder containing `app.py`.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL displayed by Streamlit, usually `http://localhost:8501`.

Run basic checks:

```powershell
.\.venv\Scripts\python.exe test_cases.py
```

## Understanding the output

The dashboard displays:
- Green-light duration in seconds.
- Short, Medium or Long output category.
- Membership degrees for traffic density and waiting time.
- Rules that fired and their strengths.
- Membership-function plots.
- Aggregated output membership function and centroid marker.
- Response surface showing output behavior across input ranges.

The output is deterministic for fixed inputs and model parameters. It is a simulated recommendation, not a validated signal timing plan.

## Technologies

Python, Streamlit, NumPy, Matplotlib and Pandas. The Mamdani inference process is implemented directly in Python for transparency and learning.

## Limitations and safety

- No live camera, loop detector or traffic sensor data.
- One simulated traffic approach only; no multi-road coordination.
- Pedestrian phases, emergency priority, yellow/all-red intervals and fail-safe controls are not implemented.
- Rules and membership functions are illustrative, not validated traffic-engineering standards.
- Real-world use requires qualified traffic-engineering design, safety validation and regulatory approval.

## Future enhancements

- Add separate inputs for multiple approaches.
- Model pedestrian demand and emergency-vehicle priority.
- Tune rules using simulated or recorded traffic data.
- Add a visual intersection simulation.
- Compare fuzzy timing against fixed-time signals.

## Academic summary

This mini-project demonstrates fuzzy sets, membership functions, fuzzification, linguistic variables, IF–THEN rules, minimum AND, Mamdani implication, maximum aggregation and centroid defuzzification in an adaptive traffic-light timing simulation.
