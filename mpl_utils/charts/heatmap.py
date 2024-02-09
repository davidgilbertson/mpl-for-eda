from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.category import StrCategoryConverter
import pandas as pd

import mpl_utils


def plot_heatmap(
    df: pd.DataFrame,
    ax=None,
    title="Heatmap",
    cmap="Blues_r",
    cbar=True,
    tooltips=True,
    **kwargs,
) -> Axes:
    if ax is None:
        mpl_utils.setup()
        ax = plt.subplots(num=title, clear=True)[1]
        mpl_utils.clear_events()

    ax.grid(False)

    quad_mesh = ax.pcolormesh(
        df.columns,
        df.index,
        df,
        cmap=cmap,
        **kwargs,
    )

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    ax.invert_yaxis()

    if cbar:
        # We'll manually define the colorbar's axes as a child of this axes
        # So that ax.clear() removes it
        # Note we lose the ability to pan the colorbar
        cb = ax.figure.colorbar(
            quad_mesh,
            cax=ax.inset_axes((1.05, 0, 0.05, 1)),
        )
        cb.outline.set_visible(False)

    if tooltips:

        def get_text(event: MouseEvent):
            if not quad_mesh.contains(event)[0]:
                return

            if isinstance(ax.xaxis.converter, StrCategoryConverter):
                x_value = ax.format_xdata(event.xdata)
            else:
                x_value = mpl_utils.get_closest(df.columns, event.xdata)

            if isinstance(ax.yaxis.converter, StrCategoryConverter):
                y_value = ax.format_ydata(event.ydata)
            else:
                y_value = mpl_utils.get_closest(df.index, event.ydata)

            value = df.loc[y_value, x_value]

            return f"{x_value}\n{y_value}\n{value:g}"

        mpl_utils.add_custom_tooltip(
            ax=ax,
            get_text=get_text,
        )

    return ax


if __name__ == "__main__":
    df = pd.read_csv("../../data/crop-data.csv")

    df = df[df.Region.eq("Africa")]
    chart_df = df.pivot_table(
        index="Country",
        columns="Crop",
        values="Yield",
    )
    ax = plot_heatmap(df=chart_df)
