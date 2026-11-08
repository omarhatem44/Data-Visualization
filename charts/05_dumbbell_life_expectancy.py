"""Dumbbell chart: life expectancy in 1952 and 2007 (matplotlib).

Two dots and a connecting line show both levels and the change between them,
which a pair of bar charts would split apart.
"""
import matplotlib.pyplot as plt
import plotly.express as px

import _theme as T

T.use_style()
gm = px.data.gapminder()
wide = gm.pivot(index="country", columns="year", values="lifeExp")[[1952, 2007]]
wide.columns = ["start", "end"]
wide["gain"] = wide["end"] - wide["start"]
largest = wide.nlargest(10, "gain")
smallest = wide.nsmallest(6, "gain").iloc[::-1]
print("smallest gains:", ", ".join(smallest.index))

fig, ax = plt.subplots(figsize=(10.5, 8.2))
y, ticks, names = 0.0, [], []
for group, rows in [("Largest gains", largest), ("Smallest gains", smallest)]:
    ax.text(-0.012, y + 0.95, group, transform=ax.get_yaxis_transform(), ha="right", va="center",
            fontsize=11.5, fontweight="bold", color=T.INK)
    for country, r in rows.iterrows():
        color = T.BLUE if r.gain >= 0 else T.VERMILION
        ax.plot([r.start, r.end], [y, y], color="#D5DAE0", linewidth=3.4, zorder=1)
        ax.scatter(r.start, y, s=46, color="#9AA5B1", zorder=2)
        ax.scatter(r.end, y, s=62, color=color, zorder=3)
        ax.text(max(r.start, r.end) + 1.3, y, f"{r.gain:+.1f} yrs".replace("-", "\u2212"), va="center",
                fontsize=9.5, color=T.darken(color, 0.1))
        ticks.append(y)
        names.append(country)
        y -= 1
    y -= 1.2

first = largest.iloc[0]
ax.text(first.start, 0.55, "1952", ha="center", fontsize=9.5, color=T.MUTED)
ax.text(first.end, 0.55, "2007", ha="center", fontsize=9.5, color=T.darken(T.BLUE, 0.1))

ax.set_yticks(ticks, labels=names)
ax.set_xlim(25, 88)
ax.set_ylim(y + 1.6, 1.5)
ax.yaxis.grid(False)
ax.xaxis.grid(True)
ax.spines["left"].set_visible(False)
ax.set_xlabel("Life expectancy at birth (years)")

n30, declines = int((wide["gain"] >= 30).sum()), int((wide["gain"] < 0).sum())


def spell(n):
    return "zero one two three four five six seven eight nine ten".split()[n] if n <= 10 else str(n)


southern = {"Botswana", "Lesotho", "Malawi", "Mozambique", "Namibia", "South Africa",
            "Swaziland", "Zambia", "Zimbabwe"}
where = ", all six in southern Africa" if set(smallest.index) <= southern else ""
T.finish(fig,
         f"{spell(n30).capitalize()} countries gained over 30 years of life expectancy; {spell(declines)} went backwards",
         f"Life expectancy at birth in 1952 and 2007: the ten largest gains and the six smallest{where}.",
         "Data: Gapminder, via plotly")
T.save(fig, "05_dumbbell_life_expectancy")
