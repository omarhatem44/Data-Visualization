"""Raincloud plot: penguin body mass by species (matplotlib + SciPy).

Each species is shown three ways at once: a density curve (the cloud), a slim
boxplot, and every individual bird (the rain), so the summary never hides the data.
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter
from scipy.stats import gaussian_kde

import _theme as T

T.use_style()
df = sns.load_dataset("penguins").dropna(subset=["species", "body_mass_g"])
colors = {"Adelie": T.ORANGE, "Chinstrap": T.PURPLE, "Gentoo": T.GREEN}
medians = df.groupby("species")["body_mass_g"].median()
order = medians.sort_values(kind="stable").index.tolist()

rng = np.random.default_rng(42)
grid = np.linspace(2400, 6600, 600)
fig, ax = plt.subplots(figsize=(10.5, 5.6))

for i, species in enumerate(order):
    mass = df.loc[df["species"] == species, "body_mass_g"].to_numpy()
    color = colors[species]
    density = gaussian_kde(mass)(grid)
    cloud = i + 0.1 + density / density.max() * 0.42
    ax.fill_between(grid, i + 0.1, cloud, color=color, alpha=0.75, linewidth=0)
    ax.plot(grid, cloud, color=color, linewidth=1.3)
    ax.boxplot(mass, positions=[i], widths=0.1, orientation="horizontal", manage_ticks=False,
               showfliers=False, patch_artist=True,
               boxprops=dict(facecolor="white", edgecolor=T.INK, linewidth=1),
               medianprops=dict(color=T.INK, linewidth=2.2),
               whiskerprops=dict(color=T.INK, linewidth=1), capprops=dict(linewidth=0))
    rain = i - 0.2 + rng.uniform(-0.08, 0.08, mass.size)
    ax.scatter(mass, rain, s=12, color=color, alpha=0.6, linewidth=0)
    ax.text(6660, i + 0.05, f"Median {medians[species]:,.0f} g\n{mass.size} birds",
            va="center", ha="left", fontsize=9.5, color=T.MUTED, linespacing=1.4)

ax.set_yticks(range(len(order)), labels=order, fontsize=12, fontweight="bold")
for label, species in zip(ax.get_yticklabels(), order):
    label.set_color(T.darken(colors[species], 0.2))
ax.set_xlim(grid[0], grid[-1])
ax.set_ylim(-0.45, len(order) - 0.35)
ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
ax.set_xlabel("Body mass (g)")
ax.yaxis.grid(False)
ax.xaxis.grid(True)
ax.spines["left"].set_visible(False)

gap = medians["Gentoo"] - medians.drop("Gentoo").mean()
T.finish(fig,
         f"Gentoo penguins weigh about {gap / 1000:.1f} kg more than the other two species",
         f"Body mass of {len(df)} penguins from the Palmer Archipelago, Antarctica: "
         "density, boxplot and every bird",
         "Data: Gorman, Williams & Fraser (2014), Palmer Station LTER, via seaborn")
T.save(fig, "01_raincloud_penguins")
