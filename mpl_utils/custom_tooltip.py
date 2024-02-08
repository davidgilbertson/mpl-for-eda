from collections.abc import Callable
from typing import Optional

from matplotlib import pyplot as plt
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.figure import Figure
from matplotlib.patheffects import withSimplePatchShadow
from matplotlib.text import Text
from matplotlib.transforms import IdentityTransform
import pandas as pd

import mpl_utils


# Added in #603
class Blitter:
    def __init__(self, fig: Figure = None):
        fig = fig or plt.gcf()
        self.fig = fig
        self.canvas = fig.canvas
        self.background = None
        self.capture_background()

        fig.canvas.mpl_connect("draw_event", self.capture_background)

    def capture_background(self, _=None):
        self.background = self.canvas.copy_from_bbox(self.fig.bbox)

    def blit(self, artist: Artist):
        self.canvas.restore_region(self.background)
        self.fig.draw_artist(artist)
        self.canvas.blit()


def _default_get_text(event: MouseEvent):
    return f"x={event.xdata:g}\ny={event.ydata:g}"


# Added in #602
class add_custom_tooltip(mpl_utils.EventsMixin):
    def __init__(
        self,
        ax: Axes = None,
        get_text: Callable[[MouseEvent], Optional[str]] = _default_get_text,
        use_blit=True,
    ):
        ax = ax or plt.gca()
        super().__init__(ax)
        self.ax = ax
        self.fig = ax.figure
        self.get_text = get_text

        if use_blit and self.fig.canvas.supports_blit:
            self.blitter = Blitter(self.fig)
        else:
            self.blitter = None

        self.tooltip: Text = self.fig.text(
            x=0,
            y=0,
            s="",
            transform=IdentityTransform(),
            bbox=dict(
                alpha=0.8,
                path_effects=[withSimplePatchShadow(offset=(2, -2))],
            ),
            linespacing=1.4,
            multialignment="left",
            visible=False,
            animated=use_blit,
        )

        self.fig.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        ax._custom_tooltip_ref = self

    def on_mouse_move(self, event: MouseEvent):
        if event.button:
            self.hide_tooltip()
            return
        if event.inaxes != self.ax:
            return

        text = self.get_text(event)

        if text:
            is_left = event.x < self.fig.bbox.width / 2
            is_bottom = event.y < self.fig.bbox.height / 2

            self.tooltip.set(
                text=text,
                x=event.x + (15 if is_left else -15),
                y=event.y + (15 if is_bottom else -15),
                ha="left" if is_left else "right",
                va="bottom" if is_bottom else "top",
                visible=True,
            )
            self.render()
        else:
            self.hide_tooltip()

    def on_leave(self, _):
        if self.tooltip.get_visible():
            self.hide_tooltip()

    def hide_tooltip(self):
        self.tooltip.set_visible(False)
        self.render()

    def render(self):
        if self.blitter:
            self.blitter.blit(self.tooltip)
        else:
            self.fig.canvas.draw_idle()


if __name__ == "__main__":

    def get_text(event: MouseEvent):
        year = mpl_utils.get_closest_x(event)

        has_match = False
        text = mpl_utils.bold(f"{year:g}")

        for line in event.inaxes.lines:
            if line.contains(event)[0]:
                has_match = True
                country = line.get_label()
                value = mpl_utils.get_y_at_x(line, year)
                text += f"\n{country}: {value:.2f}"

        if has_match:
            return text

    mpl_utils.setup()
    fig, ax = plt.subplots(num="Custom tooltip", clear=True)
    mpl_utils.clear_events()

    df = pd.read_csv("../data/crop-data.csv")
    chart_df = df.pivot_table(
        index="Year",
        columns="Country",
        # columns=["Country", "Crop"],
        values="Yield",
    )
    # Mock missing data
    chart_df.iloc[20:25, 60:65] = 0

    ax.plot(
        chart_df,
        label=chart_df.columns,
        color="C0",
        linestyle="-",
        alpha=0.3,
    )

    self = add_custom_tooltip(
        ax=ax,
        get_text=get_text,
    )
