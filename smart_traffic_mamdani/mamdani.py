import numpy as np
from membership import TRAFFIC_SETS, WAITING_SETS, GREEN_SETS, fuzzify, triangular_membership

RULES = [
    ("Low", "Short", "Short"), ("Low", "Medium", "Short"), ("Low", "Long", "Medium"),
    ("Medium", "Short", "Short"), ("Medium", "Medium", "Medium"), ("Medium", "Long", "Long"),
    ("High", "Short", "Medium"), ("High", "Medium", "Long"), ("High", "Long", "Long"),
]
OUTPUT_UNIVERSE = np.linspace(5, 60, 551)

def calculate_green_duration(traffic_count, waiting_time):
    if not 0 <= traffic_count <= 30:
        raise ValueError("Traffic count must be between 0 and 30 vehicles.")
    if not 0 <= waiting_time <= 120:
        raise ValueError("Waiting time must be between 0 and 120 seconds.")

    traffic = fuzzify(traffic_count, TRAFFIC_SETS)
    waiting = fuzzify(waiting_time, WAITING_SETS)
    aggregate = np.zeros_like(OUTPUT_UNIVERSE)
    fired = []

    for t_label, w_label, out_label in RULES:
        strength = min(traffic[t_label], waiting[w_label])
        if strength <= 0:
            continue
        a, b, c = GREEN_SETS[out_label]
        output_mf = np.array([triangular_membership(x, a, b, c) for x in OUTPUT_UNIVERSE])
        aggregate = np.maximum(aggregate, np.minimum(strength, output_mf))
        fired.append({
            "Rule": f"IF traffic is {t_label} AND waiting is {w_label} THEN green is {out_label}",
            "Traffic membership": round(traffic[t_label], 3),
            "Waiting membership": round(waiting[w_label], 3),
            "Firing strength": round(strength, 3),
            "Output set": out_label
        })

    area = aggregate.sum()
    if area <= 0:
        raise ValueError("No fuzzy rule fired; check membership functions.")
    duration = float((OUTPUT_UNIVERSE * aggregate).sum() / area)
    category = "Short" if duration < 25 else ("Medium" if duration < 42 else "Long")
    fired.sort(key=lambda row: row["Firing strength"], reverse=True)
    return {
        "green_duration": duration, "category": category,
        "traffic_memberships": traffic, "waiting_memberships": waiting,
        "fired_rules": fired, "output_universe": OUTPUT_UNIVERSE,
        "aggregated_output": aggregate
    }
