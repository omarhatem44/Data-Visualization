"""Annotated heatmap with marginal bars: monthly airline passengers (seaborn).

The heatmap shows seasonality and growth at once; the bar strip on top adds
the yearly totals that the cells alone make hard to compare.
"""
import matplotlib.pyplot as plt
import seaborn as sns

import _theme as T

T.use_style()
flights = sns.load_dataset("flights")
table = flights.pivot(index="month", columns="year", values="passengers")
totals = table.sum()
cmap = sns.color_palette("crest", as_cmap=True)

fig = plt.figure(figsize=(12, 7.8))
layout = fig.add_gridspec(2, 1, height_ratios=[1, 4.4], hspace=0.05)
bars, heat = fig.add_subplot(layout[0]), fig.add_subplot(layout[1])

sns.heatmap(table, ax=heat, cmap=cmap, annot=True, fmt="d", annot_kws=dict(fontsize=9.5),
            linewidths=1.5, linecolor="white", cbar=False)
heat.set(xlabel="", ylabel="")
heat.tick_params(axis="both", rotation=0)
heat.grid(False)

positions = [i + 0.5 for i in range(len(totals))]
bars.bar(positions, totals.values, width=0.86, color=cmap(0.72))
for xpos, total in zip(positions, totals.values):
    bars.text(xpos, total + 60, f"{total:,}", ha="center", va="bottom", fontsize=9, color=T.MUTED)
bars.text(-0.25, totals.max() * 0.45, "Yearly\ntotal", ha="right", va="center", fontsize=10, color=T.MUTED)
bars.set_xlim(0, len(totals))
bars.set_ylim(0, totals.max() * 1.25)
bars.axis("off")

growth = totals.iloc[-1] / totals.iloc[0]
peaks = set(table.idxmax())
print("peak months:", peaks)
T.finish(fig,
         f"Air travel grew {growth:.1f}-fold in twelve years, peaking every summer",
         "International airline passengers per month, in thousands, 1949\u20131960. Bars show yearly totals.",
         "Data: Box & Jenkins (1976), Series G, via seaborn")
T.save(fig, "06_heatmap_air_passengers")
