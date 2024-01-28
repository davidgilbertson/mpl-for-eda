from typing import Callable

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox

import mpl_utils


class add_axes_tooltip(mpl_utils.AxesEventHandlers):
    def __init__(
        self,
        ax: Axes,
        render: Callable[[Axes, Axes, MouseEvent], bool],
        width=300,
        height=185,
        alpha=0.9,
    ):
        """
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The main axes object on which the tooltip will be displayed.
        render : callable
            A callback function that accepts three arguments: `ax`, `hover_ax`, and `event`.
            This function is responsible for plotting data into `hover_ax` based on the mouse event.
            It should return `True` if the tooltip should be displayed, `False` otherwise.
        width : int, optional
            The width of the hover tooltip in pixels. Default is 300.
        height : int, optional
            The height of the hover tooltip in pixels. Default is 185.
        alpha : float, optional
            The transparency of the hover tooltip. Default is 0.9.
        """
        super().__init__(ax)
        self.ax = ax
        self.render = render
        self.fig = ax.figure
        self.width = width
        self.height = height
        self.alpha = alpha

        self.hover_ax = self.fig.add_axes(
            rect=(0, 0, 1, 1),
            visible=False,
        )

        self.hover_ax.set_facecolor(plt.rcParams["grid.color"])
        self.hover_ax.spines[:].set(
            visible=True,
            color=plt.rcParams["text.color"],
            linewidth=0.5,
        )

        self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)
        ax._add_axes_tooltip_ref = self

    def on_hover(self, event: MouseEvent):
        if event.inaxes != self.ax:
            return

        self.hover_ax.clear()
        self.hover_ax.patch.set_alpha(self.alpha)
        show_tooltip = self.render(self.ax, self.hover_ax, event)

        if show_tooltip:
            self.show_hover_ax(event)
        else:
            self.hide_hover_ax()

    def on_leave(self, event):
        self.hide_hover_ax()

    def show_hover_ax(self, event):
        pad_px = 15
        is_left = event.x < self.fig.bbox.width / 2
        is_bottom = event.y < self.fig.bbox.height / 2

        bb_px = Bbox.from_bounds(
            x0=event.x + (pad_px if is_left else -self.width - pad_px),
            y0=event.y + (pad_px if is_bottom else -self.height - pad_px),
            width=self.width,
            height=self.height,
        )

        self.hover_ax.set(
            position=bb_px.transformed(self.fig.transFigure.inverted()),
            visible=True,
        )
        self.fig.canvas.draw_idle()

    def hide_hover_ax(self):
        self.hover_ax.set_visible(False)

        self.fig.canvas.draw_idle()


if __name__ == "__main__":
    df = pd.read_csv("../../data/crop-data.csv")

    def render_ax(ax: Axes, item):
        item_name, item_df = item
        chart_df = item_df.pivot_table(
            index="Country",
            columns="Crop",
            values="Yield",
            aggfunc="last",
        )
        mpl_utils.plot_heatmap(
            df=chart_df,
            ax=ax,
            tooltips=False,
        )
        ax.set_title(f"Crop yields — {item_name}")

    paginator = mpl_utils.plot_paginated(
        items=df.groupby("Region"),
        render=render_ax,
        items_per_page=1,
    )

    def render_hover_ax(heatmap_ax: Axes, hover_ax: Axes, event):
        crop = heatmap_ax.format_xdata(event.xdata)
        country = heatmap_ax.format_ydata(event.ydata)

        chart_df = df[df.Crop.eq(crop) & df.Country.eq(country)]
        hover_ax.plot(chart_df.Year, chart_df.Yield)
        hover_ax.set(xticks=[], yticks=[])
        hover_ax.set_ylim(0)

        if chart_df.Yield.dropna().empty:
            show_tooltip = False
        else:
            show_tooltip = True

        return show_tooltip

    add_axes_tooltip(
        ax=paginator.axs[0],
        render=render_hover_ax,
    )
