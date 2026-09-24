"""Построить три иллюстрации к определениям O, Omega и Theta.

Для повторного запуска нужен matplotlib. Готовые PNG работают без него.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent
THRESHOLD = 4
PAPER = "#fffefa"
INK = "#263630"
MUTED = "#65716a"
BLUE = "#245fa8"
GREEN = "#267454"
AMBER = "#aa6018"


def plot_bound(kind: str) -> None:
    n = np.linspace(0, 12.8, 1601)
    function = n + 2 * np.sin(2 * n)
    upper = 2 * n
    lower = 0.5 * n
    after_threshold = n >= THRESHOLD

    # При n > 4: n - 2 >= n/2 и n + 2 <= 2n.
    # Поэтому обе границы верны для всего хвоста, а не только на рисунке.
    assert np.all(function >= 0)
    assert np.all(function[after_threshold] >= lower[after_threshold])
    assert np.all(function[after_threshold] <= upper[after_threshold])

    settings = {
        "o": (
            "O — верхняя граница",
            r"При $n > N$:  $T(n) \leq C\,F(n)$",
            r"$F(n)=n$,  $C=2$,  $N=4$",
            "После N кривая T(n) целиком ниже верхней границы или на ней.",
        ),
        "omega": (
            "Ω — нижняя граница",
            r"При $n > N$:  $T(n) \geq C\,F(n)$",
            r"$F(n)=n$,  $C=0{,}5$,  $N=4$",
            "После N кривая T(n) целиком выше нижней границы или на ней.",
        ),
        "theta": (
            "Θ — точный порядок роста",
            r"При $n > N$:  $C_1\,F(n) \leq T(n) \leq C_2\,F(n)$",
            r"$F(n)=n$,  $C_1=0{,}5$,  $C_2=2$,  $N=4$",
            "После N кривая T(n) остаётся между двумя границами, включая их.",
        ),
    }
    title, condition, constants, caption = settings[kind]

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 12,
            "mathtext.fontset": "dejavusans",
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
        }
    )
    fig = plt.figure(figsize=(10.4, 5.6), facecolor=PAPER)
    ax = fig.add_axes((0.09, 0.22, 0.865, 0.52), facecolor=PAPER)
    fig.text(0.09, 0.965, title, fontsize=20, weight="bold", va="top")
    fig.text(0.09, 0.875, condition, fontsize=14, va="top")
    fig.text(0.955, 0.96, constants, fontsize=11, color=MUTED, ha="right", va="top")

    ax.axvspan(0, THRESHOLD, color="#ebede7", zorder=0)
    if kind == "o":
        ax.fill_between(n, 0, upper, where=after_threshold, color=GREEN, alpha=0.10)
    elif kind == "omega":
        ax.fill_between(n, lower, 29, where=after_threshold, color=GREEN, alpha=0.10)
    else:
        ax.fill_between(n, lower, upper, where=after_threshold, color=GREEN, alpha=0.10)

    ax.plot(n, function, color=BLUE, linewidth=2.8, label=r"$T(n)$", zorder=5)
    if kind in {"o", "theta"}:
        label = r"$C\,F(n)=2n$" if kind == "o" else r"$C_2\,F(n)=2n$"
        ax.plot(n, upper, color=GREEN, linewidth=2, linestyle="--", label=label)
    if kind in {"omega", "theta"}:
        label = r"$C\,F(n)=0{,}5n$" if kind == "omega" else r"$C_1\,F(n)=0{,}5n$"
        ax.plot(n, lower, color=AMBER, linewidth=2, linestyle="--", label=label)

    # Точки показывают целые размеры входа; плавная линия помогает видеть форму.
    integers = np.arange(13)
    ax.scatter(integers, integers + 2 * np.sin(2 * integers), s=16, color=BLUE, zorder=6)
    ax.axvline(THRESHOLD, color=MUTED, linewidth=1.5, linestyle=(0, (4, 4)))
    ax.text(1.95, 27.3, r"До порога $N$", ha="center", color=MUTED, fontsize=11)
    ax.text(8.3, 27.3, r"Для всех $n > N$", ha="center", color=GREEN, fontsize=11)
    ax.set(xlim=(0, 12.8), ylim=(0, 29))
    ax.set_xticks([0, THRESHOLD, 8, 12], ["0", r"$N=4$", "8", "12"])
    ax.set_yticks([0, 5, 10, 15, 20, 25])
    ax.set_xlabel(r"Размер входа $n$", labelpad=8)
    ax.set_ylabel("Затраты", labelpad=10)
    ax.grid(axis="y", color="#ccd3c9", linewidth=0.7, alpha=0.65)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("bottom", "left"):
        ax.spines[side].set_color("#9ba99d")
    ax.tick_params(length=0, pad=7)
    ax.legend(
        loc="lower left",
        bbox_to_anchor=(-0.012, 1.025),
        frameon=False,
        ncol=3,
        fontsize=12,
        handlelength=2.4,
        columnspacing=2,
    )

    fig.text(0.09, 0.075, caption, fontsize=12)
    fig.text(
        0.09,
        0.027,
        "Зелёная область — допустимые значения T(n) после N. До N условие не требуется.",
        fontsize=10,
        color=MUTED,
    )
    fig.savefig(OUTPUT_DIR / f"asymptotic-{kind}.png", dpi=160, facecolor=PAPER)
    plt.close(fig)


if __name__ == "__main__":
    for bound in ("o", "omega", "theta"):
        plot_bound(bound)
