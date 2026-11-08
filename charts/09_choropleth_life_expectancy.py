"""Choropleth map: life expectancy by country in 2007 (plotly express)."""
import plotly.express as px

import _theme as T

T.plotly_theme()
df = px.data.gapminder().query("year == 2007")
low, high = df.nsmallest(1, "lifeExp").iloc[0], df.nlargest(1, "lifeExp").iloc[0]

fig = px.choropleth(df, locations="iso_alpha", color="lifeExp", hover_name="country",
                    color_continuous_scale=T.LIFE_SCALE, range_color=(40, 83), projection="natural earth",
                    labels={"lifeExp": "Life expectancy", "continent": "Continent"},
                    hover_data={"iso_alpha": False, "lifeExp": ":.1f", "continent": True})
fig.update_traces(marker_line_color="white", marker_line_width=0.4)
fig.update_geos(showframe=False, showcoastlines=False, showland=True, landcolor="#E3E6EA",
                showcountries=True, countrycolor="white", countrywidth=0.4,
                lataxis_range=[-57, 84], bgcolor="white")
fig.update_layout(
    title=T.headline(f"Life expectancy in 2007 ranged from {low.lifeExp:.0f} years in {low.country} "
                     f"to {high.lifeExp:.0f} in {high.country}",
                     "Life expectancy at birth. Grey countries are not in the Gapminder dataset.",
                     "Data: Gapminder, via plotly"),
    margin=dict(l=10, r=10, t=125, b=60),
    coloraxis_colorbar=T.bottom_colorbar("Years"),
)
T.save_plotly(fig, "09_choropleth_life_expectancy", "Life expectancy by country, 2007", height=640)
