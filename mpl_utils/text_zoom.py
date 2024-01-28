from itertools import cycle

from matplotlib.figure import Figure
from matplotlib.text import Text
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import KeyEvent

import mpl_utils


class add_text_zoom:
    def __init__(self, fig: Figure = None):
        self.fig = fig or plt.gcf()
        self.delta = 0
        self.fig.canvas.mpl_connect("key_press_event", self.on_key_press)
        self.fig._add_text_zoom_ref = self

    def on_key_press(self, event: KeyEvent):
        if event.key == "ctrl+equal":
            for text in self.fig.findobj(Text):
                text.set_fontsize(text.get_fontsize() + 1)
            self.delta += 1
        elif event.key == "ctrl+minus":
            for text in self.fig.findobj(Text):
                text.set_fontsize(text.get_fontsize() - 1)
            self.delta -= 1
        elif event.key == "ctrl+0":
            for text in self.fig.findobj(Text):
                text.set_fontsize(text.get_fontsize() - self.delta)
            self.delta = 0
        else:
            return

        self.fig.canvas.draw_idle()


if __name__ == "__main__":
    mpl_utils.setup()
    fig, ax = plt.subplots(num="Text zoom", clear=True)
    mpl_utils.clear_events()

    df = pd.read_csv("../data/crop-data.csv")
    chart_df = df.pivot_table(
        index="Year",
        columns="Region",
        values="Yield",
    )
    ax.plot(chart_df, label=chart_df.columns)
    ax.legend()
    fig.suptitle("Crop yields")
    ax.set(
        title="Yield by region",
        xlabel="Year",
        ylabel="Yield",
    )

    self = add_text_zoom()
