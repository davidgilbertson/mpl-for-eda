from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import pandas as pd

import mpl_utils


class add_dynamic_legend(mpl_utils.EventsMixin):
    def __init__(
        self,
        ax: Axes = None,
        title_format="{:g}",
        **kwargs,
    ):
        if kwargs.get("reverse"):
            raise ValueError("Reversed legend is not supported")

        ax = ax or plt.gca()
        super().__init__(ax)

        self.ax = ax
        self.title_format = title_format
        self.fig = ax.figure
        self.legend = ax.legend(title="Legend", alignment="left", **kwargs)

        self.vline = ax.axvline(
            x=float("nan"),  # ax.dataLim.xmin would be fine too
            linestyle=":",
            color="white",
            alpha=0.4,
            visible=False,
        )

        self.locked = False

        self.fig.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        ax._dynamic_legend_ref = self

    def on_mouse_move(self, event):
        if event.button:  # a drag
            return

        if self.locked:
            return

        if event.inaxes != self.ax:
            return

        self.update(event)

    def on_left_click(self, event):
        self.locked = True
        self.update(event)

    def on_right_click(self, event):
        self.locked = False
        self.update(event)

    def on_leave(self, event):
        if not self.locked:
            self.reset()

    def update(self, event):
        x_value = mpl_utils.get_closest_x(event)
        x_value_string = self.title_format.format(x_value)
        self.legend.set_title(f"Legend (values for {x_value_string})")

        legend_texts = self.legend.texts
        ax_artists, labels = self.ax.get_legend_handles_labels()
        for text, ax_artist, label in zip(legend_texts, ax_artists, labels):
            value = mpl_utils.get_y_at_x(ax_artist, x_value)
            text.set_text(f"{label} ({value:g})")

        self.vline.set_xdata([x_value])
        self.vline.set_visible(True)
        self.fig.canvas.draw_idle()

    def reset(self):
        self.vline.set_visible(False)

        self.legend.set_title("Legend")
        legend_texts = self.legend.texts
        artists, labels = self.ax.get_legend_handles_labels()
        for text, artist, label in zip(legend_texts, artists, labels):
            text.set_text(label)

        self.fig.canvas.draw_idle()


if __name__ == "__main__":
    mpl_utils.setup()
    fig, ax = plt.subplots(num="Dynamic legend", clear=True)
    mpl_utils.clear_events()

    df = pd.read_csv("../data/crop-data.csv")
    chart_df = df.pivot_table(
        index="Year",
        columns="Region",
        values="Yield",
    )
    ax.plot(chart_df, label=chart_df.columns)
    add_dynamic_legend(loc="upper left")
