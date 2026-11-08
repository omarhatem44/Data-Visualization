"""Hexbin density with marginal histograms: 53,940 diamonds (seaborn JointGrid).

Too many points for a scatter plot, so they are binned into hexagons on log-log
axes, where the price-weight relationship becomes a straight line.
"""
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

import _theme as T

T.use_style()
df = sns.load_dataset("diamonds")
slope, intercept = np.polyfit(np.log10(df["carat"]), np.log10(df["price"]), 1)
cmap = LinearSegmentedColormap.from_list("stones", ["#DCEBF7", T.SKY, T.BLUE, "#0A2F51"])

g = sns.JointGrid(data=df, x="carat", y="price", height=7.4, ratio=5, space=0.1)
ax = g.ax_joint
ax.hexbin(df["carat"], df["price"], gridsize=55, xscale="log", yscale="log", bins="log",
          mincnt=1, cmap=cmap, linewidths=0.2)
sns.histplot(data=df, x="carat", ax=g.ax_marg_x, bins=60, log_scale=True, color=T.BLUE, alpha=0.45, linewidth=0)
sns.histplot(data=df, y="price", ax=g.ax_marg_y, bins=60, log_scale=True, color=T.BLUE, alpha=0.45, linewidth=0)
for marginal in (g.ax_marg_x, g.ax_marg_y):
    marginal.grid(False)
    for spine in marginal.spines.values():
        spine.set_visible(False)

xs = np.logspace(np.log10(0.22), np.log10(2.2), 50)
ax.plot(xs, 10 ** (intercept + slope * np.log10(xs)), color=T.VERMILION, linewidth=2, linestyle=(0, (5, 3)))
ax.text(1.15, 480, f"Power-law fit, slope {slope:.2f}:\ndoubling the weight multiplies\nthe price by about {2 ** slope:.1f}",
        color=T.darken(T.VERMILION, 0.15), fontsize=10, linespacing=1.35)

ax.xaxis.set_major_locator(FixedLocator([0.25, 0.5, 1, 2, 4]))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax.yaxis.set_major_locator(FixedLocator([500, 1000, 2000, 5000, 10000, 20000]))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.xaxis.set_minor_locator(NullLocator())
ax.yaxis.set_minor_locator(NullLocator())
ax.grid(True, axis="both")
ax.set_ylim(300, 25000)
ax.set(xlabel="Weight (carat, log scale)", ylabel="Price (US$, log scale)")

T.finish(g.figure,
         f"Double the weight, pay about {2 ** slope:.1f}\u00d7 the price",
         f"{len(df):,} diamonds on log\u2013log axes; darker hexagons hold more stones.",
         "Data: diamonds dataset (ggplot2), via seaborn")
T.save(g.figure, "04_hexbin_diamonds")
