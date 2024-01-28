from collections.abc import Sequence
from typing import Literal

from matplotlib import pyplot as plt
from matplotlib.transforms import Bbox

import mpl_utils


# Added in #702
def mixed_to_rel_sizes(sizes, ref_size):
    # Loop once to calculate the totals
    total_px_size = 0
    total_rel_units = 0
    for size in sizes:
        if isinstance(size, str):
            total_px_size += float(size.removesuffix("px"))
        else:
            total_rel_units += size

    rel_factor = (ref_size - total_px_size) / total_rel_units

    # Loop again to convert everything to pixel units
    px_sizes = []
    for size in sizes:
        if isinstance(size, str):
            px_sizes.append(float(size.removesuffix("px")))
        else:
            px_sizes.append(size * rel_factor)

    return px_sizes


# Added in #702
def flex_subplots(
    num="Chart",
    nrows: int = None,
    ncols: int = None,
    row_heights: Sequence[float | str] = None,
    col_widths: Sequence[float | str] = None,
    **kwargs,
):
    if num and "clear" not in kwargs:
        kwargs["clear"] = True

    mpl_utils.setup()
    fig, ax_or_axs = plt.subplots(
        num=num,
        nrows=nrows or (len(row_heights) if row_heights else 1),
        ncols=ncols or (len(col_widths) if col_widths else 1),
        **kwargs,
    )
    mpl_utils.clear_events()

    grid_spec = fig.axes[0].get_gridspec()

    def set_sizes(event=None):
        if row_heights is not None:
            height_ratios = mixed_to_rel_sizes(row_heights, fig.bbox.height)
            grid_spec.set_height_ratios(height_ratios)

        if col_widths is not None:
            width_ratios = mixed_to_rel_sizes(col_widths, fig.bbox.width)
            grid_spec.set_width_ratios(width_ratios)

    set_sizes()
    fig.canvas.mpl_connect("resize_event", set_sizes)

    return fig, ax_or_axs


# Added in #703
def add_axes_px(
    bounds: tuple[float, float, float, float],
    origin: Literal[
        "top left",
        "top right",
        "bottom left",
        "bottom right",
    ] = "bottom left",
    fig=None,
    **kwargs,
):
    """
    Add a new axes to a matplotlib figure at a specific position and size defined in pixels.

    This function allows for the precise placement and sizing of an axes within a matplotlib
    figure using pixel coordinates. The position and size are controlled by the `bounds` parameter,
    and the origin of these bounds can be specified with the `origin` parameter.

    Parameters
    ----------
    bounds : tuple[float, float, float, float]
        A tuple containing the x, y, width, and height of the new axes in pixel coordinates.

    origin : {'top left', 'top right', 'bottom left', 'bottom right'}, default 'bottom left'
        The origin point for the bounds. This determines where the x and y coordinates
        start from within the figure.

    fig : matplotlib.figure.Figure, optional
        The figure to which the axes will be added. If not provided, the current figure
        is used.

    **kwargs : dict
        Additional keyword arguments passed to the `add_axes` method of the matplotlib figure.

    Returns
    -------
    matplotlib.axes.Axes
        The axes object added to the figure.

    Notes
    -----
    - The `bounds` are given in pixels and are relative to the specified `origin`.
    - This function is useful for adding axes to a figure where precise control of
      their placement and size is required.
    """
    fig = fig or plt.gcf()
    bbox_px = Bbox.from_bounds(*bounds)

    def axes_locator(ax, renderer):
        fig_to_px = ax.figure.transFigure
        px_to_fig = fig_to_px.inverted()
        bbox_fig = bbox_px.transformed(px_to_fig)

        if origin.startswith("top"):
            bbox_fig.bounds = (
                bbox_fig.x0,
                1 - bbox_fig.y0 - bbox_fig.height,
                bbox_fig.width,
                bbox_fig.height,
            )
        if origin.endswith("right"):
            bbox_fig.bounds = (
                1 - bbox_fig.x0 - bbox_fig.width,
                bbox_fig.y0,
                bbox_fig.width,
                bbox_fig.height,
            )

        return bbox_fig

    return fig.add_axes(
        rect=(0, 0, 1, 1),  # Ignored but required
        axes_locator=axes_locator,
        **kwargs,
    )


if __name__ == "__main__":
    fig, axs = flex_subplots(row_heights=["100px", 1, 1])
    axs[0].set_axis_off()
    # fixed_ax = fig.add_axes(
    #     rect=(0.1, 0.2, 0.3, 0.4),
    #     facecolor="teal",
    # )
    ax = add_axes_px(
        bounds=(10, 20, 300, 400),
        origin="top right",
        facecolor="teal",
    )
