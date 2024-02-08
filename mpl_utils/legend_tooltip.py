from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D
from matplotlib.transforms import IdentityTransform
import pandas as pd

import mpl_utils


# Added in #604
class add_legend_tooltip(mpl_utils.EventsMixin):
    def __init__(
        self,
        ax: Axes = None,
        title_format="{:g}",
    ):
        ax = ax or plt.gca()
        super().__init__(ax)
        self.ax = ax
        self.title_format = title_format
        self.fig = ax.figure
        self.artists = [
            artist
            for artist in ax.get_children()
            if isinstance(artist, (Line2D, PathCollection))
        ]
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        ax._legend_tooltip_ref = self

    def on_mouse_move(self, event: MouseEvent):
        if event.inaxes != self.ax:
            return

        handles = []
        labels = []

        x_value = mpl_utils.get_closest_x(event)

        for artist in self.artists:
            if artist.contains(event)[0]:
                handles.append(artist)
                value = mpl_utils.get_y_at_x(artist, x_value)
                labels.append(f"{artist.get_label()}: {value:g}")
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
                title=mpl_utils.bold(self.title_format.format(x_value)),
                bbox_to_anchor=(event.x, event.y),
                bbox_transform=IdentityTransform(),
                loc=f"{va} {ha}",
                shadow=True,
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
        values="Yield",
    )
    # Mock missing data
    chart_df.iloc[20:25, 60:65] = 0

    ax.plot(chart_df, label=chart_df.columns)
    add_legend_tooltip()
