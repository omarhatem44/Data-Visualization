"""Before and after: redesigning a first-draft chart (matplotlib).

Same data, same question: does spending more on health buy longer lives?
"""
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter

import _theme as T

hx = sns.load_dataset("healthexp").sort_values("Year")

# Before: a typical first draft with default settings
with plt.style.context("default"):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for country, g in hx.groupby("Country"):
        ax.scatter(g["Spending_USD"], g["Life_Expectancy"], label=country)
    ax.set(xlabel="Spending_USD", ylabel="Life_Expectancy", title="healthexp")
    ax.legend()
    ax.grid(True)
    T.save(fig, "12_makeover_before")

# After: one highlighted country, grey context, direct labels, a headline that states the finding
T.use_style()
names = {"USA": "United States", "Great Britain": "United Kingdom"}
fig, ax = plt.subplots(figsize=(11, 6.6))
labels = []
for country, g in hx.groupby("Country"):
    us = country == "USA"
    color = T.VERMILION if us else "#8C99A6"
    ax.plot(g["Spending_USD"], g["Life_Expectancy"], color=color, linewidth=2.6 if us else 1.5,
            zorder=3 if us else 2)
    end = g.iloc[-1]
    ax.scatter(end["Spending_USD"], end["Life_Expectancy"], s=28, color=color, zorder=4)
    labels.append([end["Life_Expectancy"], end["Spending_USD"], names.get(country, country), us, color])

peers = sorted(label for label in labels if not label[3])
for below, above in zip(peers, peers[1:]):  # nudge peer labels apart so they never overlap
    above[0] = max(above[0], below[0] + 0.75)
for y, x, name, us, color in labels:
    ax.text(x + 180, y, name, va="center", fontsize=10.5 if us else 10,
            color=T.darken(color, 0.1) if us else T.MUTED, fontweight="bold" if us else "normal")

usa = hx[hx["Country"] == "USA"]
for row, offset in ((usa.iloc[0], (-10, -4)), (usa.iloc[-1], (0, -16))):
    ax.annotate(str(int(row["Year"])), (row["Spending_USD"], row["Life_Expectancy"]), xytext=offset,
                textcoords="offset points", ha="right" if offset[0] else "center", fontsize=9, color=T.MUTED)

ax.grid(True, axis="both")
ax.xaxis.set_major_formatter(StrMethodFormatter("${x:,.0f}"))
ax.set(xlabel="Health spending per person (US$, purchasing-power adjusted)",
       ylabel="Life expectancy at birth (years)")

latest = hx.groupby("Country")["Year"].max().min()
snap = hx[hx["Year"] == latest].set_index("Country")
ratio = snap.loc["USA", "Spending_USD"] / snap.drop("USA")["Spending_USD"].mean()
print("latest common year:", latest, "| ratio:", round(ratio, 2),
      "| US lowest life expectancy:", snap["Life_Expectancy"].idxmin() == "USA")
T.finish(fig,
         "The US spends the most on health per person, yet has the shortest lives",
         f"Health spending against life expectancy, {hx['Year'].min()}\u2013{hx['Year'].max()}, one line per country. "
         f"In {latest}, US spending was {ratio:.1f}\u00d7 the average of the other five.",
         "Data: OECD health statistics, via seaborn")
T.save(fig, "12_makeover_after")
