"""Ridgeline plot: fuel economy of cars by model year (matplotlib + SciPy).

Overlapping density curves compare thirteen distributions in little space and
make the shift over time easy to follow.
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy.stats import gaussian_kde

import _theme as T

T.use_style()
df = sns.load_dataset("mpg").dropna(subset=["mpg"])
years = sorted(df["model_year"].unique())
medians = df.groupby("model_year")["mpg"].median()
cmap = LinearSegmentedColormap.from_list("economy", ["#C4E6D1", T.GREEN, "#00543D"])
norm = Normalize(medians.min(), medians.max())
grid = np.linspace(6, 50, 500)
height = 1.6  # ridge height in row units; above 1, neighbouring rows overlap

fig, ax = plt.subplots(figsize=(10, 8.6))
for i, year in enumerate(years):
    base = -i
    values = df.loc[df["model_year"] == year, "mpg"].to_numpy()
    density = gaussian_kde(values, bw_method=0.3)(grid)
    ridge = base + density / density.max() * height
    ax.fill_between(grid, base, ridge, color=cmap(norm(medians[year])), linewidth=0, zorder=2 * i)
    ax.plot(grid, ridge, color="white", linewidth=1.5, zorder=2 * i + 1)
    ax.plot(medians[year], base, "o", color=T.INK, markersize=4, zorder=100)
    ax.text(5.4, base + 0.08, f"19{year}", ha="right", va="bottom", fontsize=10.5, color=T.INK)

events = {74: "Oil crisis, 1973\u201374", 78: "First federal fuel-economy (CAFE) standards"}
for year, text in events.items():
    y = -years.index(year) + 0.18
    ax.annotate(text, xy=(46, y), xytext=(51, y), ha="left", va="center", fontsize=9.5,
                color=T.MUTED, annotation_clip=False,
                arrowprops=dict(arrowstyle="-", color=T.MUTED, linewidth=0.8))

ax.set_xlim(grid[0], grid[-1])
ax.set_ylim(-len(years) + 0.6, height + 0.2)
ax.set_yticks([])
ax.grid(False)
ax.spines["left"].set_visible(False)
ax.set_xlabel("Miles per gallon")

first, last = medians[years[0]], medians[years[-1]]
T.finish(fig,
         f"Typical fuel economy rose from {first:.0f} to {last:.0f} mpg in twelve model years",
         f"Fuel economy of {len(df)} car models sold in the US, by model year. Dots mark each year's median; darker ridges have higher medians.",
         "Data: Auto MPG dataset, UCI Machine Learning Repository, via seaborn")
T.save(fig, "02_ridgeline_fuel_economy")
