from collections.abc import Callable

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.transforms import Bbox

import mpl_utils


class add_axes_tooltip(mpl_utils.EventsMixin):
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
            A callback function that accepts three arguments: `ax`, `tooltip_ax`, and `event`.
            This function is responsible for plotting data into `tooltip_ax` based on the mouse event.
            It should return `True` if the tooltip should be displayed, `False` otherwise.
        width : int, optional
            The width of the tooltip axes in pixels. Default is 300.
        height : int, optional
            The height of the tooltip axes in pixels. Default is 185.
        alpha : float, optional
            The transparency of the tooltip axes. Default is 0.9.
        """
        super().__init__(ax)
        self.ax = ax
        self.render = render
        self.fig = ax.figure
        self.width = width
        self.height = height
        self.alpha = alpha

        self.tooltip_ax = self.fig.add_axes(
            rect=(0, 0, 1, 1),
            visible=False,
        )

        self.tooltip_ax.set_facecolor(plt.rcParams["grid.color"])
        self.tooltip_ax.spines[:].set_visible(True)
        self.tooltip_ax.spines[:].set_color(plt.rcParams["text.color"])
        self.tooltip_ax.spines[:].set_linewidth(0.5)

        self.fig.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        ax._add_axes_tooltip_ref = self

    def on_mouse_move(self, event: MouseEvent):
        if event.inaxes != self.ax:
            return

        self.tooltip_ax.clear()
        self.tooltip_ax.patch.set_alpha(self.alpha)

        show_tooltip = self.render(self.ax, self.tooltip_ax, event)

        if show_tooltip:
            self.show_tooltip_ax(event)
        else:
            self.hide_tooltip_ax()

    def show_tooltip_ax(self, event):
        is_left = event.x < self.fig.bbox.width / 2
        is_bottom = event.y < self.fig.bbox.height / 2

        bb_px = Bbox.from_bounds(
            x0=event.x + (15 if is_left else -self.width - 15),
            y0=event.y + (15 if is_bottom else -self.height - 15),
            width=self.width,
            height=self.height,
        )

        self.tooltip_ax.set(
            position=bb_px.transformed(self.fig.transFigure.inverted()),
            visible=True,
        )
        self.fig.canvas.draw_idle()

    def on_leave(self, event):
        self.hide_tooltip_ax()

    def hide_tooltip_ax(self):
        self.tooltip_ax.set_visible(False)

        self.fig.canvas.draw_idle()


if __name__ == "__main__":
    df = pd.read_csv("../../data/crop-data.csv")

    def render_heatmap_ax(ax: Axes, item: tuple[str, pd.DataFrame]):
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
        render=render_heatmap_ax,
        items_per_page=1,
    )

    def render_tooltip_ax(
        heatmap_ax: Axes,
        tooltip_ax: Axes,
        event: MouseEvent,
    ) -> bool:
        crop = heatmap_ax.format_xdata(event.xdata)
        country = heatmap_ax.format_ydata(event.ydata)

        chart_df = df[df.Crop.eq(crop) & df.Country.eq(country)]

        if chart_df.Yield.dropna().empty:
            return False

        tooltip_ax.plot(chart_df.Year, chart_df.Yield)
        tooltip_ax.set(xticks=[], yticks=[])
        tooltip_ax.set_ylim(0)

        return True

    add_axes_tooltip(
        ax=paginator.axs[0],
        render=render_tooltip_ax,
    )
