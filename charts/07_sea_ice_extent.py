"""Highlighted time series: Arctic sea ice extent, one line per year (matplotlib).

Forty seasonal cycles share one axis, coloured from early (light) to recent
(dark), with the record-low year picked out in a contrasting colour.
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize

import _theme as T

T.use_style()
ice = sns.load_dataset("seaice")
ice["Date"] = pd.to_datetime(ice["Date"])
ice = ice[ice["Date"].dt.year.between(1980, 2019)].copy()
ice["year"] = ice["Date"].dt.year
ice["day"] = ice["Date"].dt.dayofyear
monthly = ice.groupby(ice["Date"].dt.month)["Extent"].mean()
print("seasonal max month:", monthly.idxmax(), "| min month:", monthly.idxmin())

cmap = LinearSegmentedColormap.from_list("ice", ["#C9DFF0", "#4F8FC0", "#0B2545"])
norm = Normalize(1980, 2019)
fig, ax = plt.subplots(figsize=(11, 6.4))
for year, g in ice.groupby("year"):
    if year != 2012:
        ax.plot(g["day"], g["Extent"], color=cmap(norm(year)), linewidth=0.9, alpha=0.9)
record = ice[ice["year"] == 2012]
ax.plot(record["day"], record["Extent"], color=T.VERMILION, linewidth=2.4, zorder=5)
low = record.loc[record["Extent"].idxmin()]
ax.annotate(f"2012: record low of\n{low['Extent']:.2f} million km\u00b2", xy=(low["day"], low["Extent"]),
            xytext=(low["day"] - 40, 1.5), ha="right", va="center", fontsize=10, linespacing=1.35,
            color=T.darken(T.VERMILION, 0.15),
            arrowprops=dict(arrowstyle="-", color=T.VERMILION, linewidth=1, shrinkB=3))

cax = ax.inset_axes([0.03, 0.1, 0.22, 0.03])
bar = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation="horizontal", ticks=[1980, 2000, 2019])
bar.outline.set_visible(False)
bar.ax.tick_params(labelsize=9, colors=T.MUTED)
bar.ax.set_title("Year", fontsize=9.5, color=T.MUTED, fontweight="normal", pad=4)

starts = pd.date_range("2001-01-01", periods=12, freq="MS")
ax.set_xticks(starts.dayofyear, labels=list(starts.strftime("%b")))
ax.set(xlim=(1, 366), ylim=(0, 17), ylabel="Sea ice extent (million km\u00b2)")

sept = ice[ice["Date"].dt.month == 9].groupby("year")["Extent"].mean()
drop = 1 - sept.loc[2010:2019].mean() / sept.loc[1980:1989].mean()
T.finish(fig,
         f"Arctic sea ice at its September low has shrunk by {drop:.0%} since the 1980s",
         "Daily sea ice extent in the Northern Hemisphere, one line per year from 1980 (light) to 2019 (dark).",
         "Data: National Snow and Ice Data Center, Sea Ice Index, via seaborn")
T.save(fig, "07_sea_ice_extent")
