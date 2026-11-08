"""Shared look and feel for every chart in this repository.

One palette, one typeface and a few helpers keep the matplotlib, seaborn and
plotly figures consistent with each other.
"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import to_hex, to_rgb
from matplotlib.transforms import Bbox, offset_copy

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
WEB_DIR = ROOT / "docs" / "charts"

# Okabe-Ito palette: stays distinguishable for the common types of colour blindness
BLUE, ORANGE, GREEN = "#0072B2", "#E69F00", "#009E73"
VERMILION, PURPLE, SKY = "#D55E00", "#CC79A7", "#56B4E9"
PALETTE = [BLUE, ORANGE, GREEN, VERMILION, PURPLE, SKY]

INK = "#1F2933"     # headlines and key labels
MUTED = "#5F6B78"   # subtitles, axis labels, sources
FAINT = "#C3CAD3"   # context lines and points
GRID = "#E8EBEF"

# Scale for life expectancy, shared by the map and the treemap
LIFE_SCALE = [[0.0, "#A63603"], [0.3, ORANGE], [0.55, "#F2E8C9"], [0.78, SKY], [1.0, "#0B4F8A"]]

FONT_STACK = "'Fira Sans', Inter, Arial, sans-serif"

# The typeface ships with the repo (SIL Open Font License), so figures look the same everywhere
for ttf in (ROOT / "fonts").glob("*.ttf"):
    font_manager.fontManager.addfont(str(ttf))


def darken(color, amount=0.25):
    """Same hue, darker: for text drawn in a series colour."""
    r, g, b = to_rgb(color)
    return to_hex((r * (1 - amount), g * (1 - amount), b * (1 - amount)))


# ---------------------------------------------------------------- matplotlib / seaborn
def use_style():
    plt.style.use(Path(__file__).with_name("portfolio.mplstyle"))


def finish(fig, title, subtitle=None, source=None):
    """Headline, subtitle and source line, aligned with the left edge of the plot content."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    boxes = [ax.get_tightbbox(renderer) for ax in fig.axes if ax.get_visible()]
    box = Bbox.union(boxes).transformed(fig.transFigure.inverted())

    def shifted(points):
        return offset_copy(fig.transFigure, fig=fig, y=points, units="points")

    offset = 12
    if subtitle:
        fig.text(box.x0, box.y1, subtitle, transform=shifted(offset), ha="left", va="bottom",
                 fontsize=11.5, color=MUTED, linespacing=1.4)
        offset += (subtitle.count("\n") + 1) * 11.5 * 1.4 + 6
    fig.text(box.x0, box.y1, title, transform=shifted(offset), ha="left", va="bottom",
             fontsize=17, fontweight="bold", color=INK)
    if source:
        fig.text(box.x0, box.y0, source, transform=shifted(-12), ha="left", va="top",
                 fontsize=9, color=MUTED)


def save(fig, name):
    """Write figures/<name>.png, without software tags in the file metadata."""
    FIG_DIR.mkdir(exist_ok=True)
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.35,
                facecolor="white", metadata={"Software": None})
    plt.close(fig)
    print("saved", path.relative_to(ROOT))


# ---------------------------------------------------------------- plotly
def plotly_theme():
    """Register a 'portfolio' plotly template and make it the default."""
    import plotly.graph_objects as go
    import plotly.io as pio

    if os.environ.get("TOPOJSON_URL"):  # optional: export map PNGs without internet access
        pio.kaleido.scope.topojson = os.environ["TOPOJSON_URL"]

    axis = dict(gridcolor=GRID, zeroline=False, linecolor=FAINT, ticks="",
                tickfont=dict(color=MUTED), title=dict(font=dict(color=MUTED, size=13)))
    pio.templates["portfolio"] = go.layout.Template(layout=dict(
        font=dict(family=FONT_STACK, size=13, color=INK),
        title=dict(x=0, xref="paper", xanchor="left", y=0.97, yanchor="top", font=dict(size=21)),
        colorway=PALETTE,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=70, r=40, t=125, b=70),
        xaxis=axis,
        yaxis=axis,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED)),
        hoverlabel=dict(bgcolor="white", bordercolor=FAINT, font=dict(family=FONT_STACK, size=13, color=INK)),
    ))
    pio.templates.default = "plotly_white+portfolio"


def headline(title, subtitle=None, source=None):
    """Plotly title block: bold headline, muted subtitle, small source line."""
    parts = [f"<b>{title}</b>"]
    if subtitle:
        parts.append(f"<span style='font-size:14px;color:{MUTED}'>{subtitle}</span>")
    if source:
        parts.append(f"<span style='font-size:11.5px;color:{MUTED}'>{source}</span>")
    return "<br>".join(parts)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;700&display=swap" rel="stylesheet">
<style>html, body, body > div { height: 100%; margin: 0; background: #fff; }</style>
</head>
<body>
__BODY__
</body>
</html>
"""


def save_plotly(fig, name, page_title, static=None, width=1100, height=660):
    """Write figures/<name>.png (static) and docs/charts/<name>.html (interactive)."""
    FIG_DIR.mkdir(exist_ok=True)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    png = FIG_DIR / f"{name}.png"
    (static or fig).write_image(png, width=width, height=height, scale=2)
    body = fig.to_html(full_html=False, include_plotlyjs="cdn", default_width="100%",
                       default_height="100%", config={"responsive": True, "displaylogo": False})
    page = WEB_DIR / f"{name}.html"
    page.write_text(PAGE.replace("__TITLE__", page_title).replace("__BODY__", body), encoding="utf-8")
    print("saved", png.relative_to(ROOT), "and", page.relative_to(ROOT))


def bottom_colorbar(title):
    """Horizontal colour bar placed under a map or treemap."""
    return dict(title=dict(text=title, side="top"), orientation="h", x=0, xanchor="left",
                y=-0.02, yanchor="top", len=0.32, thickness=12, outlinewidth=0,
                tickfont=dict(color=MUTED))
