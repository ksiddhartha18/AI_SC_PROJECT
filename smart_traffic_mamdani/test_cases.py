from mamdani import calculate_green_duration

CASES = [
    ("Light traffic, short wait",3,10),
    ("Moderate traffic, medium wait",15,60),
    ("Heavy traffic, long wait",28,110),
    ("Heavy traffic, short wait",27,15),
    ("Light traffic, long wait",4,110),
]

if __name__ == "__main__":
    print(f"{'Scenario':<32}{'Vehicles':>9}{'Wait(s)':>9}{'Green(s)':>11}{'Category':>12}")
    for name,t,w in CASES:
        r=calculate_green_duration(t,w)
        print(f"{name:<32}{t:>9}{w:>9}{r['green_duration']:>11.2f}{r['category']:>12}")
    for t in range(0,31,3):
        for w in range(0,121,10):
            assert 5 <= calculate_green_duration(t,w)["green_duration"] <= 60
    print("\nAll output-range checks passed.")
