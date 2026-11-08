"""Parallel categories diagram: who survived the Titanic (plotly graph objects).

A Sankey diagram merges the flows at each stage; parallel categories keep each
group's full path from ticket class to outcome, coloured by the outcome.
"""
import plotly.graph_objects as go
import seaborn as sns

import _theme as T

T.plotly_theme()
t = sns.load_dataset("titanic")
t["Class"] = t["class"].astype(str)
t["Passenger"] = t["who"].str.capitalize()
t["Outcome"] = t["survived"].map({1: "Survived", 0: "Died"})
rates = t.groupby(["Class", "Passenger"])["survived"].mean()


def dimension(column, label, order):
    return go.parcats.Dimension(values=t[column], label=label, categoryorder="array", categoryarray=order)


fig = go.Figure(go.Parcats(
    dimensions=[dimension("Class", "Ticket class", ["First", "Second", "Third"]),
                dimension("Passenger", "Passenger", ["Woman", "Child", "Man"]),
                dimension("Outcome", "Outcome", ["Survived", "Died"])],
    line=dict(color=t["survived"], colorscale=[[0, T.VERMILION], [1, T.BLUE]], shape="hspline"),
    hoveron="color", hoverinfo="count+probability", arrangement="freeform",
    labelfont=dict(size=15, color=T.INK), tickfont=dict(size=14, color=T.INK),
))
key = (f"<span style='color:{T.BLUE}'><b>blue</b></span> survived, "
       f"<span style='color:{T.VERMILION}'><b>orange</b></span> died")
fig.update_layout(
    title=T.headline(f"Women and children first, yet only {rates[('Third', 'Woman')]:.0%} "
                     "of third-class women survived",
                     f"Each ribbon follows a group of the {len(t)} passengers in the dataset: {key}.",
                     "Data: Titanic passenger list (891-passenger training set), via seaborn"),
    margin=dict(l=70, r=70, t=135, b=40),
)
T.save_plotly(fig, "11_parallel_categories_titanic", "Titanic survival by class and passenger group")
