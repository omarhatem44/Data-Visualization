"""Animated bubble chart: income against life expectancy, 1952-2007 (plotly express).

The web version plays through 55 years with a slider; the static PNG shows 2007.
"""
import plotly.express as px

import _theme as T

T.plotly_theme()
gm = px.data.gapminder()
then = gm[gm["year"] == 1952].set_index("country")
now = gm[gm["year"] == 2007].set_index("country")
both = ((now["gdpPercap"] > then["gdpPercap"]) & (now["lifeExp"] > then["lifeExp"])).mean()

continents = {"Africa": T.VERMILION, "Americas": T.ORANGE, "Asia": T.BLUE, "Europe": T.GREEN, "Oceania": T.PURPLE}
options = dict(
    x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country",
    log_x=True, size_max=58, range_x=[200, 130000], range_y=[22, 88],
    color_discrete_map=continents, category_orders={"continent": list(continents)},
    labels={"gdpPercap": "GDP per person (US$, inflation-adjusted, log scale)",
            "lifeExp": "Life expectancy (years)", "pop": "Population", "continent": "Continent", "year": "Year"},
    hover_data={"gdpPercap": ":,.0f", "lifeExp": ":.1f", "pop": ":,.0f", "continent": False},
)


def styled(fig, subtitle):
    fig.update_layout(
        title=T.headline(f"Since 1952, {both:.0%} of countries have become both richer and longer-lived",
                         subtitle, "Data: Gapminder, via plotly"),
        legend=dict(title_text="", x=0.99, xanchor="right", y=0.03, yanchor="bottom",
                    bgcolor="rgba(255,255,255,0.85)"),
    )
    fig.update_xaxes(tickvals=[500, 1000, 2000, 5000, 10000, 20000, 50000, 100000],
                     ticktext=["$500", "$1k", "$2k", "$5k", "$10k", "$20k", "$50k", "$100k"])
    fig.update_traces(marker=dict(line=dict(width=0.6, color="white"), opacity=0.85))
    return fig


animated = styled(px.scatter(gm, animation_frame="year", animation_group="country", **options),
                  "Each bubble is a country, sized by population. Press play to run from 1952 to 2007.")
animated.update_layout(margin=dict(b=140))
static = styled(px.scatter(gm[gm["year"] == 2007], **options),
                "Each bubble is a country, sized by population, in 2007. The web version animates 1952 to 2007.")
T.save_plotly(animated, "08_animated_bubbles_gapminder", "Income and life expectancy, 1952-2007", static=static)
