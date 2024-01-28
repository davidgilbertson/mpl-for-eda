from matplotlib import pyplot as plt
from matplotlib.dates import num2date
import pandas as pd

import mpl_utils

mpl_utils.setup()
fig, ax = plt.subplots(num="Tooltips with dates", clear=True)
mpl_utils.clear_events()

df = pd.read_csv("../data/crop-data.csv", parse_dates=["Year"])
df = df[df.Country.eq("France")]
chart_df = df.pivot_table(
    index="Year",
    columns="Crop",
    values="Yield",
)
ax.plot(chart_df, label=chart_df.columns)
ax.legend()


def get_text(event):
    hovered_lines = [line for line in event.inaxes.lines if line.contains(event)[0]]

    if not hovered_lines:
        return

    # Just take the first line
    line = hovered_lines[0]
    crop = line.get_label()

    # Get the x axis dates as numbers
    x_dates_mpl_num = line.get_xdata(orig=False)

    # Get the date under the cursor
    x_date_mpl_num = mpl_utils.get_closest(
        options=x_dates_mpl_num,
        target=event.xdata,
    )

    # Convert to a date
    x_date_py_tz = num2date(x_date_mpl_num)

    # Drop the timezone
    x_date_py = x_date_py_tz.replace(tzinfo=None)

    # Find the matching row
    row = df[df.Year.eq(x_date_py) & df.Crop.eq(crop)].squeeze()
    row.Year = row.Year.year

    return mpl_utils.series_to_string(row)


mpl_utils.add_custom_tooltip(get_text=get_text)
