from dataclasses import dataclass

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.artist import Artist
from matplotlib.backend_bases import PickEvent
from matplotlib.text import Text

import mpl_utils


# Added in #505
class add_interactive_legend:
    @dataclass
    class SeriesItem:
        legend_handle: Artist
        legend_text: Text
        ax_artist: Artist
        original_alpha: float
        visible: bool

    def __init__(self, ax=None, **kwargs):
        if kwargs.get("reverse"):
            raise ValueError("Reversed legend is not supported")

        ax = ax or plt.gca()
        self.fig = ax.figure
        self.legend = ax.legend(**kwargs)
        self.series_items = {}
        self.focused_item = None

        legend_handles = self.legend.legend_handles
        legend_texts = self.legend.texts
        ax_artists = ax.get_legend_handles_labels()[0]

        for legend_handle, legend_text, ax_artist in zip(
            legend_handles,
            legend_texts,
            ax_artists,
            strict=True,
        ):
            legend_handle.set_picker(8)
            self.series_items[ax_artist.get_label()] = self.SeriesItem(
                legend_handle=legend_handle,
                legend_text=legend_text,
                ax_artist=ax_artist,
                original_alpha=legend_handle.get_alpha(),
                visible=True,
            )

        self.fig.canvas.mpl_connect("pick_event", self.on_pick)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        ax._interactive_legend_ref = self

    def on_pick(self, event: PickEvent):
        if event.artist not in self.legend.legend_handles:
            return

        item = self.series_items[event.artist.get_label()]

        visible = not item.visible
        item.visible = visible
        item.ax_artist.set_visible(visible)
        item.legend_handle.set_alpha(item.original_alpha if visible else 0.2)
        item.legend_text.set_alpha(1 if visible else 0.2)
        self.fig.canvas.draw_idle()

    def on_mouse_move(self, event):
        matching_item = self.get_item_from_event(event)

        if matching_item == self.focused_item:
            return

        if matching_item:
            for item in self.series_items.values():
                item.ax_artist.set_alpha(1 if item is matching_item else 0.2)
        elif self.focused_item:
            for item in self.series_items.values():
                item.ax_artist.set_alpha(item.original_alpha)

        self.focused_item = matching_item

        self.fig.canvas.draw_idle()

    def get_item_from_event(self, event):
        if not self.legend.contains(event)[0]:
            return None

        # We'll only use the legend text (not handles)
        for artist in self.legend.texts:
            if artist.contains(event)[0]:
                return self.series_items[artist.get_text()]


if __name__ == "__main__":
    mpl_utils.setup()
    fig, ax = plt.subplots(num="Interactive legend", clear=True)
    mpl_utils.clear_events()

    df = pd.read_csv("../data/crop-data.csv")
    # df = df[df.Region.eq("Europe")]
    chart_df = df.pivot_table(
        index="Year",
        columns="Region",
        values="Yield",
    )
    ax.plot(chart_df, label=chart_df.columns, alpha=1)

    self = add_interactive_legend()
