from collections.abc import Sequence, Iterable

from matplotlib.axes import Axes
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import mpl_utils


def plot_searchable_scatter(
    x,
    y,
    labels: Iterable,
    **kwargs,
) -> Axes:
    if not isinstance(labels, list):
        labels = list(labels)

    if len(labels) != len(x):
        raise ValueError("Length of labels must match length of x and y")

    fig, (spacer_ax, ax) = mpl_utils.flex_subplots(row_heights=["40px", 1])
    spacer_ax.set_axis_off()

    path_collection = ax.scatter(x, y, **kwargs)

    mpl_utils.add_mplcursors_tooltip(
        get_text=lambda sel: labels[sel.index],
    )

    def on_text_change(text):
        if text == "":
            path_collection.set(linewidth=0)
        else:
            matches = [text.lower() in label.lower() for label in labels]
            path_collection.set(
                edgecolor=plt.rcParams["text.color"],
                linewidth=np.where(matches, 2, 0),
            )
        fig.canvas.draw_idle()

    mpl_utils.add_text_box(
        bounds=(10, 10, 200, 30),
        origin="top right",
        label="Search: ",
        on_change=on_text_change,
    )

    return ax


if __name__ == "__main__":
    df = pd.read_csv("../../data/crop-data.csv")

    crop = "Wheat"
    df = df[df.Crop.eq(crop)]
    df = df.dropna(subset=["Yield", "GDPPC"])

    chart_df = df.groupby("Country", as_index=False).last()

    ax = plot_searchable_scatter(
        x=chart_df.GDPPC / 1000,
        y=chart_df.Yield,
        labels=chart_df.Country,
        s=200,
        alpha=0.6,
    )

    ax.set_xlabel("GDP per capita ($k)")
    ax.set_ylabel(f"Yield of {crop} (t/ha)")
    ax.set_xmargin(0.02)
