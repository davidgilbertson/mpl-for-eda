from typing import Union

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.collections import PathCollection
from matplotlib.dates import DateLocator, num2date
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
from pandas.plotting._matplotlib.converter import TimeSeries_DateLocator

# EventsMixin must come before modules that use it.
from .event_helpers import EventsMixin  # Added in #509
from .text_zoom import add_text_zoom  # Added in #503
from .interactive_legend import add_interactive_legend  # Added in #506
from .dynamic_legend import add_dynamic_legend  # Added in #508
from .custom_tooltip import add_custom_tooltip  # Added in #602
from .legend_tooltip import add_legend_tooltip  # Added in #604
from .mplcursors_tooltip import add_mplcursors_tooltip  # Added in #605
from .layouts import flex_subplots, add_axes_px  # Added in #702 and #703
from .widgets import add_text_box  # Added in #803
from .charts.searchable_scatter import plot_searchable_scatter  # Added in #803
from .charts.heatmap import plot_heatmap  # Added in #606
from .charts.paginator import plot_paginated  # Added in #804
from .chart_manager import chart  # Added in #901


# Added in #403
# This is called as a hook when a figure is created
def configure_figure(fig):
    try:
        # fig.canvas.manager.window.geometry("840x1054+2874+297")  # Standard
        # fig.canvas.manager.window.geometry("1924x1054+1790+297")  # Full width
        fig.canvas.manager.window.geometry("840x1054+4161+66")  # Second monitor
        # fig.canvas.manager.window.geometry("1000x1000+4161+66")  # Square
    except AttributeError:
        pass


# Added in #401
def setup(font_bump=1):
    plt.rcdefaults()

    # This cycler will cycle through the default colors with a plain line,
    # then again for a dashed line, and again for a dotted line
    prop_cycle = (
        plt.cycler("linestyle", ["-", "--", ":", "-."])
        * plt.rcParams["axes.prop_cycle"]
    )

    blue_gray_100 = "#cfd8dc"
    blue_gray_300 = "#90a4ae"
    blue_gray_700 = "#455a64"
    blue_gray_900 = "#263238"
    blue_gray_950 = "#1d272b"

    plt.rcParams.update(
        {
            # Window config
            "backend": "TkAgg",
            "interactive": True,
            # Layout
            "figure.figsize": (10, 10),  # Avoid layout collapse
            "figure.constrained_layout.use": True,
            "figure.constrained_layout.h_pad": 0.1,
            "figure.constrained_layout.w_pad": 0.1,
            "figure.constrained_layout.hspace": 0.0,
            "figure.constrained_layout.wspace": 0.05,
            # Styles
            "font.size": 10 + font_bump,
            "figure.facecolor": blue_gray_950,
            "axes.facecolor": blue_gray_950,
            "text.color": blue_gray_100,
            "axes.labelcolor": blue_gray_300,
            "axes.grid": True,
            "grid.color": blue_gray_900,
            "axes.edgecolor": blue_gray_700,  # used by spines
            "axes.linewidth": 1,  # used by spines
            "axes.spines.top": False,
            "axes.spines.left": False,
            "axes.spines.right": False,
            "axes.spines.bottom": False,
            "figure.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.titlepad": 12,
            "axes.titleweight": "bold",
            "axes.labelpad": 12 + font_bump,
            "xtick.bottom": False,
            "ytick.left": False,
            "ytick.right": False,
            "xtick.major.width": 0,
            "ytick.major.size": 0,
            "xtick.minor.width": 0,
            "ytick.minor.size": 0,
            "xtick.color": blue_gray_300,
            "ytick.color": blue_gray_300,
            # Other
            "axes.prop_cycle": prop_cycle,
            "axes.xmargin": 0.01,
            "axes.ymargin": 0.02,
            "date.converter": "concise",
            "axes.axisbelow": True,  # grid lines behind chart elements
            "legend.columnspacing": 1,
            "hist.bins": "auto",
            "scatter.edgecolors": "none",
            "patch.facecolor": blue_gray_900,  # used by tooltip
            "patch.edgecolor": blue_gray_700,
            "patch.linewidth": 0.5,
            "figure.hooks": "mpl_utils:configure_figure",
        }
    )


# Added in #502
# Connection IDs present in a new figure.
_initial_cids = {}


# Added in #502
def clear_events(fig=None):
    """
    Clears user-added event handlers so that code can be rerun without
    a build up of events.
    Should be called after figure creation, before connecting event handlers
    """
    fig = fig or plt.gcf()

    # Get all the CIDs in the callback registry
    cids = []
    for cb_dict in fig.canvas.callbacks.callbacks.values():
        cids.extend(cb_dict.keys())

    if _initial_cids.get(fig.number) is None:
        # These are the event CIDs for a new figure
        _initial_cids[fig.number] = cids
    else:
        # We must be rerunning code for an existing figure
        # What CIDs have been added since the first time this was called?
        added_cids = set(cids).difference(_initial_cids[fig.number])

        # Disconnect those CIDs
        for cid in added_cids:
            fig.canvas.mpl_disconnect(cid)


