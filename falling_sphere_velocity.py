"""Plot the symbolic, dimensionless Stokes velocity profile for Homework 5."""

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    """Create and display the normalized transient velocity profile."""
    t_norm = np.linspace(0.0, 5.0, 500)
    v_norm = 1.0 - np.exp(-t_norm)

    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams["figure.dpi"] = 300
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        t_norm,
        v_norm,
        color="navy",
        linewidth=2.5,
        label=r"$v_z(t) / v_{t,z}$",
        zorder=3,
    )
    ax.axhline(
        1.0,
        color="crimson",
        linestyle="--",
        linewidth=1.6,
        label=r"Asymptote: $v_z(t) \to v_{t,z}$",
        zorder=2,
    )

    annotation_specs = (
        (1.0, 1.0 - np.exp(-1.0), r"$t=\tau$: 63.2%", (-78, 20)),
        (3.0, 1.0 - np.exp(-3.0), r"$t=3\tau$: 95.0%", (16, -38)),
    )
    for point_x, point_y, label, offset in annotation_specs:
        ax.vlines(
            point_x,
            0.0,
            point_y,
            color="0.35",
            linestyle=":",
            linewidth=1.1,
            zorder=1,
        )
        ax.hlines(
            point_y,
            0.0,
            point_x,
            color="0.35",
            linestyle=":",
            linewidth=1.1,
            zorder=1,
        )
        ax.plot(
            point_x,
            point_y,
            marker="o",
            markersize=5.5,
            color="crimson",
            zorder=4,
        )
        ax.annotate(
            label,
            xy=(point_x, point_y),
            xytext=offset,
            textcoords="offset points",
            fontsize=9,
            ha="left" if offset[0] > 0 else "right",
            va="center",
            bbox={
                "boxstyle": "round,pad=0.3",
                "facecolor": "white",
                "edgecolor": "none",
                "alpha": 0.8,
            },
            zorder=5,
        )

    ax.set_title(
        r"Normalized Velocity Profile $v_z(t) / v_{t,z} = 1 - e^{-t/\tau}$",
        pad=14,
    )
    ax.set_xlabel(r"Time $t$ [units of $\tau$]", labelpad=10)
    ax.set_ylabel(
        r"Velocity Component $v_z(t)$ [units of $v_{t,z}$]",
        labelpad=12,
    )
    ax.set_xlim(0.0, 5.0)
    ax.set_ylim(-0.08, 1.12)
    ax.set_xticks(
        [0, 1, 2, 3, 4, 5],
        labels=[
            r"$0$",
            r"$\tau$",
            r"$2\tau$",
            r"$3\tau$",
            r"$4\tau$",
            r"$5\tau$",
        ],
    )
    ax.set_yticks(
        [0.0, 0.632, 0.950, 1.0],
        labels=[
            r"$0$",
            r"$0.632\,v_{t,z}$",
            r"$0.950\,v_{t,z}$",
            r"$v_{t,z}$",
        ],
    )
    ax.legend(loc="lower right", frameon=True)

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
