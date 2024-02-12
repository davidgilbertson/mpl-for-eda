from matplotlib.colors import Normalize
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from mplcursors import Selection

import mpl_utils

df = pd.read_csv("../data/crop-data.csv")
df = df[df.Crop.eq("Potatoes")].dropna()

regions = df.Region.unique().tolist()

fig, (ax, spacer_ax) = mpl_utils.flex_subplots(
    "Slider widget",
    row_heights=[1, "40px"],
)
spacer_ax.set_axis_off()

path_collection = ax.scatter(x=[], y=[])

ax.set(
    title="Potato yields",
    xlabel="Population",
    xscale="log",
    xlim=(df.Population.min(), df.Population.max() * 1.1),
    ylabel="Yield",
    ylim=(0, df.Yield.max() * 1.1),
)


def plot_year(year):
    year_df = df[df.Year.eq(year)]
    path_collection.set(
        offsets=year_df[["Population", "Yield"]],
        sizes=10 + Normalize()(year_df.GDPPC) * 200,
        color=[f"C{regions.index(r)}" for r in year_df.Region],
    )
    fig.canvas.draw_idle()


slider = Slider(
    ax=mpl_utils.add_axes_px((60, 10, 300, 30), "bottom right"),
    label="Year ",
    valmin=df.Year.min(),
    valmax=df.Year.max(),
    valinit=df.Year.min(),
    valstep=df.Year.unique(),
    initcolor="none",
    track_color=plt.rcParams["patch.facecolor"],
)

slider.track.set(y=0.4, height=0.2)
slider.poly.set_visible(False)
slider.on_changed(plot_year)

slider.set_val(slider.valinit)  # Trigger the first render


def get_text(sel: Selection):
    year_df = df[df.Year.eq(slider.val)]
    row = year_df.iloc[sel.index]
    row = row.drop(["SubRegion", "Crop", "Year"])
    return mpl_utils.series_to_string(row)


mpl_utils.add_mplcursors_tooltip(get_text=get_text, pickables=ax)
