from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.figure import Figure
import pandas as pd

import mpl_utils

mpl_utils.setup()
fig, ax = plt.subplots(num="Event system", clear=True)
mpl_utils.clear_events()  # Added in 502
fig: Figure
ax: Axes

df = pd.read_csv("../data/crop-data.csv")
chart_df = df.pivot_table(
    index="Year",
    columns="Region",
    values="Yield",
)
ax.plot(chart_df, label=chart_df.columns)
ax.legend()


def on_mouse_move(event: MouseEvent):
    if not event.inaxes:
        return

    year = round(event.xdata)
    mean_yield = df[df.Year.eq(year)].Yield.mean()
    msg = f"Global average yield in {year} was {mean_yield:.1f} t/ha"

    fig.suptitle(msg)

    fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", on_mouse_move)
