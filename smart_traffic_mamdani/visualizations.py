import numpy as np
import matplotlib.pyplot as plt
from membership import TRAFFIC_SETS, WAITING_SETS, GREEN_SETS, triangular_membership
from mamdani import OUTPUT_UNIVERSE, calculate_green_duration

def membership_figure():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    specs = [
        (axes[0], np.linspace(0,30,301), TRAFFIC_SETS, "Traffic density", "Vehicles"),
        (axes[1], np.linspace(0,120,301), WAITING_SETS, "Waiting time", "Seconds"),
        (axes[2], OUTPUT_UNIVERSE, GREEN_SETS, "Green-light duration", "Seconds")
    ]
    for ax, xs, sets, title, xlabel in specs:
        for name, params in sets.items():
            ax.plot(xs, [triangular_membership(x,*params) for x in xs], label=name, linewidth=2)
        ax.set(title=title, xlabel=xlabel, ylabel="Membership degree", ylim=(-.03,1.05))
        ax.grid(alpha=.25); ax.legend()
    fig.tight_layout()
    return fig

def output_figure(result):
    fig, ax = plt.subplots(figsize=(9,4))
    xs, ys = result["output_universe"], result["aggregated_output"]
    ax.fill_between(xs, ys, alpha=.3, label="Aggregated output")
    ax.plot(xs, ys, linewidth=2)
    ax.axvline(result["green_duration"], linestyle="--", label=f"Centroid = {result['green_duration']:.2f} s")
    ax.set(title="Mamdani aggregation and centroid defuzzification",
           xlabel="Green-light duration (seconds)", ylabel="Aggregated membership degree", ylim=(-.03,1.05))
    ax.grid(alpha=.25); ax.legend(); fig.tight_layout()
    return fig

def response_surface_figure():
    traffic = np.linspace(0,30,31); waiting = np.linspace(0,120,31)
    z = np.zeros((len(waiting),len(traffic)))
    for yi,w in enumerate(waiting):
        for xi,t in enumerate(traffic):
            z[yi,xi] = calculate_green_duration(float(t),float(w))["green_duration"]
    fig, ax = plt.subplots(figsize=(8,4.5))
    c = ax.contourf(traffic,waiting,z,levels=16)
    fig.colorbar(c,ax=ax,label="Green-light duration (seconds)")
    ax.set(title="Traffic controller response surface",xlabel="Vehicles waiting",ylabel="Waiting time (seconds)")
    fig.tight_layout()
    return fig
