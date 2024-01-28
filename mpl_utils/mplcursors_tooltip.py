from collections.abc import Callable

from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D
from matplotlib.patheffects import withSimplePatchShadow
import matplotlib.pyplot as plt
import mplcursors
import pandas as pd


# Added in #605
def add_mplcursors_tooltip(
    get_text: Callable[[mplcursors.Selection], str | None] = None,
    pickables=None,  # Added in #802
):
    tooltip_cursor = mplcursors.cursor(
        pickables=pickables,  # Added in #802
        hover=mplcursors.HoverMode.Transient,
        annotation_kwargs=dict(
            bbox=dict(
                alpha=0.8,
                path_effects=[withSimplePatchShadow(offset=(2, -2))],
            ),
            linespacing=1.4,
            multialignment="left",
        ),
        highlight=True,
        highlight_kwargs=dict(
            edgecolor=plt.rcParams["text.color"],
            color=plt.rcParams["text.color"],
        ),
        bindings=dict(  # Added in #803
            toggle_enabled="ctrl+alt+e",
            toggle_visible="ctrl+alt+v",
        ),
    )

    if get_text:

        def set_text(sel: mplcursors.Selection):
            text = get_text(sel)
            if text is not None:
                sel.annotation.set_text(text)

        tooltip_cursor.connect("add", set_text)


if __name__ == "__main__":
    import mpl_utils

    mpl_utils.setup()
    fig, ax = plt.subplots(num="mplcursors", clear=True)
    mpl_utils.clear_events()

    df = pd.read_csv("../data/crop-data.csv")
    df = df[df.Region.eq("Europe") & df.Crop.eq("Rice")].dropna()

    for country_name, country_df in df.groupby("Country"):
        if "n" in country_name:
            ax.plot(country_df.Year, country_df.Yield, label=country_name)
        else:
            ax.scatter(country_df.Year, country_df.Yield, label=country_name)

    mock_events = [
        [1964, "Drought"],
        [1973, "Storms"],
        [1975, "Major drought"],
        [2003, "Heat wave"],
        [2015, "Locust plague"],
        [2018, "Drought"],
    ]
    for year, event_name in mock_events:
        ax.axvline(
            x=year,
            label=f"_{event_name}",
            color="#444",
            linestyle=":",
            linewidth=3,
            zorder=0,
        )
    ax.legend(loc="upper left")

    def get_text(sel: mplcursors.Selection):
        label = sel.artist.get_label()

        if isinstance(sel.artist, PathCollection):
            x_value = sel.target[0]
        elif isinstance(sel.artist, Line2D):
            x_data = sel.artist.get_xdata()
            x_value = x_data[round(sel.index)]

            if len(set(x_data)) == 1:  # Vertical line
                label = label.removeprefix("_")
                return f"{x_value}\n{label}"
        else:
            return

        row = df[df.Country.eq(label) & df.Year.eq(x_value)]
        assert len(row) == 1, "There should only be one match"
        row = row.squeeze()
        return mpl_utils.series_to_string(row)

    add_mplcursors_tooltip(get_text=get_text)
