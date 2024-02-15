from collections.abc import Callable
import contextlib
import math

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.layout_engine import ConstrainedLayoutEngine
from matplotlib.transforms import Bbox
import pandas as pd

import mpl_utils


# Added in #902
class FastLayoutEngine(ConstrainedLayoutEngine):
    def __init__(self, fig=None):
        super().__init__()

        self.enabled = True
        self.timer = None

        fig = fig or plt.gcf()
        self.fig = fig
        fig.canvas.mpl_connect("figure_enter_event", self.on_figure_enter)
        fig.canvas.mpl_connect("figure_leave_event", self.on_figure_leave)
        fig.canvas.mpl_connect("button_release_event", self.force_execute)
        fig.canvas.mpl_connect("key_release_event", self.force_execute)
        fig.canvas.mpl_connect("scroll_event", self.on_scroll)

    def on_figure_enter(self, _):
        self.enabled = False

    def on_figure_leave(self, _):
        self.enabled = True

    # Added in 903
    def on_scroll(self, event):
        if self.timer:
            self.timer.stop()

        self.timer = self.fig.canvas.new_timer(100)  # ms
        self.timer.single_shot = True
        self.timer.add_callback(self.force_execute)
        self.timer.start()

    def force_execute(self, event=None):
        super().execute(self.fig)
        self.fig.canvas.draw_idle()

    def execute(self, fig):
        if self.enabled:
            super().execute(fig)


# Added in #903
class add_zoom_on_scroll:
    def __init__(self, fig=None):
        self.fig = fig or plt.gcf()
        self.fig.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.fig.canvas.mpl_connect("button_press_event", self.on_mouse_down)
        self.fig._scroll_on_zoom_ref = self

        self.timer = None

    def on_scroll(self, event: MouseEvent):
        ax = event.inaxes
        if not ax:
            return

        if not ax.get_navigate():  # E.g. Widgets
            return

        if not ax.can_zoom():  # E.g. polar axes
            return

        if self.fig.canvas.toolbar._nav_stack() is None:
            self.fig.canvas.toolbar.push_current()

        scale = 1.3 if event.button == "up" else 0.7

        ax._set_view_from_bbox(
            (event.x, event.y, scale),
            mode=event.key if event.key in ["x", "y"] else None,
        )

        # Limit zooming out
        new_limits = Bbox.intersection(ax.viewLim, ax.dataLim) or ax.viewLim
        if new_limits.bounds != ax.dataLim.bounds:
            ax.set_xbound(new_limits.xmin, new_limits.xmax)
            ax.set_ybound(new_limits.ymin, new_limits.ymax)
        else:
            ax.autoscale()

        self.fig.canvas.toolbar.push_current()

        self.fig.canvas.draw_idle()

    def on_mouse_down(self, event: MouseEvent):
        if ax := event.inaxes and event.dblclick:
            ax.autoscale()
            self.fig.canvas.draw_idle()


class AxesWithSpawn(Axes):
    spawn: Callable[[], Axes]


# Added in #901
class chart:
    def __init__(
        self,
        name="Chart",
        ncols=None,
        tooltips=True,
        pan=True,
        **kwargs,
    ):
        self.tooltips = tooltips
        self.ncols = ncols
        self.existing_figure = name in plt.get_figlabels()

        mpl_utils.setup()
        self.fig, self.ax = plt.subplots(num=name, clear=True, **kwargs)
        mpl_utils.clear_events()
        mpl_utils.add_text_zoom()

        if pan and not self.existing_figure:
            self.fig.canvas.toolbar.pan()

        self.axs = [self.ax]

    def __enter__(self) -> AxesWithSpawn:
        # Slightly dodgy monkey-patching of `Axes`
        self.ax.spawn = self.spawn
        return self.ax

    def __exit__(self, *args):
        ax_count = len(self.axs)
        if self.ncols:
            ncols = min(self.ncols, ax_count)
        else:
            ncols = math.floor(math.sqrt(ax_count))
        nrows = math.ceil(ax_count / ncols)

        grid_spec = self.fig.add_gridspec(nrows=nrows, ncols=ncols)

        for ax, subplot_spec in zip(self.axs, grid_spec):
            ax.set_subplotspec(subplot_spec)

        if self.tooltips:
            mpl_utils.add_mplcursors_tooltip(pickables=self.fig)

        if self.existing_figure:
            with contextlib.suppress(AttributeError):
                window = self.fig.canvas.manager.window
                # Only unminimize when needed to avoid focus issues
                if window.state() == "iconic":
                    window.deiconify()
            self.fig.show()

        add_zoom_on_scroll(self.fig)  # Added in 903
        self.fig.set_layout_engine(FastLayoutEngine(self.fig))  # Added in 902

    def spawn(self):
        if not self.ax.has_data():
            return self.ax

        new_ax = self.fig.add_subplot()
        self.axs.append(new_ax)
        return new_ax


if __name__ == "__main__":
    df = pd.read_csv("../data/crop-data.csv")

    with chart() as ax:
        for group_name, group_df in df.groupby("Region"):
            chart_df = group_df.pivot_table(
                index="Year",
                columns="Crop",
                values="Yield",
            )

            new_ax = ax.spawn()
            new_ax.plot(chart_df, label=chart_df.columns)
            new_ax.set_title(group_name)
