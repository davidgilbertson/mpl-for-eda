from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor, Button
import pandas as pd

import mpl_utils

df = pd.read_csv("../data/crop-data.csv")
chart_df = df.pivot_table(
    index="Year",
    columns="Crop",
    values="Yield",
)

fig, (spacer_ax, ax) = mpl_utils.flex_subplots(
    "Widgets introduction",
    row_heights=["40px", 1],
)
spacer_ax.set_axis_off()

ax.plot(chart_df, label=chart_df.columns)
ax.legend()
cursor = Cursor(
    ax=ax,
    vertOn=False,
    linestyle="--",
    linewidth=1,
    color="#aaa",
)

button = Button(
    ax=mpl_utils.add_axes_px((20, 20, 130, 30), "top right"),
    label="Toggle legend",
    color=plt.rcParams["grid.color"],
    hovercolor=plt.rcParams["axes.edgecolor"],
)


def toggle_legend(event):
    if legend := ax.get_legend():
        legend.remove()
    else:
        ax.legend()

    fig.canvas.draw_idle()


button.on_clicked(toggle_legend)
