TRAFFIC_SETS = {"Low": (0, 0, 12), "Medium": (6, 15, 24), "High": (18, 30, 30)}
WAITING_SETS = {"Short": (0, 0, 40), "Medium": (20, 60, 100), "Long": (80, 120, 120)}
GREEN_SETS = {"Short": (5, 5, 25), "Medium": (15, 32.5, 50), "Long": (40, 60, 60)}

def triangular_membership(x, a, b, c):
    if x < a or x > c: return 0.0
    if a == b and x <= b: return 1.0
    if b == c and x >= b: return 1.0
    if x == b: return 1.0
    if x < b: return max(0.0, min(1.0, (x-a)/(b-a)))
    return max(0.0, min(1.0, (c-x)/(c-b)))

def fuzzify(value, sets):
    return {name: triangular_membership(value, *params) for name, params in sets.items()}
