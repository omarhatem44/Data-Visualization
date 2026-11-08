"""Treemap: population by continent and country, coloured by life expectancy (plotly express)."""
import plotly.express as px

import _theme as T

T.plotly_theme()
df = px.data.gapminder().query("year == 2007")
asia = df.loc[df["continent"] == "Asia", "pop"].sum() / df["pop"].sum()

fig = px.treemap(df, path=[px.Constant(f"All {len(df)} countries"), "continent", "country"], values="pop",
                 color="lifeExp", color_continuous_scale=T.LIFE_SCALE, range_color=(40, 83))
fig.update_traces(
    texttemplate="<b>%{label}</b><br>%{percentRoot:.1%}",
    hovertemplate="<b>%{label}</b><br>Population: %{value:,.0f}<br>Share of total: %{percentRoot:.1%}"
                  "<br>Life expectancy: %{color:.1f} years<extra></extra>",
    marker=dict(line=dict(color="white", width=1)),
    root_color="#EEF0F3",
    tiling=dict(pad=2),
)
fig.update_layout(
    title=T.headline(f"{asia:.0%} of the people in these countries lived in Asia in 2007",
                     "Area shows population, colour shows life expectancy (same scale as the map). "
                     "Click a continent to zoom in.",
                     "Data: Gapminder, via plotly"),
    uniformtext=dict(minsize=10, mode="hide"),
    margin=dict(l=10, r=10, t=125, b=60),
    coloraxis_colorbar=T.bottom_colorbar("Life expectancy (years)"),
)
T.save_plotly(fig, "10_treemap_population", "Population and life expectancy by country, 2007")
