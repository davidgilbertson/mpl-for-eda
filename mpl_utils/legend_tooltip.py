from typing import Union

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D
from matplotlib.transforms import IdentityTransform
import pandas as pd

import mpl_utils


# Added in #604
class add_legend_tooltip(mpl_utils.AxesEventHandlers):
    def __init__(self, ax: Axes = None):
        ax = ax or plt.gca()
        super().__init__(ax)
        self.ax = ax
        self.fig = ax.figure
        self.artists: list[Union[Line2D, PathCollection]] = ax.lines + ax.collections
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        ax._legend_tooltip_ref = self

    def on_mouse_move(self, event: MouseEvent):
        if event.inaxes != self.ax:
            return

        handles = []
        labels = []

        x_values = mpl_utils.get_x_values_from_ax(self.ax)
        x_value = mpl_utils.get_closest(x_values, event.xdata)

        for artist in self.artists:
            if artist.contains(event)[0]:
                value = mpl_utils.get_y_at_x(artist, x_value)
                labels.append(f"{artist.get_label()}: {value:g}")
                handles.append(artist)
                artist.set_alpha(1)
            else:
                artist.set_alpha(0.07)

        if handles:
            is_left = event.x < self.fig.bbox.width / 2
            is_bottom = event.y < self.fig.bbox.height / 2
            ha = "left" if is_left else "right"
            va = "lower" if is_bottom else "upper"

            self.ax.legend(
                handles=handles,
                labels=labels,
                title=mpl_utils.bold(x_value),
                bbox_to_anchor=(event.x, event.y),
                loc=f"{va} {ha}",
                bbox_transform=IdentityTransform(),
            ).set(in_layout=False)
        else:
            if legend := self.ax.get_legend():
                legend.remove()
            plt.setp(self.artists, alpha=1)

        self.fig.canvas.draw_idle()

    def on_leave(self, event):
        if legend := self.ax.get_legend():
            legend.remove()
            plt.setp(self.artists, alpha=1)

            self.fig.canvas.draw_idle()


if __name__ == "__main__":
    mpl_utils.setup()
    fig, ax = plt.subplots(num="Legend tooltip", clear=True)
    mpl_utils.clear_events()

    df = pd.read_csv("../data/crop-data.csv")
    chart_df = df.pivot_table(
        index="Year",
        columns="Country",
        # columns=["Country", "Crop"],
        values="Yield",
    )
    # Mock missing data
    chart_df.loc[1980:1983, "F":"G"] = 0

    ax.plot(chart_df, label=chart_df.columns)
    self = add_legend_tooltip()
