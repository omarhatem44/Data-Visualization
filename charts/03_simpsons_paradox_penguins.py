"""Simpson's paradox in the Palmer penguins (seaborn regression plots).

Pooled together, bill length and bill depth are negatively related; within
every species the relationship is positive. Two panels make the reversal visible.
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import _theme as T

T.use_style()
df = sns.load_dataset("penguins").dropna(subset=["species", "bill_length_mm", "bill_depth_mm"])
x, y = "bill_length_mm", "bill_depth_mm"
colors = {"Adelie": T.ORANGE, "Chinstrap": T.PURPLE, "Gentoo": T.GREEN}


def r_label(data):
    return f"r = {data[x].corr(data[y]):.2f}".replace("-", "\u2212")


def line_end(data, left=False):
    slope, intercept = np.polyfit(data[x], data[y], 1)
    x_end = data[x].min() if left else data[x].max()
    return x_end + (-0.7 if left else 0.7), slope * x_end + intercept


fig, (pooled, split) = plt.subplots(1, 2, figsize=(12.5, 5.8), sharex=True, sharey=True)

sns.regplot(data=df, x=x, y=y, ax=pooled, seed=1,
            scatter_kws=dict(s=16, color="#9AA5B1", alpha=0.7, linewidths=0),
            line_kws=dict(color=T.INK, linewidth=2.4))
pooled.text(*line_end(df), f"All species\n{r_label(df)}", ha="left", va="center",
            color=T.INK, fontsize=10.5, fontweight="bold", linespacing=1.3)

for species, color in colors.items():
    sub = df[df["species"] == species]
    sns.regplot(data=sub, x=x, y=y, ax=split, seed=1, color=color,
                scatter_kws=dict(s=16, alpha=0.65, linewidths=0), line_kws=dict(linewidth=2.4))
    left = species == "Adelie"
    split.text(*line_end(sub, left), f"{species}\n{r_label(sub)}", ha="right" if left else "left",
               va="center", color=T.darken(color, 0.2), fontsize=10.5, fontweight="bold", linespacing=1.3)

pooled.set_title("Pooled: longer bills look shallower")
split.set_title("By species: longer bills are deeper")
pooled.set(xlabel="Bill length (mm)", ylabel="Bill depth (mm)", xlim=(25, 67))
split.set(xlabel="Bill length (mm)", ylabel="")

T.finish(fig,
         "Simpson's paradox: the trend reverses once the species are separated",
         f"Bill length against bill depth in {len(df)} penguins. Shaded bands are 95% confidence intervals.",
         "Data: Gorman, Williams & Fraser (2014), Palmer Station LTER, via seaborn")
T.save(fig, "03_simpsons_paradox_penguins")