# Added here in #504, explained in #404
class pack_y_ticks:
    def __init__(self, ax=None):
        ax = ax or plt.gca()
        self.ax = ax
        self.ax_height = None
        ax.figure.canvas.mpl_connect("draw_event", self.on_draw)
        ax._pack_y_ticks_ref = self

    def on_draw(self, event):
        if self.ax.bbox.height != self.ax_height:
            self.ax_height = self.ax.bbox.height

            self.ax.yaxis.set_major_locator(
                MaxNLocator(
                    nbins=self.ax.yaxis.get_tick_space(),
                    steps=[1, 2, 5],
                )
            )
            self.ax.figure.canvas.draw()


# Added in #508
def get_x_values_from_ax(ax: Axes):
    """
    Extract and return sorted unique x-values from all Line2D and
    PathCollection artists in a matplotlib Axes.

    Parameters
    ----------
    ax : Axes
        The matplotlib Axes object from which to extract x-values.

    Returns
    -------
    list
        A sorted list of unique x-values present in the Line2D and
        PathCollection artists of the provided Axes.

    Notes
    -----
    - The function only considers Line2D and PathCollection objects
    within the Axes. Other artist types are ignored.
    - If there are no Line2D or PathCollection artists in the Axes,
    an empty list is returned.
    - The x-values are extracted from Line2D objects (representing
    lines) and PathCollection objects (representing scatter plots).
    """
    unique_x_values = set()

    for artist in ax.get_children():
        if isinstance(artist, Line2D):
            unique_x_values.update(artist.get_xdata(orig=False))
        elif isinstance(artist, PathCollection):
            x_data = artist.get_offsets()[:, 0]
            unique_x_values.update(x_data)

    return sorted(unique_x_values)


# Added in #508
def get_closest(options, target):
    """
    Finds and returns the element from a given array of options that is closest to a
    specified target value, ignoring any NaN values in the array.

    Parameters
    ----------
    options : array_like
        An array-like object containing numerical values. NaN values within this
        array are ignored.
    target : float
        The target value to which the closest element in the `options` array is sought.

    Returns
    -------
    float
        The element from `options` that is closest to the `target` value. If multiple
        elements are equally close, the first one encountered is returned.

    Notes
    -----
    The function converts the input `options` to a NumPy array and filters out NaN
    values. It then calculates the absolute differences between the non-NaN elements
    and the target, returning the element with the minimum difference.
    """
    options = np.asarray(options)
    options = options[~np.isnan(options)]
    diffs = np.abs(options - target)
    return options[np.argmin(diffs)]


# Added in #508
def get_closest_x(event: MouseEvent):
    ax = event.inaxes

    if not ax:
        return

    x_values = get_x_values_from_ax(ax)
    x_value = get_closest(x_values, event.xdata)

    # Added in #510
    if isinstance(ax.xaxis.get_major_locator(), TimeSeries_DateLocator):
        x_value = pd.Period(
            ordinal=int(x_value),
            freq=ax.xaxis.get_major_locator().freq,
        )
        x_value = x_value.to_timestamp().to_pydatetime()
    elif isinstance(ax.xaxis.get_major_locator(), DateLocator):
        x_value = num2date(x_value).replace(tzinfo=None)

    return x_value


# Added in #508
def get_y_at_x(artist: Union[Line2D, PathCollection], x):
    """
    Extract the y-coordinate corresponding to a given x-coordinate from a matplotlib
    artist object, which can be either a Line2D or a PathCollection.

    Parameters
    ----------
    artist : Line2D | PathCollection
        The matplotlib artist object from which to extract the data. It should be
        either a Line2D object representing a line plot, or a PathCollection object
        representing a scatter plot.
    x : float or int
        The x-coordinate for which the corresponding y-coordinate is desired.

    Returns
    -------
    float
        The y-coordinate corresponding to the specified x-coordinate. If the x-coordinate
        is not found in the data, NaN is returned.

    Raises
    ------
    ValueError
        If the artist type is neither Line2D nor PathCollection.
    """

    # This will convert dates to floats
    x = artist.convert_xunits(x)

    if isinstance(artist, Line2D):
        x_data, y_data = artist.get_data(orig=False)
    elif isinstance(artist, PathCollection):
        x_data, y_data = artist.get_offsets().T
    else:
        raise ValueError(f"Unhandled artist type: {artist}")

    try:
        index = list(x_data).index(x)
        return y_data[index]
    except ValueError:
        return float("nan")


# Added in #602
def bold(val):
    return rf"$\mathbf{{{val}}}$"


# Added in #605
def series_to_string(series: pd.Series):
    text_rows = []
    for key, val in series.items():
        if isinstance(val, float):
            if pd.isna(val):
                val = "-"
            else:
                val = f"{val:,.2f}"
        text_rows.append(f"{bold(key)}: {val}")

    return "\n".join(text_rows)
